from django.db import models

# Create your models here.
class Day(models.Model):
  day = models.DateField()
  max_cal = models.IntegerField(default = 0)

  def cals(self):
    servings = Serving.objects.filter(day = self)
    return reduce(lambda acc, serv: acc + serv.cals(), servings, 0)
  cals.short_description = "Calories"
  cals.admin_order_field = 'self'

  def delta_cals(self):
    return self.max_cal - self.cals()

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



class Serving(models.Model):
  day = models.ForeignKey(Day)
  food = models.ForeignKey(Food)
  amount = models.IntegerField(default = 0) # grams
  MEAL_CHOICE = (
    ('BF', 'Breakfast'),
    ('PN', 'Pre-noon'),
    ('LU', 'Lunch'),
    ('AN', 'After-noon'),
    ('DI', 'Dinner'),
    ('EV', 'Evening'),
  )
  meal = models.CharField(max_length = 2, choices = MEAL_CHOICE)

  def cals(self):
    return int((self.food.energy / 100.0) * self.amount)

  def __unicode__(self):
    return "%d g. %s" % (self.amount, self.food.text)