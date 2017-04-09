import os
from pledge.models import *
from django.conf import settings


ROOT = lambda *args: os.path.join(settings.BASE_DIR, 'pledge', 'static', 'pledge', 'txt', *args)

def congressman_db_create():
    # 크롤링 해놓은 데이터를 불러와 디비에 저장
    with open(ROOT("congressman_detail.txt"), "rt") as f:
        mem_detail_list = f.read().split('\n')


    img_path = os.path.join('pledge', 'img', 'congressman') # 프로필 사진 경로 설정
    mem_dic = {} # 각 정보를 저장할 사전형 선언

    for mem_detail in mem_detail_list:
        '''
            각 의원별로 개행시캬 놓았기에 개행을 기준하여 디비에 저장한다.
        '''
        if mem_detail != '':
            mem_index = mem_detail.split(':')[0]
            mem_value = mem_detail.split(':')[1]
            mem_dic[mem_index] = mem_value
        else:
            if mem_dic:
                # 의원 데이터가 있을 경우
                congressman = CongressMan() # 모델 인스턴스 생성
                congressman.name = mem_dic['이름']
                congressman.profile_image_path = img_path + '/' + mem_dic['id'] + '.jpg'
                congressman.description = mem_dic['약력']
                congressman.party = mem_dic['정당']
                congressman.constituency = mem_dic['선거구']
                congressman.email = mem_dic['이메일']
                mem_dic = {} # 다음 의원을 위해 변수 초기화
                congressman.save() # 디비에 저장



#     for name, addr, latlng in zip(name_list,addr_list,latlng_list):

#         lat = latlng.split(',')[0]
#         lng = latlng.split(',')[1]
#         sch = School()

#         sch.name = name
#         sch.address = addr
#         sch.save()

#         sch_loc = SchoolLocation()
#         print("sch_loc1")
#         sch_loc.school = sch
#         print("sch_loc2")

#         sch_loc.point = 'POINT(' + lng +' ' + lat + ')'
#         print(sch_loc.point)

#         sch_loc.save()

# school_db_create()
