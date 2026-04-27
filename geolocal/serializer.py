from rest_framework import serializers
from django.conf import settings
import jwt
import base64
import binascii
import io
from PIL import Image, UnidentifiedImageError

class GeolocalSerializer(serializers.Serializer):
    
    latitude = serializers.CharField(required=False, max_length=100)
    longitude = serializers.CharField(required=False, max_length=100)

    def validate(self, attrs):

        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')

        return attrs

     

