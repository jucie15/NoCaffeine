from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from pledge.models import *


def index(request):
    # 인덱스
    return render(request, 'pledge/index.html')


def congressman_list(request):
    # 국회의원 리스트
    congressman_list = CongressMan.objects.all()

    context = {}
    context['congressman_list'] = congressman_list

    return render(request, 'pledge/congressman_list.html', context)


def congressman_detail(request, pk):
    # 국회의원 세부
    pass


def pledge_list(request):
    # 공약 리스트
    pledge_list = Pledge.objects.all()

    context = {}
    context['pledge_list'] = pledge_list

    return render(request, 'pledge/pledge_list.html', context)

def pledge_detail(request):
    # 공약 세부
    pass


def pledge_status_event(request):
    # 공약 상태 이벤트
    pass

def search(reqeust):
    # 검색바를 통한 검색
    keyword = request.GET.get('q', '') # 검색 키워드
    # 국회의원 검색 결과
    condition = Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(party__icontains=keyword) | Q(constituency__icontains=keyword) # 검색 조건

    search_congressman_list = CongressMan.objects.filter(condition)

    # 공약 검색 결과
    condition = Q(congressman_name__icontains=keyword) | Q(title__icontains=keyword) | Q(status__icontains=keyword) | Q(description__icontains=keyword)

    search_pledge_list = Pledge.objects.filter(condition)

    context = {}
    context['search_congressman_list'] = search_congressman_list
    context['search_pledge_list'] = search_pledge_list

    return render(request, 'pledge/search_result.html', context)
