from django.http import HttpResponse
from .models import Alba
from .crawler.albamon import AlbamonCrawler

def make_db(request) :
    for a in Alba.objects.all():
        a.delete()

    albamon_crawler = AlbamonCrawler()
    albamon_info_result = albamon_crawler.get_info_list()
    for info in albamon_info_result :
        Alba.objects.create(
            sex = info['sex'],
            age_lower_bound = info['age'][0],
            age_upper_bound = info['age'][1],
            address = info['address'],
            pay = info['pay'],
            worktime_start = int(info['worktime'][0][:2])*60 + int(info['worktime'][0][3:]),
            worktime_end = int(info['worktime'][1][:2])*60 + int(info['worktime'][1][3:]),
            alba_site_name = info['alba_site_name'],
            alba_site_number = info['alba_site_number']
        )
    return HttpResponse(str(albamon_info_result))
