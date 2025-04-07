from django.db import models
from django.db.models.query import QuerySet

from familylineage.apps.persons.models import Person


class ParentChild(models.Model):
    parent = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='parent')
    child = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='child')


class Marriage(models.Model):
    husband = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='husband')
    wife = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='wife')
    is_divorced = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.husband.name} & {self.wife.name}"

    def children(self) -> QuerySet:
        """
        Returns a queryset of the actual Person objects that are children of this marriage
        """
        husband_children = set(ParentChild.objects.filter(parent=self.husband).values_list('child', flat=True))
        wife_children = set(ParentChild.objects.filter(parent=self.wife).values_list('child', flat=True))
        common_child_ids = husband_children & wife_children

        return Person.objects.filter(id__in=common_child_ids)
