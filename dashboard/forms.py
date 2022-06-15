from django import forms
from django.contrib.auth.models import User
from .models import *


class productForm(forms.ModelForm):
      class Meta:
            model=loanType
            exclude=['created_by','updated_by','updated_on','company','branch']
            widgets={
            'name':forms.TextInput(attrs={'class':'form-control lmsinput', 'required':True}),
            'rate':forms.NumberInput(attrs={'class':'form-control lmsinput', 'required':True, 'max':'100', 'min':'0', 'step':'0.1'}),
            'description':forms.Textarea(attrs={'class':'form-control lmsinput', 'required':True}),
            'payment_frequency':forms.Select(attrs={'class':'form-control lmsinput', 'required':True}),
            'tenure':forms.NumberInput(attrs={'class':'form-control lmsinput', 'required':True}),
            'market':forms.Select(attrs={'class':'form-control lmsinput'}),
            }
