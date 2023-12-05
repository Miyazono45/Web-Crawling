import time
import re
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains



#User Input
# quer = input('whats your Searching = ')
# pricemin = input('what is min price = ')
# pricemax = input('what is max price = ')


urls = 'https://www.tokopedia.com/search?'

quer = 'VGA Graphic Card'
min = '10000000'
max = '11000000'
quer = re.sub(" ", "%20", quer)

driver = webdriver.Chrome()
driver.get(urls + f'&ob=3&pmax={max}&pmin={min}&q={quer}')

time.sleep(1.5)
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

primaryUrl = driver.current_url

page = 1

visited = []
def web_crawl(Url,page,mainUrl):
    global quer
    global urls
    # driver = webdriver.Chrome()
    print(f"crawling data in : {page} pages")
    time.sleep(1)
    soup =BeautifulSoup(driver.page_source, 'html.parser')
    if Url in visited or soup.find(text="Oops, produk nggak ditemukan"):
          return
    visited.append(Url)
    
    time.sleep(5)
    primary_item = soup.findAll('div', attrs={'class': 'css-1asz3by'})
    for i, sub_item in enumerate(primary_item):
    # Find Items on First Page
        item_name = sub_item.find(
            'div', attrs={'class': 'prd_link-product-name'}).text
        item_price = sub_item.find(
            'div', attrs={'class': 'prd_link-product-price'}).text
        item_link = sub_item.find(
           'a', attrs={'class': 'pcv3__info-content'}).get('href')
        print(i,item_name, item_price, item_link)   
        
        driver.get(item_link)
        if item_link not in visited:
             visited.append(item_link)
        else:
             return
        time.sleep(5)
       
        soup  =  BeautifulSoup(driver.page_source, 'html.parser')
        findStore = soup.find('a', attrs={'class': 'css-1sl4zpk'}).get('href')
        quer = re.sub(" ", "%20", quer)
        driver.implicitly_wait(10)
        driver.get(str('https://www.tokopedia.com' + findStore + f'?q={quer}&sort=10'))
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(5)
        prodinStore = soup.findAll('div',attrs={'class' : 'css-1asz3by'})
        for j, sub_item in enumerate(prodinStore):
            name = sub_item.find('div', attrs={'class':'prd_link-product-name'}).text
            price = sub_item.find('div', attrs={'class':'prd_link-product-price'}).text
            link = sub_item.find('a', attrs={'class':'pcv3__info-content'}).get('href')
            print(link)
            if link not in visited:
                 visited.append(link)
                 print(f'name = {name}, price = {price}, link = {link}')
            elif link in visited:
                 print('data is Duplicate')     
    page += 1
    newurl = mainUrl + f'&page={page}'
    print(newurl)
    driver.get(newurl)
    web_crawl(newurl,page,primaryUrl)

web_crawl(primaryUrl,page,primaryUrl)
print(visited)
