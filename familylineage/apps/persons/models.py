from django.db import models
from model_utils import Choices


class Person(models.Model):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True, null=True)

    GENDER = Choices(
        (1, 'male', 'Male'),
        (2, 'female', 'Female')
    )
    source = models.PositiveSmallIntegerField(choices=GENDER)

    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    death_place = models.CharField(max_length=255, blank=True, null=True)
    is_living = models.BooleanField(default=True)
