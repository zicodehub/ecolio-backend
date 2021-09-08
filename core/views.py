from .serializers import ClientDBSerializer
from .models import ClientDB

from rest_framework import (
viewsets,
permissions,
response,
exceptions,
status
)

from django.core import management 
from .utils import (
	get_db_alias_from_request, 
	create_database, 
	insert_database, 
	test_database, 
	migrate,
	create_superuser
)

class ClientDBViewSet(viewsets.ModelViewSet):
	queryset = ClientDB.objects.all()
	serializer_class = ClientDBSerializer

	def create(self, request, *args, **kw) :
		res = super().create(request, *args, **kw)
		if res.status_code == status.HTTP_201_CREATED :
			model = self.serializer_class.Meta.model
			
			# Opération effetuée dans la DB --default--
			instance = model.objects.get(pk= res.data.get('id') )

			if not request.data.get('exists', False) :
				create_database(instance.db_name)
			
			if not request.data.get('inactive', False) :
				if test_database("") :
					insert_database(instance)
					migrate(instance.db_alias)
					create_superuser(instance.db_alias)
					instance.is_active = True
					instance.save()
		return res

	def activate(self, request, id) :
		try:
			model = self.serializer_class.Meta.model
			instance = model.objects.get(pk= id)
			instance.is_active = True
			instance.save()
		except:
			raise exceptions.ValidationError({'details': 'Client inexistant'})
		return response.Response({'status': "Action done"})