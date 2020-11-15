from django.contrib import admin

from .models import Author, Book, Language

# titles
admin.site.site_header = "Library Manager administration"
admin.site.site_title = "Library Manager site admin"
admin.site.index_title = "Welcome to Library Manager"


# Menu
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Language)
