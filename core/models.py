from django.db import models
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import time


hasher = PBKDF2PasswordHasher()

class ClientDB(models.Model):
	# Le champ --db_alias-- est un hash du matricule de l'école sur la plateforme
	# Il n'est pas obligatoire car c'est une valeur calculée  
	db_alias = models.CharField(max_length= 255, blank= True)
	db_name = models.CharField(max_length= 100)

	db_engine = models.CharField(max_length= 100, default= "postgresql")
	db_host = models.CharField(max_length= 100, default= "localhost")

	db_user = models.CharField(max_length= 100, default= "postgres")
	db_password = models.CharField(max_length= 100, default= "root")
	db_port = models.CharField(max_length= 100, default= "5432")

	code = models.CharField(max_length= 100, unique= True)
	is_active = models.BooleanField(default= False)

	image = models.FileField(upload_to= "cooo", default= "lala.png")



	@property
	def lala(self):
		return "self._lala"
	

	def save(self, *args, **kw) :
		if not self.db_alias :
			self.db_alias = self.crypt()
		super().save(*args, **kw)

	def crypt(self) :
		return hasher.encode(self.code, hasher.salt())
	
	def verify(self, brute_alias):
		return hasher.verify(brute_alias, self.db_alias)

	@classmethod
	def has_existance(cls, brute_alias):
		new_alias = hasher.encode(brute_alias, hasher.salt())
		try:
			cls.objects.get(db_alias= new_alias)
			return True
		except :
			return False
