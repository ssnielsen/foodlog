from django.conf.urls import patterns, url, include
from log import views

urlpatterns = patterns('',
  url(r'^$', views.index, name = 'index'),

  # User handling
  url(r'^login/$', views.login_user, name = 'login'),
  url(r'^logout/$', views.logout_user, name = 'logout'),
  url(r'^signup/$', views.signup, name = 'signup'),


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
  url(r'^food/add/$', views.food_add, name = 'food_add'),
  url(r'^food/edit/$', views.food_edit, name = 'food_edit'),
  # url(r'^food/external/(?P<query>\w{1,100})/$', views.external_food_search, name = 'external_food_search'),

  # Pastebuffer
  url(r'^paste/$', views.paste_get, name = 'paste'),
  url(r'^paste/add/$', views.paste_add, name = 'paste_add'),
  url(r'^paste/remove/$', views.paste_remove, name = 'paste_remove'),
  url(r'^paste/reset/$', views.paste_reset, name = 'paste_reset'),
  url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/paste/$', views.paste_to_meal, name = 'paste_to_meal'),

  # Catch all
  url(r'^.*/$', views.catchall, name = 'catchall')
)
