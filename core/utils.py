from threadlocals.threadlocals import set_request_variable, get_request_variable
from django.apps import apps as django_apps

from django.conf import settings
from django.db import connections
from django.core import management

from server.settings import DATABASE_ROUTER_MODEL


def get_dbrm() :
	return django_apps.get_model(settings.DATABASE_ROUTER_MODEL)	

def get_client_db(filters) :
	DBR = get_dbrm()
	try :
		return DBR.objects.get(
			code= filters.get(settings.DATABASE_LOGIN_ROUTER_NAME, False), 
			is_active= True
		)
	except:
		return False

def get_db_alias_from_request():
	return get_request_variable(settings.DATABASE_ALIAS_NAME_FROM_REQUEST)

def set_db_alias_from_request(value):
	set_request_variable(settings.DATABASE_ALIAS_NAME_FROM_REQUEST, value)

def create_database(db_name):
	""" 
		Crée une base de données avec un curseur existant.
		Le curseur essayé en premier est celui de la DB --default--
		Attention, le curseur d'un backend ne peut créer que les bases de données de ce même type

		Par exemple, un curseur de type sqlite3 ne peut pas créer de DB postgresql

		Pour l'instant, on suppose que toutes les bases de données sont du même type que
			- la base de donnée par défaut (si définie)
			- la seconde DB du settings.DATABASES (si --default n'est pas définie) 
	"""
	try :
		cursor = connection.cursor()
	except:
		cursor = connections.all()[1].cursor()

	cursor.execute(f"CREATE DATABASE {db_name}")
	cursor.close()

def insert_database(db):
	db_configs = {
		'ENGINE': f'django.db.backends.{db.db_engine}',
		'NAME': db.db_name,
		'USER': db.db_user,
		'PASSWORD': db.db_password,
		'HOST': db.db_host,
		'PORT': db.db_port
	}
	settings.DATABASES[db.db_alias] = db_configs
	connections.databases[db.db_alias] = settings.DATABASES[db.db_alias]

def test_database(db):
	return True

def migrate(db_alias) :
	management.call_command("migrate", database= db_alias )

def refresh_databases():
	count = 0
	DATABASE_ROUTER_MODEL = get_dbrm()
	print("Refreshing started")
	for db in DATABASE_ROUTER_MODEL.objects.filter(is_active= True) :
		if not db.db_name :
			raise f"La DB doit avoir un name. Valeurs actuelles : {db}"
		if not db.db_host :
			raise f"La DB doit avoir un host. Valeurs actuelles : {db}"
		insert_database(db)
		print(f"Insertion of {[db]} DONE. We will migrate into {db.db_alias}")
		print(f"Current databases are {settings.DATABASES}")
		migrate(db.db_alias)
		print("Migration DONE")
		
		count += 1

	print(f" Refreshed Databases : {count} ")

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

def create_superuser(db_alias, first_user= False, username= "admin", password= "admin", **extra_fields) :
	from durin.models import Client 
	User = get_user_model()

	if first_user :
		if  User.objects.using(db_alias).filter(is_superuser = True) :
			return
	# else:
	extra_fields.setdefault('is_staff', True)
	extra_fields.setdefault('is_superuser', True)

	if extra_fields.get('is_staff') is not True:
		raise ValueError('Superuser must have is_staff=True.')
	if extra_fields.get('is_superuser') is not True:
		raise ValueError('Superuser must have is_superuser=True.')

	user = User(username=username, **extra_fields)
	user.password = make_password(password)
	user.save(using= db_alias)

	Client(name= username).save(using= db_alias) 

	return user