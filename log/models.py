from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Day(models.Model):
  user_ref = models.ForeignKey(User)
  day = models.DateField()
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

  def _cals(self):
    servings = Serving.objects.filter(day = self)
    return reduce(lambda acc, serv: acc + serv.cals(), servings, 0)
  cals = property(_cals)

  def _protein(self):
    servings = Serving.objects.filter(day = self)
    return reduce(lambda acc, serv: acc + serv.protein(), servings, 0.0)
  protein = property(_protein)

  def _carbo(self):
    servings = Serving.objects.filter(day = self)
    return reduce(lambda acc, serv: acc + serv.carbo(), servings, 0.0)
  carbo = property(_carbo)

  def _fat(self):
    servings = Serving.objects.filter(day = self)
    return reduce(lambda acc, serv: acc + serv.fat(), servings, 0.0)
  fat = property(_fat)

  def delta_cals(self):
    return self.max_cal - self.cals()

  def next_day(self):
    return self.day + datetime.timedelta(days = 1)

  def prev_day(self):
    return self.day + datetime.timedelta(days = -1)  

  def __unicode__(self):
    return str(self.day)

class Food(models.Model):
  text = models.CharField(max_length = 255)
  energy = models.DecimalField(max_digits = 4, decimal_places = 1) # kcal/100 g
  protein = models.DecimalField(max_digits = 4, decimal_places = 1) # g/100g
  carbo = models.DecimalField(max_digits = 4, decimal_places = 1) # g/100g
  fat = models.DecimalField(max_digits = 4, decimal_places = 1) # g/100g
  public = models.BooleanField(default = False)
  creator = models.ForeignKey(User)

  def __unicode__(self):
    return self.text + " " + str(self.energy) + " " + str(self.carbo) + " " + str(self.protein) + " " + str(self.fat) 

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
    return int(round(float(self.food.energy) / 100.0 * self.amount))

  def protein(self):
    return float(self.food.protein) / 100.0 * float(self.amount)

  def carbo(self):
    return float(self.food.carbo) / 100.0 * float(self.amount)

  def fat(self):
    return float(self.food.fat) / 100.0 * float(self.amount)

  def __unicode__(self):
    return "%d g. %s" % (self.amount, self.food.text)


class UserSettings(models.Model):
  max_cal = models.IntegerField(default = 0)
  user_ref = models.ForeignKey(User)