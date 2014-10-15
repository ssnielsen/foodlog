from django.http import HttpResponse
import xml.etree.ElementTree as ET

from log.models import Food

def parse_and_insert_dtu_data(request):
  foods = ET.parse('dtu_foods.xml').getroot()
  print("Loading data...")
  for food in foods.findall('.//food'):
    print(food.tag)
    name_en = food.findall("FoodName[@language='en']").text
    name_da = food.findall("FoodName[@language='da']").text
    print(name_en)    
    print(name_da)

  return HttpResponse()