from django.contrib import admin
from feedback.models import FeedbackPost, FeedbackComment


class FeedbackCommentAdmin(admin.ModelAdmin):
    model = FeedbackComment

class FeedbackPostAdmin(admin.ModelAdmin):
    model = FeedbackPost


admin.site.register(FeedbackPost,FeedbackPostAdmin)
admin.site.register(FeedbackComment, FeedbackCommentAdmin)
