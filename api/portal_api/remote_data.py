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

# Class that will allow CRUD of remote datasets
class remoteDataView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=genericRemoteDataSerializer ,operation_description="Get an remote dataset with Mapping Portal")
    def get(self, request):
        serializer = genericRemoteDataSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
            details = remoteUserData.objects.get(data_id=serializer.validated_data['data_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = remoteUserData.objects.filter(reduce(lambda x, y: x | y, [Q(read_access_list__icontains=group,data_id=serializer.validated_data['data_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        details = remoteUserData.objects.get(data_id=serializer.validated_data['data_id'])
        details.save()
        serializer = remoteDataSerializer(details)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=remoteDataSerializer, operation_description="Create an remote dataset within Mapping Portal")
    def post(self, request):
        serializer = remoteDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {str(request.user.username)} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {str(request.user.username)} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=remoteDataSerializer, operation_description="Update an remote dataset within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        try:
            details = remoteUserData.objects.get(data_id=request.data['data_id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            details = remoteUserData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,data_id=request.data['data_id']) for group in user_groups]))
        except details.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = remoteDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)

        if details.username not in serializer.validated_data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {details.username} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if details.username not in serializer.validated_data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {details.username} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=details.username,updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericRemoteDataSerializer, operation_description="Delete an remote dataset within Mapping Portal")
    def delete(self, request):
        serializer = genericRemoteDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_groups = get_user_groups(request.user.username) 
        try:
             details = remoteUserData.objects.get(reduce(lambda x, y: x | y, [Q(write_access_list__icontains=group,data_id=serializer.validated_data['data_id']) for group in user_groups]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
