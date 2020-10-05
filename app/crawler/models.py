from django.db import models

from django.utils import timezone

class AlbaInfo(models.Model):
    '''
    {
    'sex' : str, '남자', '여자', '무관'
    'age' : tuple(int, int), (낮은 나이, 높은 나이), 없으면 None
    'address' : str
    'pay' : int
    type_of_pay : str, '월급', '일급', etc
    worktime : tuple(str, str), ('00:00', '24:00') 포맷, 없으면 None
    }
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