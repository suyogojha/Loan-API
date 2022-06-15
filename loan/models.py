from django.db import models
from dashboard.models import loanType, personAccount, baseModel
from dashboard.choices import STATUS_CHOICES, PAYMENT_METHOD, PAYMENT_FREQUENCY_CHOICES
from assetmanager.models import Asset
from .choices import FEE_CHARGE_METHOD_CHOICES
from django.contrib.auth.models import User



# Create your models here.
class Loan(baseModel):
	status=models.CharField(max_length=200, choices=STATUS_CHOICES)
	borrower=models.ForeignKey(User,on_delete=models.CASCADE)
	application_date=models.DateField(auto_now_add=True)
	amount=models.IntegerField()
	preferred_payment_date=models.DateField()
	method_of_payt=models.CharField(max_length=20,choices=PAYMENT_METHOD )
	bank_account=models.ForeignKey(personAccount,on_delete=models.CASCADE, null=True, related_name='loan_payment_account')
	collateral=models.ForeignKey(Asset,on_delete=models.CASCADE, related_name='loan_colateral', null=True, blank=True)
	loan_type=models.ForeignKey(loanType,on_delete=models.CASCADE)
	tenure=models.IntegerField( null=True)
	tenure_qualifier=models.CharField(max_length=50)
	issue_date=models.DateField(null=True)
	payment_frequency=models.CharField(max_length=50, choices=PAYMENT_FREQUENCY_CHOICES)
	fee=models.IntegerField(null=True, blank=True)
	fee_charge_method=models.IntegerField(null=True, blank=True, choices=FEE_CHARGE_METHOD_CHOICES)
	


