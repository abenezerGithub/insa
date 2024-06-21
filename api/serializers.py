import os
from rest_framework import serializers
from base.models import Report,Attachment
from django.contrib.auth import get_user_model
from ReportInsa import settings
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'username', 'name', 'password',"uid"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data.get('name', '')
        )
        return user

class AttachmentSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Attachment
        fields = ('id', 'image')
    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            domain = request.build_absolute_uri('/')
        else:
            domain = settings.DEFAULT_DOMAIN   # Define a default domain in settings.py if request is not available
            print(*(obj.image.url.split("/")[2:]))
        return "/".join((domain,"api","report-attachment",*(obj.image.url.split("/")[2:])))
class ReportSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True)  # Use 'attachments' here

    class Meta:
        model = Report
        fields = ('id', 'report_type', 'report_description', 'location_url',
                  'date_of_crime', 'date_reported', 'is_resolved', 'seen', 'attachments')