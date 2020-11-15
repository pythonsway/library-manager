from rest_framework import serializers

from catalog.models import Book


class BookSerializer(serializers.ModelSerializer):
    language = serializers.StringRelatedField()
    authors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ['title', 'authors', 'pub_date',
                  'isbn', 'pages_num', 'cover', 'language']
