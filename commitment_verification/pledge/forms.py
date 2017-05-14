from django import forms
from pledge.models import PledgeComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = PledgeComment
        # fields = '__all__'
        fields = ['message']
        widgets = {
             'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
         }
