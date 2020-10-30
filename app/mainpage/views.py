from django.shortcuts import render
from django.http import HttpResponse
from crawler.models import AlbaInfo

# Create your views here.
def mainpage(request):
    albas = AlbaInfo.objects.order_by('-alba_site_number')[:20]
    print(albas)
    return render(request, 'index.html', {'albas' : albas})

#http://www.alba.co.kr/job/Detail.asp?adid=101945597