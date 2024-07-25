from django import forms
from .models import Book, OrderBook, SendBook


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'year', 'pages', 'category',
                  'isbn', 'sub_category', 'url', 'file', 'size']


class OrderBookForm(forms.ModelForm):
    class Meta:
        model = OrderBook
        fields = ['book_name', 'description', 'author']


class SendBookForm(forms.ModelForm):
    class Meta:
        model = SendBook
        fields = ['book_name', 'description', 'author', 'file', 'url']


