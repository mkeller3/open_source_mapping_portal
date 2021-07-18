import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

api_db = 'mapping_portal'
api_db_user = 'postgres'
api_db_pwd = 'postgres'
api_db_host = 'localhost'
admin_groups = ['admins']
data_db = 'mapping_portal'
data_db_schema = 'user_data'
media_location = os.path.join(BASE_DIR, 'media/')