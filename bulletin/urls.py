from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, MyPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_view'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('myposts/', MyPostListView.as_view(), name='my_post'),
]
