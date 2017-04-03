from django.contrib import admin
from .models import *


class CongressManAdmin(admin.ModelAdmin):
    model = CongressMan


class PledgeAdmin(admin.ModelAdmin):
    model = Pledge



admin.site.register(CongressMan, CongressManAdmin)
admin.site.register(Pledge, PledgeAdmin)
