from django.contrib import admin
from log.models import Day, Food, Serving

# Register your models here.

class ServingInline(admin.TabularInline):
  model = Serving
  extra = 0

class DayAdmin(admin.ModelAdmin):
  fieldsets = [
        ('Date',               {'fields': ['day']}),
        ('Calories', {'fields': ['max_cal']}),
    ]
  readonly_fields = ['cals']
  list_display = ('day', 'max_cal', 'cals')
  inlines = [ServingInline]

admin.site.register(Food)
admin.site.register(Serving)
admin.site.register(Day, DayAdmin)
