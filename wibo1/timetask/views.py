from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.forms.models import inlineformset_factory, formset_factory
from django.template import Context, loader, RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from cards.models import *
from timetask.models import *
from employee.models import Employee