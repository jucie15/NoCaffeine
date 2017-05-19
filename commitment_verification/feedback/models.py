from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.shortcuts import reverse


class FeedbackPost(models.Model):
    # 피드백 게시판 POST 모델
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feedback_post_set') # 글쓴이
    title = models.CharField(max_length=128,
        validators=[MinLengthValidator(5)],
        verbose_name='제목') # 제목
    content = models.TextField(verbose_name='내용') # 내용
    hits = models.IntegerField(default=0) # 조회수
    created_at = models.DateTimeField(auto_now_add=True) # 게시일
    updated_at = models.DateTimeField(auto_now=True) # 수정일


    class Meta:
        ordering = ['-id'] # 최신글 순서로 정렬

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('feedback:post_detail', args = [self.pk])

    def hit_count(self):
        # 조회수 증가 함수
        self.hits += 1
        self.save()

class FeedbackComment(models.Model):
    # 각 피드백 글에 대한 댓글 모델
    post = models.ForeignKey(FeedbackPost, related_name='feedback_comment_set') # 해당 글 1:N 관계 설정
    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 해당 댓글을 쓴 유저와 1:N 관계 설정
    message = models.TextField() # 댓글 내용

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "{}의 댓글 {}".format(self.post, self.message)
