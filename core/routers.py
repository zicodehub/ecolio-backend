from django.conf import settings
from threadlocals.threadlocals import get_request_variable

from .utils import get_db_alias_from_request

class GatewayRouter :
    """
    Ce premier Router ne gère que les models de l'application --core
    Il s'assure que tous les models de --core restent dans la base de données du GATEWAY 
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "core" :
            return "gateway"

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "core" :
            return "gateway"

        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Les models de l'application --core ne sont migrés que dans BD du GATEWAY
        """
        if db == 'gateway' :
            if app_label not in ('core', 'contenttypes') :
                return False
            else :
                return True
        return None


class RuntimeRouter:
    """
    Utilisé seulement pour l'écriture et la lecture lorsque le serveur est déjà lancé
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """

        # --choice-- a une valeur ou est --None--
        choice = get_db_alias_from_request() 
        return choice

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        # --choice-- a une valeur ou est --None--
        choice = get_db_alias_from_request() 
        return choice


    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        return None
        # if app_label not in settings.PRIVATE_APPS :
        #     return True
        # print("MIGRATIONS NON REUSSIE")
        # return None


class TIRRouter:
    """
        Router de dernier recours
        Elle restreint la migration les applications de TIR dans les DB des clients 
        Mais migre les applications client dans les DB des clients et de TIR

        Dernier rempart pour les allow_relation() afin que les relations ne soient pas interdites
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        return None

        
    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in settings.PRIVATE_APPS :
            print("POTENTIELLE ERREUR")
            if db != settings.SUPER_USER_DATABASE.get('alias') :
                print("MIGRATION RESTREINTE")
                return False
        return True

