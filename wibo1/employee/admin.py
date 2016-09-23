from employee.models import *
from django.contrib import admin

class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Django Stuff',{'fields':['wibo_user']}),
            ('Contact Info',{
                'fields':['first_name','last_name','email','phone','birthday','graduation']}),
            ('Employment Info',{
                'fields':['active','classification','title','photo']}),
            ]

admin.site.register(Employee, EmployeeAdmin)
