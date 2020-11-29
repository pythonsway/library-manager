from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # email = models.EmailField(max_length=254, unique=True)

    def save(self, *args, **kwargs):
        self._meta.get_field('email')._unique = True
        self._meta.get_field('email').blank = False
        self._meta.get_field('email').null = False
        super().save(*args, **kwargs)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['email',], name='unique email')
    #     ]

# User._meta.get_field('email')._unique = True
