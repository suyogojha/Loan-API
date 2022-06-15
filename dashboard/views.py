from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import *#employeeForm, clientForm, userForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.template.loader import render_to_string
import pdb
# Create your views here.
#@login_required(login_url='/account/login/')

class HomeView(LoginRequiredMixin,TemplateView):
	login_url = '/account/login/'
	redirect_field_name = 'redirect_to'
	template_name = "dashboard/index.html"


@login_required(login_url='/account/login/')
@transaction.atomic
def loantype(request):
	if request.user.is_staff:
		
		loantype=loanType.objects.filter(company=request.user.person.company)

	else:
		loantype=loanType.objects.filter(company=request.user.client.company)
	return render(request, 'dashboard/loantype.html', {'loantype':loantype})

@login_required(login_url='/account/login/')
@transaction.atomic
def save_product_form(request, form, template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			product=form.save(commit=False)
			product.audit(request)
			product.save()
			data['form_is_valid'] = True
			#pdb.set_trace()
			products = loanType.objects.all()
			data['html_product_list'] = render_to_string('dashboard/includes/partial_product_list.html', {
                'loantype': products
            })
		else:
			data['form_is_valid'] = False
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	#pdb.set_trace()
	return JsonResponse(data)

@login_required(login_url='/account/login/')
@transaction.atomic
def product_create(request):
	if request.method == 'POST':
		form = productForm(request.POST)
	else:
		form = productForm()
	return save_product_form(request, form, 'dashboard/includes/partial_product_create.html')

@login_required(login_url='/account/login/')
@transaction.atomic
def product_update(request,id):
	product=get_object_or_404(loanType, id=id)
	if request.method =='POST':
		form=productForm(request.POST, instance=product)
	else:
		form=productForm(instance=product)
	return save_product_form(request, form, 'dashboard/includes/partial_product_update.html')

@login_required(login_url='/account/login/')
def product_delete(request,id):
	product=get_object_or_404(loanType, id=id)
	data = dict()
	#pdb.set_trace()
	if request.method=='POST':
		product.delete()
		data['form_is_valid'] = True  # This is just to play along with the existing code
		products = loanType.objects.all()
		data['html_product_list'] = render_to_string('dashboard/includes/partial_product_list.html', {
		    'loantype': products
		})
	else:
		context = {'product': product}
		data['html_form'] = render_to_string('dashboard/includes/partial_product_delete.html',
		context,
		request=request,
		)
	return JsonResponse(data)











    