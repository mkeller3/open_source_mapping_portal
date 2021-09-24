import os
import socket

print(f"Running api on server: {socket.gethostname()}")

if socket.gethostname() == 'michael-laptop':
    api_db_host = 'localhost'
else:
    api_db_host = 'postgresql.mkeller3.svc.cluster.local'

api_db = 'mapping_portal'
api_db_user = 'postgres'
api_db_pwd = 'postgres'
admin_groups = ['admins']
data_db = 'mapping_portal'
data_db_schema = 'user_data'
media_location = f"{os.getcwd()}/api/media/"
mapbox_token = "pk.eyJ1IjoibWtlbGxlcjMiLCJhIjoieFdYUUg5TSJ9.qzhP1v5f1elHrnTV4YpkiA"