# Wibo Documentation: Cards

## Terms 
Django
: a web application framework for Python. [djangoproject.org](http://djangoproject.org)

## Django Overview
The Django framework breaks everything down into "Apps." The idea is an app is a modular component of your larger site. You can program several Django apps for your site, then redistrubute them to other projects without much alteration. 

Each app is made up of a handful of `.py` files that define what the app is and what it can do. The basic structure of an app on disk is given below, followed by a description of the important pieces. 

    wibo
    |-- <app name>
    |   |-- models.py
    |   |-- views.py
    |   |-- urls.py
    |   |-- admin.py
    |   |-- tests.py
    |-- wibo
    |   |-- settings.py
    |   |-- local_settings.py
    |   |-- urls.py
    |   |-- templates
    |   |   |-- site_base.html
    |   |   |-- <app name>
    |-- manage.py

Django apps follow the Model View Controller (MVC) paradigm (though it's important to note Django's "views" do not correspond to the View in MVC).

### models.py
`models.py` is a collection of classes ("models") that define the objects used by the app and in the MVC paradigm can be thought of as the Model.
Each class in `models.py` represents a database table and each variable ("field") added to the model is a column in that table. 
A basic model is shown below. All models are derived from Django's `models.Model` class and all fields should be instances of `models.Field` classes (or classes derived from `models.Field`). The `__unicode__` function returns a unicode string used when calling `print` on an instance of the model (this is also what is displayed when the model is viewed in the Django Admin and in selection UI elements).

    from django.db import models

    class Card(models.Model):
        """Doc string"""

        # attributes/fields
        name = models.CharField(max_length=255)

        def __unicode__(self):
            return "card %s" (self.name)

#### Inheritance
Since Django is a Python framework, they've tried to give you full access to Python's inheritance model. *Technically* you can create "is-a" relationships in models, but since models are so tightly tied to database tables, it often causes more trouble than it's worth. 

There are two ways Django implements the "is-a" paradigm in the database tables: a purely abstract base class (that does not create a table of its own) and a base class that creates a table to hold all common attributes (with foreign keys to instances of child classes). The idea behind both is that repeating code is bad, so if you can write it once for a base class, when you change the code it will change for all child classes. In practice it seems to just spread out the code you have to edit when you want to change something (you end up adding half the new code to the base class and half to the child class). A better way to do it might be to create standard function that get called by "child" classes instead. 

With that said, most of Wibo attempts to use Django inheritance. JobCards, ProductCards, AdjustmentCards and ServiceCards all inherit from the generic Card class. The card class is an abstract class, so no table is created for a generic Card. 

#### Card
The base Card class contains attributes common to all cards (and, as previously stated, is an abstract class and therefore doesn't create a table of its own). Most fields and functions are self explanatory (see inline comments in `models.py`).

**Status Choices**
All status choices are defined in the Card base class. This makes it easier to test for status choices in other functions (you can do `if status == Card.HOLD` instead of `if type(card) == JobCard and status == JobCard.HOLD`). The `STATUS_CHOICES` variable can them be extended in each child class. 
**Note:** in the child class, the last item in `STATUS_CHOICES` *MUST* end with `,` (e.g. `(TEMPLATE, 'template'),`).


**Cost and Waste Cost**
To speed up queries for price and cost information, those related values are cached in the database. The `save()` method for the card updates the cached values so *in theory* the value is never stale. There have, however, been limited cases where saving the card has failed and the values are out of date. These failures are typically indicative of code errors and should be fixed anyway, so I'm not hugely concerned with stale data at this point (though you should be aware this is happening).

**Validation**
As of 28-Apr-2014 the validation system isn't currently operational. The idea is before a job can be marked complete certain criteria must be met (like having waste notes entered or uploading a thumbnail). The requisite code framework has been written. 

#### AdjustmentCard
The adjustment card was designed to add arbitrary values to an invoice. This would be used for things like rush fees and discounts (or 'other items' like banner stands or outsourced installation). The card type was created in September 2013 and tested via command line, but the front end interface was never created (we started hacking the product cards and materials to get the job done and there hasn't been time to fully roll out new card types).

#### ServiceCard
The service card was created to bill design and copyrighting time. The current implementation is limited, but could (should) be extended to include fields for quoted hours (what we tell the client) and worked hours (how long we've actually worked on the project). Adding a "clock in" and "clock out" function would be cool too, but that was way beyond the scope of the "new cards" project at the time.
The card type was created in September 2013 and tested via command line, but the front end interface was never created (we started hacking the product cards and materials to get the job done and there hasn't been time to fully roll out new card types).

#### ProductCard
Product cards store information about how to create a finished product. Product card templates let managers define what a "building banner" will be (and how we will charge for it), then users can copy and modify those templates on their individual jobs. Products are made up of materials, adjustment cards and service cards.

#### JobCard
Job cards store information about our clients and how they're going to pay us. They're made up of the other card types. 

#### CardQuantity
CardQuantity objects (are not cards) store information about how many of a card is associated with another card. It also stores square-footage and waste information. 

#### Forms
Django makes form validation easy. To create a form, create a class that inherits from `ModelForm` and create an inner "meta class" with a "model" attribute like below:

    from django.forms import ModelForm
    class CardForm(ModelForm):

        class Meta:
            model = ProductCard


By default, the order fields are defined in the model is the order they show up in the form (this is also true when you manually define form fields in the form class). Each model field type corresponds to a form field type (like date fields will use the date form field). You can also exclude model fields from the form (e.g. `JobCard.cost` is a calculated field, so it doesn't make sense to let a user type a value). Read the [Django Forms documentation](https://docs.djangoproject.com/en/dev/topics/forms/) for more info. 