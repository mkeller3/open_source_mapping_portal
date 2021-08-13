from django.conf import settings
from .serializers import *
from .constants import *
from .models import *
import random
import string
import subprocess
import psycopg2
from psycopg2 import sql
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import pandas as pd
import requests
import json
import mercantile
import requests

user_data_db_pool = psycopg2.pool.SimpleConnectionPool(
    1,
    20,
    dbname='mapping_portal',
    user='postgres',
    host=api_db_host,
    password=api_db_pwd,
    port='5432',
    options="-c search_path=user_data,postgis,default_maps"
)
 
def table_id_generator():
    return ''.join(random.choice(string.ascii_letters) for x in range(50)).lower()

def load_geographic_data_to_server(upload_settings):
    table_name = upload_settings['table_id']
    file_path = upload_settings['file']
    subprocess.call(f'ogr2ogr -f "PostgreSQL" "PG:host={api_db_host} user={api_db_user} dbname={data_db} password={api_db_pwd}" "{file_path}" -lco GEOMETRY_NAME=geom -lco FID=gid -lco PRECISION=no -nln {data_db_schema}.{table_name} -overwrite', shell=True)

def get_user_groups(username):
    groups = []
    groups_list = list(groupData.objects.filter(users__contains=username).values('group_name'))
    for group in groups_list:
        groups.append(group['group_name'])
    groups.append(username)
    return groups

def delete_data_backend(table_id, table_name):
    for file in os.listdir(media_location):
        file_name = os.path.splitext(file)[0]
        if file_name == table_name:
            os.remove(media_location+file)
    conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql.SQL("DROP TABLE IF EXISTS {table}").format(table=sql.SQL(table_id)))
    conn.commit()
    cur.close()
    conn.close()

def add_table_into_mapping_portal(table_information):
    conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql.SQL("SELECT pg_relation_size('{table}') as size;").format(table=sql.SQL(table_information['table_id'])))
    results = cur.fetchone()
    table_information['size'] = results['size']
    cur.execute(sql.SQL("SELECT COUNT(*) FROM {table};").format(table=sql.SQL(table_information['table_id'])))
    results = cur.fetchone()
    table_information['rows'] = results['count']
    cur.close()
    conn.close()

    # TODO
    table_information['bounding_box'] = []

    del table_information['file']
    if 'latitude_field' in table_information:
        del table_information['latitude_field']
        del table_information['longitude_field']
        del table_information['file_name']
        del table_information['extenstion']
    data = tableData(**table_information)
    data.save()

def load_point_data_to_server(table_information):
    if table_information['extenstion'] == '.xlsx' or table_information['extenstion'] == '.xls':
        df = pd.read_excel(file, table_information['sheet_name'], index_col=None)
        df.to_csv(media_location+table_information['']+'.csv', encoding='utf-8')

    df = pd.read_csv(media_location+table_information['file_name']+'.csv', nrows=1000)

    columns = []

    # TODO check for starting with number
    for name, dtype in df.dtypes.iteritems():
        column_type = 'text'
        if dtype == 'float64':
            column_type = 'double precision'
        if dtype == 'int64':
            column_type = 'integer'
        columns.append(
            {
                "name": name.lower().replace(' ','_'),
                "type": column_type
            }
        )

    table_id = table_information['table_id']

    create_table_sql = f"CREATE TABLE {table_id}("

    for index, column in enumerate(columns):
        if index == len(columns)-1:
            create_table_sql+= f"{column['name']} {column['type']}"
        else:
            create_table_sql+= f"{column['name']} {column['type']},"

    create_table_sql += ");"

    conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(create_table_sql)
    conn.commit()
    with open(media_location+table_information['file_name']+'.csv', 'r') as f:
        next(f)
        cur.copy_expert(f"COPY {table_id} FROM STDIN WITH CSV NULL ''", f)
    f.close()
    conn.commit()
    cur.close()
    conn.close()

    add_lat_lng_columns(table_id, table_information['latitude_field'], table_information['longitude_field'])

