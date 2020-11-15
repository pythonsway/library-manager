from datetime import date

from dal import autocomplete
from django import forms

from .models import Book, Language


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'authors', 'pub_date',
                  'isbn', 'pages_num', 'cover', 'language']
        widgets = {
            'pub_date': forms.DateInput(format=('%Y-%m-%d'),
                                        attrs={'type': 'date', 'max': date.today}),
            'authors': autocomplete.ModelSelect2Multiple(url='author-autocomplete',
                                                         forward=('authors', )),
            'language': autocomplete.ModelSelect2(url='language-autocomplete'),
        }


class BookSearchForm(forms.Form):
    title = forms.CharField(label='Book title', max_length=100)
    authors = forms.CharField(label='Authors', max_length=100)
    language = forms.ModelChoiceField(label='Language',
                                      queryset=Language.objects.all(), to_field_name="name")
    date_from = forms.DateField(label='Publication date from',
                                widget=forms.DateInput(
                                    format=('%Y-%m-%d'), attrs={'type': 'date'}))
    date_to = forms.DateField(label='Publication date to',
                              widget=forms.DateInput(
                                  format=('%Y-%m-%d'), attrs={'type': 'date'}))


class GoogleSearchForm(forms.Form):
    intitle = forms.CharField(label='Book title',
                              max_length=100, required=False)
    inauthor = forms.CharField(label='Authors',
                               max_length=100, required=False)
    inpublisher = forms.CharField(label='Publisher',
                                  max_length=100, required=False)
    subject = forms.CharField(label='Subject',
                              max_length=100, required=False)
    isbn = forms.CharField(label='ISBN',
                           max_length=13, required=False)
    lccn = forms.CharField(label='Library of Congress Control Number',
                           max_length=12, required=False)
    oclc = forms.CharField(label='Online Computer Library Center number',
                           max_length=8, required=False)
