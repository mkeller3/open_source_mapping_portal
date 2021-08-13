from django.core.exceptions import ObjectDoesNotExist
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

columns = ['username','app_id','app_type','app_data','created_time',
    'updated_time','updated_username','read_access_list','write_access_list',
    'notification_access_list','bounding_box','tags','title','basemap', 
    'disclaimer','description','searchable','built_from_map','map_id',
    'retention_date','views','image','built_from_map','map_id']

# Class that will allow CRUD of apps
class appView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericAppSerializer ,operation_description="Get an app with Mapping Portal")
    def get(self, request):
        serializer = genericAppSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            details = appData.objects.get(app_id=serializer.validated_data['app_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = appData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,app_id=serializer.validated_data['app_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        details = appData.objects.get(app_id=serializer.validated_data['app_id'])
        details.views+=1
        details.save()
        serializer = appDataNoImageSerializer(details)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=appDataSerializer, operation_description="Create an app within Mapping Portal")
    def post(self, request):
        serializer = appDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {str(request.user.username)} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {str(request.user.username)} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=appDataSerializer, operation_description="Update an app within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        try:
            details = appData.objects.get(app_id=request.data['app_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = appData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,app_id=request.data['app_id']) for group in user_groups]))
        except details.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = appDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)

        if details.username not in serializer.validated_data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {details.username} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if details.username not in serializer.validated_data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {details.username} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=details.username,updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericAppSerializer, operation_description="Delete an app within Mapping Portal")
    def delete(self, request):
        serializer = genericAppSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
             details = appData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,app_id=serializer.validated_data['app_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Class that returns the image tied to an app
class appImageView(LoggingMixin, APIView):

    @swagger_auto_schema(query_serializer=genericAppSerializer ,operation_description="Get an app image within Mapping Portal")
    def get(self, request):
        serializer = genericAppSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            details = appData.objects.get(app_id=serializer.validated_data['app_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = appDataImageSerializer(details)
        return Response(details)

# Class that returns all apps created by a user
class personalAppsView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=apiSearchSerializer, operation_description="Get an array of all your apps within Mapping Portal")
    def get(self, request):
        serializer = apiSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        limit, offset = get_limit_and_offset(serializer)
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            details = appData.objects.filter(Q(username=request.user.username),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values(*columns)[offset:limit]
            total_results = appData.objects.filter(Q(username=request.user.username),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values('app_id')
        else:
            details = appData.objects.filter(username=request.user.username).values(*columns)[offset:limit]
            total_results = appData.objects.filter(username=request.user.username).values('app_id')[offset:limit]
        serializer = appDataNoImageSerializer(details, many=True)
        results = {
            'results': serializer.data,
            'count': len(serializer.data),
            'total_results': len(total_results)
        }
        return Response(results)

# Class that returns all apps a user has read access to
class allAppsView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=apiSearchSerializer, operation_description="Get an array of all apps you have access to within Mapping Portal")
    def get(self, request):
        serializer = apiSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        limit, offset = get_limit_and_offset(serializer)
        user_groups = get_user_groups(request.user.username) 
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            details = appData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups]),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values(*columns)[offset:limit]
            total_results = appData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups]),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values('app_id')
        else:
            details = appData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups])).values(*columns)[offset:limit]
            total_results = appData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups])).values('app_id')[offset:limit]
        serializer = appDataNoImageSerializer(details, many=True)
        results = {
            'results': serializer.data,
            'count': len(serializer.data),
            'total_results': len(total_results)
        }
        return Response(results)

# Class that allows a user to duplicate an app that they have write access to
class duplicateAppView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=genericAppSerializer, operation_description="Duplicate an app you have access to within Mapping Portal.")
    def post(self, request):
        serializer = genericAppSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            appData.objects.get(app_id=serializer.validated_data['app_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            appData.objects.filter(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,app_id=serializer.validated_data['app_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        details = appData.objects.get(app_id=serializer.validated_data['app_id'])

        details.user_alias = request.user.username
        details.updated_user_alias = request.user.username
        details.title = f"{details.title} (Copy)"

        del details['app_id']

        new_app_data = appData.objects.create(details)

        new_details = appData.objects.get(app_id=new_app_data.app_id)

        serializer = appDataSerializer(new_details)

        return Response(serializer.data)

# Class that allows a users to pull back analytics for an app they have write access to
class analyticsAppView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericAppSerializer, operation_description="Get an activity log of an app you have write access to within Mapping Portal.")
    def get(self, request):
        serializer = genericAppSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            appData.objects.get(app_id=serializer.validated_data['app_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            appData.objects.filter(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,app_id=serializer.validated_data['app_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        conn = psycopg2.connect(database=api_db, user=api_db_user, password=api_db_pwd, host=api_db_host)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql.SQL("SELECT b.username, a.requested_at, a.response_ms, a.method, a.host FROM rest_framework_tracking_apirequestlog a JOIN auth_user b ON b.id = a.user_id WHERE path = '/api/v1/apps/app/' AND query_params = '{''app_id'': '%s'}'"),(serializer.validated_data['app_id'],))
        results = cur.fetchall()

        return Response({'api_calls': results})

# Transfer Ownership