from django.urls import path
from books.views import (BookListView, BookCreateView, BookUpdateView, BookDeleteView, BookDetailView,
                         CategoryBookListView, OrderBookView, SendBookView, OrderedBookView, SendedBookView,
                         OrderedBookDetailView, SendedBookDetailView
                         )

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('order/', OrderBookView.as_view(), name='book_order'),
    path('send/', SendBookView.as_view(), name='book_send'),
    path('ordered/', OrderedBookView.as_view(), name='book_ordered'),
    path('sended/', SendedBookView.as_view(), name='book_sended'),
    path('ordered/<int:pk>', OrderedBookDetailView.as_view(), name='book_ordered_detail'),
    path('sended/<int:pk>', SendedBookDetailView.as_view(), name='book_sended_detail'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('category/<int:category_id>/', CategoryBookListView.as_view(), name='category_book_list'),
]