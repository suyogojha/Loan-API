from django.test import TestCase
from .models import Employee, Client
from django.contrib.auth import get_user_model
from .forms import employeeForm, clientForm, userForm


#class userFormTest(TestCase):

#	def setUp(self):
#		employee=get_user_model().objects.create_user('zoidberg')
