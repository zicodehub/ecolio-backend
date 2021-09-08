from django.urls import path

from . import views

urlpatterns = [
	path("clientdb", views.ClientDBViewSet.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy" }) ),
	path("clientdb/activate/<int:id>", views.ClientDBViewSet.as_view({"get": "activate"}) )
]