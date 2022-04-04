from django import forms
from .models import Book
from django.core.exceptions import ValidationError
import datetime


class Book_update_form(forms.ModelForm):
    class Meta:
        """Using all book model fields and widget to make app more coherent """
        model = Book
        fields = '__all__'
        widgets = {
                    'publish_date': forms.DateInput(attrs={'type': 'date'})
                }

    def clean(self):
        author = self.cleaned_data.get('author')
        title = self.cleaned_data.get('title')
        ISBN = self.cleaned_data.get('ISBN_Number')
        publish_date = self.cleaned_data.get('publish_date')
        if Book.objects.filter(author=author, title=title).exists():
            """Checking if there is not duplicate book in database"""
            raise ValidationError('That Book already exists in your library!')
        if publish_date >= datetime.date(2006, 12, 30) and len(str(ISBN)) != 13:
            """Checking if ISBN is correct using information about ISBN number"""
            raise ValidationError('This book should have 13 digit ISBN')
        elif publish_date <= datetime.date(2006, 12, 30) and len(str(ISBN)) != 10:
            raise ValidationError('This book should have 10 digit ISBN')

    def clean_ISBN_Number(self):
        ISBN_number = self.cleaned_data.get('ISBN_Number')
        if len(Book.objects.filter(ISBN_Number=ISBN_number)) >= 1:
            """Checking if book with the same ISBN does not exists"""
            raise ValidationError('That Book already exists in your library!')
        else:
            return ISBN_number


class Book_create_form(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
                    'publish_date': forms.DateInput(attrs={'type': 'date'})
                }

    def clean(self):
        author = self.cleaned_data.get('author')
        title = self.cleaned_data.get('title')
        ISBN = self.cleaned_data.get('ISBN_Number')
        publish_date = self.cleaned_data.get('publish_date')
        if Book.objects.filter(author=author, title=title).exists():
            """Checking if there is not duplicate book in database"""
            raise ValidationError('That Book already exists in your library!')
        if publish_date >= datetime.date(2006, 12, 30) and len(str(ISBN)) != 13:
            """Checking if ISBN is correct using information about ISBN number"""
            raise ValidationError('This book should have 13 digit ISBN')
        elif publish_date <= datetime.date(2006, 12, 30) and len(str(ISBN)) != 10:
            raise ValidationError('This book should have 10 digit ISBN')

    def clean_ISBN_Number(self):
        ISBN_number = self.cleaned_data.get('ISBN_Number')
        if Book.objects.filter(ISBN_Number=ISBN_number).exists():
            """Checking if book with the same ISBN does not exists"""
            raise ValidationError('That Book already exists in your library!')
        else:
            return ISBN_number
