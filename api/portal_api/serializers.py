from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

class mapDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = mapData
        fields = '__all__'

class mapDataNoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = mapData
        exclude = ['image']

class mapDataImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = mapData
        fields = ['image']

class groupDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = groupData
        fields = '__all__'

class genericGroupSerializer(serializers.Serializer):

    group_id = serializers.CharField()

class tableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = tableData
        fields = '__all__'

class tableDataNoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = tableData
        exclude = ['image']

class tableDataImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = tableData
        fields = ['image']

class styleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = tableData
        fields = ['table_id','style']

class appDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = appData
        fields = '__all__'

class appDataNoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = appData
        exclude = ['image']

class appDataImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = appData
        fields = ['image']

class siteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = siteData
        fields = '__all__'

class siteDataNoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = siteData
        exclude = ['image']

class siteDataImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = siteData
        fields = ['image']

class genericMapSerializer(serializers.Serializer):

    map_id = serializers.CharField()

class genericAppSerializer(serializers.Serializer):

    app_id = serializers.CharField()

class genericTableSerializer(serializers.Serializer):

    table_id = serializers.CharField()

class genericSiteSerializer(serializers.Serializer):

    site_id = serializers.CharField()

class mapServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = mapServiceData
        fields = '__all__'

class genericMapServiceSerializer(serializers.Serializer):

    map__service_id = serializers.CharField()


class mapServiceSecurityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = mapServiceData
        fields = '__all__'

class genericMapServiceSecuritySerializer(serializers.Serializer):

    map_service_security_id = serializers.CharField()

class blockedUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = blockedUserData
        fields = '__all__'

class genericBlockedUserDataSerializer(serializers.Serializer):

    blocked_user_id = serializers.CharField()

class alertDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = alertData
        fields = '__all__'

class genericAlertDataSerializer(serializers.Serializer):

    alert_id = serializers.CharField()

class userSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class groupSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = groupData
        fields = ('group_name', 'group_id')

class geographicFileSerializer(serializers.Serializer):

    upload_files = serializers.FileField()
    file_name = serializers.CharField()
    table_name = serializers.CharField(max_length=300)
    tags = serializers.JSONField()
    description = serializers.CharField(max_length=1000)
    read_access_list = serializers.JSONField()
    write_access_list = serializers.JSONField()
    searchable = serializers.BooleanField()
    sensitive = serializers.BooleanField()
    retention_date = serializers.IntegerField()

class tableColumnsSerializer(serializers.Serializer):
    table_name = serializers.CharField()
    table_type = serializers.CharField()

class tableQuerySerializer(serializers.Serializer):
    table_name = serializers.CharField()
    table_type = serializers.CharField()
    format = serializers.CharField()
    where = serializers.JSONField(required=False)

class pointFileSerializer(serializers.Serializer):

    upload_files = serializers.FileField()
    file_name = serializers.CharField()
    table_name = serializers.CharField(max_length=300)
    tags = serializers.JSONField()
    description = serializers.CharField(max_length=1000)
    read_access_list = serializers.JSONField()
    write_access_list = serializers.JSONField()
    searchable = serializers.BooleanField()
    sensitive = serializers.BooleanField()
    retention_date = serializers.IntegerField()
    latitude_field = serializers.CharField()
    longitude_field = serializers.CharField()
    sheet_name = serializers.CharField()

class pointUrlSerializer(serializers.Serializer):

    url = serializers.URLField()
    table_name = serializers.CharField(max_length=300)
    tags = serializers.JSONField()
    description = serializers.CharField(max_length=1000)
    read_access_list = serializers.JSONField()
    write_access_list = serializers.JSONField()
    searchable = serializers.BooleanField()
    sensitive = serializers.BooleanField()
    retention_date = serializers.IntegerField()
    latitude_field = serializers.CharField()
    longitude_field = serializers.CharField()
    sheet_name = serializers.CharField()

class esriServiceSerializer(serializers.Serializer):

    url = serializers.URLField()
    table_name = serializers.CharField(max_length=300)
    tags = serializers.JSONField()
    description = serializers.CharField(max_length=1000)
    read_access_list = serializers.JSONField()
    write_access_list = serializers.JSONField()
    searchable = serializers.BooleanField()
    sensitive = serializers.BooleanField()
    retention_date = serializers.IntegerField()

class apiSearchSerializer(serializers.Serializer):

    search = serializers.CharField(required=False)
    limit = serializers.IntegerField(required=False,validators=[
        MaxValueValidator(settings.MAX_NUMBER_OF_API_RESULTS),
        MinValueValidator(1)
    ])
    offset = serializers.IntegerField(required=False)

