from django import forms
from .models import Post, Comment, Reply

class AddPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'image',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class CommentUForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class search_post(forms.Form):
    q = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'}
        )

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        widgets = {
          'text': forms.Textarea(attrs={'rows':1, 'cols':5}),
        }
        fields = ['text']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ""
        