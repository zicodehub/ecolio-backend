from durin import views as durinViews
from .views import Login
from django.urls import path

urlpatterns = [
    path(r"login/", Login.as_view(), name="login"),

    path(r"refresh/", durinViews.RefreshView.as_view(), name="durin_refresh"),
    path(r"logout/", durinViews.LogoutView.as_view(), name="durin_logout"),
    path(r"logoutall/", durinViews.LogoutAllView.as_view(), name="durin_logoutall"),
]
