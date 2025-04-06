from django.db import models
from model_utils import Choices

from familylineage.apps.persons.models import Person


class ParentChild(models.Model):
    parent = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='parent')
    child = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='child')


class Marriage(models.Model):
    husband = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='husband')
    wife = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='wife')
    is_divorced = models.BooleanField(default=False)
