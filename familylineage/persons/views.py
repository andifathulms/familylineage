from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from familylineage.apps.persons.models import Person


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