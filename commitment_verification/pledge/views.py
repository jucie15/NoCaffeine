from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from pledge.models import CongressMan


def index(request):
    return HttpResponse('welcome')


def congressman_list(request):
    congressman_list = CongressMan.objects.all()

    context = {}
    context['congressman_list'] = congressman_list

    return render(request, 'pledge/congressman_list.html', context)


def congressman_detail(request):
    pass
