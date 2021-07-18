from os import name
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

columns = ['username','site_id','created_time',
    'updated_time','updated_username','read_access_list','write_access_list',
    'notification_access_list','bounding_box','tags','title',
    'disclaimer','description','searchable','views','image']

# Class that will allow CRUD of sites
class siteView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericSiteSerializer, operation_description="Get an site within Mapping Portal")
    def get(self, request):
        serializer = genericSiteSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            details = siteData.objects.get(site_id=serializer.validated_data['site_id'])
        except siteData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = siteData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,site_id=serializer.validated_data['site_id']) for group in user_groups]))
        except siteData.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        details = siteData.objects.get(site_id=serializer.validated_data['site_id'])
        details.views+=1
        details.save()
        serializer = siteDataNoImageSerializer(details)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=siteDataSerializer, operation_description="Create an site within Mapping Portal")
    def post(self, request):
        serializer = siteDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {str(request.user.username)} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {str(request.user.username)} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=siteDataSerializer, operation_description="Update an site within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        try:
            details = siteData.objects.get(site_id=request.data['site_id'])
        except siteData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = siteData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,site_id=request.data['site_id']) for group in user_groups]))
        except details.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = siteDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)

        if details.username not in serializer.validated_data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {details.username} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if details.username not in serializer.validated_data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {details.username} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=details.username,updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericSiteSerializer, operation_description="Delete an site within Mapping Portal")
    def delete(self, request):
        serializer = genericSiteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
             details = siteData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,site_id=serializer.validated_data['site_id']) for group in user_groups]))
        except siteData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Class that returns the image tied to an table
class siteImageView(LoggingMixin, APIView):

    @swagger_auto_schema(query_serializer=genericSiteSerializer ,operation_description="Get an site image within Mapping Portal")
    def get(self, request):
        serializer = genericSiteSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            details = siteData.objects.get(site_id=serializer.validated_data['site_id'])
        except siteData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = siteDataImageSerializer(details)
        return Response(details)

# Class that returns all sites created by a user
class personalSitesView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=apiSearchSerializer, operation_description="Get an array of all your sites within Mapping Portal")
    def get(self, request):
        serializer = apiSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        limit, offset = get_limit_and_offset(serializer)
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            details = siteData.objects.filter(Q(username=request.user.username),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values(*columns)[offset:limit]
            total_results = siteData.objects.filter(Q(username=request.user.username),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values('site_id')
        else:
            details = siteData.objects.filter(username=request.user.username).values(*columns)[offset:limit]
            total_results = siteData.objects.filter(username=request.user.username).values('site_id')[offset:limit]
        serializer = siteDataNoImageSerializer(details, many=True)
        results = {
            'results': serializer.data,
            'count': len(serializer.data),
            'total_results': len(total_results)
        }
        return Response(results)

# Class that returns all sites a user has read access to
class allSitesView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=apiSearchSerializer, operation_description="Get an array of all sites you have access to within Mapping Portal")
    def get(self, request):
        serializer = apiSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        limit, offset = get_limit_and_offset(serializer)
        user_groups = get_user_groups(request.user.username) 
        if 'search' in serializer.validated_data:
            search_term = serializer.validated_data['search']
            details = siteData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups]),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values(*columns)[offset:limit]
            total_results = siteData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups]),Q(description__icontains=search_term)|Q(title__icontains=search_term)).values('site_id')
        else:
            details = siteData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups])).values(*columns)[offset:limit]
            total_results = siteData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group) for group in user_groups])).values('site_id')[offset:limit]
        serializer = siteDataNoImageSerializer(details, many=True)
        results = {
            'results': serializer.data,
            'count': len(serializer.data),
            'total_results': len(total_results)
        }
        return Response(results)

# Class that allows a user to duplicate an site that they have write access to
class duplicateSiteView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=genericSiteSerializer, operation_description="Duplicate an site you have access to within Mapping Portal.")
    def post(self, request):
        serializer = genericSiteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            siteData.objects.get(site_id=serializer.validated_data['site_id'])
        except siteData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            siteData.objects.filter(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,site_id=serializer.validated_data['site_id']) for group in user_groups]))
        except siteData.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        details = siteData.objects.get(site_id=serializer.validated_data['site_id'])

        details.user_alias = request.user.username
        details.updated_user_alias = request.user.username
        details.title = f"{details.title} (Copy)"

        del details['site_id']

        new_site_data = siteData.objects.create(details)

        new_details = siteData.objects.get(site_id=new_site_data.site_id)

        serializer = siteDataSerializer(new_details)

        return Response(serializer.data)

# Class that allows a users to pull back analytics for an site they have write access to
class analyticsSiteView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericSiteSerializer, operation_description="Get an activity log of an site you have write access to within Mapping Portal.")
    def get(self, request):
        serializer = genericSiteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            siteData.objects.filter(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,site_id=serializer.validated_data['site_id']) for group in user_groups]))
        except siteData.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        conn = psycopg2.connect(database=api_db, user=api_db_user, password=api_db_pwd, host=api_db_host)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql.SQL("SELECT b.username, a.requested_at, a.response_ms, a.method, a.host FROM rest_framework_tracking_apirequestlog a JOIN auth_user b ON b.id = a.user_id WHERE path = '/api/v1/sites/site/' AND query_params = '{''site_id'': '%s'}'"),(serializer.validated_data['site_id'],))
        results = cur.fetchall()

        return Response({'api_calls': results})

# Transfer Ownership