from celery import shared_task
from telegram import Bot
from django.conf import settings

@shared_task
def send_telegram_notification(book_id):
    from .models import Book
    book = Book.objects.get(id=book_id)
    if book:
        if book.file_path:
            print('ishladi')
            # bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            # chat_id = settings.TELEGRAM_CHAT_ID
            # message = f'A new book "{book.title}" has been added with file: {book.file_path}'
            # bot.send_message(chat_id=chat_id, text=message)
