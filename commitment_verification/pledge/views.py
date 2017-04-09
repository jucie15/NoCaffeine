from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from pledge.models import CongressMan


def index(request):
    # 인덱스 페이지
    return HttpResponse('welcome')


def congressman_list(request):
    # 국회의원 리스트 페이지
    congressman_list = CongressMan.objects.all()

    context = {}
    context['congressman_list'] = congressman_list

    return render(request, 'pledge/congressman_list.html', context)


def congressman_detail(request):
    # 국회의원 세부 페이지
    pass


def pledge_list(request):
    # 공약 리스트 페이지
    pass


def pledge_detail(request):
    # 공약 세부 페이지
    pass


def pledge_status_event(request):
    # 공약 상태 이벤트 페이지
    pass
