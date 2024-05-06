from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import OneTimeCode
from .tasks import send_code_email


@receiver(post_save, sender=OneTimeCode)
def create_reply(instance, **kwargs):
    send_code_email.delay(instance.id)
