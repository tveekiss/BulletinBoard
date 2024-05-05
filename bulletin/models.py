from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200)
    text = CKEditor5Field('Текст', config_name='extends')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_view', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField('Название', max_length=200)

    def __str__(self):
        return self.name


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    agree = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
