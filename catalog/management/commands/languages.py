from django.core.management.base import BaseCommand, CommandError

from catalog.models import Language

from catalog.constants import languages


class Command(BaseCommand):
    help = 'Imports language choices based on ISO 639-1 codes'

    def handle(self, *args, **options):
        for code, name in languages:
            Language.objects.create(code=code, name=name)
            self.stdout.write(self.style.SUCCESS(
                f'added {name} language'))
