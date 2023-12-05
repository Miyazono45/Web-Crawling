import time
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

class WebCrawl:
    def __init__(self, urls, search, pMax, pMin):
        self.URl = urls
        self.driver = None
        self.url_visited = []
        self.query = search
        self.max = pMax
        self.min = pMin
    
    def getURL(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URl)
    
    def addSearch(self):
        self.URl += f'&ob=3&pmax={self.max}&pmin={self.min}&q={self.query}'

    def scroll(self):
        SCROLL_PAUSE_TIME = 0.5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def Run(self):
        self.getURL()
        self.addSearch()
        self.driver.get(self.URl)
        self.scroll()
        self.getProductCrawl()

    def getProductCrawl(self):
        df = pd.DataFrame(
            columns=[
                'Name',
                'Price',
                'URL',
            ]
        )
        df1 = pd.DataFrame(
            columns=[
                'Name',
                'Price',
                'URL',
            ]
        )
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        primary = soup.findAll('div', attrs={'class':'css-1asz3by'})
        for i, sub_item in enumerate(primary):
            item_name = sub_item.find(
                'div', attrs={'class': 'prd_link-product-name'}).text
            item_price = sub_item.find(
                'div', attrs={'class': 'prd_link-product-price'}).text
            item_link = sub_item.find(
            'a', attrs={'class': 'pcv3__info-content'}).get('href')
            if item_link not in self.url_visited:
                self.url_visited.append(item_link)
            else : return
            df.loc[i] = [
                item_name if item_name else "N/A",
                item_price,
                item_link,
            ]
            self.driver.get(item_link)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            store = soup.find('a', attrs={'class': 'css-1sl4zpk'}).get('href')
            storename = soup.find('h2',attrs={'class': 'css-1wdzqxj-unf-heading'}).text
            self.driver.get(f'https://www.tokopedia.com{store}?q={self.query}&sort=10')
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            instore = soup.findAll('div', attrs={'class':'css-1asz3by'})
            for j, itemStore in enumerate(instore):
                item_name = itemStore.find(
                    'div', attrs={'class': 'prd_link-product-name'}).text
                item_price = itemStore.find(
                    'div', attrs={'class': 'prd_link-product-price'}).text
                item_link = itemStore.find(
                'a', attrs={'class': 'pcv3__info-content'}).get('href')
                if item_link not in self.url_visited:
                    self.url_visited.append(item_link)
                else:
                    return
                df1.loc[j] = [
                    item_name if item_name else "N/A",
                    item_price,
                    item_link,
                ]
            df1.drop_duplicates(inplace=True)
            df1.to_csv(f'result{storename}.csv', index=False)
        df.drop_duplicates(inplace=True)
        df.to_csv('result.csv', index=False)
        
if __name__ == "__main__":
    quer = "Graphic Card"
    quer = re.sub(" ","%20",quer)
    Pmin = "10000000"
    Pmax = "11000000"
    url = "https://www.tokopedia.com/search?"

    crawl = WebCrawl(url,quer,Pmax,Pmin)
    crawl.Run()