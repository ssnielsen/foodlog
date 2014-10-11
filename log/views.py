from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils import timezone
from django.core import serializers
from django.views import generic
from django.template import RequestContext
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

import json
import datetime
import urllib2

from log.models import Day, Serving, Food, REV_MEAL_DICT
from log.forms import FoodSearchForm

import sys

def landing_page(request):
  return render_to_response('log/landing.html', context_instance=RequestContext(request))

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
  '''Find the best match for a newly created day'''
  days_lt = Day.objects.filter(day__lt = date, user_ref = user).order_by('-day')
  for day in days_lt:
    return day.max_cal
  days_gt = Day.objects.filter(day__gt = date, user_ref = user).order_by('day')
  for day in days_gt:
    return day.max_cal
  return 1234

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

def add_serving(request, year, month, day):
  if 'amount' in request.POST and 'meal' in request.POST and 'food_id' in request.POST:
    date = datetime.date(int(year), int(month), int(day))
    user = request.user
    day_obj = get_object_or_404(Day, day = date, user_ref = user)
    food = get_object_or_404(Food, pk = request.POST['food_id'])
    amount = int(request.POST['amount'])
    meal = REV_MEAL_DICT[request.POST['meal']]
    serving = Serving(day = day_obj, meal = meal, food = food, amount = amount)
    serving.save()
    to_json = {
      "serving_obj" : serializers.serialize('json', (serving,)),
      "food_text" : food.text,
      "cals" : serving.cals(),
    }
    data = json.dumps(to_json)
    return HttpResponse(data, content_type = 'application/json')
  return index(request)

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
  if request.method == 'POST':
    form = FoodSearchForm(request.POST)
    if form.is_valid():
      food_query = form.cleaned_data['food_query']
      matches = Food.objects.filter(Q(text__contains = food_query) & (Q(public = True) | Q(creator = request.user)))
      #public_matches = matches.filter(public = True)
      #private_mactches = matches.filter(creator = request.user)
      #public_serialized = serializers.serialize('json', public_matches)
      #private_serialized = serializers.serialize('json', private_mactches)
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
  if request.method == 'POST' and request.POST and 'name' in request.POST and 'energy' in request.POST and 'carbo' in request.POST and 'protein' in request.POST and 'fat' in request.POST:
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
          return index(request)
      else:
        return HttpResponse(status = 403)
  return HttpResponse(status = 400)

def logout_user(request):
  logout(request)
  return index(request)
