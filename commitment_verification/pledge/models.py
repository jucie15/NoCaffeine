from django.db import models
from django.conf import settings


class CongressMan(models.Model):
    # 국회의원 모델
    name = models.CharField(max_length=32) #국회의원 이름
    profile_image_path = models.CharField(max_length=512, null=True, blank=True) # 프로필 사진 저장 경로
    description = models.TextField(max_length=512, null=True, blank=True) # 추가 정보
    party = models.CharField(max_length=32, null=True, blank=True) # 정당
    constituency = models.CharField(max_length=32, null=True, blank=True) # 선거구
    email = models.CharField(max_length=64, null=True, blank=True) # 이메일 주소
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # 업데이트 날짜

    class Meta():
        ordering =['id']

    def __str__(self):
        return self.name

class Pledge(models.Model):
    # 공약 모델
    congressman = models.ForeignKey(CongressMan) # 국회의원 모델과 1toN 관계 설정
    title = models.CharField(max_length=32) # 공약 이름
    status = models.IntegerField(default=0) # 공약 상태
    # event_status = models.BooleanField(default=False) # 공약 상태변경 이벤트 활성화 상태
    description = models.TextField(max_length=1024) # 공약에 대한 추가 설명
    created_at = models.DateTimeField(auto_now_add=True) # 공약 날짜

    def __str__(self):
        return self.title

class Comment(models.Model):
    # 각 공약에 대한 댓글 모델
    pledge = models.ForeignKey(Pledge)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()

    class Meta:
        ordering = ['-id']

class PledgeEvent(models.Model):
    # 공약 상태 변경 이벤트 모델
    pledge = models.OneToOneField(Pledge) # 해당 공약과 1:1 관계 설정
    title = models.CharField(max_length=128) # 상태 변경 이벤트 이름
    status1_vote = models.IntegerField(default=0) # 미시행 투표 수
    status2_vote = models.IntegerField(default=0) # 시행중 투표 수
    status3_vote = models.IntegerField(default=0) # 시행완료 투표 수
    status4_vote = models.IntegerField(default=0) # 시행
    due_date = models.DateTimeField(auto_now_add=True) # 이벤트 마감 기한

    def __str__(self):
        return self.title

class PledgeEventPost(models.Model):
    # 공약 상태 변경 이벤트의 근거 제시 글 모델
    pledge_event = models.ForeignKey(PledgeEvent) # 해당 상태 변경 이벤트와 1toN 관계 설정
    author = models.ForeignKey(settings.AUTH_USER_MODEL) # 글쓴이, 유저 모델과 1toN 관계 설정
    title = models.CharField(max_length=128) # 글의 제목
    agreement_vote = models.IntegerField(default=0) # 찬성 투표 수
    opposition_vote = models.IntegerField(default=0) # 반대 투표 수
    description = models.TextField() # 글의 내용
    # 사진 여러개 포함?

    def __str__(self):
        return self.title


