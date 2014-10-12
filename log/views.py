from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils import timezone
from django.core import serializers
from django.views import generic
from django.template import RequestContext
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.db import IntegrityError

import json
import datetime
import urllib2

from log.models import Day, Serving, Food, UserSettings, REV_MEAL_DICT

import sys

def landing_page(request, extra_context = dict()):
  return render_to_response('log/landing.html', extra_context, context_instance = RequestContext(request))

def catchall(request):
  return HttpResponseRedirect(reverse('foodlog:index'))

def index(request):
  if request.user.is_authenticated():
    now = timezone.now()
    year = now.year
    month = now.month
    day = now.day
    return HttpResponseRedirect(reverse('foodlog:day', kwargs = {'year': year, 'month': month, 'day': day}))
  else:
    return landing_page(request)

class DayView(generic.DateDetailView):
  model = Day
  date_field = 'day'
  allow_future = True
  template_name = 'log/day.html'

  @method_decorator(login_required(login_url = '/foodlog/'))
  def dispatch(self, *args, **kwargs):
    return super(DayView, self).dispatch(*args, **kwargs)

  def get_object(self):
    user = self.request.user
    kwargs = self.request.resolver_match.kwargs
    date = datetime.date(int(kwargs['year']), int(kwargs['month']), int(kwargs['day']))
    try:
      day = Day.objects.get(day = date, user_ref = user)
    except Day.DoesNotExist: # Create new day
      max_cal = findBestMaxCal(user, date)
      day = Day(day = date, max_cal = max_cal, user_ref = user)
      day.save()
    return day

def findBestMaxCal(user, date):
  settings = UserSettings.objects.get(user_ref = user)
  return settings.max_cal
  # '''Find the best match for a newly created day'''
  # days_lt = Day.objects.filter(day__lt = date, user_ref = user).order_by('-day')
  # for day in days_lt:
  #   return day.max_cal
  # days_gt = Day.objects.filter(day__gt = date, user_ref = user).order_by('day')
  # for day in days_gt:
  #   return day.max_cal
  # return 1234

def day_info(request, year, month, day):
  date = datetime.date(int(year), int(month), int(day))  
  user = request.user
  day_obj = get_object_or_404(Day, day = date, user_ref = user)
  to_json = {
    "day_obj": serializers.serialize('json', (day_obj,)),
    "cals": day_obj.cals,
    "protein": day_obj.protein,
    "carbo": day_obj.carbo,
    "fat": day_obj.fat,
    "cals_by_meal": day_obj.cals_by_meal(),
    "amount_by_meal": day_obj.amount_by_meal(),
  }
  data = json.dumps(to_json)
  return HttpResponse(data, content_type = 'application/json')

def meal_info(request, year, month, day, meal):
  date = datetime.date(int(year), int(month), int(day))
  user = request.user
  meal = REV_MEAL_DICT[meal]
  day_obj = get_object_or_404(Day, day = date, user_ref = user)
  servings = Serving.objects.filter(day = day_obj, meal = meal)
  data = serializers.serialize('json', servings)
  return HttpResponse(data, content_type = 'application/json')

def addServingToDate(user, date, meal, food_id, amount):
  day_obj = get_object_or_404(Day, day = date, user_ref = user)
  food = get_object_or_404(Food, pk = food_id)
  serving = Serving(day = day_obj, meal = meal, food = food, amount = amount)
  serving.save()
  to_json = {
    "serving_obj" : serializers.serialize('json', (serving,)),
    "food_text" : food.text,
    "cals" : serving.cals(),
  }
  data = json.dumps(to_json)
  return data  

def add_serving(request, year, month, day):
  if 'amount' in request.POST and 'meal' in request.POST and 'food_id' in request.POST:
    user = request.user
    date = datetime.date(int(year), int(month), int(day))
    meal = REV_MEAL_DICT[request.POST['meal']]
    amount = int(request.POST['amount'])
    food_id = request.POST['food_id']
    response = addServingToDate(user, date, meal, food_id, amount)  
    return HttpResponse(response, content_type = 'application/json')
  else:
    return HttpResponse(status = 400)

def remove_serving(request, year, month, day):
  if 'serving_id' in request.POST:
    serving = Serving.objects.get(pk = request.POST['serving_id'])
    serving.delete()
  return HttpResponse()

def edit_serving(request, year, month, day):
  if 'serving_id' in request.POST and 'amount' in request.POST:
    serving =  get_object_or_404(Serving, pk = request.POST['serving_id'])
    serving.amount = int(request.POST['amount'])
    serving.save()
    to_json = {
      "serving_obj" : serializers.serialize('json', (serving,)),
      "cals" : serving.cals(),
    }
    data = json.dumps(to_json)
    return HttpResponse(data, content_type = 'application/json')
  return HttpResponse()


class FoodView(generic.ListView):
  model = Food
  template_name = 'log/food.html'

  # Only select the food-items private to the user. I.e. created by the user.
  def get_queryset(self):
    return Food.objects.filter(creator = self.request.user)

  @method_decorator(login_required(login_url = '/foodlog/'))
  def dispatch(self, *args, **kwargs):
    return super(FoodView, self).dispatch(*args, **kwargs)

def food_search(request):
  if request.method == 'POST' and request.POST and request.POST['food_query']:
    food_query = request.POST['food_query']
    matches = Food.objects.filter(Q(text__contains = food_query) & (Q(public = True) | Q(creator = request.user)))
    serialized = serializers.serialize('json', matches)
    return HttpResponse(serialized, content_type = 'application/json')
  return HttpResponse()

