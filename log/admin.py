from django.contrib import admin
from log.models import Day, Food, Serving
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)

class ServingInline(admin.TabularInline):
  model = Serving
  extra = 0
  ordering = ('meal',)

class DayAdmin(admin.ModelAdmin):
  fieldsets = [
        ('Date',               {'fields': ['day']}),
        ('Calories', {'fields': ['max_cal']}),
        ('User', {'fields': ['user_ref']})
    ]
  readonly_fields = ['cals']
  list_display = ('day', 'max_cal', 'cals', 'user_ref')
  inlines = [ServingInline]

class FoodAdmin(admin.ModelAdmin):
  list_display = ('text', 'energy', 'carbo', 'protein', 'fat', 'public', 'creator')

admin.site.register(Food, FoodAdmin)
admin.site.register(Serving)
admin.site.register(Day, DayAdmin)
