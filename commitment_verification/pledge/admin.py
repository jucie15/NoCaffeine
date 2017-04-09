from django.contrib import admin
from .models import *

class PledgeInline(admin.TabularInline):
    model = Pledge

class CongressManAdmin(admin.ModelAdmin):
    model = CongressMan
    list_display = ['id', 'name', 'party', 'constituency', 'updated_at']
    inlines = [
        PledgeInline,
    ]

class PledgeAdmin(admin.ModelAdmin):
    model = Pledge

class PledgeEventAdmin(admin.ModelAdmin):
    model = PledgeEvent

class PledgeEventPostAdmin(admin.ModelAdmin):
    model = PledgeEventPost

admin.site.register(CongressMan, CongressManAdmin)
admin.site.register(Pledge, PledgeAdmin)
admin.site.register(PledgeEvent, PledgeEventAdmin)
admin.site.register(PledgeEventPost, PledgeEventPostAdmin)
