from django.core.management.base import BaseCommand

from catalog.constants import LANGUAGES
from catalog.models import Language


class Command(BaseCommand):
    help = 'Imports language choices based on ISO 639-1 codes'

    def handle(self, *args, **options):
        for code, name in LANGUAGES:
            Language.objects.create(code=code, name=name)
            self.stdout.write(self.style.SUCCESS(f'added {name} language'))
