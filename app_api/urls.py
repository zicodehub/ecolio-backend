from django.urls import path, include
from . import views
from rest_framework.authtoken import views as authView


from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# class CustomAuthToken(ObtainAuthToken):

# 	def post(self, request, *args, **kwargs):
# 		serializer = self.serializer_class(
# 			data=request.data,
# 			context={'request': request}
# 		)
# 		serializer.is_valid(raise_exception=True)
# 		print(request.headers)
# 		user = serializer.validated_data['user']
# 		token, created = Token.objects.get_or_create(user=user)
# 		return Response({
# 		    'token': token.key,
# 		    'user_id': user.pk,
# 		    'email': user.email
# 		})

urlpatterns = [
    path('auth/', include("app_auth.urls")),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name= 'dlistcreate'),
    path('posts/', views.PostList.as_view(), name= 'listcreate'),
    path('t1/', views.T1ViewSet.as_view(), name= 't1'),
    path('t2/', views.T2ViewSet.as_view(), name= 't2'),
    path('users/', views.UserViewSet.as_view() ),
    path('users/<int:pk>/', views.UserDetail.as_view() ),
    path('groups', views.GroupViewSet.as_view({'get': 'list', 'post': 'create'}) ),
    path('<int:pk>/', views.PostDetail.as_view(), name= 'detailcreate'),
    # path('auth', CustomAuthToken.as_view() ),
]