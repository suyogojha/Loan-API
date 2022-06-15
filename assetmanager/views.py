from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Asset, assetDocument
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import assetForm,assetDocumentForm
from django.db import transaction
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.forms.models import modelformset_factory
import pdb
# Create your views here.
class assetList(LoginRequiredMixin, ListView):
	login_url = '/account/login/'
	model=Asset
	template_name = 'assetmanager/asset_list.html'
	context_object_name = 'asset_list'
	
	
	def get_queryset(self):
		return Asset.objects.filter(company=self.request.user.person.company)


@login_required(login_url='/account/login/')
@transaction.atomic
def save_asset_form(request, form, template_name,formset):
	data = dict()
	if request.method == 'POST' :
		if form.is_valid() and formset.is_valid():
			asset=form.save(commit=False)
			asset.audit(request)
			asset.save()
			assetDocument.objects.filter(proof_of=asset).delete()
			data['form_is_valid'] = True
			for document_form in formset:
				name=document_form.cleaned_data['document_name']
				file=document_form.cleaned_data['file']
				document=assetDocument.objects.create(proof_of=asset, document_name=name, file=file)
				document.audit(request)
				document.save()
			assets = Asset.objects.all()
			#pdb.set_trace()
			data['html_product_list'] = render_to_string('assetmanager/includes/partial_asset_list.html', {
                'asset_list': assets
            })
		else:
			data['form_is_valid'] = False
	context = {'form': form, 'formset':formset}
	#pdb.set_trace()
	data['html_form'] = render_to_string(template_name, context, request=request)
	#pdb.set_trace()
	return JsonResponse(data)


@login_required(login_url='/account/login/')
@transaction.atomic
def createAsset(request):
	modelformset=modelformset_factory(assetDocument, assetDocumentForm)
	if request.method == 'POST':
		form = assetForm(request,request.POST)
		documentformset=modelformset(data=request.POST, files=request.FILES)
	else:
		form=assetForm(request)
		documentformset=modelformset()
		#pdb.set_trace()
	return save_asset_form(request, form, 'assetmanager/includes/partial_asset_create.html', documentformset)

@login_required(login_url='/account/login/')
@transaction.atomic
def asset_update(request,id):
	modelformset=modelformset_factory(assetDocument,assetDocumentForm,extra=1)
	asset=get_object_or_404(Asset, id=id)
	documentobjects=assetDocument.objects.filter(proof_of=asset)
	documents=[{'name':document.document_name, 'file':document.file} for document in documentobjects]
	#pdb.set_trace()
	if request.method =='POST':
		form=assetForm(request=request,data=request.POST, instance=asset)
		documentformset=modelformset(data=request.POST, files=request.FILES)
	else:
		documentformset=modelformset(initial=documents)
		#pdb.set_trace()
		form=assetForm(request=request,instance=asset)
	return save_asset_form(request, form, 'assetmanager/includes/partial_asset_update.html',documentformset)

@login_required(login_url='/account/login/')
def asset_delete(request,id):
	asset=get_object_or_404(Asset, id=id)
	data = dict()
	#pdb.set_trace()
	if request.method=='POST':
		assetDocument.objects.filter(proof_of=asset).delete()
		asset.delete()
		data['form_is_valid'] = True  # This is just to play along with the existing code
		assets = Asset.objects.all()
		data['html_product_list'] = render_to_string('assetmanager/includes/partial_asset_list.html', {
		    'asset_list': assets
		})
	else:
		context = {'asset': asset}
		data['html_form'] = render_to_string('assetmanager/includes/partial_asset_delete.html',
		context,
		request=request,
		)
	return JsonResponse(data)
	





	
		





	