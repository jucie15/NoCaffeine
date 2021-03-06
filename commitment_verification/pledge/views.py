from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from pledge.models import *
from pledge.forms import CommentForm
import json

def index(request):
    # 인덱스
    return render(request, 'pledge/index.html')

def congressman_list(request):
    # 국회의원 리스트
    party = request.GET.get('party', '')

    if party == '전체' or party == '':
        # 전체 필터링이나, 처음 접근시 전체 리스트 노출
        congressman_list = CongressMan.objects.all()
    else:
        # 각 정당별 필터릴 적용 리스트
        congressman_list = CongressMan.objects.filter(party__icontains=party) # 국회의원 리스트

    context = {}
    context['congressman_list'] = congressman_list

    return render(request, 'pledge/congressman_list.html', context)

def congressman_detail(request, cm_pk):
    # 국회의원 세부
    congressman = get_object_or_404(CongressMan, pk=cm_pk)

    pledge_status = {}

    try:
        pledge_status['not_enforcement'] = congressman.pledge_set.filter(status='0').count() / congressman.pledge_set.all().count() * 100
        pledge_status['progress'] = congressman.pledge_set.filter(status='1').count() / congressman.pledge_set.all().count() * 100
        pledge_status['complete'] = congressman.pledge_set.filter(status='2').count() / congressman.pledge_set.all().count() * 100
        pledge_status['falied'] = congressman.pledge_set.filter(status='3').count() / congressman.pledge_set.all().count() * 100
    except ZeroDivisionError:
        pledge_status['not_enforcement'] = 100
        pledge_status['progress'] = 0
        pledge_status['complete'] =0
        pledge_status['falied'] = 0

    context = {}
    context['congressman'] = congressman
    context['pledge_status'] = pledge_status

    return render(request, 'pledge/congressman_detail.html', context)

def pledge_list(request):
    # 공약 리스트
    pledge_list = Pledge.objects.all()

    context = {}
    context['pledge_list'] = pledge_list

    return render(request, 'pledge/pledge_list.html', context)

def pledge_detail(request, pledge_pk):
    # 공약 세부
    pledge = get_object_or_404(Pledge, pk=pledge_pk)
    comment_form = CommentForm()

    context = {}
    context['pledge'] = pledge
    context['comment_form'] = comment_form


    return render(request, 'pledge/pledge_detail.html', context)

def pledge_status_event(request):
    # 공약 상태 변경 이벤트
    pass

def pledge_status_event_post(request):
    # 공약 상태 변경 이벤트 근거 글 쓰기
    pass

@login_required
def pledge_comment_new(request, pledge_pk):
    # 공약 디테일 내 댓글 달기
    pledge = get_object_or_404(Pledge, pk=pledge_pk)

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = CommentForm(request.POST, request.FILES) # 받아온 데이터를 통해 폼 인스턴스 생성

        if form.is_valid():
            # 폼에 데이터가 유효할 경우
            comment = form.save(commit=False) # 디비에 저장하지 않고 인스턴스 생성
            comment.user = request.user
            comment.pledge = pledge
            comment.save() # 유저와 공약 연결 후 디비에 저장
            messages.success(request, '새 댓글을 저장했습니다.')

            return redirect(comment.pledge)
    else:
        # 포스트 요청이 아닐 경우 빈 폼 생성
        form = CommentForm()

    return render(request, 'pledge/comment_form.html', {
        'form' : form,
        }) # 포스트 요청이 아닐 경우 빈 폼으로 페이지 렌더링

@login_required
def pledge_comment_delete(request, pledge_pk, comment_pk):
    # 공약 디테일 내 댓글 지우기
    comment = get_object_or_404(PledgeComment, pk=comment_pk)

    if comment.user != request.user:
        # 댓글 작성자와 현재 유저가 다를 경우
        messages.warning(request, '작성자만 삭제할 수 있습니다.')
    else:
        # 작성자와 동일할 경우
        comment.delete() # 댓글 삭제
        messages.success(request, '댓글을 삭제했습니다.')

    return redirect(comment.pledge)

@login_required
def pledge_comment_edit(request, pledge_pk, comment_pk):
    # 공약 디테일 내 댓글 수정
    comment = get_object_or_404(PledgeComment, pk=comment_pk)

    if comment.user != request.user:
        # 댓글 작성자와 현재 유저가 다를 경우 해당 공약페이지로 리다이렉트
        messages.warning(request, '댓글 작성자만 수정할 수 있습니다.')
        return reditrect(comment.pledge)

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = CommentForm(request.POST, request.FILES, instance=comment) # 받아온 데이터와 현재 댓글 인스턴스를 통해 폼 인스턴스 생성

        if form.is_valid():
            comment = form.save() # 수정된 댓글 저장
            messages.success(request, '기존 댓글을 수정헀습니다.')
            return redirect(comment.pledge)
    else:
        form = CommentForm(instance=comment) # 현재 댓글 인스턴스 정보를 가진 폼 인스턴스 생성

    return render(request, 'pledge/comment_form.html', {
        'form':form,
        })

