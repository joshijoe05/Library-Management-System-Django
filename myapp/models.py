from django.db import models
from isbn_field import ISBNField

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    date = models.DateField()
    isbn = ISBNField(clean_isbn=False,unique=True)

    def __str__(self):
        return self.title

