class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ['message']
        widgets = {
             'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
         }
