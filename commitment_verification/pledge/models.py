from django.db import models



class CongressMan(models.Model):
    # 국회의원 모델
    name = models.CharField(max_length=32) #국회의원 이름
    # profile_image = models.ImageField() # 프로필 사진
    description = models.TextField(max_length=512, null=True, blank=True) # 추가 정보
    party = models.CharField(max_length=32, null=True, blank=True) # 정당
    constituency = models.CharField(max_length=32, null=True, blank=True) # 선거구
    email = models.CharField(max_length=64, null=True, blank=True) # 이메일 주소
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True) # 업데이트 날짜

    def __str__(self):
        return self.name


class Pledge(models.Model):
    congressman = models.ForeignKey(CongressMan) # 국회의원 모델과 1toN 관계 설정
    name = models.CharField(max_length=32) # 공약 이름
    status = models.IntegerField(default=0) # 공약 상태
    event_status = models.BooleanField(default=False) # 공약 상태변경 이벤트 활성화 상태
    description = models.TextField(max_length=1024) # 공약에 대한 추가 설명
    created_at = models.DateTimeField(auto_now_add=True) # 공약 날짜


