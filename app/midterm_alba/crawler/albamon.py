import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pickle

class AlbamonCrawler :
    def __init__(self) :
        self.base_url = 'https://www.albamon.com/'
        self.detail_source_list = [] #[(url, source)]
        
    def norm_age(self, age) :
        if age == "무관" :
            return (None, None)
        l = age.split()[0]
        l = int(l[:l.find('세')])
        r = age.split()[2]
        r = int(r[:r.find('세')])
        return (l, r)

    def norm_pay(self, pay) :
        return pay[:-1].replace(',', '')

    def norm_worktime(self, worktime) :
        if worktime.startswith('시간협의') : 
            return (None, None)
        else :
            (l, r) = (worktime[:5], worktime[6:11])
            l = int(l[:l.find(':')])*60 + int(l[l.find(':')+1:])
            r = int(r[:r.find(':')])*60 + int(r[r.find(':')+1:])
            return (l,r)

    def get_info_from_source(self, alba_site_number, source) :
        '''
        source : 주소 url에 request를 날린 text
        return : dict
                {
                'sex' : str, '남자', '여자', '무관'
                'age' : tuple(int, int), (낮은 나이, 높은 나이), 없으면(None, None)
                'address' : str
                'pay' : int
                'type_of_pay' : str, '월급', '일급', etc
                'worktime' : tuple(int, int), (시작 시간의 분, 끝 시간의 분), 없으면(None, None)
                'alba_site_name' : str
                'alba_site_number' : str
                }
        '''
        soup = BeautifulSoup(source, 'html.parser')
        condition_selector = '#allcontent > div.viewContent.viewRecruitType > div.viewTypeFullWidth > div.conditionInfo.verticalLine > div.column.column_620.infoBox > div.recruitCondition > div > table > tbody'
        info = {}
        for tr_tag in soup.select(condition_selector)[0].find_all("tr") :
            if tr_tag.find("th").text == "성별" :
                info['sex'] = tr_tag.find("span").text
            if tr_tag.find("th").text == "연령" :
                info['age'] = self.norm_age(tr_tag.find("span").text)
        info['address']= soup.select(
            f'div.viewContent.viewRecruitType > div.viweTab > div.tabItem_workArea > div.workAddr > span')[0].text
        info['pay']= self.norm_pay(soup.select(
            f'div.workCondition > div.viewTable > table > tbody > tr:nth-child(1) > td > div.payInfoBox > span.monthPay')[0].text)
        info['type_of_pay']= soup.select(
            f'div.workCondition > div.viewTable > table > tbody > tr:nth-child(1) > td > div.payInfoBox > span.textPoint > strong')[0].text
        info['worktime']= self.norm_worktime(soup.select(
        f'div.workCondition > div.viewTable > table > tbody > tr:nth-child(4) > td > span')[0].text.strip())
        info['alba_site_name'] = 'albamon'
        info['alba_site_number'] = alba_site_number
        return info
    
    def crawl_from_site(self) :
        PAGE_NUM = 1
        SLEEP_TIME = 5.0

        #PAGE_NUM만큼 URL 리스트를 뽑는다.
        #알바몬은 한 페이지 당 20개
        detail_url_list = []
        for page in range(1, 1+PAGE_NUM) :
            time.sleep(SLEEP_TIME)
            source = requests.get(self.base_url + f'/list/gi/mon_gi_tot_list.asp?page={page}').text
            soup = BeautifulSoup(source, 'html.parser')
        
            for i in range(5) :
            #for i in range(20) :
                detail_url_list.append(soup.select(f'td.subject > div.subWrap > p.cName > a')[i]['href'])

        #URL 리스트들에서 소스를 얻어낸다
        for i in detail_url_list :
            self.detail_source_list.append((i, requests.get(self.base_url + i).text))
            time.sleep(SLEEP_TIME)
            
        #소스들을 피클로 저장
        save_pkl_file_name = 'albamon_source_' + str(datetime.now().isoformat(sep='_')).replace(':','-') +'.pkl'
        with open(save_pkl_file_name, 'wb') as f:
            pickle.dump(self.detail_source_list, f)
            
    def get_alba_site_number_form_url(self, url) :
        end_pos = url.find('&mj_stat')
        return url[26:end_pos]
        
    def get_info_list(self) :
        # open_pkl_file_name = 'C:\\Users\\Green\\Desktop\\2020_hongik_project\\app\\midterm_alba\\crawler\\albamon_source_2020-05-21_14-09-07.593744.pkl'
        # with open(open_pkl_file_name, 'rb') as f:
        #     self.detail_source_list = pickle.load(f)
        self.crawl_from_site()
        result = []
        for i in self.detail_source_list :
            result.append(self.get_info_from_source(self.get_alba_site_number_form_url(i[0]), i[1]))
        return result
