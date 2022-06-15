from django import forms
from .models import Asset, assetDocument
from django.contrib.auth.models import User

class assetForm(forms.ModelForm):
	def __init__(self,request,*args,**kwargs):
		super (assetForm,self ).__init__(*args,**kwargs) # populates the post
		self.fields['owner'].queryset = User.objects.filter(person__company=request.user.person.company).filter(is_staff=False)
		
	class Meta:
		model=Asset
		exclude=['created_by','updated_by','updated_on','company','branch']
		widgets={
	            'name':forms.TextInput(attrs={'class':'form-control lmsinput', 'required':True}),
	            'owner':forms.Select(attrs={'class':'form-control lmsinput', 'required':True}),
	            'description':forms.Textarea(attrs={'class':'form-control lmsinput', 'required':True}),
	            'inspection_date':forms.DateInput(attrs={'class':'form-control lmsinput', 'required':True}),
	            'expiry_date':forms.DateInput(attrs={'class':'form-control lmsinput', 'required':True}),
	            'value':forms.NumberInput(attrs={'class':'form-control lmsinput', 'required':True}),
	            'status':forms.Select(attrs={'class':'form-control lmsinput'}),
	            }

class assetDocumentForm(forms.ModelForm):
	class Meta:
		model=assetDocument
		exclude=['created_by','updated_by','updated_on','company','branch','proof_of']
		widgets={
				'document_name':forms.TextInput(attrs={'class':'form-control ', 'required':True, 'placeholder':'enter document type'}),
				'file':forms.FileInput(attrs={'class':'form-control ', 'required':True}),
		}