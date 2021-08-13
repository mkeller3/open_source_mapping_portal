from rest_framework.compat import distinct
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


class geocodeView(LoggingMixin, APIView):
    ### Class that allows someone to geocode an array of addresses
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=addressSerializer, operation_description="Geocode an array of addresses within Mapping Portal")
    def post(self, request):
        serializer = addressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        results = {
            "type": "FeatureCollection",
            "features": []
        }

        for address in serializer.validated_data['addresses']:
            results['features'].append(geocode_address(address))
        
        return Response(results)

# Map Query
class mapQueryView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=tableQuerySerializer, operation_description="Query a table within Mapping Portal")
    def get(self, request):
        serializer = tableQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 

        if serializer.validated_data['table_type'] == 'user_data':
            try:
                details = tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,table_id=serializer.validated_data['table_name']) for group in user_groups]))
            except tableData.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis")
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = sql.SQL("SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(ST_AsGeoJSON({table}.*)::json)) FROM {table} ").format(table=sql.SQL(serializer.validated_data['table_name']))

            if 'offset' in serializer.validated_data:
                query += sql.SQL("OFFSET {offset} ").format(offset=sql.SQL(str(serializer.validated_data['offset'])))

            if 'limit' in serializer.validated_data:
                limit = serializer.validated_data['limit']
            else:
                limit = settings.MAX_NUMBER_OF_FEATURE_RESULTS
            query += sql.SQL("LIMIT {limit} ").format(limit=sql.SQL(str(limit)))
            
            print(query)
            cur.execute(query)
            data = cur.fetchone()['json_build_object']

            cur.close()
            conn.close()
        
        return Response(data)

# Portal Tables
class portalTablesView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=portalTablesSerializer, operation_description="Get an array of all prebuilt tables within Mapping Portal")
    def get(self, request):
        serializer = portalTablesSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            map_services = mapServiceData.objects.filter(Q(display_name_icontains=search_term)|Q(description_icontains=search_term))
        else:
            map_services = mapServiceData.objects.all()

        map_security = mapSecurityData.objects.all()

        accessible_maps = get_accessible_maps(map_security, user_groups)

        for map in map_services:
            if map['secure'] == True and map['display_name'] not in accessible_maps:
                map_services = map_services.exclude(pk=map['id'])

        serializer = mapServiceDataSerializer(map_services, many=True)
        return Response(serializer.data)

# Portal Table
class portalTableView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=portalTableSerializer, operation_description="Get a prebuilt table within Mapping Portal")
    def get(self, request):
        serializer = portalTableSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            mapServiceData.objects.get(table_name=serializer.validated_data['table_name'])
        except mapServiceData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.validated_data['table_name'] not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        details = mapServiceData.objects.get(table_name=serializer.validated_data['table_name'])
        return Response(details)


# Autocomplete
class autocompleteView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=autocompleteSerializer, operation_description="Get an array of possible values for a table within Mapping Portal.")
    def get(self, request):
        serializer = autocompleteSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 

        if serializer.validated_data['table_type'] == 'user_data':
            try:
                tableData.objects.get(table_id=serializer.validated_data['table'])
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,table_id=serializer.validated_data['table']) for group in user_groups]))
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif serializer.validated_data['table_type'] == 'map_layer':
            try:
                secure_layer = mapServiceData.objects.get(table_name=serializer.validated_data['table']).secure_layer
            except mapServiceData.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if secure_layer:
                if serializer.validated_data['table'] not in user_groups:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host, options="-c search_path=user_data,postgis")
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql.SQL("SELECT DISTINCT({column}) FROM {table} WHERE LOWER(CAST({column} AS text)) LIKE LOWER('%{value}%') LIMIT 10;").format(table=sql.SQL(serializer.validated_data['table']),value=sql.SQL(serializer.validated_data['table_value']),column=sql.SQL(serializer.validated_data['table_column'])))
        distinct_values = cur.fetchall()
        cur.close()
        conn.close()
        return Response({"values": distinct_values})

# WMS Search

# Page View

# Survey View

# Master portal search

# View map services

# Break Values

# Download Data

# map service view
