from django.db import connections
from django.core import management 
from django.conf import settings
from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response


from .utils import (
	get_dbrm, 
	set_db_alias_from_request, 
	refresh_databases,
	create_superuser
)

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

####### CONSTANTS
DATABASE_ROUTER_MODEL = get_dbrm()

class ClientDatabaseRouterMiddleware(MiddlewareMixin):
	"""
		Middleware principal de routage des requetes HTTP en base  de données

		Toute requete doit contenir un indice sur la DB :
			- code 
				Version claire de l'identifiant de la DB
				S'utilise dans les requêtes POST à l'URL de connexion
				Il est différent de l'alias qui est son hash
				Sa valeur est donnée par settings.DATABASE_LOGIN_ROUTER_NAME

			- alias : 
				C'est la version hashée du --code
				Pour des raisons de sécurité, même cet alias est enregistré en DB,
				il faut qu'il le soit aussi dans settings.DATABASES de l'instance courante du serveur
				Cela peut être problématique si nous avons pliusieurs instances du serveur.
				Ce comportement peut être modifié en mettant CHECK_IN_CURRENT_INSTANCE = False

		L'indice de routage dans  HEADERS de la requete est prioritaire sur celui du login
		une fois l'indice trouvé, vérifié et validé, sa valeur est stockée dans
		le thread de la requete en cours. 
		
		En plus de l'URL de login, on peut ajouter des exceptions pour bypasser le gateway. 
		Elles sont définies dans la méthode is_exception() qui revoie True dès qu-une correspondance est trouvée

	"""
	CHECK_IN_CURRENT_INSTANCE = True
	def __init__(self, get_response):
		self.get_response = get_response

		""" Excécutée une seule fois après démarrage du serveur
		
			Ici, c'est la DB du Super Administrateur qui est ajoutée au Model du Gateway
			Ainsi, les Super Admin peuvent aussi utiliser ce gateway
		"""

		# To be deleted
		try :
			db_su = settings.SUPER_USER_DATABASE
			db_conf = db_su.get('conf')
			DATABASE_ROUTER_MODEL.objects.get_or_create(
				db_name= db_conf.get('NAME'),
				db_host= db_conf.get('HOST'),
				db_user= db_conf.get('USER'),
				db_password= db_conf.get('PASSWORD'),
				code= db_su.get('alias'), 
				is_active= True
			)

		except :
			pass

		# Mandatory
		refresh_databases()

		# To be deleted
		try :
			create_superuser(
				db_su.get('alias'), 
				first_user= True 
			)
		except :
			pass
			
		print("Middleware excécuté")

	def  process_view(self, request, view_func, view_args, view_kwargs):
		"""
			Excécuté à chaaque requete
		"""
		print(request.headers)
		print(request.body)
		db_alias = request.headers.get(settings.DATABASE_HEADER_ROUTER_NAME, None)

		if db_alias :
			# Si la requete possède l'indice dans le HEADER
			try :
				client = DATABASE_ROUTER_MODEL.objects.get(
					db_alias= db_alias,
					is_active= True
				)

				if ClientDatabaseRouterMiddleware.CHECK_IN_CURRENT_INSTANCE :
					if not settings.DATABASES.get(db_alias, False) :
						raise "ERRR"
				set_db_alias_from_request( client.db_alias )

			except :
				return JsonResponse({'detail': 'Code nonn valide'}, status= 400)
	
		else:
			if self.is_exception(request) :

				# A ce stade, la requete n'est pas encore parsée. 
				# Il faut donc extraire l'attribut manuellement 
				try:
					dico = eval(request.body.decode())
					if not isinstance(dico, dict) :
						return JsonResponse({'detail': 'Corpus incorrect'}, status= 400)
					brute_alias = dico.get(settings.DATABASE_LOGIN_ROUTER_NAME, None)
					
					if not brute_alias :
						return JsonResponse({'detail': 'Code manquant'}, status= 400)
					else: 
						try :
							client = DATABASE_ROUTER_MODEL.objects.get(code= brute_alias)
							set_db_alias_from_request(client.db_alias)
						except:
							return JsonResponse({'detail': 'Code incorrect'}, status= 400)
				except:
					return JsonResponse({'detail': 'Erroror'}, status= 400)
			else :
				return JsonResponse({'detail': 'Code innexistant'}, status= 400)

	def is_exception(self, request) :
		path = request.get_full_path()
		if (path.endswith('login') or path.endswith('login/') ) and request.method == "POST" :
			return True
		if (path.endswith('createschool') or path.endswith('createschool/') ) and request.method == "POST" :
			return True
		return False

	def process_template_response(self, request, response) :
		# response.headers["Access-Control-Allow-Headers"] = "x-code"
		print(response.headers, dir(response.headers))
		print("OKOKOKOKOK")
		return response
