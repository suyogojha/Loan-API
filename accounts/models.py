from django.db import models
from django.contrib.auth.models import User
from dashboard.models import baseModel
from dashboard.choices import *
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class person(baseModel):
	user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='person', default='1')
	title=models.CharField(max_length=200, blank=True,choices=TITLE_CHOICES)
	fullname=models.CharField(max_length=200, blank=True)
	full_address=models.CharField(max_length=200, blank=True)
	city=models.CharField(max_length=200, blank=True)
	zip=models.CharField(max_length=200, blank=True)
	state=models.CharField(max_length=200, blank=True)
	phone=models.CharField(max_length=200, blank=True)
	gender=models.CharField(max_length=200, choices=GENDER_CHOICES, blank=True)
	dob=models.DateField( blank=True, null=True)
	state_of_origin=models.CharField(max_length=200, blank=True)
	current_salary=models.CharField(max_length=200, blank=True)
	employment_date=models.DateField(blank=True, null=True)
	lga=models.CharField(max_length=200, blank=True)
	job_description=models.TextField( blank=True)
	marital_status=models.CharField(max_length=200, choices=RELATIONSHIP_STATUS_CHOICES, blank=True)
	picture=models.ImageField(max_length=200, blank=True,upload_to='employee/')
	bio=models.TextField(max_length=200, blank=True)




class Client(person):
	current_employer=models.CharField(max_length=200, blank=True)
	years_in_workplace=models.TextField(max_length=100, blank=True)
	vehicles_owned=models.CharField(max_length=200, blank=True)
	years_at_residence=models.CharField(max_length=200, blank=True)
	loan_officer=models.ForeignKey(User,on_delete=models.CASCADE, help_text='Someone who manages the client among your staffs',related_name='officer',null=True, blank=True)
	residential_status=models.CharField(max_length=200, choices=RESIDENTIAL_STATUS_CHOICES, blank=True)
	educational_status=models.CharField(max_length=200,choices=EDUCATIONAL_STATUS_CHOICES, blank=True)
    
class Employee(person):
	years_in_workplace=models.TextField(max_length=100, blank=True)
	manager=models.ForeignKey(User,on_delete=models.CASCADE,related_name='manager', blank=True, null=True)
	educational_status=models.CharField(max_length=200,choices=EDUCATIONAL_STATUS_CHOICES, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        if instance.is_staff==True:
            Employee.objects.create(user=instance)
        else:
            Client.objects.create(user=instance)
'''
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_staff==True:
        instance.employee.save()
    else:
        instance.client.save()
'''




	


