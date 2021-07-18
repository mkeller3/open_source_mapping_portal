from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .constants import *
from .helpers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework_tracking.mixins import LoggingMixin
from django.core.files.storage import FileSystemStorage

# Import geographic file
class importGeographicFileView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=geographicFileSerializer, operation_description="Upload a geogrpahic file into Mapping Portal")
    def post(self, request):
        serializer = geographicFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {str(request.user.username)} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {str(request.user.username)} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        file_name = serializer.validated_data['file_name']
        table_id = table_id_generator()

        try:
            for f in request.FILES.getlist('upload_files'):
                fs = FileSystemStorage()
                fs.save(f.name, f)

            valid_upload_files = False

            for file in os.listdir(media_location):
                file_extension = os.path.splitext(file)[1]
                file_name = os.path.splitext(file)[0]
                formatted_file_name = file_name.replace(' ','_').replace('/','_')
                os.rename(media_location+file_name+file_extension,media_location+formatted_file_name+file_extension)

                if file_extension.lower() in ['.shp', '.tab', '.geojson', '.json', '.kml']:  
                    valid_upload_files = True

            if valid_upload_files:

                for file in os.listdir(media_location):
                    file_name = os.path.splitext(file)[0]

                    if file_extension.lower() in ['.shp', '.tab', '.geojson', '.json', '.kml']:                        

                        table_information = {
                            'username': request.user.username,
                            'table_id': table_id,
                            'table_name': serializer.validated_data['table_name'],
                            'updated_username': request.user.username,
                            'tags': serializer.validated_data['tags'],
                            'description': serializer.validated_data['description'],
                            'read_access_list': serializer.validated_data['read_access_list'],
                            'write_access_list': serializer.validated_data['write_access_list'],
                            'searchable': serializer.validated_data['searchable'],
                            'sensitive': serializer.validated_data['sensitive'],
                            'retention_date': serializer.validated_data['retention_date'],
                            "file": media_location+file_name+file_extension,
                        }

                        load_geographic_data_to_server(table_information)

                        clean_table(table_information['table_id'])

                        add_table_into_mapping_portal(table_information)

                        for file in os.listdir(media_location):
                            file_name = os.path.splitext(file)[0]
                            if file_name == serializer.validated_data['table_name']:
                                os.remove(media_location+file)


                return Response({'table_id':table_id})
            else:
                delete_data_backend(table_id, file_name)

                return Response({"error":f"You have not upload a valid geogrpahic file type. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            delete_data_backend(table_id, file_name)
            return Response({
                "error":str(e),
                "line_number": exc_tb.tb_lineno,
                "file": os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Import point file
class importPointFileView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=pointFileSerializer, operation_description="Upload a point file into Mapping Portal")
    def post(self, request):
        serializer = pointFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {str(request.user.username)} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {str(request.user.username)} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        file_name = serializer.validated_data['file_name']
        table_id = table_id_generator()

        try:
            for f in request.FILES.getlist('upload_files'):
                fs = FileSystemStorage()
                fs.save(f.name, f)

            valid_upload_files = False

            for file in os.listdir(media_location):
                file_extension = os.path.splitext(file)[1]
                file_name = os.path.splitext(file)[0]
                formatted_file_name = file_name.replace(' ','_').replace('/','_')
                os.rename(media_location+file_name+file_extension,media_location+formatted_file_name+file_extension)

                if file_extension.lower() in ['.csv', '.txt', '.xlsx', '.xls']:  
                    valid_upload_files = True

            if valid_upload_files:

                for file in os.listdir(media_location):
                    file_name = os.path.splitext(file)[0]

                    if file_extension.lower() in ['.csv', '.txt', '.xlsx', '.xls']:    

                        table_information = {
                            'username': request.user.username,
                            'table_id': table_id,
                            'table_name': serializer.validated_data['table_name'],
                            'updated_username': request.user.username,
                            'tags': serializer.validated_data['tags'],
                            'description': serializer.validated_data['description'],
                            'read_access_list': serializer.validated_data['read_access_list'],
                            'write_access_list': serializer.validated_data['write_access_list'],
                            'searchable': serializer.validated_data['searchable'],
                            'sensitive': serializer.validated_data['sensitive'],
                            'retention_date': serializer.validated_data['retention_date'],
                            "file": media_location+file_name+file_extension,
                            "file_name": file_name,
                            "extenstion": file_extension.lower(),
                            "latitude_field": serializer.validated_data['latitude_field'],
                            "longitude_field": serializer.validated_data['longitude_field'],
                        }

                        load_point_data_to_server(table_information)

                        clean_table(table_information['table_id'])

                        add_table_into_mapping_portal(table_information)

                        for file in os.listdir(media_location):
                            file_name = os.path.splitext(file)[0]
                            if file_name == serializer.validated_data['file_name']:
                                os.remove(media_location+file)
                    
                    return Response({'table_id':table_id})
            else:
                delete_data_backend(table_id, file_name)

                return Response({"error":f"You have not upload a valid point file type. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            delete_data_backend(table_id, file_name)
            return Response({
                "error":str(e),
                "line_number": exc_tb.tb_lineno,
                "file": os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Import geo data from csv

# Import geo data from url

# Import point data from url
class importPointUrlView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=pointUrlSerializer, operation_description="Upload a point file into Mapping Portal")
    def post(self, request):
        serializer = pointUrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {str(request.user.username)} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {str(request.user.username)} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        table_id = table_id_generator()

        try:
            table_information = {
                'username': request.user.username,
                'table_id': table_id,
                'table_name': serializer.validated_data['table_name'],
                'updated_username': request.user.username,
                'tags': serializer.validated_data['tags'],
                'description': serializer.validated_data['description'],
                'read_access_list': serializer.validated_data['read_access_list'],
                'write_access_list': serializer.validated_data['write_access_list'],
                'searchable': serializer.validated_data['searchable'],
                'sensitive': serializer.validated_data['sensitive'],
                'retention_date': serializer.validated_data['retention_date'],
                "file": media_location+file_name+file_extension,
                "file_name": file_name,
                "extenstion": file_extension.lower(),
                "latitude_field": serializer.validated_data['latitude_field'],
                "longitude_field": serializer.validated_data['longitude_field'],
            }

            load_point_data_to_server(table_information)

            clean_table(table_information['table_id'])

            add_table_into_mapping_portal(table_information)

            for file in os.listdir(media_location):
                file_name = os.path.splitext(file)[0]
                if file_name == serializer.validated_data['file_name']:
                    os.remove(media_location+file)
        
            return Response({'table_id':table_id})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            delete_data_backend(table_id, file_name)
            return Response({
                "error":str(e),
                "line_number": exc_tb.tb_lineno,
                "file": os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Import json geo data

# Import json point data

# Import data from esri
class importEsriUrlView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated),

    @swagger_auto_schema(request_body=esriServiceSerializer, operation_description="Upload a esri map service into Mapping Portal")
    def post(self, request):
        serializer = esriServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.username) not in request.data['read_access_list']:
            return Response({"error":f"Username is not in read_access_list. Add {str(request.user.username)} to read_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.username) not in request.data['write_access_list']:
            return Response({"error":f"Username is not in write_access_list. Add {str(request.user.username)} to write_access_list and try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            table_id = table_id_generator()

            table_information = {
                'username': request.user.username,
                'table_id': table_id,
                'table_name': serializer.validated_data['table_name'],
                'updated_username': request.user.username,
                'tags': serializer.validated_data['tags'],
                'description': serializer.validated_data['description'],
                'read_access_list': serializer.validated_data['read_access_list'],
                'write_access_list': serializer.validated_data['write_access_list'],
                'searchable': serializer.validated_data['searchable'],
                'sensitive': serializer.validated_data['sensitive'],
                'retention_date': serializer.validated_data['retention_date'],
                'file': media_location+table_id+'.geojson',
            }

            download_esri_service_data(serializer.validated_data['url'], table_id)

            load_geographic_data_to_server(table_information)

            clean_table(table_information['table_id'])

            add_table_into_mapping_portal(table_information)

            for file in os.listdir(media_location):
                file_name = os.path.splitext(file)[0]
                if file_name == table_id:
                    os.remove(media_location+file)
            
            return Response({'table_id':table_id})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            delete_data_backend(table_id, table_id)
            return Response({
                "error":str(e),
                "line_number": exc_tb.tb_lineno,
                "file": os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Import geo data from geojson string

# Update geo data from file

# Update point data from file