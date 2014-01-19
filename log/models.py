from django.db import models

# Create your models here.
class Day(models.Model):
  day = models.DateField()
  max_cal = models.IntegerField(default = 0)

  def __unicode__(self):
    return str(self.day)

class Meal(models.Model):
  day = models.ForeignKey(Day)
  MEAL_CHOICE = (
    ('BF', 'Breakfast'),
    ('PN', 'Pre-noon'),
    ('LU', 'Lunch'),
    ('AN', 'After-noon'),
    ('DI', 'Dinner'),
    ('EV', 'Evening'),
  )
  meal = models.CharField(max_length = 2, choices = MEAL_CHOICE)

  def __unicode__(self):
    return str(self.day.day) + ' ' + self.meal

class Food(models.Model):
  text = models.CharField(max_length = 255)
  energy = models.IntegerField() # kcal/100 g
  protein = models.DecimalField(max_digits = 3, decimal_places = 1)
  carbo = models.DecimalField(max_digits = 3, decimal_places = 1)
  fat = models.DecimalField(max_digits = 3, decimal_places = 1)

  def __unicode__(self):
    return self.text


class Serving(models.Model):
  meal = models.ForeignKey(Meal)
  food = models.ForeignKey(Food)
  amount = models.IntegerField(default = 0) # grams

  def __unicode__(self):
    return self.amount + " g. " + self.food.text