from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django_filters import rest_framework as filters

from .forms import PostForm, ReplyForm
from .models import Post, Reply, Category
from .filters import ReplyFilter


class PostListView(ListView):
    model = Post
    ordering = '-date'
    paginate_by = 5
    template_name = 'posts/post_list.html'
    context_object_name = 'bulletins'
    extra_context = {
        'title': 'Объявления',
        'categories': Category.objects.all(),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(snt=Count('post')).filter(snt__gt=0)
        context['title'] = 'Объявления'
        return context


class PostByCategoryListView(ListView):
    model = Post
    ordering = '-date'
    context_object_name = 'bulletins'
    paginate_by = 5
    template_name = 'posts/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(snt=Count('post')).filter(snt__gt=0)
        context['title'] = 'Объявления'
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=category)


class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-date'
    paginate_by = 5
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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_add.html'
    extra_context = {'title': 'Создание объявления'}

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_add.html'
    extra_context = {'title': 'Редактирование объявления'}

    def form_valid(self, form):
        messages.success(self.request, 'Объявление успешно изменено!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    extra_context = {'title': 'Удаление объявления'}
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Объявление успешно удалено!')
        return super().form_valid(form)


# ========== REPLY ==========

class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    ordering = '-date'
    template_name = 'replies/reply_list.html'
    context_object_name = 'replies'
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        queryset = Reply.objects.filter(post__author=self.request.user)
        self.filter = ReplyFilter(self.request.GET, request=self.request, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filter
        context['title'] = 'Отклики'
        return context


@login_required
def agree_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.agree = True
    reply.delete()
    messages.success(request, 'Вы приняли отклик')
    return redirect('replies_list')


@login_required
def disagree_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    messages.error(request, 'Вы отклонили отклик')
    return redirect('replies_list')


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'replies/reply_add.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Создание сообщения'}

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        reply.post = post
        messages.success(self.request, 'Вы успешно отправили сообщение!')
        return super().form_valid(form)








