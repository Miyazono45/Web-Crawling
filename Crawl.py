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


urls = 'https://www.tokopedia.com'



driver = webdriver.Chrome()
driver.get(urls)
driver.find_element(By.TAG_NAME,'input')
data_input = driver.find_element(By.CLASS_NAME,'css-3017qm')
ActionChains(driver)\
    .send_keys_to_element(data_input,'VGA Graphic Card')\
    .key_down(Keys.RETURN)\
    .perform()
time.sleep(1.5)
driver.current_url

driver.find_element(By.CLASS_NAME,'css-1g467vj').click()
driver.find_elements(By.CLASS_NAME, 'e83okfj5')
driver.find_element(By.CSS_SELECTOR,'[data-item-text="Harga Terendah"]').click()
time.sleep(1)

driver.current_url

driver.find_element(By.CLASS_NAME, 'css-1cb34wj')
min = driver.find_element(By.NAME,'pmin')
ActionChains(driver)\
    .send_keys_to_element(min,'0')\
    .send_keys_to_element(min,'10000000')\
    .key_down(Keys.RETURN)\
    .perform()
time.sleep(1)
driver.find_element(By.CLASS_NAME, 'css-1cb34wj')
max = driver.find_element(By.NAME,'pmax')
ActionChains(driver)\
    .send_keys_to_element(max,'0')\
    .send_keys_to_element(max,'15000000')\
    .key_down(Keys.RETURN)\
    .perform()
time.sleep(1)
primaryUrl = driver.current_url

page = 1

visited = []
def web_crawl(Url,page,mainUrl):
    # driver = webdriver.Chrome()
    print(f"crawling data in : {page} pages")
    time.sleep(1)

    # Just A little bit more (I am Lazy)
    if Url in visited:
          return
    visited.append(Url)
    time.sleep(5)
    driver.get(Url)
    soup =BeautifulSoup(driver.page_source, 'html.parser')
    primary_item = soup.findAll('div', attrs={'class': 'css-1asz3by'})
    for i, sub_item in enumerate(primary_item):
    
        item_name = sub_item.find(
            'div', attrs={'class': 'prd_link-product-name'}).text
        item_price = sub_item.find(
            'div', attrs={'class': 'prd_link-product-price'}).text
        item_link = sub_item.find(
           'a', attrs={'class': 'pcv3__info-content'}).get('href')
            
        print(item_name, item_price, item_link)       
    page += 1
    newurl = mainUrl + f'&page={page}'
    print(newurl)
    web_crawl(newurl,page,primaryUrl)

   
        
    


web_crawl(primaryUrl,page,primaryUrl)
print(visited)
