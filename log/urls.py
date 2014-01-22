from django.conf.urls import patterns, url
from log import views

urlpatterns = patterns('',
  url(r'^$', views.index, name = 'index'),
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/$', views.DayView.as_view(), name = 'day'),
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/serving/add/$', views.add_serving, name = 'add_serving'),
  url(r'^food/$', views.FoodView.as_view(), name = 'food'),
  url(r'^food/search/$', views.food_search, name = 'food_search'),
)