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


# Feature Columns
class featureColumnsView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(operation_description="Get an tables columns with in Mapping Portal")
    def post(self, request):
        serializer = tableColumnsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 

        if serializer.validated_data['table_type'] == 'user_data':
            try:
                details = tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,table_id=serializer.validated_data['table_name']) for group in user_groups]))
            except tableData.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(sql.SQL("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '{table}' AND data_type != 'USER-DEFINED' And column_name != 'gid';").format(table=sql.SQL(serializer.validated_data['table_name'])))
            columns = cur.fetchall()
            cur.close()
            conn.close()

        return Response(columns)

# Map Query
class featureQueryView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(operation_description="Query a table within Mapping Portal")
    def post(self, request):
        serializer = tableColumnsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        format = serializer.validated_data['format']

        if serializer.validated_data['table_type'] == 'user_data':
            try:
                details = tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,table_id=serializer.validated_data['table_name']) for group in user_groups]))
            except tableData.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            conn = psycopg2.connect(database=data_db, user=api_db_user, password=api_db_pwd, host=api_db_host)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            if format == 'geojson':
                cur.execute(sql.SQL("SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(ST_AsGeoJSON({table}.*)::json)) FROM {table};").format(table=sql.SQL(serializer.validated_data['table_name'])))
                data = cur.fetchone()['json_build_object']
            # elif format == 'json':
                # TODO
            cur.close()
            conn.close()
        
        return Response(data)

# Map Stats

# bbox

# custom range values

# bins