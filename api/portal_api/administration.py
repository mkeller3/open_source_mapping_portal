from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .helpers import *
from .constants import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework_tracking.mixins import LoggingMixin

# Map Service Configuration
class mapServiceConfigurationView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=mapServiceDataSerializer, operation_description="Create a map service within Mapping Portal")
    def post(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = mapServiceDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=mapServiceDataSerializer, operation_description="Update a map service within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            details = mapServiceData.objects.get(map_service_id=request.data['map_service_id'])
        except mapServiceData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = mapServiceDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(username=details.username, updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericMapServiceSerializer, operation_description="Delete a map service within Mapping Portal")
    def delete(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            details = mapServiceData.objects.get(map_service_id=request.data['map_service_id'])
        except mapServiceData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Map Service Security
class mapServiceSecurityConfigurationView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=mapServiceSecurityDataSerializer, operation_description="Create a map service security within Mapping Portal")
    def post(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = mapServiceSecurityDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=mapServiceSecurityDataSerializer, operation_description="Update a map service security within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            details = mapSecurityData.objects.get(map_service_security_id=request.data['map_service_security_id'])
        except mapSecurityData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = mapServiceSecurityDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(username=details.username, updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericMapServiceSecuritySerializer, operation_description="Delete a map service security within Mapping Portal")
    def delete(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            details = mapSecurityData.objects.get(map_service_security_id=request.data['map_service_security_id'])
        except mapSecurityData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Blocked Users
class blockedUserView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=blockedUserDataSerializer, operation_description="Create a blocked user within Mapping Portal")
    def post(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = blockedUserDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=blockedUserDataSerializer, operation_description="Update a blocked user within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            details = blockedUserData.objects.get(blocked_user_id=request.data['blocked_user_id'])
        except blockedUserData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = blockedUserDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(username=details.username, updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericBlockedUserDataSerializer, operation_description="Delete a map service security within Mapping Portal")
    def delete(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            details = blockedUserData.objects.get(blocked_user_id=request.data['blocked_user_id'])
        except blockedUserData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Alerts
class alertView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=alertDataSerializer, operation_description="Create an alert within Mapping Portal")
    def post(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = alertDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=alertDataSerializer, operation_description="Update an alert within Mapping Portal")
    def put(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            details = alertData.objects.get(alert_id=request.data['alert_id'])
        except alertData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = alertDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(username=details.username, updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericAlertDataSerializer, operation_description="Delete an alert within Mapping Portal")
    def delete(self, request):
        user_groups = get_user_groups(request.user.username) 
        if 'admins' not in user_groups:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            details = alertData.objects.get(alert_id=request.data['alert_id'])
        except alertData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)