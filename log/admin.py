from django.contrib import admin
from log.models import Day, Food, Serving
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)

# Register your models here.

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

admin.site.register(Food)
admin.site.register(Serving)
admin.site.register(Day, DayAdmin)
