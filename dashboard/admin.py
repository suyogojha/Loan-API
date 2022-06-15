from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Company)
admin.site.register(Branch)
#admin.site.register(Employee)
#admin.site.register(Client)
admin.site.register(personAccount)
admin.site.register(companyAccount)
#admin.site.register(Loan)
#admin.site.register(Asset)
admin.site.register(loanType)
admin.site.register(Message)
admin.site.register(activityLog)
admin.site.register(Documents)
admin.site.register(documentType)

