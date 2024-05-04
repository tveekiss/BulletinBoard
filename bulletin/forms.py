from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from bulletin.models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = False

    class Meta:
        model = Post
        fields = ['title', 'text', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': CKEditor5Widget(attrs={'class': 'form-control django_ckeditor_5'}, config_name='extends'),
            'category': forms.Select(attrs={'class': 'form-control'})
        }