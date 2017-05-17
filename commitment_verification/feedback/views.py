from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from feedback.models import FeedbackPost, FeedbackComment
from feedback.forms import PostForm, CommentForm

def post_list(request):
    # 피드백 게시판 리스트
    post_list = FeedbackPost.objects.all()

    return render(request,  'feedback/post_list.html', {
            'post_list' : post_list,
        })

def post_detail(request, post_pk):
    # 피드백 게시판 글 내용
    post = get_object_or_404(FeedbackPost, pk=post_pk)
    comment_form = CommentForm()

    post.hit_count() # 조회수 증가

    return render(request, 'feedback/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
    })

@login_required
def post_new(request):
    # 피드백 게시판 글 쓰기
    if request.method == 'POST':
        # 포스트 요청일 경우
        form = PostForm(request.POST, request.FILES) # 받아온 데이터를 통해 포스트 폼 인스턴스 생성

        if form.is_valid():
            # 값이 유효할 경우
            post = form.save(commit=False)
            post.author = request.user # 글쓴이를 현재 유저로 저장한 뒤
            post.save() # 글 저장
            messages.info(request, '포스팅을 잘 저장했습니다.')
            return redirect(post) # post get_absolute_url로 이동
    else:
        # 포스트 요청이 아닐경우 빈 폼 인스턴스 생성
        form = PostForm()

    return render(request, 'feedback/post_form.html', {
        'form': form,
    })


@login_required
def post_edit(request, post_pk):
    # 피드백 게시판 글 수정
    post = get_object_or_404(FeedbackPost, pk=post_pk) # 해당 게시글의 인스턴스 생성

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = PostForm(request.POST, request.FILES, instance=post) # 받아온 데이터와 현재 포스트 인스턴스의 데이터를 통해 포스트 폼 인스턴스 생성
        if form.is_valid():
            # 값이 유효할 경우 바뀐 값을 통해 저장
            post = form.save(commit=True)
            messages.info(request, '포스팅을 잘 저장했습니다.')
            return redirect(post) # post get_absolute_url로 이동
    else:
        # 포스트 요청이 아닐 경우
        form = PostForm(instance=post) # 현재 포스트 인스턴스의 값을 통해

    return render(request, 'feedback/post_form.html', {
        'form': form,
    })

@login_required
def comment_new(request, post_pk):
    # 피드백 디테일 내 댓글 달기
    post = get_object_or_404(FeedbackPost, pk=post_pk) # 해당 게시글의 인스턴스 생성

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = CommentForm(request.POST, request.FILES) # 받아온 데이터를 통해 폼 인스턴스 생성

        if form.is_valid():
            # 폼에 데이터가 유효할 경우
            comment = form.save(commit=False) # 디비에 저장하지 않고 인스턴스 생성
            comment.user = request.user
            comment.post = post
            comment.save() # 유저와 피드백 연결 후 디비에 저장
            messages.success(request, '새 댓글을 저장했습니다.')

            return redirect(comment.post)
    else:
        # 포스트 요청이 아닐 경우 빈 폼 생성
        form = CommentForm()

    return render(request, 'feedback/comment_form.html', {
        'form' : form,
        }) # 포스트 요청이 아닐 경우 빈 폼으로 페이지 렌더링

@login_required
def comment_delete(request, post_pk, comment_pk):
    # 피드백 디테일 내 댓글 지우기
    comment = get_object_or_404(FeedbackComment, pk=comment_pk) # 해당 댓글의 인스턴스 생성

    if comment.user != request.user:
        # 댓글 작성자와 현재 유저가 다를 경우
        messages.warning(request, '작성자만 삭제할 수 있습니다.')
    else:
        # 작성자와 동일할 경우
        comment.delete() # 댓글 삭제
        messages.success(request, '댓글을 삭제했습니다.')

    return redirect(comment.post)

@login_required
def comment_edit(request, post_pk, comment_pk):
    # 피드백 디테일 내 댓글 수정
    comment = get_object_or_404(FeedbackComment, pk=comment_pk) # 해당 댓글의 인스턴스 생성

    if comment.user != request.user:
        # 댓글 작성자와 현재 유저가 다를 경우 해당 피드백페이지로 리다이렉트
        messages.warning(request, '댓글 작성자만 수정할 수 있습니다.')
        return reditrect(comment.post)

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = CommentForm(request.POST, request.FILES, instance=comment) # 받아온 데이터와 현재 댓글 인스턴스를 통해 폼 인스턴스 생성

        if form.is_valid():
            comment = form.save() # 수정된 댓글 저장
            messages.success(request, '기존 댓글을 수정헀습니다.')
            return redirect(comment.post)
    else:
        form = CommentForm(instance=comment) # 현재 댓글 인스턴스 정보를 가진 폼 인스턴스 생성

    return render(request, 'feedback/comment_form.html', {
        'form':form,
        })
