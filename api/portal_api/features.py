from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .helpers import *
from .constants import *
from django.db.models import Q
from functools import reduce
from drf_yasg.utils import swagger_auto_schema
from rest_framework_tracking.mixins import LoggingMixin
from django.core.exceptions import ObjectDoesNotExist


# Feature Columns
class featureColumnsView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=tableColumnsSerializer, operation_description="Get an tables columns with in Mapping Portal")
    def get(self, request):
        serializer = tableColumnsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 

        if serializer.validated_data['table_type'] == 'user_data':
            try:
                tableData.objects.get(table_id=serializer.validated_data['table_name'])
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,table_id=serializer.validated_data['table_name']) for group in user_groups]))
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif serializer.validated_data['table_type'] == 'map_layer':
            try:
                secure_layer = mapServiceData.objects.get(table_name=serializer.validated_data['table_name']).secure_layer
            except mapServiceData.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if secure_layer:
                if serializer.validated_data['table_name'] not in user_groups:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql.SQL("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '{table}' AND data_type != 'USER-DEFINED';").format(table=sql.SQL(serializer.validated_data['table_name'])))
        columns = cur.fetchall()
        cur.close()
        conn.close()

        return Response(columns)

# Map Query
class featureQueryView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=tableQuerySerializer, operation_description="Query a table within Mapping Portal")
    def get(self, request):
        serializer = tableQuerySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 

        if serializer.validated_data['table_type'] == 'user_data':
            try:
                tableData.objects.get(table_id=serializer.validated_data['table_name'])
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,table_id=serializer.validated_data['table_name']) for group in user_groups]))
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif serializer.validated_data['table_type'] == 'map_layer':
            try:
                secure_layer = mapServiceData.objects.get(table_name=serializer.validated_data['table_name']).secure_layer
            except mapServiceData.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if secure_layer:
                if serializer.validated_data['table_name'] not in user_groups:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

        conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis,default_maps")
        cur = conn.cursor(cursor_factory=RealDictCursor)

        query = sql.SQL("SELECT jsonb_build_object('type','FeatureCollection','features',jsonb_agg(feature))FROM(SELECT jsonb_build_object('type','Feature','id',gid,")
        if 'return_geometry' in serializer.validated_data:
            if serializer.validated_data['return_geometry']:
                query += sql.SQL("'geometry', ST_AsGeoJSON(geom)::jsonb,")
            else:
                query += sql.SQL("'geometry', Null,")
        
        query += sql.SQL("'properties', to_jsonb(row) - 'gid' - 'geom') AS feature FROM (")

        if 'fields' in serializer.validated_data:
            query += sql.SQL("SELECT gid,geom,{fields} FROM {table}").format(fields=sql.SQL(serializer.validated_data['fields']),table=sql.Identifier(serializer.validated_data['table_name']))
        else:
            query += sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(serializer.validated_data['table_name']))

        count_query = sql.SQL("SELECT COUNT(*) FROM {table}").format(table=sql.Identifier(serializer.validated_data['table_name']))

        if 'coordinates' in serializer.validated_data and 'geometry_type' in serializer.validated_data and 'spatial_relationship' in serializer.validated_data:
            if serializer.validated_data['geometry_type'] == 'POLYGON':
                query += sql.SQL("WHERE {spatial_rel}(ST_GeomFromText('{geom_type}(({coords}))',4326) ,{table}.geom)").format(coords=sql.SQL(serializer.validated_data['coordinates']),geom_type=sql.SQL(serializer.validated_data['geometry_type']),spatial_rel=sql.SQL(serializer.validated_data['spatial_relationship']),table=sql.Identifier(serializer.validated_data['table_name']))
                count_query += sql.SQL("WHERE {spatial_rel}(ST_GeomFromText('{geom_type}(({coords}))',4326) ,{table}.geom)").format(coords=sql.SQL(serializer.validated_data['coordinates']),geom_type=sql.SQL(serializer.validated_data['geometry_type']),spatial_rel=sql.SQL(serializer.validated_data['spatial_relationship']),table=sql.Identifier(serializer.validated_data['table_name']))
            else:
                query += sql.SQL("WHERE {spatial_rel}(ST_GeomFromText('{geom_type}({coords})',4326) ,{table}.geom)").format(coords=sql.SQL(serializer.validated_data['coordinates']),geom_type=sql.SQL(serializer.validated_data['geometry_type']),spatial_rel=sql.SQL(serializer.validated_data['spatial_relationship']),table=sql.Identifier(serializer.validated_data['table_name']))
                count_query += sql.SQL("WHERE {spatial_rel}(ST_GeomFromText('{geom_type}({coords})',4326) ,{table}.geom)").format(coords=sql.SQL(serializer.validated_data['coordinates']),geom_type=sql.SQL(serializer.validated_data['geometry_type']),spatial_rel=sql.SQL(serializer.validated_data['spatial_relationship']),table=sql.Identifier(serializer.validated_data['table_name']))

        if 'limit' in serializer.validated_data:
            query += sql.SQL(" LIMIT {limit}").format(limit=sql.SQL(str(serializer.validated_data['limit'])))
        else:
            query += sql.SQL(" LIMIT {limit}").format(limit=sql.SQL(str(settings.MAX_FEATURES_PER_TILE)))

        if 'offset' in serializer.validated_data:
            query += sql.SQL(" OFFSET {offset}").format(offset=sql.SQL(str(serializer.validated_data['offset'])))

        query += sql.SQL(") row) features;")

        cur.execute(query)
        data = cur.fetchone()['jsonb_build_object']
        cur.execute(count_query)

        if data['features'] != None:
            data['number_of_results'] = len(data['features'])
        else:
            data['number_of_results'] = 0
        data['number_of_possible_results'] = cur.fetchone()['count']

        cur.close()
        conn.close()
        
        return Response(data)

# Map Stats

# bbox

# custom range values

# bins