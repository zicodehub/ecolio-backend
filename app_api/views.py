from django.shortcuts import render

from .models import Post, Test1, Test2
from .serializers import PostSerializer, T1Serializer, T2Serializer
from .serializers import PostSerializer, UserSerializer, GroupSerializer

from django.contrib.auth.models import User, Group
from rest_framework import (
    viewsets,
    generics,
    permissions,
    response,
    status
)
# from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from durin.models import Client

class CustomListing :
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        res = {
            "count": len(serializer.data),
            "results": serializer.data
        }
        return response.Response(res)


class UserViewSet(CustomListing, generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = [ DjangoFilterBackend, OrderingFilter ]
    filterset_fields = ('id', )
    ordering_fields = ['username', 'email']
    # filterset_fields = '__all__'

    def create(self, request, **kw) :
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Client(name= request.data.get("username")).save() 
            # serializer.data[""]
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [ DjangoFilterBackend ]
    filterset_fields = '__all__'

class PostList(CustomListing, generics.ListCreateAPIView) :
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class T1ViewSet(generics.ListCreateAPIView):
    queryset = Test1.objects.all()
    serializer_class = T1Serializer

class T2ViewSet(generics.ListCreateAPIView):
    queryset = Test2.objects.all()
    serializer_class = T2Serializer