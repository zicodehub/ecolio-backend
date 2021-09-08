from django.test import TestCase

from django.contrib.auth.models import User
from .models import Post, Catgegory

class Test_Create_Post(TestCase):

    @classmethod
    def setUpTestData(cls) :
        test_category = Category.objects.create(name= 'django')
        testuser1 = User.objects.create_user(
            username= 'test_user1',
            password= "zabfjb1",
        )
        testpost1 = Post.objects.create(category=1, title="inz", excerpt='jzsnioev', content="zbsjbklns", author=1, status= 'published')