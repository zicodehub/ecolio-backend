from django.contrib.auth.models import User, Group
from rest_framework import serializers

from django_restql.mixins import DynamicFieldsMixin
from django_restql.serializers import NestedModelSerializer
from django_restql.fields import NestedField, DynamicSerializerMethodField

from .models import Post, Test1, Test2

class GroupSerializer(DynamicFieldsMixin, NestedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    groups2 = GroupSerializer(many=True, read_only=True)
    related_books = DynamicSerializerMethodField()
    class Meta:
        model = User
        fields = ( 'id', 'password', 'last_login', 'groups', 'groups2', 'related_books', 'user_permissions' )

    def save(self, **kw) :
        password = self.validated_data.get("password")

        u = super().save(**kw)
        u.set_password(password)
        u.save()
        
        return u

    def get_related_books(self, obj, parsed_query):
        # With `DynamicSerializerMethodField` you get this extra
        # `parsed_query` argument in addition to `obj`
        books = obj.groups.all()

        # You can do what ever you want in here

        # `parsed_query` param is passed to BookSerializer to allow further querying
        serializer = GroupSerializer(
            books,
            many=True, 
            parsed_query=parsed_query
        )
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, **kw) :
        password = self.validated_data.get("password")

        u = super().save(**kw)
        u.set_password(password)
        u.save()
        
        return u

class PostSerializer(serializers.ModelSerializer):
    class Meta :
        model = Post
        fields = ('id', 'title', 'author', 'excerpt', 'content', 'status')


class T1Serializer(serializers.ModelSerializer):
    class Meta :
        model = Test1
        fields = '__all__'

class T2Serializer(serializers.ModelSerializer):
    class Meta :
        model = Test2
        fields = '__all__'

class PostDetail(serializers.ModelSerializer):
    pass