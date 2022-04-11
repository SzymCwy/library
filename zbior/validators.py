import datetime
from django.core.exceptions import ValidationError


def date_validator(value):
    if value > datetime.date.today():
        raise ValidationError('The book publish date cannot be in the future!')


def isbn_validator(value):
    ISBN = str(value)
    if len(ISBN) != 13 and len(ISBN) != 10:
        raise ValidationError('Incorrect ISBN')
    try:
        int(ISBN)
    except ValueError:
        raise ValidationError('ISBN must be 10 or 13 numbers')

    if len(ISBN) == 13:
        isbn_sum = 0
        for i in range(len(ISBN) - 1):
            if i % 2 == 0:
                isbn_sum += int(ISBN[i]) * 1
            else:
                isbn_sum += int(ISBN[i]) * 3
        if isbn_sum % 10 != 10-(int(ISBN[-1])):
            raise ValidationError('ISBN control sum incorrect!')

    elif len(ISBN) != 10:
        isbn_sum = 0
        for i in range(len(ISBN) - 1):
            isbn_sum += (int(i) + 1) * int(ISBN[i])
        if str(isbn_sum % 11) != ISBN[-1]:
            raise ValidationError('ISBN control sum incorrect!')
