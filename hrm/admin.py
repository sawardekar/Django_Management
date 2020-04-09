from django.contrib import admin
from hrm.models import EmployeeType,Employee,Product


# Register your models here.
admin.site.register(Employee)
admin.site.register(EmployeeType)
admin.site.register(Product)