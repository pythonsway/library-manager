from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Language(models.Model):
    """Language of book."""
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Author(models.Model):
    """Author of book."""
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Book(models.Model):
    """Book details."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, help_text='Book title')
    authors = models.ManyToManyField(Author, help_text='Author(s)')
    pub_date = models.DateField(null=True, blank=True,
                                validators=[MaxValueValidator(limit_value=date.today)],
                                help_text='Publication date')
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True,
                            unique=True, validators=[RegexValidator(regex=r'\d{13}')],
                            help_text='ISBN-13 (unmbers only)')
    pages_num = models.PositiveIntegerField(default=1, null=True, blank=True,
                                            validators=[MaxValueValidator(9999)],
                                            help_text='Number of pages')
    cover = models.ImageField(upload_to='covers/', default='default.jpg',
                              help_text='Photo cover')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True,
                                 blank=True, help_text='Natural language')
    slug = models.SlugField(max_length=300)

    class Meta:
        ordering = ['title', ]

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-details', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}-{self.pages_num}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
