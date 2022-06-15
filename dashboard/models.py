from django.contrib.auth.models import User
from django.db import models

from .choices import *


class Company(models.Model):
    name=models.CharField(max_length=200)
    domain=models.CharField(max_length=200)
    primary_color=models.CharField(max_length=200, choices=COLOR_CHOICES)
    website=models.URLField(max_length=500)
    email=models.EmailField()
    owner=models.CharField(max_length=200)
    currency_type=models.CharField(max_length=10, default='NGN', choices=CURRENCY_CHOICES)
    logo=models.ImageField(max_length=200, help_text='require a 100 by 100 img size', upload_to='logos/')
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField( auto_now=True)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE, blank=True, related_name='created_by_company')
    
class Branch(models.Model):
    full_address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    zip=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    email=models.EmailField()
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    manager=models.ForeignKey(User,on_delete=models.CASCADE, blank=True,related_name='branch_manager')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE, blank=True,related_name='created_by_on_branch')
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE, blank=True,related_name='updated_by_branch')

class baseModel(models.Model):
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='applicationcreator', blank=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True, blank=True)
    updated_on=models.DateTimeField(auto_now=True, blank=True)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE, blank=True,related_name='applicationupdater', null=True)
    company=models.ForeignKey(Company,on_delete=models.CASCADE, related_name='applicationcompany',null=True)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE,related_name='applicationbranch',null=True)
   
    def audit(self,request):
        self.created_by=request.user
        self.company=request.user.person.company
        self.branch=request.user.person.branch
     




   

class Bank(baseModel):
    bank_name=models.CharField(max_length=50)
    account_number=models.CharField(max_length=50, null=True)
    account_type=models.CharField(max_length=50, choices=ACCOUNT_CHOICES)

class companyAccount(Bank):
    owner=models.ForeignKey(Company,on_delete=models.CASCADE, related_name="company_account")
    description=models.TextField()

class personAccount(Bank):
    owner=models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_bank')

class documentType(baseModel):
    name=models.CharField(max_length=50)
    description=models.TextField()

    def __str__(self):
        return self.name
       
    
class loanType(baseModel):
    name=models.CharField(max_length=50)
    rate=models.DecimalField(max_digits=5, decimal_places=2)
    description=models.TextField()
    need_collateral=models.BooleanField(help_text='does this type of Loan need Coollateral')
    need_guarantor=models.BooleanField(help_text='does this type of loan need a gurantor')
    market=models.CharField(null=True, help_text="these include the category of people who will be interested in this particular product", max_length=50, choices=MARKET_CHOICES )
    documents=models.ManyToManyField(documentType,help_text="Include documents that are needed here for this particular loan.. You can go to the document section to add or delete document")
    min_amount_allowed=models.IntegerField(null=True, blank=True)#null means that any price
    max_amount_allowed=models.IntegerField(null=True, blank=True)#min price must not be more than maximum price
    interest_type=models.CharField(max_length=50, choices=INTEREST_TYPE_CHOICES, default='Flat Rate')



#class Loan(baseModel):
 ##  status=models.CharField(max_length=200, choices=STATUS_CHOICES)
   # application_date=models.DateField(auto_now_add=True)
    #amount=models.IntegerField()
    #preferred_payment_date=models.DateField()
   # method_of_payt=models.CharField(max_length=20,choices=PAYMENT_METHOD )
   # bank_account=models.ForeignKey(personAccount, null=True, related_name='loan_payment_account')
   # collateral=models.ForeignKey(Asset, related_name='loan_colateral')
   # loan_type=models.ForeignKey(loanType)
   # issue_date=models.DateField(null=True)


class activityLog(baseModel):
    date=models.DateTimeField(auto_now_add=True)
    initiator=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    level=models.IntegerField()

class Documents(baseModel):
    upload_date=models.DateField(auto_now_add=True)
    document_type=models.CharField(max_length=200)
    file=models.FileField(upload_to='documents/')

class Message(baseModel):
    subject=models.CharField(max_length=200)
    messages=models.TextField()
    sent_on=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=20, choices=MESSAGE_STATUS)
    sent_by=models.ForeignKey(User,on_delete=models.CASCADE, related_name='message_sender')
    sent_to=models.ForeignKey(User,on_delete=models.CASCADE)









    

