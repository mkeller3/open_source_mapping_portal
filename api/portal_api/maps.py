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

columns = ['username','map_id','created_time', 'layers', 'pitch', 'bearing',
    'updated_time','updated_username','read_access_list','write_access_list',
    'notification_access_list','bounding_box','tags','title','basemap', 
    'disclaimer','description','searchable','views','image']

# Class that will allow CRUD of maps
class mapView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericMapSerializer, operation_description="Get an map within Mapping Portal")
    def get(self, request):
        serializer = genericMapSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            details = mapData.objects.get(map_id=serializer.validated_data['map_id'])
        except mapData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = mapData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,map_id=serializer.validated_data['map_id']) for group in user_groups]))
        except mapData.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        details = mapData.objects.get(map_id=serializer.validated_data['map_id'])
        details.views+=1
        details.save()
        serializer = mapDataNoImageSerializer(details)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=mapDataSerializer, operation_description="Create an map within Mapping Portal")
    def post(self, request):
        serializer = mapDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {str(request.user.username)} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {str(request.user.username)} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=mapDataSerializer, operation_description="Update an map within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        try:
            details = mapData.objects.get(map_id=request.data['map_id'])
        except mapData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = mapData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,map_id=request.data['map_id']) for group in user_groups]))
        except details.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = mapDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)

        if details.username not in serializer.validated_data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {details.username} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if details.username not in serializer.validated_data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {details.username} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=details.username,updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericMapSerializer, operation_description="Delete an map within Mapping Portal")
    def delete(self, request):
        serializer = genericMapSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
             details = mapData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,map_id=serializer.validated_data['map_id']) for group in user_groups]))
        except mapData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Class that returns the image tied to an table
class mapImageView(LoggingMixin, APIView):

    @swagger_auto_schema(query_serializer=genericMapSerializer ,operation_description="Get an map image within Mapping Portal")
    def get(self, request):
        serializer = genericMapSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            details = mapData.objects.get(map_id=serializer.validated_data['map_id'])
        except mapData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = mapDataImageSerializer(details)
        return Response(details)

# Class that returns all maps created by a user
class personalMapsView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=apiSearchSerializer, operation_description="Get an array of all your maps within Mapping Portal")
    def get(self, request):
        serializer = apiSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        limit, offset = get_limit_and_offset(serializer)
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            details = mapData.objects.filter(Q(username=request.user.username),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values(*columns)[offset:limit]
            total_results = mapData.objects.filter(Q(username=request.user.username),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values('map_id')
        else:
            details = mapData.objects.filter(username=request.user.username).values(*columns)[offset:limit]
            total_results = mapData.objects.filter(username=request.user.username).values('map_id')[offset:limit]
        serializer = mapDataNoImageSerializer(details, many=True)
        results = {
            'results': serializer.data,
            'count': len(serializer.data),
            'total_results': len(total_results)
        }
        return Response(results)

# Class that returns all maps a user has read access to
class allMapsView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=apiSearchSerializer, operation_description="Get an array of all maps you have access to within Mapping Portal")
    def get(self, request):
        serializer = apiSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        limit, offset = get_limit_and_offset(serializer)
        user_groups = get_user_groups(request.user.username) 
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            details = mapData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups]),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values(*columns)[offset:limit]
            total_results = mapData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups]),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values('map_id')
        else:
            details = mapData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups])).values(*columns)[offset:limit]
            total_results = mapData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups])).values('map_id')[offset:limit]
        serializer = mapDataNoImageSerializer(details, many=True)
        results = {
            'results': serializer.data,
            'count': len(serializer.data),
            'total_results': len(total_results)
        }
        return Response(results)

# Class that allows a user to duplicate an map that they have write access to
class duplicateMapView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=genericMapSerializer, operation_description="Duplicate an map you have access to within Mapping Portal.")
    def post(self, request):
        serializer = genericMapSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            mapData.objects.get(map_id=serializer.validated_data['map_id'])
        except mapData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            mapData.objects.filter(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,map_id=serializer.validated_data['map_id']) for group in user_groups]))
        except mapData.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        details = mapData.objects.get(map_id=serializer.validated_data['map_id'])

        details.user_alias = request.user.username
        details.updated_user_alias = request.user.username
        details.title = f"{details.title} (Copy)"

        del details['map_id']

        new_map_data = mapData.objects.create(details)

        new_details = mapData.objects.get(map_id=new_map_data.map_id)

        serializer = mapDataSerializer(new_details)

        return Response(serializer.data)

# Class that allows a users to pull back analytics for an map they have write access to
class analyticsMapView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericMapSerializer, operation_description="Get an activity log of an map you have write access to within Mapping Portal.")
    def get(self, request):
        serializer = genericMapSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            mapData.objects.filter(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,map_id=serializer.validated_data['map_id']) for group in user_groups]))
        except mapData.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        conn = psycopg2.connect(database=api_db, user=api_db_user, password=api_db_pwd, host=api_db_host)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql.SQL("SELECT b.username, a.requested_at, a.response_ms, a.method, a.host FROM rest_framework_tracking_apirequestlog a JOIN auth_user b ON b.id = a.user_id WHERE path = '/api/v1/maps/map/' AND query_params = '{''map_id'': '%s'}'"),(serializer.validated_data['map_id'],))
        results = cur.fetchall()

        return Response({'api_calls': results})

# Transfer Ownership