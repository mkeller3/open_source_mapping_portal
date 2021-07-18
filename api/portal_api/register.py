


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema


class registerView(APIView):

    @swagger_auto_schema(request_body=UserSerializer, operation_description="Register to use the portal api")
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.data['username'],
                email=serializer.data['email']
            )

            user.set_password(serializer.data['password'])
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)