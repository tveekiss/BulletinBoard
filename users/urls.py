from django.urls import path


from .views import register, user_login, user_logout, email_confirm


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('confirm/', email_confirm, name='email-confirm'),
    path('logout/', user_logout, name='logout'),
]
