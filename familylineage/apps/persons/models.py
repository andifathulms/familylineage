from django.db import models

from datetime import date
from dateutil.relativedelta import relativedelta  # type: ignore[import-untyped]

from model_utils import Choices
from thumbnails.fields import ImageField

from familylineage.core.utils import FilenameGenerator


class Person(models.Model):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True, null=True)

    GENDER = Choices(
        (1, 'male', 'Male'),
        (2, 'female', 'Female')
    )
    gender = models.PositiveSmallIntegerField(choices=GENDER)

    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    death_place = models.CharField(max_length=255, blank=True, null=True)
    is_living = models.BooleanField(default=True)

    photo = ImageField(upload_to=FilenameGenerator(prefix='persons'), blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def display_age(self) -> str:
        """
        Returns age as a string in format "X years Y months" based on birth_date.
        Handles living and deceased persons appropriately.
        """
        if not self.birth_date:
            return "Unknown age"

        reference_date = self.death_date if not self.is_living and self.death_date else date.today()

        try:
            delta = relativedelta(reference_date, self.birth_date)
            years = delta.years
            months = delta.months

            if years < 0:  # Handle future birth dates
                return "Not born yet"

            if years == 0 and months == 0:
                days = (reference_date - self.birth_date).days
                if days < 30:
                    return f"{days} days old"
                else:
                    return "Less than 1 month"

            age_parts = []
            if years > 0:
                age_parts.append(f"{years} year{'s' if years != 1 else ''}")
            if months > 0:
                age_parts.append(f"{months} month{'s' if months != 1 else ''}")

            return ' '.join(age_parts)

        except Exception as e:
            return f"Age calculation error :{e}"

    @property
    def parents(self):
        """Optimized query to get all parents"""
        from familylineage.apps.relationships.models import ParentChild

        return Person.objects.filter(
            id__in=ParentChild.objects.filter(child_id=self.id).values('parent_id')
        ).order_by('gender')

    @property
    def children(self):
        """Optimized query to get all children"""
        from familylineage.apps.relationships.models import ParentChild

        return Person.objects.filter(
            id__in=ParentChild.objects.filter(parent_id=self.id).values('child_id')
        ).order_by('birth_date', 'name')

    @property
    def spouses(self):
        """
        Returns all spouses of this person, automatically detecting
        whether to look for wife (if male) or husband (if female)
        """
        if self.gender == self.GENDER.male:
            return Person.objects.filter(
                id__in=Marriage.objects.filter(husband=self).values('wife')
            )
        elif self.gender == self.GENDER.female:
            return Person.objects.filter(
                id__in=Marriage.objects.filter(wife=self).values('husband')
            )
        return Person.objects.none()  # For other/unspecified genders

    @property
    def marriages(self):
        """
        Returns all Marriage relationships for this person
        """
        from familylineage.apps.relationships.models import Marriage
        if self.gender == self.GENDER.male:
            return Marriage.objects.filter(husband=self)
        elif self.gender == self.GENDER.female:
            return Marriage.objects.filter(wife=self)
        return Marriage.objects.none()
