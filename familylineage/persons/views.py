from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from familylineage.apps.persons.models import Person

from .forms import AddParentForm


def index(request: HttpRequest) -> HttpResponse:
    persons = Person.objects.order_by('name')

    paginator = Paginator(persons, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Persons',
        'persons': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'persons/index.html', context)


def details(request: HttpRequest, person_id: int) -> HttpResponse:
    person = Person.objects.get(pk=person_id)
    return render(request, 'persons/details.html', {'person': person})


def add_parents(request: HttpRequest, person_id: int) -> HttpResponse:
    person = Person.objects.get(pk=person_id)

    form = AddParentForm(request.POST or None)
    if form.is_valid():
        form.save(person=person)
        messages.success(request, 'Parents added successfully')
        return redirect("persons:details", person_id=person.id)

    return render(request, 'forms.html', {'person': person, 'form': form})


def family_tree(request: HttpRequest, person_id: int) -> HttpResponse:
    person = Person.objects.get(pk=person_id)
    return render(request, 'persons/family_tree.html', {'person': person})
