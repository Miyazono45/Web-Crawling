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

# User Input
price = input("Harga VGA nya (Angka saja -> satuan juta) = ")
newOrUsed = input("Preferensi Bekas / Baru = ")

# Penyimpanan Data (Nama Barang, Harga Barang, Link, Kondisi, Nama Toko)
firstData = np.zeros([1, 5], dtype='<U250')
visited = []

dataRTX = np.zeros([1, 5], dtype='<U250')
dataRX = np.zeros([1, 5], dtype='<U250')
dataGTX = np.zeros([1, 5], dtype='<U250')

# Set url dengan harga asli dan harga 1 juta diatasnyanya dan kondisi barang
primaryUrl = "https://www.tokopedia.com/search?condition=0%23" + (str(2) if newOrUsed == "Bekas" or newOrUsed == "bekas" else str(
    1)) + "&st=&pmin=" + (price+"000000") + "&pmax=" + (str((int(price)+1))+"000000") + "&q=VGA%20" + price + "%20Juta"


def crawlData():
    global firstData

    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(10)
    driver.get(primaryUrl)
    # driver =WebDriverWait()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    primary_item = soup.findAll('div', attrs={'class': 'css-1asz3by'})

    # For Halaman Awal
    for i, sub_item in enumerate(primary_item):
        # Find Items on First Page
        item_name = sub_item.find(
            'div', attrs={'class': 'prd_link-product-name'}).text
        item_price = sub_item.find(
            'div', attrs={'class': 'prd_link-product-price'}).text
        item_link = sub_item.find(
            'a', attrs={'class': 'pcv3__info-content'}).get('href')

        # check if item is duplicate
        checker_link = np.isin(item_link, firstData)
        if checker_link:
            print("DATA IS DUPLICATE")
            return

         # Clean Information Apart from RTX GTX RX and ARC, it will be removed
        if "GTX" in item_name:
            addPR = "GTX"
        elif "RTX" in item_name:
            addPR = "RTX"
        elif "RX" in item_name:
            addPR = "RX"
        elif "Arc" or "ARC" in item_name:
            continue
        else:
            return

        # Navigate to Sub_Item Link =================================================>
        driver.implicitly_wait(10)
        driver.get(item_link)

        # Get item_condition and item_store
        item_condition_temp = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-bwcbiv")))
        item_condition = item_condition_temp.find_element(
            By.CLASS_NAME, "main").text
        second_item_2 = driver.find_element(By.CLASS_NAME, "css-1sl4zpk")
        item_store = second_item_2.find_element(
            By.TAG_NAME, "h2").text

        # Wrap Up for append in numpy
        item_container = [item_name, item_price,
                          item_link, item_condition, item_store]

        # Add Data to firstData (Primary Data)
        firstData = np.append(firstData, [item_container], axis=0)
        if second_item_2.get_attribute("href") not in visited:
            # add mark (visited) which store is has been visited
            visited.append(second_item_2.get_attribute("href"))
        # else:
        #     return

        print("Harga Asli : " + item_price)

        # Navigate to Product Page Link ============================================>
        # Collect Name of VGA
        try:
            # If "RTX 3060 TI"
            patternRegex = addPR + r'(\s)?\d{4}( TI)?'
            res = re.search(patternRegex, item_name, re.IGNORECASE)
        except:
            # If Intel GPU
            patternRegexIntel = r'intel\sarc\s[A-Z]([0-9]{3})'
            res = re.search(patternRegexIntel, item_name, re.IGNORECASE)

        # Sorted by "Harga terendah"
        driver.implicitly_wait(10)
        driver.get(str(second_item_2.get_attribute("href")) +
                   "/product?q=" + str(res.group()) + "&sort=9&perpage=20")

        # Find main class

        div_container_page2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]")))

        # PLEASE AJUST THIS
        time.sleep(3)
        container_page2 = div_container_page2.find_elements(By.XPATH, "./div")

        whichPage = 0
        # Mencari div berapa yang merupakan item tersebut
        for i in range(len(container_page2)):
            item_price_page2 = container_page2[i].find_element(
                By.CLASS_NAME, "prd_link-product-price")
            if item_price_page2.text == item_price:
                whichPage = i+1

        print("Item ada di : " + str(whichPage))

        # Finding One-by-One items
        for j in range(whichPage-1):
            div_page_found = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]/div[" + str(j+1) + "]")
            item_price_found = div_page_found.find_element(
                By.CLASS_NAME, "prd_link-product-price")
            print("Item " + str(j+1) + " : " + item_price_found.text)

    driver.close()


crawlData()
print(firstData)
print("")
print(visited)

# for i, dataWhat in enumerate(data):
#     if "RTX" in dataWhat[0]:
#         dataRTX = np.append(dataRTX, [dataWhat], axis=0)
#     elif "RX" in dataWhat[0]:
#         dataRX = np.append(dataRX, [dataWhat], axis=0)
#     elif "GTX" in dataWhat[0]:
#         dataGTX = np.append(dataGTX, [dataWhat], axis=0)
