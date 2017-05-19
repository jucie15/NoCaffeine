from django import forms
from feedback.models import FeedbackComment, FeedbackPost


class CommentForm(forms.ModelForm):
    class Meta:
        model = FeedbackComment
        # fields = '__all__'
        fields = ['message']
        widgets = {
             'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
         }

class PostForm(forms.ModelForm):
    class Meta:
        model = FeedbackPost
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        return title

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
