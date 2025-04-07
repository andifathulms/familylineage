from django import forms

from familylineage.apps.persons.models import Person
from familylineage.apps.relationships.models import Marriage, ParentChild


class AddParentForm(forms.Form):
    parents = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['parents'].queryset = Marriage.objects.all()
        self.fields['parents'].label_from_instance = lambda obj: f"{obj.husband.name} & {obj.wife.name}"

    def save(self, person: Person) -> None:
        parents = self.cleaned_data['parents']
        husband = parents.husband
        wife = parents.wife

        ParentChild.objects.create(parent=husband, child=person)
        ParentChild.objects.create(parent=wife, child=person)
