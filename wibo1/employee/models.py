from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.conf import settings

class Employee(models.Model):
    """
    Abstract base class for employees
    """
    INTERN = 'intern'
    PART_TIME = 'part-time'
    GC451 = 'gc 451'
    GRADUATE_ASSISTANT = 'graduate assistant'
    WORK_STUDY = 'work study'
    FULL_TIME = 'full-time'
    
    CLASSIFICATION_CHOICES = (
            (INTERN,        'intern'),
            (PART_TIME,     'part-time'),
            (GC451,         'GC 451'),
            (GRADUATE_ASSISTANT,'grad assistant'),
            (WORK_STUDY, 'federal work study'),
            (FULL_TIME, 'full-time')
            )

    DESIGNER = 'designer'
    WRITER = 'writer'
    PRODUCTION_MANAGER = 'production manager'
    ART_DIRECTOR = 'art director'
    SALES = 'sales'
    HR = 'human resources'
    MARKETING = 'marketing'
    SUPPLY = 'supply'
    PHOTOGRAPHER = 'photographer'
    STUDENT_ADMIN = 'student admin'
    WEB = 'web'
    SAPUB_ADMIN = 'sapub admin'
    SAPUB_STAFF = 'sapub staff'

    TITLE_CHOICES = (
            (DESIGNER, 'designer'),
            (WRITER, 'writer'),
            (PRODUCTION_MANAGER, 'production manager'),
            (ART_DIRECTOR, 'art director'),
            (SALES, 'sales'),
            (HR, 'human resources'),
            (MARKETING, 'marketing'),
            (SUPPLY, 'supply'),
            (PHOTOGRAPHER, 'photographer'),
            (STUDENT_ADMIN, 'student admin'),
            (WEB, 'web'),
            (SAPUB_ADMIN, 'SAPUB with admin access'),
            (SAPUB_STAFF,'SAPUB with user access')
            )
    
    wibo_user = models.ForeignKey(User, primary_key=True)
    user_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, blank=True)
    phone = models.CharField(max_length=24)
    birthday = models.DateField(blank=True, null=True)
    graduation = models.DateField(blank=True, null=True)
    classification = models.CharField('position type', max_length=100, 
            choices=CLASSIFICATION_CHOICES)
    title = models.CharField('title', max_length=100, choices=TITLE_CHOICES)
    photo = models.ImageField(upload_to='employees',blank=True)
    active = models.BooleanField()
    
    def _get_full_name(self):
        """
        Returns the full name
        """
        if self.first_name or self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.wibo_user

    full_name = property(_get_full_name)

    def save(self):
        '''saves the instance in the database'''
        self.active = self.wibo_user.is_active

        self.wibo_user.is_active = self.active
        self.wibo_user.save()

        super(Employee,self).save()

    def __unicode__(self):
        return self.full_name

# default permission groups for new employees
PERMISIONS = {
        'admin': [      # has full read/write/delete priviledges for everything
            Employee.PRODUCTION_MANAGER,
            Employee.ART_DIRECTOR,
            Employee.SAPUB_ADMIN, ],
        'designer': [   # can add, edit and delete jobs
            Employee.DESIGNER, ],
        'staff' : [     # can add and edit jobs
            Employee.SAPUB_STAFF ],
        'student' : [   # can view jobs
            Employee.SALES,
            Employee.HR,
            Employee.MARKETING,
            Employee.SUPPLY,
            Employee.PHOTOGRAPHER,
            Employee.STUDENT_ADMIN,
            Employee.WEB, ],
        }
            
class EmployeeForm(ModelForm):
    """
    Creates a form based on the Employee Model
    """
    class Meta:
        model = Employee
        exclude= ('wibo_user',)

