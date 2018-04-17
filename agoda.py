# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 11:25:47 2018

@author: Putra
"""
import time
import pandas as pd
import datetime
from selenium import webdriver

class Hotel(object):
    name = ""
    address = ""
    stars = ""
    price = 0
    score = 0
    city = ""
    usefulInf = ""
    jKamar = ""
    sKamar = ""
    link = ""
    
    def __init__(self, name="Unknown name", address="unknown addr", stars="unknown star",price=0,score=0,city="unknown city",usefulInf="not Found",jKamar="unknown",sKamar="unknown",link="unknown"):
        self.name = name
        self.address = address
        self.stars = stars
        self.price = price
        self.score = score
        self.city = city
        self.usefulInf = usefulInf
        self.jKamar = jKamar
        self.sKamar = sKamar
        self.link = link
    
    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'stars':self.stars,
            'score':self.score,
            'city':self.city,
            'usefulInf':self.usefulInf,
            'jKamar':self.jKamar,
            'sKamar':self.sKamar,
            'link':self.link
        }


class CrawlHotelList(object):
    hotels = []
    resData = []
    cIn = ""
    cOut = ""
    looping = 100
    city = "8691"
    url = 'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?languageId=1&pageTypeId=1&origin=ID&locale=en-US&cid=-1&aid=130589&currencyCode=IDR&htmlLanguage=en-us&cultureInfoName=en-US&prid=0&rooms=1&adults=2&children=0&tabId=1&priceCur=IDR&checkIn='
    
    def __init__(self, cIn="", cOut="", city="8691",looping=100):
        self.cIn = cIn
        self.cOut = cOut
        self.city = city
        self.looping = looping
    
    def crawl(self,detail=1,type="city",delay=2):
        url = self.url+self.cIn+'&checkOut='+self.cOut+'&'+type+'='+self.city
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        
        firefoxOptions = webdriver.FirefoxOptions()
        firefoxOptions.set_headless()
        
        
        print("Setup Driver")
        
        driver = webdriver.Firefox(executable_path='D:\\Python Project\\geckodriver.exe',firefox_profile=firefox_profile,firefox_options=firefoxOptions)
        #driver = webdriver.Firefox(executable_path='D:\\Python_Project\\gecko\\geckodriver.exe',firefox_profile=firefox_profile,firefox_options=firefoxOptions)
        driver.get(url)
        
        current_window = driver.current_window_handle
        
        for loop in range(0,self.looping):
            print("loop number-"+str(loop+1))
            time.sleep(2)
            
            SCROLL_PAUSE_TIME = 0.2
            new_height= 0
            
            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollBy(0, 120);")
            
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
            
                # Calculate new scroll height and compare with last scroll height
                new_height = new_height+120
                if new_height >= last_height:
                    break
                last_height = driver.execute_script("return document.body.scrollHeight")
            
            hotel_item = driver.find_elements_by_class_name('hotel-item-box')
            
            start_time = time.time()
            
            for h in hotel_item:
                hotel_name = h.find_element_by_class_name('hotel-name')
                hotel_name_ = h.find_element_by_class_name('hotel-name').text
                print("crawl: %s" % hotel_name.text)
                link = hotel_name.get_attribute("href")
                hotel_addr = h.find_elements_by_class_name('areacity-name-text')
                if(len(hotel_addr)>0):
                    hotel_addr = hotel_addr[0].text
                
                hotel_score = h.find_elements_by_class_name('ReviewScore-Number')
                if len(hotel_score)>0:
                    hotel_score = hotel_score[0].text
                else:
                    hotel_score = "-"
                
                hotel_stars = driver.find_element_by_class_name('star-rating')
                star_temp = hotel_stars.find_elements_by_tag_name('i')
                if len(star_temp)>0:
                    star_temp = star_temp[0].get_attribute("class")
                else:
                    star_temp = "-"
                
                
                if detail==1:
                    print("get details information")
                    ##start click item
                    hotel_name.click()
                    time.sleep(delay)
                    new_window = [window for window in driver.window_handles if window != current_window][0]
                    # Switch to new window/tab
                    driver.switch_to.window(new_window)
                    time.sleep(1)
                    
                    show_more = driver.find_elements_by_class_name('show-more')
                    for s in show_more:
                        try:  
                            s.click()
                        except Exception:
                            pass
                    
                    name = driver.find_elements_by_class_name('hotel-header-info-name-text')
                    full_address = driver.find_elements_by_class_name('hotel-header-info-address-text')
                    sisa = driver.find_elements_by_class_name('RoomGrid-titleCountersText')
                    active_link = driver.current_url
                    
                    try:
                        usefulInf = driver.find_element_by_id('abouthotel-usefulinfo').get_attribute('innerHTML')
                    except Exception:
                        usefulInf = "Not Found"
                    
                    
                    if usefulInf.find("Number of rooms :&nbsp;<strong>")!=-1:
                        startIndex=usefulInf.find("Number of rooms :&nbsp;<strong>")+31
                        elem_1 = usefulInf[startIndex:]
                        endIndex=elem_1.find("</strong>")
                        elem_2 = elem_1[:endIndex]
                        jKamar = elem_2
                    else:
                        jKamar = "Not Found"
                    
                    if(len(full_address)>0):
                        full_address = full_address[0].text
                    else:
                        full_address = "unknown"
                    
                    if(len(sisa)>0):
                        sisa = sisa[0].text
                    else:
                        sisa = "unknown"
                        
                    try:
                        self.hotels.append(Hotel(name=hotel_name_,address=hotel_addr+" "+full_address,stars=star_temp,score=hotel_score,city=self.city,sKamar=sisa,jKamar=jKamar,usefulInf=usefulInf,link=active_link))
                    except Exception:
                        print("failed")
                        self.hotels.append(Hotel(name=hotel_name_,address=hotel_addr,stars=star_temp,score=hotel_score,city=self.city,link=link))
                        
                    #close new tab
                    driver.close()
                    time.sleep(2)
                    # Switch to initial window/tab
                    driver.switch_to.window(current_window)
                else:
                    self.hotels.append(Hotel(name=hotel_name_,address=hotel_addr,stars=star_temp,score=hotel_score,city=self.city,link=link))
                           
                ##stop
                
                
            print("--- %s seconds ---" % (time.time() - start_time))
            
            
            button_next = driver.find_elements_by_class_name('pagination2__next')
            if len(button_next)>0:
                button_next = button_next[0]
            else:
                break
            
            driver.execute_script("arguments[0].click();",button_next)
            
        driver.close()
        print('close driver')        
        ##return
        self.resData = pd.DataFrame.from_records([hotel.to_dict() for hotel in self.hotels])
    
    def export(self,path):
        self.resData.to_csv("path", encoding='utf-8')

bali = '17193'
jakarta = '8691'
denpasar = '31530'
ubud = '26638'

current_year = (datetime.datetime.now().strftime("%Y"))
current_month = (datetime.datetime.now().strftime("%m"))
current_day = (datetime.datetime.now().strftime("%d"))

tomorrow_year = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y")
tomorrow_month = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")
tomorrow_day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d")

cIn = current_year+'-'+current_month+'-'+current_day
cOut = tomorrow_year+'-'+tomorrow_month+'-'+tomorrow_day

#cIn = '2018-07-08'
#cOut = '2018-07-09'

cek = CrawlHotelList(cIn=cIn,cOut=cOut,city=jakarta,looping=200)
cek.crawl(detail=2,type="city")
result_jkt = cek.resData.drop_duplicates()
result_jkt.to_csv("resJKT"+cIn+".csv", encoding='utf-8')
    
cek2 = CrawlHotelList(cIn=cIn,cOut=cOut,city=bali,looping=200)
cek2.crawl(detail=2,type="city")
result_bali = cek2.resData.drop_duplicates()
result_bali.to_csv("resBALI_"+cIn+".csv",sep=";",encoding='utf-8')

cek3 = CrawlHotelList(cIn=cIn,cOut=cOut,city=denpasar,looping=200)
cek3.crawl(detail=1,type="area",delay=3)
result_denpasar = cek3.resData.drop_duplicates()
result_denpasar.to_excel("master_resdsp_"+cIn+"April.xlsx",encoding='utf-8')
links = result_denpasar.iloc[:]["link"].drop_duplicates()
