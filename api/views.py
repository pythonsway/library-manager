from rest_framework import viewsets
from rest_framework import permissions
from .serializers import BookSerializer

from catalog.models import Book


class BookViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Books to be viewed"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
