# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 12:46:06 2018

@author: Amanda Pratama Putra

#dependency :
pandas, selenium, time, threading, joblib
using python 2.7

the task of this script is to crawl the information from links (crawling directory) in parallel processing. 
The purpose of parallel processing is to increase the speed and performance of our robots and also to maximize the potential of CPU and Memory
"""

import numpy as np
import datetime
import time
import pandas as pd
from selenium import webdriver
import threading
from joblib import Parallel, delayed

##define the class for Hotels
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

##for parallel processing
def unwrap_self(arg, **kwarg):
    return CrawlParallelURL.scrape(*arg, **kwarg)

##depend with class hotel
#define the crawler class
class CrawlParallelURL:
    hotels = []
    result = []
    links = []
    drivers = {}
    delay = 3
    time = ""
    core = -1 #number of cores that will be used for parallel processing
    cIn = "" #date to crawl the room left
    mcIn = "" #default date in the hotel links from crawling directory
    driver_path = "" 

    def __init__(self, links=[], cIn = "2018-04-08",mcIn="2018-04-08", delay=10,core=-1,driver_path=""):
        self.delay = delay
        self.links = links
        self.core = core
        self.cIn = cIn
        self.mcIn = mcIn
        self.driver_path = driver_path

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
        #replace the default date in the link with the current date
        URL = URL.replace(self.mcIn,self.cIn)
        
        #configuration for chrome driver
        option = webdriver.ChromeOptions()
        chrome_prefs = {}
        option.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        option.set_headless()

        #activate the robot
        try:
            driver = self.drivers[threading.current_thread().name]
        except KeyError:
            self.drivers[threading.current_thread().name] = webdriver.Chrome(executable_path=self.driver_path,chrome_options=option)
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
            driver.quit() #close the robot


current_year = (datetime.datetime.now().strftime("%Y"))
current_month = (datetime.datetime.now().strftime("%m"))
current_day = (datetime.datetime.now().strftime("%d"))

tomorrow_year = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y")
tomorrow_month = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")
tomorrow_day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d")

#setup for driver
cur_driver_path = "D:\\1. Mandes\\MyCloud\\OneDrive\\Work\\python-crawl\\chromedriver.exe" #define the chrome driver path
out_dir_path = "D:\\1. Mandes\\MyCloud\\OneDrive\\Work\\" #define the directory excel crawling result
crawl_dir_path = "D:\\1. Mandes\\MyCloud\\OneDrive\\Work\\final_directory_bali_link.xlsx" #define the crawling directory path that have the links of the hotel

cIn = current_year+'-'+current_month+'-'+current_day #get the current date

hotels = pd.read_excel(crawl_dir_path)

links = hotels.iloc[:]['link'].drop_duplicates() #get the links from crawling directory, make sure that the links are not duplicate

#assume, the number of links is not bigger than 5.600. We divide the crawling to several loops, to make sure that the memory is not leak
for i in range(1,15):
    a = (i-1)*400
    b = i*400-1
    print(a," - ",b) #see the progress
    links_ = links[a:b] #define the index of links to process within the loop
    testing1 = CrawlParallelURL(links_,core=4,cIn=cIn,mcIn="2018-07-08",driver_path=cur_driver_path) #define the objects
    testing1.start_crawl() #call the function to start crawling
    result=testing1.result.drop_duplicates() #get the result
    result.to_excel(out_dir_path+"loop "+str(i)+" master_resBali_"+cIn+".xlsx",encoding='utf-8') #export the data to excel data format
