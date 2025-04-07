from django import forms

from familylineage.apps.persons.models import Person
from familylineage.apps.relationships.models import Marriage, ParentChild


class AddParentForm(forms.Form):
    parents = forms.ModelChoiceField(queryset=Marriage.objects.all())

    def save(self, person: Person) -> None:
        parents = self.cleaned_data['parents']
        husband = parents.husband
        wife = parents.wife

        ParentChild.objects.create(parent=husband, child=person)
        ParentChild.objects.create(parent=wife, child=person)
