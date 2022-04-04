from django.urls import path
from zbior.views import Book_API, books_list_view, books_edit, books_create, books_delete, book_import

"""Creating separate url list in case of expanding app in the future"""

urlpatterns = [
    path('', books_list_view, name='book-list'),
    path('edit/<my_id>/', books_edit, name='book-edit'),
    path('create/', books_create),
    path('API/', Book_API.as_view(), name='book-api'),
    path('delete/<my_id>/', books_delete),
    path('import/', book_import, name='book-import'),
]
