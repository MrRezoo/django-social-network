from django import forms
from django.forms import ModelForm

from posts.models import Post, Comment


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class EditPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
        error_messages = {
            'body': {
                'required': 'این فیلد اجباری است',
            }
        }
        help_texts = {
            'body': 'max 400 character'
        }


class AddReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'})
        }
