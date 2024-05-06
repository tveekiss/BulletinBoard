from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .tasks import create_reply, delete_reply

from .models import Reply


@receiver(post_save, sender=Reply)
def reply_create(instance: Reply, created, **kwargs):
    if created:
        create_reply.delay(instance.id)


@receiver(pre_delete, sender=Reply)
def reply_delete(instance: Reply, **kwargs):
    if instance.agree:
        delete_reply.delay(instance.author.id, instance.post.id)
