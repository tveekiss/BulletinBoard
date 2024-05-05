from celery import shared_task
import time

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .models import Reply, Post


@shared_task
def create_reply(reply):
    instance = Reply.objects.get(id=reply)
    email = instance.post.author.email
    subject = f'Новый отклик на объявление {instance.post.title}'
    text_content = (f'На ваше объявление "{instance.post.title}" откликнулся {instance.author.username}\n\n'
                    f'{instance.text}\n\n'
                    f'Принять можно по ссылке: http://127.0.0.1:8000/myreply/')
    html_content = (f'На ваше объявление <a href="http://127.0.0.1:8000/{instance.post.id}/">{instance.post.title}</a>'
                    f' откликнулся <strong>{instance.author.username}</strong><br><br>'
                    f'{instance.text}<br><br>'
                    f'Принять объявление можно <a href="http://127.0.0.1:8000/myreply/">здесь</a>')

    msg = EmailMultiAlternatives(subject, text_content, None, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def delete_reply(user_id, post_id):
    user = User.objects.get(id=user_id)
    post = Post.objects.get(id=post_id)
    email = user.email
    subject = f'{post.author.username} принял ваш отклик'
    text_content = f'{post.author.username} принял ваш отклик на объявление: "{post.title}"'
    html_content = (f'<strong>{post.author.username}</strong> принял ваш отклик на объявление: '
                    f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a>')
    msg = EmailMultiAlternatives(subject, text_content, None, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
