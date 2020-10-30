from django.db import models

from django.utils import timezone

class AlbaInfo(models.Model):

    '''
    sex : 성별 (남자 or 여자 or 무관)
    age_lower_bound : 최소 나이 (없을시 0)
    age_upper_bound : 최대 나이 (없을시 200)
    address : 주소
    type_of_pay : 월급 or 일급 or 시급 ...
    worktime_start : 근무 시작 시간 (정수 : 시 * 60 + 분)
    worktime_end : 근무 끝나는 시간 (정수 : 시 * 60 + 분)
    alba_site_name : '알바천국' or ...
    alba_stie_number : 주소 고유 번호
    '''
    
    sex = models.CharField(max_length = 2, null=True)
    age_lower_bound = models.PositiveSmallIntegerField(null=True)
    age_upper_bound = models.PositiveSmallIntegerField(null=True)
    address = models.CharField(max_length = 100, null=True)
    pay = models.PositiveIntegerField(null=True)
    type_of_pay = models.CharField(max_length = 5, null=True)
    worktime_start = models.PositiveSmallIntegerField(null=True)
    worktime_end = models.PositiveSmallIntegerField(null=True)
    alba_site_name = models.CharField(max_length = 10, null=True)
    alba_site_number = models.CharField(max_length = 20, null=True)

    def __str__(self) :
        return self.alba_site_name + ' ' + self.alba_site_number