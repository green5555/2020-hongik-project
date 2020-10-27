import requests
from bs4 import BeautifulSoup, NavigableString
import time
from datetime import datetime
from itertools import chain 
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
            try :
                source = requests.get(self.base_url + f'/job/Main.asp?page={page}').text
                soup = BeautifulSoup(source, 'html.parser')
                detail_url_list.append(soup.select(
                        '#NormalInfo > table > tbody > tr.firstLine > td.title > span > a.applBtn.blankView')[0]['href'])
                print(f'successfully crawl page {page}')
            except Exception as e:
                print(f'Fail to crawl page {page} : {e}')

            for i in range(3, 7, 2):
            # for i in range(3, 101, 2):
                try :
                    detail_url_list.append(soup.select(
                        f'#NormalInfo > table > tbody > tr:nth-child({i}) > td.title > span > a.applBtn.blankView')[0]['href'])
                except Exception as e:
                    print(f'Fail to crawl page {page} - {i}th content : {e}')

        for i in detail_url_list :
            try :
                self.detail_source_list.append((i, requests.get(self.base_url + i).text))
            except Exception as e:
                print(f'Fail to request detail url {i} - {e}')
            time.sleep(SLEEP_TIME)
            

    def norm_sex(self, sex) :
        if sex.count('무관') :
            return '무관'
        return sex

    def norm_age(self, age) :
        if age.count('무관') :
            return (0, 200) 
        s_age = age.split()
        l = s_age[0]
        l = int(l[:l.find('세')])
        if s_age[2] == '이전' :
            r = 150
        else :
            r = s_age[2]
            r = int(r[:r.find('세')])
        return (l, r)

    def norm_worktime(self, worktime) :
        if worktime.startswith('시간협의') : 
            return (None, None)
        else :
            (l,r) = (worktime[:5], worktime[worktime.find('~')+1:worktime.find('~')+5])
            l = int(l[:l.find(':')])*60 + int(l[l.find(':')+1:])
            r = int(r[:r.find(':')])*60 + int(r[r.find(':')+1:])
            return (l,r)
        
    def parse_pay_tag(self, tag) :
        return (tag.i.text, tag.strong.text.replace(',', ''))

    def get_text_except_child_from_tag(self, tag) :
        return [element for element in tag if isinstance(element, NavigableString)][0].strip()

    def get_info_from_source(self, alba_site_number, source) :
        cond_selector = [
            '#DetailView > div.detail-content > div:nth-child(2) > div > div.detail-content__condition--first > div.detail-content__condition-list',
            '#DetailView > div.detail-content > div:nth-child(2) > div > div.detail-content__condition--first > div.detail-content__condition-list.detail-content__list--last',
            '#InfoWork > div'
        ]
        
        soup = BeautifulSoup(source, 'html.parser')
        
        info = {}
        for selector in cond_selector:
            tags = soup.select(selector)[0].find_all('dl')
            for tag in tags :
                (dt, dd) = tag.dt.text, tag.dd.text
                if dt == '성별' :
                    info['sex'] = self.norm_sex(dd)
                if dt == '연령' :
                    info['age'] = self.norm_age(dd)
                if dt == '근무지주소' :
                    info['address'] = dd
                if dt == '급여' :
                    (info['type_of_pay'], info['pay']) = self.parse_pay_tag(tag.dd)
                if dt == '근무시간' :
                    info['worktime'] = self.norm_worktime(dd)
        info['alba_site_name'] = '알바천국'
        info['alba_site_number'] = alba_site_number[alba_site_number.find('adid=')+5:alba_site_number.find('&list')]
        return info


    def get_info_list(self) :
        self.crawl_from_site()
        result = []
        for i in self.detail_source_list :
            try :
                result.append(self.get_info_from_source(i[0], i[1]))
            except Exception as e:
                print(f'Fail to parse {i[1]} : {e}')
                pass
        return result