# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 14:49:56 2018

@author: Putra
"""
import numpy as np
import datetime
import time
import pandas as pd
from selenium import webdriver
import threading
from joblib import Parallel, delayed

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
    desc = ""
    opened = ""
    
    def __init__(self, name="Unknown name", address="unknown addr", stars="unknown star",price=0,score=0,city="unknown city",usefulInf="not Found",jKamar="unknown",sKamar="unknown",link="unknown",desc="unknown",opened="unknown"):
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
        self.desc = desc
        self.opened = opened
    
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
            'link':self.link,
            'desc':self.desc,
            'opened':self.opened
        }


def unwrap_self(arg, **kwarg):
    return CrawlParallelURL.scrape(*arg, **kwarg)

##depend with class hotel
class CrawlParallelURL:
    hotels = []
    result = []
    links = []
    drivers = {}
    delay = 3
    time = ""    
    core = -1
    cIn = ""
    
    def __init__(self, links=[], cIn = "2018-04-08", delay=10,core=-1):
        self.delay = delay
        self.links = links
        self.core = core
        self.cIn = cIn
    
    def crawl_data(self,driver):
        try:     
            active_link = driver.current_url
            try:
                name = driver.find_element_by_class_name('hotel-header-info-name-text').text
            except Exception:
                name = "Not Found"
            
            print("crawl: "+name)
            
            try:
                full_address = driver.find_element_by_class_name('hotel-header-info-address-text').text
            except Exception:
                full_address = "Not Found"

            try:
                header = driver.find_element_by_class_name('review-branding-right')
                score = header.find_element_by_class_name('ReviewScore-Number').text
            except Exception:
                score = "Not Found"
            
            try:
                sisa = driver.find_element_by_class_name('RoomGrid-titleCountersText').text
            except Exception:
                sisa = "Not Found"
                        
            try:
                desc = driver.find_element_by_class_name('hotel-desc').text
            except Exception:
                desc = "Not Found"
            
            try:
                usefulInf = driver.find_element_by_id('abouthotel-usefulinfo').get_attribute('innerHTML')
            except Exception:
                usefulInf = "Not Found"
            
            try:
                usefulInf = driver.find_element_by_id('abouthotel-usefulinfo').get_attribute('innerHTML')
            except Exception:
                usefulInf = "Not Found"
            
            if usefulInf.find("Year property opened:&nbsp;<strong>")!=-1:
                startIndex=usefulInf.find("Year property opened:&nbsp;<strong>")+35
                elem_1 = usefulInf[startIndex:]
                endIndex=elem_1.find("</strong>")
                elem_2 = elem_1[:endIndex]
                opened = elem_2
            else:
                opened = "Not Found"
            
            if usefulInf.find("Number of rooms :&nbsp;<strong>")!=-1:
                startIndex=usefulInf.find("Number of rooms :&nbsp;<strong>")+31
                elem_1 = usefulInf[startIndex:]
                endIndex=elem_1.find("</strong>")
                elem_2 = elem_1[:endIndex]
                jKamar = elem_2
            else:
                jKamar = "Not Found"
                        
            hotel=Hotel(name=name,address=full_address,link=active_link,usefulInf=usefulInf,jKamar=jKamar,sKamar=sisa,score=score,desc=desc,opened=opened)
            self.hotels.append(hotel)
            
        except Exception:
            print("FAILED")
            pass
    
    def scrape(self,URL):
        URL = URL.replace('2018-04-09',self.cIn)
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
                
        firefoxOptions = webdriver.FirefoxOptions()
        firefoxOptions.set_headless()
    
        try:
            driver = self.drivers[threading.current_thread().name]
        except KeyError:
            #self.drivers[threading.current_thread().name] = webdriver.Firefox(executable_path='D:\\Python_Project\\gecko\\geckodriver.exe',firefox_profile=firefox_profile,firefox_options=firefoxOptions)
            self.drivers[threading.current_thread().name] = webdriver.Firefox(executable_path='D:\\Python Project\\geckodriver.exe',firefox_profile=firefox_profile,firefox_options=firefoxOptions)
            driver = self.drivers[threading.current_thread().name]
        driver.get(URL)
        self.crawl_data(driver)
        
    def start_crawl(self):
        start_time = time.time()
        
        Parallel(n_jobs=self.core, backend="threading")(delayed(unwrap_self)(URL) for URL in zip([self]*len(self.links),self.links))
        
        print("--- %s seconds ---" % (time.time() - start_time))    
        self.time = (time.time() - start_time)
        
        self.result = pd.DataFrame.from_records([hotel.to_dict() for hotel in self.hotels])

        for driver in self.drivers.values():
            driver.quit()        



current_year = (datetime.datetime.now().strftime("%Y"))
current_month = (datetime.datetime.now().strftime("%m"))
current_day = (datetime.datetime.now().strftime("%d"))

tomorrow_year = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y")
tomorrow_month = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")
tomorrow_day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d")

cIn = current_year+'-'+current_month+'-'+current_day
cOut = tomorrow_year+'-'+tomorrow_month+'-'+tomorrow_day

hotels = pd.read_excel('D:\\1. Mandes\\MyCloud\\OneDrive\\Work\\master_resdsp_2018-04-09April.xlsx')
links = hotels.iloc[:]['link'].drop_duplicates()

testing1 = CrawlParallelURL(links,core=2,cIn=cIn)
testing1.start_crawl()
result=testing1.result.drop_duplicates()
result.to_excel("master_resdsp_"+cIn+"April full.xlsx",encoding='utf-8')