# def external_food_search(request, query):
#   if request.method == 'GET':
#     external_url = u''.join(('http://www.vaegttab.nu/ajax/foods?q=', query)).encode('utf-8').strip() # Funky join due to encoding
#     external_request = urllib2.Request(external_url)
#     external_response = urllib2.urlopen(external_request)
#     external_data = external_response.read()
#     return HttpResponse(external_data)
#   else:
#     return HttpResponse(json.dumps([]))

def food_add(request):
  if request.method == 'POST' and request.POST and 'name' in request.POST and 'energy' in request.POST and 'carbo' in request.POST and 'protein' in request.POST and 'fat' in request.POST:
    name = request.POST['name']
    energy = float(request.POST['energy'])
    carbo = float(request.POST['carbo'])
    protein = float(request.POST['protein'])
    fat = float(request.POST['fat'])
    food = Food(text = name, energy = energy, carbo = carbo, protein = protein, fat = fat, creator = request.user)
    food.save()
    return HttpResponseRedirect(reverse('foodlog:food'))
  else:
    return HttpResponse(status = 400)

def food_edit(request):
  if request.method == 'POST' and request.POST and 'id' in request.POST and 'name' in request.POST and 'energy' in request.POST and 'carbo' in request.POST and 'protein' in request.POST and 'fat' in request.POST:
    name = request.POST['name']
    food_id = int(request.POST['id'])
    energy = float(request.POST['energy'])
    carbo = float(request.POST['carbo'])
    protein = float(request.POST['protein'])
    fat = float(request.POST['fat'])
    food = get_object_or_404(Food, pk = food_id)
    food.text = name
    food.energy = energy
    food.carbo = carbo
    food.protein = protein
    food.fat = fat
    food.save()
    return HttpResponse()
  else:
    return HttpResponse(status = 400)

def paste_get(request):
  if request.method == 'GET':
    if 'patebuffer' not in request.session:
      request.session['pastebuffer'] = list()
    pastebuffer = request.session['pastebuffer']
    serialized = json.dumps(pastebuffer)
    return HttpResponse(serialized, content_type = 'application/json')
  else:
    return HttpResponse(status = 403)

def paste_add_from_food(request, food_id, amount):
  if 'pastebuffer' not in request.session:
    request.session['pastebuffer'] = list()
  pastebuffer = request.session['pastebuffer']
  food = get_object_or_404(Food, pk = food_id)
  pastebuffer.append({'id': food_id, 'name': food.text, 'amount': amount})
  request.session['pastebuffer'] = pastebuffer
  return True;

def paste_add(request):
  if request.method == 'POST' and request.POST and 'serving_id' in request.POST:
    serving = get_object_or_404(Serving, pk = int(request.POST['serving_id']))
    paste_add_from_food(request, serving.food.pk, serving.amount)
    return HttpResponse()
  else:
    return HttpResponse(status = 400)

def paste_remove(request):
  if request.method == 'POST' and request.POST and 'number' in request.POST:
    pastebuffer = request.session['pastebuffer']
    del pastebuffer[int(request.POST['number'])]
    request.session['pastebuffer'] = pastebuffer
    return HttpResponse()
  else:
    return HttpResponse(status = 400)

def paste_reset(request):
  if request.method == 'POST':
    request.session['pastebuffer'] = list()
    return HttpResponse()
  else:
    return HttpResponse(status = 403)

def paste_to_meal(request, year, month, day):
  if request.method == 'POST' and request.POST and request.POST['meal']:
    user = request.user
    date = datetime.date(int(year), int(month), int(day))
    meal = REV_MEAL_DICT[request.POST['meal']]

    pastebuffer = request.session['pastebuffer']
    response = list()
    for entry in pastebuffer:
      food_id = entry['id']
      amount = entry['amount']
      response.append(addServingToDate(user, date, meal, food_id, amount))
    return HttpResponse(json.dumps(response), content_type = 'application/json')
  else:
    return HttpResponse(status = 403)

class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField()

def login_user(request):
  if request.POST:
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(username = username, password = password)
      if user is not None:
        if user.is_active:
          login(request, user)
          request.session['pastebuffer'] = list()
          return index(request)
    messages.add_message(request, messages.ERROR, "Wrong username or password.")
    formdata = form.cleaned_data.copy()
    del formdata['password']
    print(request)
    return landing_page(request, formdata)
  return HttpResponse(status = 405)

def logout_user(request):
  logout(request)
  messages.add_message(request, messages.INFO, "Successfully signed out.")
  return landing_page(request)

class SignupForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField()
  firstname = forms.CharField()
  lastname = forms.CharField()
  email = forms.EmailField()

def signup(request):
  if request.POST:
    form = SignupForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      firstname = form.cleaned_data['firstname']
      lastname = form.cleaned_data['lastname']
      email = form.cleaned_data['email']

      try:
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
      except IntegrityError:
        messages.add_message(request, messages.ERROR, "Username is taken.")
        formdata = form.cleaned_data.copy()
        del formdata['password']
        return landing_page(request, formdata)

      user_settings = UserSettings(max_cal = 2000, user_ref = user)
      user_settings.save()

      authed_user = authenticate(username = username, password = password)
      login(request, authed_user)
      return index(request)
    else:
      return HttpResponse(400)
  else:
    return HttpResponse(405)

