from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import PostForm
from .models import Post
from django.contrib import messages


class PostListView(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts/post_list.html'
    context_object_name = 'bulletins'
    extra_context = {'title': 'Объявления'}


class MyPostListView(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts/post_list.html'
    context_object_name = 'bulletins'
    extra_context = {'title': 'Мои объявления'}

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_view.html'
    context_object_name = 'bulletin'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_add.html'
    extra_context = {'title': 'Создание объявления'}

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_add.html'
    extra_context = {'title': 'Редактирование объявления'}

    def form_valid(self, form):
        messages.success(self.request, 'Объявление успешно изменено!')
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    extra_context = {'title': 'Удаление объявления'}
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Объявление успешно удалено!')
        return super().form_valid(form)





