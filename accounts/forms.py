from django import forms
from .models import Client
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username=forms.CharField(label='Username',
	help_text='Please enter you username', 
	widget=forms.TextInput(attrs={'class':'form-control lmsinput', 'required': True}))
	
	password=forms.CharField(label='Password',
	help_text='Please Enter Your Password',
	widget=forms.PasswordInput(attrs={'class':'form-control lmsinput', 'required':True}))


class clientForm(forms.ModelForm):
	class Meta:
		model=Client
		exclude=['user','created_by','updated_by','updated_on','company','branch']
		widgets = {
            'title': forms.Select(attrs={'class': 'form-control', 'value':'Mr', 'required':True}),
            'fullname':forms.TextInput(attrs={'class': 'form-control','value':'Mr',  'required':True}),
            'full_address':forms.TextInput(attrs={'class': 'form-control','value':'Mr', 'required':True}),
            'city':forms.TextInput(attrs={'class': 'form-control','value':'Mr', 'required':True}),
            'zip':forms.TextInput(attrs={'class': 'form-control', 'value':'Mr','required':True}),
            'state':forms.TextInput(attrs={'class': 'form-control','value':'Mr', 'required':True}),
            'phone':forms.TextInput(attrs={'class': 'form-control','value':'Mr', 'required':True}),
            'state_of_origin':forms.TextInput(attrs={'class': 'form-control','value':'Mr', 'required':True}),
            'lga':forms.TextInput(attrs={'class': 'form-control','value':'Mr', 'required':True}),
            'loan_officer':forms.Select(attrs={'class': 'form-control','value':'Mr', 'required':True}),
            'gender':forms.Select(attrs={'class': 'form-control', 'required':True}),
            'dob':forms.DateInput(attrs={'class':'form-control', 'value':'1/1/1994','required':True}),
            'marital_status':forms.Select(attrs={'class':'form-control', 'required':True}),
            'picture':forms.FileInput(attrs={'class':'form-control'}),
            'bio':forms.Textarea(attrs={'class':'form-control', 'value':'Mr'}),
            'current_employer':forms.TextInput(attrs={'class':'form-control','value':'Mr', 'required':True}),
            'current_salary':forms.TextInput(attrs={'class':'form-control', 'value':'Mr','required':True}),
            'job_description':forms.TextInput(attrs={'class':'form-control','value':'Mr', 'required':True}),
            'years_in_workplace':forms.TextInput(attrs={'class':'form-control','value':'Mr', 'required':True}),
            'state_of_origin':forms.TextInput(attrs={'class':'form-control', 'value':'Mr','required':True}),
            'vehicles_owned':forms.TextInput(attrs={'class':'form-control','value':'Mr', 'required':True}),
            'years_at_residence':forms.TextInput(attrs={'class':'form-control', 'value':'Mr','required':True}),
            'residential_status':forms.Select(attrs={'class':'form-control', 'value':'Mr','required':True}),
            'educational_status':forms.Select(attrs={'class':'form-control', 'value':'Mr','required':True}),
            'employment_date':forms.DateInput(attrs={'class':'form-control', 'value':'Mr'}),
            }

class userForm(forms.ModelForm):
	class Meta:
		model=User
		fields=('first_name', 'last_name','email','username','password')
		widgets={'password':forms.PasswordInput(attrs={'class': 'form-control', 'required':True, 'value':''}),
		'username':forms.TextInput(attrs={'class':'form-control', 'required':True, 'value':''}),
		'first_name':forms.TextInput(attrs={'class':'form-control', 'required':True, 'value':''}),
		'last_name':forms.TextInput(attrs={'class':'form-control', 'required':True, 'value':''}),
		'email':forms.EmailInput(attrs={'class':'form-control', 'required':True, }),
		}	 

