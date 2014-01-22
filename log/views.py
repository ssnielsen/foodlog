from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime
from django.views import generic

from log.models import Day, Serving, Food

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
  days_lt = Day.objects.filter(day__lt = date).order_by('-day')
  for day in days_lt:
    return day.max_cal
  days_gt = Day.objects.filter(day__gt = date).order_by('day')
  for day in days_gt:
    return day.max_cal
  return 1234   