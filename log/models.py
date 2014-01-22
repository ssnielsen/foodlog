from django.db import models
import datetime
import sys

# print >>sys.stderr, meal_cal

# Create your models here.
class Day(models.Model):
  day = models.DateField()
  slug = models
  max_cal = models.IntegerField(default = 0)

  def servings_by_meal(self):
    servings = []
    for choice in MEAL_CHOICES:
      servings.append((choice[1], []))
    for serving in Serving.objects.filter(day = self):
      servings[int(serving.meal)][1].append(serving)
    return servings

  def cals_by_meal(self):
    meal_cals = {}
    for meal in self.servings_by_meal():
      meal_cal = reduce(lambda acc, serv: acc + serv.cals(), meal[1], 0)
      meal_cals[meal[0]] = meal_cal
    return meal_cals 

  def amount_by_meal(self):
    meal_amounts = {}
    for meal in self.servings_by_meal():
      meal_amount = reduce(lambda acc, serv: acc + serv.amount, meal[1], 0)
      meal_amounts[meal[0]] = meal_amount
    return meal_amounts

  def cals(self):
    servings = Serving.objects.filter(day = self)
    return reduce(lambda acc, serv: acc + serv.cals(), servings, 0)

  def delta_cals(self):
    return self.max_cal - self.cals()

  def next_day(self):
    return self.day + datetime.timedelta(days = 1)

  def prev_day(self):
    return self.day + datetime.timedelta(days = -1)  

  def __unicode__(self):
    return str(self.day)



# class Meal(models.Model):
#   day = models.ForeignKey(Day)

#   def cals(self):
#     food_in_meal = Serving.objects.filter(meal = self)
#     return reduce(lambda acc, serv: acc + serv.cals(), food_in_meal, 0)

#   def __unicode__(self):
#     return str(self.day.day) + ' - ' + self.meal



class Food(models.Model):
  text = models.CharField(max_length = 255)
  energy = models.IntegerField() # kcal/100 g
  protein = models.DecimalField(max_digits = 3, decimal_places = 1) # g/100g
  carbo = models.DecimalField(max_digits = 3, decimal_places = 1) # g/100g
  fat = models.DecimalField(max_digits = 3, decimal_places = 1) # g/100g

  def __unicode__(self):
    return self.text

MEAL_CHOICES = (
    ('0', 'Breakfast'),
    ('1', 'Pre-noon'),
    ('2', 'Lunch'),
    ('3', 'After-noon'),
    ('4', 'Dinner'),
    ('5', 'Evening'),
  )

MEAL_DICT = dict(MEAL_CHOICES)

REV_MEAL_DICT = dict((v,k) for k, v in MEAL_DICT.iteritems())

class Serving(models.Model):
  day = models.ForeignKey(Day)
  food = models.ForeignKey(Food)
  amount = models.IntegerField(default = 0) # grams
  
  meal = models.CharField(max_length = 1, choices = MEAL_CHOICES)

  class Meta:
    ordering = ['meal']

  def cals(self):
    return int((self.food.energy / 100.0) * self.amount)

  def __unicode__(self):
    return "%d g. %s" % (self.amount, self.food.text)