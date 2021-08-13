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

columns = ['username','table_id','created_time', 'geometry_type', 'bounding_box',
    'updated_time','updated_username','read_access_list','write_access_list',
    'notification_access_list','bounding_box','tags','title',
    'description','searchable','views','image', 'retention_date',
    'rows','size','style','sensitive']

# Class that will allow CRUD of tables
class tableView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericTableSerializer, operation_description="Get an table within Mapping Portal")
    def get(self, request):
        serializer = genericTableSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            tableData.objects.get(table_id=serializer.validated_data['table_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,table_id=serializer.validated_data['table_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        details = tableData.objects.get(table_id=serializer.validated_data['table_id'])
        details.views+=1
        details.save()
        serializer = tableDataNoImageSerializer(details)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=tableDataSerializer, operation_description="Update an table_within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        try:
            details = tableData.objects.get(table_id=request.data['table_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = tableData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,table_id=request.data['table_id']) for group in user_groups]))
        except details.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = tableDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)

        if details.username not in serializer.validated_data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {details.username} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if details.username not in serializer.validated_data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {details.username} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=details.username,updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericTableSerializer, operation_description="Delete an table_within Mapping Portal")
    def delete(self, request):
        serializer = genericTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            details = tableData.objects.get(table_id=request.data['table_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
             details = tableData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,table_id=serializer.validated_data['table_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Class that returns the image tied to an table
class tableImageView(LoggingMixin, APIView):

    @swagger_auto_schema(query_serializer=genericTableSerializer ,operation_description="Get an table_image within Mapping Portal")
    def get(self, request):
        serializer = genericTableSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            details = tableData.objects.get(table_id=serializer.validated_data['table_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = tableDataImageSerializer(details)
        return Response(details)

# Class that returns all tables created by a user
class personalTablesView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=apiSearchSerializer, operation_description="Get an array of all your tables within Mapping Portal")
    def get(self, request):
        serializer = apiSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        limit, offset = get_limit_and_offset(serializer)
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            details = tableData.objects.filter(Q(username=request.user.username),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values(*columns)[offset:limit]
            total_results = tableData.objects.filter(Q(username=request.user.username),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values('table_id')
        else:
            details = tableData.objects.filter(username=request.user.username).values(*columns)[offset:limit]
            total_results = tableData.objects.filter(username=request.user.username).values('table_id')[offset:limit]
        serializer = tableDataNoImageSerializer(details, many=True)
        results = {
            'results': serializer.data,
            'count': len(serializer.data),
            'total_results': len(total_results)
        }
        return Response(results)

# Class that returns all tables a user has read access to
class allTablesView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=apiSearchSerializer, operation_description="Get an array of all tables you have access to within Mapping Portal")
    def get(self, request):
        serializer = apiSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        limit, offset = get_limit_and_offset(serializer)
        user_groups = get_user_groups(request.user.username) 
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            details = tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups]),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values(*columns)[offset:limit]
            total_results = tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups]),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values('table_id')
        else:
            details = tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups])).values(*columns)[offset:limit]
            total_results = tableData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups])).values('table_id')[offset:limit]
        serializer = tableDataNoImageSerializer(details, many=True)
        results = {
            'results': serializer.data,
            'count': len(serializer.data),
            'total_results': len(total_results)
        }
        return Response(results)

# Class that allows a user to duplicate an table_that they have write access to
class duplicateTableView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=genericTableSerializer, operation_description="Duplicate an table_you have access to within Mapping Portal.")
    def post(self, request):
        serializer = genericTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            tableData.objects.get(table_id=serializer.validated_data['table_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            tableData.objects.filter(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,table_id=serializer.validated_data['table_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        details = tableData.objects.get(table_id=serializer.validated_data['table_id'])

        details.user_alias = request.user.username
        details.updated_user_alias = request.user.username
        details.title = f"{details.title} (Copy)"

        del details['table_id']

        new_table_data = tableData.objects.create(details)

        new_details = tableData.objects.get(table_id=new_table_data.table_id)

        serializer = tableDataSerializer(new_details)

        return Response(serializer.data)

# Class that allows a users to pull back analytics for an table_they have write access to
class analyticsTableView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericTableSerializer, operation_description="Get an activity log of an table_you have write access to within Mapping Portal.")
    def get(self, request):
        serializer = genericTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            tableData.objects.get(table_id=serializer.validated_data['table_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            tableData.objects.filter(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,table_id=serializer.validated_data['table_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        conn = psycopg2.connect(database=api_db, user=api_db_user, password=api_db_pwd, host=api_db_host)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql.SQL("SELECT b.username, a.requested_at, a.response_ms, a.method, a.host FROM rest_framework_tracking_apirequestlog a JOIN auth_user b ON b.id = a.user_id WHERE path = '/api/v1/tables/table/' AND query_params = '{''table_id'': '%s'}'"),(serializer.validated_data['table_id'],))
        results = cur.fetchall()

        return Response({'api_calls': results})

# Transfer Ownership

# Table Edit

# Add column

# Delete Column

# Transfer Ownership