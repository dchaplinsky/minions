from django.contrib import admin
from core.models import Convocation


class ConvocationAdmin(admin.ModelAdmin):
    list_display = ['number', 'year_from', 'year_to']


admin.site.register(Convocation, ConvocationAdmin)
