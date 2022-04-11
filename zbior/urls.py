from django.urls import path
from zbior.views import BookApi, books_list_view, books_create, books_delete, book_import, BooksEdit

"""Creating separate url list in case of expanding app in the future"""

urlpatterns = [
    path('', books_list_view, name='book-list'),
    path('create/', books_create),
    path('API/', BookApi.as_view(), name='book-api'),
    path('delete/<my_id>/', books_delete),
    path('edit/<pk>/', BooksEdit.as_view()),
    path('import/', book_import, name='book-import'),
]
