from django.forms import ModelForm
from django import forms
from myapp.models import Book

class DateInput(forms.DateInput):
    input_type = 'date'

class BooksForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        required = '__all__'
        widgets = {
            'date': DateInput(),
        }

class DeleteBookForm(forms.Form):
    confirm = forms.BooleanField(required=True)