import django_filters
from django_filters import FilterSet
from django import forms

from .models import Post, Reply


def myFilterRequests(request):
    print(request)
    if request is None:
        return Post.objects.all()

    user = request.user
    print(user)
    return Post.objects.filter(author=user)


class ReplyFilter(FilterSet):
    post = django_filters.ModelChoiceFilter(
        queryset=myFilterRequests,
        empty_label='Все посты',
        label='Поиск',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reply
        fields = ['post']

