from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser 
from django.contrib.auth.models import User, Group

from .models import ClientDB
from .utils import get_dbrm

class ClientDBSerializer(serializers.ModelSerializer):
	parser_classes = [MultiPartParser, FormParser]
	
	class Meta:
		model = get_dbrm()
		fields = '__all__'

