from django.shortcuts import render,redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import (authenticate,login as auth_login, logout as auth_logout)
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import clientForm,userForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from .models import Client
from django.db.models import Q
import pdb

def login(request):
	message=''
	if request.user.is_authenticated:
		
		return HttpResponseRedirect(reverse('dashboard:home', current_app='dashboard'))
	if request.method == "POST":
		form=LoginForm(request.POST)
		if form.is_valid():
			_username=form.cleaned_data['username']
			_password=form.cleaned_data['password']
			user=authenticate(username=_username, password=_password)
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					if request.GET.get('next'):
						return redirect(request.GET.get('next'))
					else:
					    return HttpResponseRedirect(reverse('dashboard:home', current_app='dashboard'))
				else:
					message = 'Your account is not activated'
			else:
				message = 'Invalid login, please try again.'
	form=LoginForm()			
	context = {'message': message, 'form':form}


	return render(request, 'accounts/login.html', context)

def logout(request):
	if request.user.is_authenticated():
		auth_logout(request)
		return HttpResponseRedirect(reverse('accounts:login', current_app='accounts'))
	else:
		return HttpResponseRedirect(reverse('accounts:login', current_app='accounts'))




class clientList(LoginRequiredMixin,ListView):
	login_url = '/account/login/'
	model=User
	template_name = "accounts/client_list.html"

	def get_context_data(self, **kwargs):
		context = super(clientList, self).get_context_data(**kwargs)
		context['graphs']='testing'
		context['client_list']=User.objects.filter(Q(is_staff=False), person__company= self.request.user.person.company)
		return context

@login_required(login_url='/account/login/')
#@transaction.atomic
def createCLient(request):
	if request.method=='POST':
		clientform=clientForm(request.POST)
		userform=userForm(request.POST)
	else:
		clientform=clientForm()
		userform=userForm()
	return save_client_form(request,userform,'accounts/includes/partial_client_create.html',clientform,)

def clientUpdate(request, id):
	data=dict()
	user=get_object_or_404(User, id=id)
	client=get_object_or_404(Client, user=user)
	data['form_is_valid']=True
	if request.method == 'POST':
		clientform = clientForm(data=request.POST, instance=client)
		userform=userForm(data=request.POST, instance=client)
		if clientform.is_valid() and userform.is_valid():
			userform.save()
			client=clientform.save(commit=False)
			client.audit(request)
			client.save()
			borrowers=User.objects.filter(Q(is_staff=False), person__company= request.user.person.company)
			data['html_product_list']=render_to_string('accounts/includes/partial_client_list.html', {
	               'client_list': borrowers
	            })
		else:
			data['form_is_valid']=False
		context = {'userform': userform, 'clientform':clientform}
		data['html_form'] = render_to_string('accounts/includes/partial_client_update.html', context, request=request)
		return JsonResponse(data)
	else:
		clientform=clientForm(instance=client)
		userform=userForm(instance=user)
		return save_client_form(request, userform, 'accounts/includes/partial_client_update.html', clientform)

def clientDelete(request,id):
	data=dict()
	user=get_object_or_404(User, id=id)
	data['form_is_valid']=True
	if request.method=='POST':
		user.delete()
		data['form_is_valid'] = True  # This is just to play along with the existing code
		borrowers=User.objects.filter(Q(is_staff=False), person__company= request.user.person.company)
		data['html_product_list'] = render_to_string('accounts/includes/partial_client_list.html', {
           'client_list': borrowers
        })
	else:
		context = {'client': user}
		data['html_form'] = render_to_string('accounts/includes/partial_client_delete.html',
		context,
		request=request,
		)
	return JsonResponse(data)
		

@login_required(login_url='/account/login/')
@transaction.atomic
def save_client_form(request, userform, template_name,clientform):
	data = dict()
	if request.method=='POST':
		if clientform.is_valid() and userform.is_valid():
			data['form_is_valid'] = True
			password=request.POST.get('password')
			hashpassword=make_password(password)
			try:
				new_user=User.objects.create(
					first_name=request.POST.get('first_name'), 
					is_staff=False, 
					last_name=request.POST.get('last_name'),
					username=request.POST.get('username'),
					password=hashpassword,
					email=request.POST.get('email'),
					)
				new_user.save()
				try:
				    profile=Client.objects.get(user=new_user)
				except :
					profile=Client.objects.create(user=new_user)
				clientform=clientForm(request.POST, instance=profile)
				client=clientform.save(commit=False)
				client.audit(request)
				client.save()
				borrowers=User.objects.filter(Q(is_staff=False), person__company= request.user.person.company)
				data['html_product_list'] = render_to_string('accounts/includes/partial_client_list.html', {
	               'client_list': borrowers
	            })
				#pdb.set_trace()
			except:
				#pdb.set_trace()
				#userform.errors='Username already exist. Please try another one'
				pdb.set_trace()
				data['form_is_valid']=False	
		else:
			data['form_is_valid'] = False	
	#pdb.set_trace()
	context = {'userform': userform, 'clientform':clientform}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)


		
	
	    