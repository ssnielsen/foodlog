from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.core import serializers
import datetime
from django.views import generic

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

def add_serving(request, year, month, day):
  date = datetime.date(int(year), int(month), int(day))
  day_obj = get_object_or_404(Day, day = date)
  food = get_object_or_404(Food, pk = request.POST['food_id'])
  amount = request.POST['amount']
  meal = REV_MEAL_DICT[request.POST['meal']]
  serving = Serving(day = day_obj, meal = meal, food = food, amount = amount)
  serving.save()
  return HttpResponseRedirect(reverse('foodlog:day', kwargs = {'year': year, 'month': month, 'day': day}))

def remove_serving(request, year, month, day):
  if 'serving_id' in request.POST:
    serving = Serving.objects.get(pk = request.POST['serving_id'])
    serving.delete()
  return HttpResponseRedirect(reverse('foodlog:day', kwargs = {'year': year, 'month': month, 'day': day}))

class FoodView(generic.ListView):
  model = Food
  template_name = 'log/food.html'

def food_search(request):
  # food_query = request.POST['food_query']
  # data = serializers.serialize('json', Food.objects.filter(text__contains = food_query))
  # return HttpResponse(data)
  
  if request.method == 'POST':
    form = FoodSearchForm(request.POST)
    if form.is_valid():
      food_query = form.cleaned_data['food_query']
      data = serializers.serialize('json', Food.objects.filter(text__contains = food_query))
      return HttpResponse(data)
    return HttpResponse()

