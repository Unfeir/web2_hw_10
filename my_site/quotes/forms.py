from django.forms import ModelForm, CharField, DateField, TextInput, DateInput

from . models import Author, Note


class AuthorForm(ModelForm):
    fullname = CharField(max_length=100, required=True, widget=TextInput(attrs={"class": "form-control"}))
    born_date = DateField(widget=DateInput(attrs={"class": "form-control"}))
    born_location = CharField(max_length=3000, widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(max_length=10000, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    text = CharField(max_length=10000, required=True, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Note
        fields = ['text']
        exclude = ['author', 'tags']