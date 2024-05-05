from django.urls import path
from .views import (PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, MyPostListView,
                    ReplyCreateView, ReplyList, agree_reply, disagree_reply, PostByCategoryListView)

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('category/<int:pk>', PostByCategoryListView.as_view(), name='category-home'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_view'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/like/', ReplyCreateView.as_view(), name='like'),
    path('myposts/', MyPostListView.as_view(), name='my_post'),
    path('myreply/', ReplyList.as_view(), name='replies_list'),
    path('myreply/agree/<int:pk>/', agree_reply, name='agree_reply'),
    path('myreply/disagree/<int:pk>/', disagree_reply, name='disagree_reply')

]
