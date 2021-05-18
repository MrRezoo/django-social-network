from django.forms import ModelForm

from posts.models import Post


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
