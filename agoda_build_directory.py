# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 11:25:47 2018

@author: Amanda Pratama Putra
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


class CrawlHotelListFast(object):
    hotels = []
    resData = []
    cIn = ""
    cOut = ""
    looping = 100
    city = "8691"
    url = 'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?languageId=1&pageTypeId=1&origin=ID&locale=en-US&cid=-1&aid=130589&currencyCode=IDR&htmlLanguage=en-us&cultureInfoName=en-US&prid=0&rooms=1&adults=2&children=0&tabId=1&priceCur=IDR&checkIn='
    driver_path = ''

    def __init__(self, cIn="", cOut="", city="8691",looping=100,driver_path=''):
        self.cIn = cIn
        self.cOut = cOut
        self.city = city
        self.looping = looping
        self.driver_path = driver_path
    
    def crawl(self,detail=1,type="city",delay=2):
        url = self.url+self.cIn+'&checkOut='+self.cOut+'&'+type+'='+self.city
        
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        
        firefoxOptions = webdriver.FirefoxOptions()
        firefoxOptions.set_headless()
                
        print("Setup Driver")
        
        driver = webdriver.Firefox(executable_path=self.driver_path,firefox_profile=firefox_profile,firefox_options=firefoxOptions)
        driver.maximize_window()
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
            
            hotel_items = driver.find_elements_by_class_name('ssr-search-result')
            
            start_time = time.time()
            
            for h in hotel_items:
                try:
                    hotel_name_ = h.find_element_by_class_name('hotel-name').text
                except Exception:                     
                    hotel_name_ = "unknown"
                    
                print("crawl: %s" % hotel_name_)
                
                try:
                    link = h.find_element_by_css_selector('[class*="property-card ssr-search-result-item"]').get_attribute("href")
                except Exception:
                    link = 'Not Found'
                    
                hotel_addr = h.find_elements_by_class_name('areacity-name-text')
                if(len(hotel_addr)>0):
                    hotel_addr = hotel_addr[0].text
                else:
                    hotel_addr = 'Not Found'
                
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


#configuration
#for some purpose, we decided to use firefox instead of chrome to make crawling directory
firefox_driver_path = 'D:\\Python Project\\geckodriver.exe' #setup the path of gecko driver

city_code = '17193' #agoda city code for Bali, Indonesia
cIn = '2018-07-08' #set the default check-in date 
cOut = '2018-07-09' #set the default check-out date
output_path = "resBALI_"+cIn+".xlsx"
looping_ = 200 #we assume that the number of page are less than 200


#running
cek4 = CrawlHotelListFast(cIn=cIn,cOut=cOut,city=city_code,looping=looping_,driver_path=firefox_driver_path) #build the objects
cek4.crawl(detail=2,type="city") #start the crawling process
result_bali2 = cek4.resData.drop_duplicates(subset=['link','name']) ##to make sure that there are no duplicate
result_bali2.to_excel(output_path,encoding='utf-8') #import to excel
