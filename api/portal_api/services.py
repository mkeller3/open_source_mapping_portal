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

    @swagger_auto_schema(operation_description="Get an array of all prebuilt maps within Mapping Portal")
    def get(self, request):
        serializer = mapServiceDataSerializer(mapServiceData.objects.all(), many=True)
        return Response(serializer.data)

# Autocomplete

# WMS Search

# Page View

# Survey View

# Master portal search

# View map services

# Break Values

# Download Data

# map service view

# portal table

# portal tables

# Autocomplete