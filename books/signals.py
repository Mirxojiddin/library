from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models import Book
from books.tasks import send_telegram_notification


@receiver(post_save, sender=Book)
def handle_book_creation(sender, instance, created, **kwargs):
    if created:
        if instance.file:
            print('ishladimi')

            # send_telegram_notification.delay(instance.id)
