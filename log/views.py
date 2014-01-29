from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.core import serializers
from django.views import generic
import json
import datetime

from log.models import Day, Serving, Food, REV_MEAL_DICT
from log.forms import FoodSearchForm

import sys

# Create your views here.
def index(request):
  now = timezone.now()
  year = now.year
  month = now.month
  day = now.day
  return HttpResponseRedirect(reverse('foodlog:day', kwargs = {'year': year, 'month': month, 'day': day}))

class DayView(generic.DateDetailView):
  model = Day
  date_field = 'day'
  allow_future = True
  template_name = 'log/day.html'

  def get_object(self):
    kwargs = self.request.resolver_match.kwargs
    date = datetime.date(int(kwargs['year']), int(kwargs['month']), int(kwargs['day']))
    try:
      day = Day.objects.get(day = date)
    except Day.DoesNotExist: # Create new day
      max_cal = findBestMaxCal(date)
      day = Day(day = date, max_cal = max_cal)
      day.save()
    return day

def findBestMaxCal(date):
  '''Find the best match for a newly created day'''
  days_lt = Day.objects.filter(day__lt = date).order_by('-day')
  for day in days_lt:
    return day.max_cal
  days_gt = Day.objects.filter(day__gt = date).order_by('day')
  for day in days_gt:
    return day.max_cal
  return 1234

def day_info(request, year, month, day):
  date = datetime.date(int(year), int(month), int(day))  
  day_obj = get_object_or_404(Day, day = date)
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
  meal = REV_MEAL_DICT[meal]
  day_obj = get_object_or_404(Day, day = date)
  servings = Serving.objects.filter(day = day_obj, meal = meal)
  data = serializers.serialize('json', servings)
  return HttpResponse(data, content_type = 'application/json')

def add_serving(request, year, month, day):
  if 'amount' in request.POST and 'meal' in request.POST and 'food_id' in request.POST:
    date = datetime.date(int(year), int(month), int(day))
    day_obj = get_object_or_404(Day, day = date)
    food = get_object_or_404(Food, pk = request.POST['food_id'])
    amount = int(request.POST['amount'])
    meal = REV_MEAL_DICT[request.POST['meal']]
    serving = Serving(day = day_obj, meal = meal, food = food, amount = amount)
    serving.save()
    return HttpResponseRedirect(reverse('foodlog:day', kwargs = {'year': year, 'month': month, 'day': day}))
  return index(request)

def remove_serving(request, year, month, day):
  if 'serving_id' in request.POST:
    serving = Serving.objects.get(pk = request.POST['serving_id'])
    serving.delete()
  return HttpResponse()
  #return HttpResponseRedirect(reverse('foodlog:day', kwargs = {'year': year, 'month': month, 'day': day}))

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

  #return HttpResponseRedirect(reverse('foodlog:day', kwargs = {'year': year, 'month': month, 'day': day}))


class FoodView(generic.ListView):
  model = Food
  template_name = 'log/food.html'

def food_search(request):
  if request.method == 'POST':
    form = FoodSearchForm(request.POST)
    if form.is_valid():
      food_query = form.cleaned_data['food_query']
      data = serializers.serialize('json', Food.objects.filter(text__contains = food_query))
      return HttpResponse(data, content_type = 'application/json')
    return HttpResponse()