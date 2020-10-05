import requests
from bs4 import BeautifulSoup, NavigableString
import time
from datetime import datetime
import pickle

class AlbaheavenCrawler :
    def __init__(self) :
        self.base_url = 'http://www.alba.co.kr'
        self.detail_source_list = [] #[(url, source)]
        
    def crawl_from_site(self) :
        PAGE_NUM = 1
        SLEEP_TIME = 5.0

        detail_url_list = []
        for page in range(1, 1+PAGE_NUM) :
            time.sleep(SLEEP_TIME)
            source = requests.get(self.base_url + f'/job/Main.asp?page={page}').text
            soup = BeautifulSoup(source, 'html.parser')
            detail_url_list.append(soup.select(
                    '#NormalInfo > table > tbody > tr.firstLine > td.title > span > a.applBtn.blankView')[0]['href'])
            for i in range(3, 10, 2):
            #for i in range(3, 101, 2) :
                detail_url_list.append(soup.select(
                    f'#NormalInfo > table > tbody > tr:nth-child({i}) > td.title > span > a.applBtn.blankView')[0]['href'])

        for i in detail_url_list :
            self.detail_source_list.append((i, requests.get(self.base_url + i).text))
            time.sleep(SLEEP_TIME)

    def norm_sex(self, sex) :
        if sex == '성별무관' :
            return '무관'
        return sex

    def norm_age(self, age) :
        if age == "연령무관" :
            return (None, None)
        s_age = age.split()
        l = s_age[0]
        l = int(l[:l.find('세')])
        if s_age[2] == '이전' :
            r = 150
        else :
            r = s_age[2]
            r = int(r[:r.find('세')])
        return (l, r)

    def norm_pay(self, pay) :
        return pay[:-1].replace(',', '')

    def norm_worktime(self, worktime) :
        if worktime.startswith('시간협의') : 
            return (None, None)
        else :
            (l,r) = (worktime[:5], worktime[7:13])
            l = int(l[:l.find(':')])*60 + int(l[l.find(':')+1:])
            r = int(r[:r.find(':')])*60 + int(r[r.find(':')+1:])
            return (l,r)

    def get_text_except_child_from_tag(self, tag) :
        return [element for element in tag if isinstance(element, NavigableString)][0].strip()

    def get_info_from_source(self, alba_site_number, source) :
        '''
        source : 주소 url에 request를 날린 text
        return : dict
                {
                'sex' : str, '남자', '여자', '무관'
                'age' : tuple(int, int), (낮은 나이, 높은 나이), 없으면 None
                'address' : str
                'pay' : int
                'type_of_pay' : str, '월급', '일급', etc
                'worktime' : tuple(int, int), (시작 시간의 분, 끝 시간의 분)
                'alba_site_name' : str
                'alba_site_number' : str
                }
        '''
        soup = BeautifulSoup(source, 'html.parser')
        
        sex_selector = '#DetailView > div.wrapContents > div.infoSubSide > div.infoSub.infoJob > div.infoQualify > ul > li.sex'
        age_selector = '#DetailView > div.wrapContents > div.infoSubSide > div.infoSub.infoJob > div.infoQualify > ul > li.agetemp'
        week_selector = '#DetailView > div.wrapContents > div.infoSubSide > div.infoSide.infoJob > div > ul > li.workweekcd > a'
        address_selector = '#DetailView > div.wrapContents > div.infoSubSide > div.infoSide.infoJob > div > ul > li.address.divide > strong'
        pay_selector = '#DetailView > div.wrapContents > div.infoSubSide > div.infoSide.infoJob > div > ul > li.getPay.divide > p.pay > strong'
        type_of_pay_selector = '#DetailView > div.wrapContents > div.infoSubSide > div.infoSide.infoJob > div > ul > li.getPay.divide > p.pay > img'
        worktime_selector = '#DetailView > div.wrapContents > div.infoSubSide > div.infoSide.infoJob > div > ul > li.worktimecd'
        
        info = {}
        info['sex'] = self.norm_sex(self.get_text_except_child_from_tag(soup.select(sex_selector)[0]))
        info['age'] = self.norm_age(self.get_text_except_child_from_tag(soup.select(age_selector)[0]))
        info['address'] = self.get_text_except_child_from_tag(soup.select(address_selector)[0])
        info['pay'] = self.norm_pay(soup.select(pay_selector)[0].text)
        info['type_of_pay'] = soup.select(type_of_pay_selector)[0]['alt']
        info['worktime'] = self.norm_worktime(self.get_text_except_child_from_tag(soup.select(worktime_selector)[0]))
        info['alba_site_name'] = 'albaheaven'
        info['alba_site_number'] = alba_site_number[alba_site_number.find('adid=')+5:]
        print(info)
        return info

    def get_info_list(self) :
        self.crawl_from_site()
        result = []
        for i in self.detail_source_list :
            result.append(self.get_info_from_source(i[0], i[1]))
        return result