from celery import shared_task

from .models import OneTimeCode


@shared_task
def send_code_email(code_id):
    code = OneTimeCode.objects.get(id=code_id)
    user = code.user

    subject = f'Код для подтверждения почты'
    text_email = (f'Привет {user.username}, твой код для подтверждения:\n\n'
                  f'{code.code}\n\n'
                  f'Код действителен в течении 5 минут')
    user.email_user(subject, text_email)
