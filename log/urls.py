from django.conf.urls import patterns, url, include
from log import views

urlpatterns = patterns('',
  url(r'^$', views.index, name = 'index'),

  # Days
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/$', views.DayView.as_view(), name = 'day'),
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/info/$', views.day_info, name = 'day_info'),
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/serving/add/$', views.add_serving, name = 'add_serving'),
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/serving/edit/$', views.edit_serving, name = 'edit_serving'),
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/serving/remove/$', views.remove_serving, name = 'remove_serving'),
  
  # Meal
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/meal/(?P<meal>\w+)/$', views.meal_info, name = 'meal'),

  # Food
  url(r'^food/$', views.FoodView.as_view(), name = 'food'),
  url(r'^food/search/$', views.food_search, name = 'food_search'),
)
