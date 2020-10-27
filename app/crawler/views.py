from django.shortcuts import render

from django.http import HttpResponse
from .models import AlbaInfo
from .bot.albamon import AlbamonCrawler
from .bot.albaheaven import AlbaheavenCrawler

def insert_db(info_result):
    for info in info_result :
        try :
            AlbaInfo.objects.create(
                sex = info['sex'],
                age_lower_bound = info['age'][0],
                age_upper_bound = info['age'][1],
                address = info['address'],
                type_of_pay = info['type_of_pay'],
                pay = info['pay'],
                worktime_start = info['worktime'][0],
                worktime_end = info['worktime'][1],
                alba_site_name = info['alba_site_name'],
                alba_site_number = info['alba_site_number']
            )
        except :
            pass

def make_db(request) :
    for a in AlbaInfo.objects.all():
        a.delete()

    albaheaven_crawler =  AlbaheavenCrawler()
    albaheaven_info_result = albaheaven_crawler.get_info_list()
    insert_db(albaheaven_info_result)

    # albamon_crawler = AlbamonCrawler()
    # albamon_info_result = albamon_crawler.get_info_list()
    # insert_db(albamon_info_result)

    ret = 'Done!\n'
    ret += f'heaven : {len(albaheaven_info_result)}\n'
    return HttpResponse(str(albaheaven_info_result))

def crawling(request):
    return make_db(request)