@login_required
def pledge_like(request, pledge_pk):
    # 공약 좋아요 버튼 클릭시
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user # 요청한 유저
        pledge = get_object_or_404(Pledge, pk=pledge_pk) # 해당 공약 인스턴스 생성

        if user.like_dislike.filter(pledge_id=pledge.id).exists():
            # 좋아요/싫어요 중 하나라도 눌렀을 경우능
            # 둘 중 한개만 선택 가능
            like_instance = user.like_dislike.get(pledge_id=pledge.id) # 좋아요/싫어요 인스턴스 생성
            if like_instance.like == True:
                # 눌려있는 버튼이 좋아요일 경우
                LikeOrDislike.objects.filter(pledge=pledge, user=user).delete() # 인스턴스 삭제
            else:
                # 싫어요일 경우 좋아요로 바꾼 후 저장
                like_instance.like = True
                like_instance.dislike = False
                like_instance.save()
        else:
            # 버튼이 하나도 안눌려있을 경우 새롭게 생성
            LikeOrDislike.objects.create(
                user=user,
                pledge=pledge,
                like=True,
                dislike=False,
                )

        context = {} # 좋아요 개수와 싫어요 개수를 response에 담아 보낸다
        context['like_count'] = pledge.get_total_like
        context['dislike_count'] = pledge.get_total_dislike
    else:
        # ajax 요청이 아닐 경우
        context = {'status': 'fail'}

    # dic 형식을 json 형식으로 바꾸어 전달한다.
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def pledge_dislike(request, pledge_pk):
    # 공약 싫어요 버튼 클릭 시
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user # 요청한 유저
        pledge = get_object_or_404(Pledge, pk=pledge_pk) # 해당 공약 인스턴스 생성

        if user.like_dislike.filter(pledge_id=pledge.id).exists():
            # 좋아요/싫어요 중 하나라도 눌렀을 경우
            # 둘 중 한개만 선택 가능
            like_instance = user.like_dislike.get(pledge_id=pledge.id) # 좋아요/싫어요 인스턴스 생성
            if like_instance.dislike == True:
                # 눌려있는 버튼이 싫어요일 경우
                LikeOrDislike.objects.filter(pledge=pledge, user=user).delete() # 인스턴스 삭제
            else:
                # 좋아요일 경우 싫어요로 바꾼 후 저장
                like_instance.like = False
                like_instance.dislike = True
                like_instance.save()
        else:
            # 버튼이 하나도 안눌려있을 경우 새롭게 생성
            LikeOrDislike.objects.create(
                user=user,
                pledge=pledge,
                like=False,
                dislike=True,
                )
        context = {} # 좋아요 개수와 싫어요 개수를 response에 담아 보낸다
        context['like_count'] = pledge.get_total_like
        context['dislike_count'] = pledge.get_total_dislike
    else:
        # ajax 요청이 아닐 경우
        context = {'status': 'fail'}

    # dic 형식을 json 형식으로 바꾸어 전달한다.
    return HttpResponse(json.dumps(context), content_type='application/json')

def search(request):
    # 검색바를 통한 검색

    keyword = request.GET.get('q', '') # 검색 키워드
    # 국회의원 검색 결과
    condition = (Q(name__icontains=keyword) |
    Q(description__icontains=keyword) |
    Q(party__icontains=keyword) |
    Q(constituency__icontains=keyword)) # 국회의원 검색 조건

    search_congressman_list = CongressMan.objects.filter(condition) # 국회의원 검색 결과 리스트

    condition = (Q(congressman__name__icontains=keyword) |
    Q(congressman__description__icontains=keyword) |
    Q(congressman__party__icontains=keyword) |
    Q(congressman__constituency__icontains=keyword) |
    Q(title__icontains=keyword) |
    Q(status__icontains=keyword) |
    Q(description__icontains=keyword)) # 공약 검색 조건(검색된 국회의원들의 공약을 검색)

    # 공약 검색 결과
    search_pledge_list = Pledge.objects.filter(condition) # 공역 검색 결과 리스트


    context = {}
    context['search_congressman_list'] = search_congressman_list
    context['search_pledge_list'] = search_pledge_list

    return render(request, 'pledge/search_result.html', context)
