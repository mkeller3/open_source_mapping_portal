from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.db.models import Q
from functools import reduce
from drf_yasg.utils import swagger_auto_schema
from rest_framework_tracking.mixins import LoggingMixin
from django.core.exceptions import ObjectDoesNotExist

# User Search
class userSearchView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=defaultSearchSerializer, operation_description="Search for users within Mapping Portal")
    def get(self, request):
        serializer = defaultSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            details = User.objects.filter(username__icontains=serializer.validated_data['search']).values('username', 'email')
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = userSearchSerializer(details, many=True)
        return Response(serializer.data)

# Group Search
class groupSearchView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(query_serializer=defaultSearchSerializer, operation_description="Search for groups within Mapping Portal")
    def get(self, request):
        serializer = defaultSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            details = groupData.objects.filter(group_name__icontains=serializer.validated_data['search']).values('group_name', 'group_id')
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = groupSearchSerializer(details, many=True)
        return Response(serializer.data)

# TODO
# User Preference


class groupView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(operation_description="Get a group with Mapping Portal")
    def get(self, request):
        try:
            details = groupData.objects.filter(users__contains=request.user.username)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        details = groupData.objects.get(group_id=request.GET.get('group_id'))
        serializer = groupDataSerializer(details)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=groupDataSerializer, operation_description="Create a group with Mapping Portal")
    def post(self, request):
        serializer = groupDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['users']:
            return Response({"error":f"Username is not in users. Add {str(request.user.username)} to users and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['owners']:
            return Response({"error":f"Username is not in owners. Add {str(request.user.username)} to owners and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=groupDataSerializer, operation_description="Update a group with Mapping Portal")
    def put(self, request):        
        try:
            details = groupData.objects.get(owners__contains=request.user.username)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = groupDataSerializer(details, data=request.data)
        serializer.is_valid(raise_exception=True)
        if details.username not in request.data['users']:
            return Response({"error":f"Username is not in users. Add {details.username} to users and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if details.username not in request.data['owners']:
            return Response({"error":f"Username is not in owners. Add {details.username} to owners and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(username=details.username,updated_username=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=genericGroupSerializer, operation_description="Delete a group with Mapping Portal")
    def delete(self, request):
        try:
            details = groupData.objects.get(owners__contains=request.user.username)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class allGroupsView(APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(operation_description="Get an array of all you groups you have access to within Mapping Portal")
    def get(self, request):
        details = groupData.objects.filter(users__contains=request.user.username)        
        serializer = groupDataSerializer(details, many=True)
        return Response(serializer.data)

class globalSearchView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(operation_description="Search for users/groups within Mapping Portal")
    def get(self, request):
        serializer = defaultSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            group_details = groupData.objects.filter(group_name__icontains=serializer.validated_data['search']).values('group_name', 'group_id')
            user_details = User.objects.filter(username__icontains=serializer.validated_data['search']).values('username')
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        results = []
        if len(group_details) > 0:
            for group in group_details:
                results.append({
                    "title": group.group_name,
                    "value": group.group_id
                })
        if len(user_details) > 0:
            for user in user_details:
                results.append({
                    "title": user['username'],
                    "value": user['username']
                })

        return Response(results)