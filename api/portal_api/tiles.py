from django.contrib.auth import REDIRECT_FIELD_NAME
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import fields, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
from .serializers import *
from .helpers import *
from .constants import *
from django.db.models import Q
from functools import reduce
from drf_yasg.utils import swagger_auto_schema
from rest_framework_tracking.mixins import LoggingMixin
import sys

class BinaryRenderer(BaseRenderer):
    media_type = "application/*"
    format = "binary"
    charset = None
    render_style = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

# Class to get vector tiles from map
class tilesView(APIView):
    permission_classes = (IsAuthenticated),

    renderer_classes = (BinaryRenderer,)

    @swagger_auto_schema(operation_description="Get vector tiles for map")
    def get(self, request, database, table_name, z, x, y):
        try:    

            fields = request.GET.get('fields')

            try:
                pbf = sqlToPbf(database, table_name, z, x, y, fields)
                statusCode = status.HTTP_200_OK if pbf else status.HTTP_204_NO_CONTENT
            except ValidationError:
                pbf = b""
                statusCode = status.HTTP_400_BAD_REQUEST
            return Response(
                bytes(pbf), content_type="application/vnd.mapbox-vector-tile", status=statusCode
            )
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()           
            return Response({
                "error":str(e),
                "line_number": exc_tb.tb_lineno,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)