def add_lat_lng_columns(table_id, latitude, longitude):
    conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql.SQL("SELECT AddGeometryColumn('{table_id}','geom', '4326', 'POINT',2);").format(table_id=sql.SQL(table_id)))
    cur.execute(sql.SQL("UPDATE {table_id} SET geom = ST_SetSRID(ST_MakePoint({longitude}, {latitude}),4326);").format(table_id=sql.SQL(table_id), latitude=sql.SQL(latitude), longitude=sql.SQL(longitude)))
    cur.execute(sql.SQL("ALTER TABLE {table_id} ADD COLUMN gid SERIAL PRIMARY KEY;").format(table_id=sql.SQL(table_id)))
    conn.commit()
    cur.close()
    conn.close()

def validate_geometry(table_id):
    conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql.SQL("DELETE FROM {table_id} WHERE geom is NULL;").format(table_id=sql.SQL(table_id)))
    cur.execute(sql.SQL("UPDATE {table_id} SET geom=ST_MakeValid(geom);").format(table_id=sql.SQL(table_id)))
    conn.commit()
    cur.close()
    conn.close()
    
def index_table(table_id):
    conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql.SQL("CREATE INDEX {table_id_index} ON {table_id} USING GIST(geom);").format(table_id_index=sql.SQL(f"{table_id}_spatial_index"), table_id=sql.SQL(table_id)))
    cur.execute(sql.SQL("CLUSTER {table_id} USING {table_id_index};").format(table_id_index=sql.SQL(f"{table_id}_spatial_index"), table_id=sql.SQL(table_id)))
    cur.execute(sql.SQL("ANALYZE {table_id};").format(table_id=sql.SQL(table_id)))
    conn.commit()
    cur.close()
    conn.close()

def clean_columns(table_id):
    conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql.SQL("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '{table_id}' AND data_type != 'USER-DEFINED' And column_name != 'gid';").format(table_id=sql.SQL(table_id)))
    columns = cur.fetchall()

    numeric_columns= []
    string_columns = []

    for column in columns:
        if column['data_type'] == 'integer' or column['data_type'] == 'double_precision':
            numeric_columns.append(column['column_name'])

        if column['data_type'] == 'text':
            string_columns.append(column['column_name'])

    for column in numeric_columns:
        cur.execute(sql.SQL("UPDATE {table_id} SET {column} = 0 WHERE {column} IS NULL;").format(column=sql.SQL(column), table_id=sql.SQL(table_id)))

    for column in string_columns:
        cur.execute(sql.SQL("UPDATE {table_id} SET {column} = 'No Data' WHERE {column} IS NULL;").format(column=sql.SQL(column), table_id=sql.SQL(table_id)))

    conn.commit()
    cur.close()
    conn.close()

def clean_table(table_id):
    validate_geometry(table_id)
    index_table(table_id)
    clean_columns(table_id)

def download_esri_service_data(url, table_id):
    service_url = f"{url}?f=pjson"

    r = requests.get(service_url)

    data = r.json()

    max_number_of_features_per_query = data['maxRecordCount']

    feature_stats_url = f"{url}/query?where=1%3D1&returnGeometry=false&returnIdsOnly=true&f=pjson"

    r = requests.get(feature_stats_url)

    data = r.json()
    
    object_id_name = 'OBJECTID'

    object_ids = data['objectIds']

    number_of_features = len(data['objectIds'])

    if number_of_features <= max_number_of_features_per_query:

        r = requests.get(f"{url}/query?where=1=1&outFields=*&returnGeometry=true&geometryPrecision=6&outSR=4326&f=geojson")

        data = r.json()  
        
        with open(f'{media_location}/{table_id}.geojson', 'w') as json_file:
            json.dump(data, json_file)

    else:
        start = 0
        
        feature_collection = {
            "type": "FeatureCollection",           
            "features": []
        }

        for x in range( start, number_of_features, max_number_of_features_per_query ):
            ids_requested = object_ids[x: x + max_number_of_features_per_query ]
            payload = { 'f': 'geojson', 'where': '1=1', 
                'objectIds': str( ids_requested )[1:-1], 'outSR': '4326',  
                'returnGeometry': 'true', 'outFields': '*', 
                'geometryPrecision': '6'}
            result = requests.post( f"{url}/query", data=payload ) 
            print(result.text)
            feature_collection['features'] += result.json().get('features') 

        with open(f'{media_location}/{table_id}.geojson', 'w') as json_file:
            json.dump(feature_collection, json_file)

