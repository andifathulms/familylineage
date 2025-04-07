from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from familylineage.apps.relationships.models import Marriage


def index(request: HttpRequest) -> HttpResponse:
    marriages = Marriage.objects.select_related('husband', 'wife').order_by('husband__name')

    paginator = Paginator(marriages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Families',
        'marriages': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'marriages/index.html', context)
