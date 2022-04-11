from django.db import models
from .validators import date_validator, isbn_validator


class Book(models.Model):
    title = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null=True)
    publish_date = models.DateField(null=True, validators=[date_validator])
    ISBN_Number = models.CharField(max_length=13, null=True, validators=[isbn_validator])
    number_of_pages = models.IntegerField(null=True)
    cover_link = models.URLField(null=True)
    publish_language = models.CharField(max_length=50, null=True)

    def __str__(self):
        """Changing display string to make searching through admin console easier"""
        return f'{self.title} - {self.author}'