def get_limit_and_offset(serializer):
    limit = settings.MAX_NUMBER_OF_API_RESULTS
    offset = 0
    if 'limit' in serializer.validated_data:
        limit = serializer.validated_data['limit']
    if 'offset' in serializer.validated_data:
        offset = serializer.validated_data['offset']
        if 'limit' in serializer.validated_data:
                limit = serializer.validated_data['limit'] + serializer.validated_data['offset']
    return limit, offset

def sqlToPbf(database, table_name, z, x, y, fields):
    bounds = mercantile.xy_bounds(x,y,z) 
    old_fields = fields.replace(',','","')
    fields =f'{old_fields}'

    vector_tile_query = """
            WITH
            bounds AS (
                SELECT
                    ST_Segmentize(
                        ST_MakeEnvelope(
                            {xmin},
                            {ymin},
                            {xmax},
                            {ymax},
                            {epsg}
                        ),
                        {seg_size}
                    ) AS geom
            ),
            mvtgeom AS (
                SELECT ST_AsMVTGeom(
                    ST_Transform(t.geom, {epsg}),
                    bounds.geom,
                    {tile_resolution},
                    {tile_buffer}
                ) AS geom, {fields}
                FROM {database}.{table_name} t, bounds
                WHERE ST_Intersects(
                    ST_Transform(t.geom, 4326),
                    ST_Transform(bounds.geom, 4326)
                ) LIMIT {limit}
            )
            SELECT NULL as id,ST_AsMVT(mvtgeom.*) FROM mvtgeom
        """
    sql_query = vector_tile_query.format(
        xmin=bounds.left,
        ymin=bounds.bottom,
        xmax=bounds.right,
        ymax=bounds.top,
        epsg='3857',
        seg_size=bounds.right - bounds.left,
        tile_resolution=settings.TILE_RESOLUTION,
        tile_buffer=settings.TILE_BUFFER,
        fields=fields,
        table_name=table_name,
        limit=settings.MAX_FEATURES_PER_TILE,
        database=database
    )

    if database == 'user_data':
        ps_connection = user_data_db_pool.getconn()

        if ps_connection:
            cur = ps_connection.cursor()
            cur.execute(sql_query)
            tile = cur.fetchall()[-1][-1]

            if database == 'user_data':
                user_data_db_pool.putconn(ps_connection)

    return tile

def geocode_address(address: object):
    first_address = address['address']
    city = address['city']
    state = address['state']
    zip_code = address['zip']
    r = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{first_address}, {city} {state} {zip_code}.json?access_token={mapbox_token}')
    results = r.json()
    geojson_feature = {
        "type": "Feature",
        "geometry": None,
        "properties": {
            "accuracy": None
        }    
    }
    if results['features'][0]:
        geojson_feature['geometry'] = results['features'][0]['geometry']
        geojson_feature['properties']['place_name'] = results['features'][0]['place_name']
        if 'accuracy' in results['features'][0]['properties']:
            geojson_feature['properties']['accuracy'] = results['features'][0]['properties']['accuracy']

    return geojson_feature

def get_accessible_maps(rules, user_groups):
    secure_maps_array = []
    for rule in rules:
        if rule['group'].lower() in user_groups:
            secure_maps_array.append(rule['map_service'])
    return secure_maps_array
