from django.contrib import admin
from .models import *

class PledgeInline(admin.TabularInline):
    model = Pledge

class CongressManAdmin(admin.ModelAdmin):
    model = CongressMan
    search_fields = ('name', 'party')
    list_display = ['id', 'name', 'party', 'constituency', 'updated_at']
    inlines = [
        PledgeInline,
    ]

class LikeOrDislikeInline(admin.TabularInline):
    model = LikeOrDislike

class PledgeAdmin(admin.ModelAdmin):
    model = Pledge
    inlines = [
        LikeOrDislikeInline,
    ]

class PledgeCommentAdmin(admin.ModelAdmin):
    model = PledgeComment

class PledgeEventAdmin(admin.ModelAdmin):
    model = PledgeEvent

class PledgeEventPostAdmin(admin.ModelAdmin):
    model = PledgeEventPost

class LikeOrDislikeAdmin(admin.ModelAdmin):
    model = LikeOrDislike

admin.site.register(CongressMan, CongressManAdmin)
admin.site.register(Pledge, PledgeAdmin)
admin.site.register(PledgeComment, PledgeCommentAdmin)
admin.site.register(PledgeEvent, PledgeEventAdmin)
admin.site.register(PledgeEventPost, PledgeEventPostAdmin)
admin.site.register(LikeOrDislike, LikeOrDislikeAdmin)
