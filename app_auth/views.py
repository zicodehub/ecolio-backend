from django.shortcuts import render
from durin.views import LoginView
from django.conf import settings

from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from core.utils import set_db_alias_from_request, get_db_alias_from_request, get_client_db

class Login(LoginView) :
	def post(self, request, *args, **kwargs):
		client_db = get_client_db(request.data)
		if not client_db :
			raise ValidationError({"detail": "Code école incorrect"})
		# 	set_db_alias_from_request(client_db.db_alias)
		# else :

		request.user = self.validate_and_return_user(request)
		client = self.get_client_obj(request)
		token_obj = self.get_token_obj(request, client)
		user_logged_in.send(
			sender=request.user.__class__, request=request, user=request.user
		)
		data = self.get_post_response_data(request, token_obj)

		
		# data["X-Code"] = get_db_alias_from_request()
		data[settings.CORE_CONFIGS['DATABASE_HEADER_ROUTER_NAME']] = client_db.db_alias
		return Response(data)
		# return super().post(request, *args, **kwargs)

