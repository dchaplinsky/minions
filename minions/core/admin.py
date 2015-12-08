from django.contrib import admin
from core.models import Convocation, MemberOfParliament, Minion


class ConvocationAdmin(admin.ModelAdmin):
    list_display = ['number', 'year_from', 'year_to']


class MemberOfParliamentAdmin(admin.ModelAdmin):
    pass
    # list_display = ['name', 'convocation', 'party', 'date_from', 'date_to']
    # list_select_related = ('convocation',)


class MinionAdmin(admin.ModelAdmin):
    list_display = ['name', 'mp', 'paid']
    list_select_related = ('mp', )


admin.site.register(Convocation, ConvocationAdmin)
admin.site.register(MemberOfParliament, MemberOfParliamentAdmin)
admin.site.register(Minion, MinionAdmin)
