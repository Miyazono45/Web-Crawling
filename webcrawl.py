import time
import re
from tqdm import tqdm
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd

# User Input
price = input("Harga VGA nya (Angka saja -> satuan juta) = ")
newOrUsed = input("Preferensi Bekas / Baru = ")
limitLoop = input("Batasan Awal = ")

# Penyimpanan Data (Nama Barang, Harga Barang, Link, Kondisi, Nama Toko)
dtypeFirstData = [('name', '<U100'), ('price', '<U25'),
                  ('link', '<U250'), ('condition', '<U10'), ('store', '<U25')]
firstData = np.zeros([1, 5], dtype='<U250')

# For data cleaning and checking if page was visited
dataRaw = []
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

    soup = BeautifulSoup(driver.page_source, "html.parser")
    primary_item = soup.findAll('div', attrs={'class': 'css-1asz3by'})

    starter = 0

    # For Halaman Awal
    for i, sub_item in tqdm(enumerate(primary_item[starter:int(limitLoop)], start=starter)):
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

        # Navigate to Product Page Link ============================================>
        # Collect Name of VGA
        try:
            # If "RTX 3060 TI"
            patternRegex = addPR + r'(\s)?\d{3,4}(\s)?(TI)?(XT)?'
            res = re.search(patternRegex, item_name, re.IGNORECASE)
        except:
            # If Intel GPU / AMD
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
            self_item_price_page2 = container_page2[i].find_element(
                By.CLASS_NAME, "prd_link-product-price")
            if self_item_price_page2.text == item_price:
                whichPage = i+1

        # print("Item ada di : " + str(whichPage))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        secondary_item = soup.findAll('div', attrs={'class': 'css-1asz3by'})
        # Finding One-by-One items
        start_item = 0

        for j, sub_item_2 in tqdm(enumerate(secondary_item[start_item:whichPage], start=start_item)):
            time.sleep(3)
            # WebDriverWait(driver, 20).until(lambda h: h.find_element(
            #     By.CLASS_NAME, "prd_link-product-name"))

            # Find Name,Price,Link
            item_name_page2 = sub_item_2.find(
                'div', attrs={'class': 'prd_link-product-name'}).text
            item_price_page2 = sub_item_2.find(
                'div', attrs={'class': 'prd_link-product-price'}).text
            item_link_page2 = sub_item_2.find(
                'a', attrs={'class': 'pcv3__info-content'}).get('href')

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

            # Navigate to Sub_Item_Page2 Link =================================================>
            driver.implicitly_wait(20)
            driver.get(item_link_page2)

            # Get item_condition and item_store
            item_condition_temp_2 = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "css-bwcbiv")))
            item_condition_page2 = item_condition_temp_2.find_element(
                By.CLASS_NAME, "main").text
            second_item_2_2 = driver.find_element(By.CLASS_NAME, "css-1sl4zpk")
            item_store_page2 = second_item_2_2.find_element(
                By.TAG_NAME, "h2").text

            # Wrap Up for append in numpy
            item_container_page2 = [item_name_page2, item_price_page2,
                                    item_link_page2, item_condition_page2, item_store_page2]

            # Add Data to firstData (Primary Data)
            firstData = np.append(firstData, [item_container_page2], axis=0)

    driver.close()


crawlData()

dataSort = firstData[firstData[:, 1].argsort()]

for i, dataWhat in enumerate(dataSort):
    if "RTX" in dataWhat[0]:
        dataRTX = np.append(dataRTX, [dataWhat], axis=0)
    elif "RX" in dataWhat[0]:
        dataRX = np.append(dataRX, [dataWhat], axis=0)
    elif "GTX" in dataWhat[0]:
        dataGTX = np.append(dataGTX, [dataWhat], axis=0)

# pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
datasetRTX = pd.DataFrame(dataRTX, columns=[
    'Nama', 'Harga', 'Link', 'Kondisi', 'Toko'])
datasetRTX.to_csv("result.csv", mode='a', index=False, header=False)

datasetRX = pd.DataFrame(dataRX, columns=[
    'Nama', 'Harga', 'Link', 'Kondisi', 'Toko'])
datasetRX.to_csv("result.csv", mode='a', index=False, header=False)

datasetGTX = pd.DataFrame(dataGTX, columns=[
    'Nama', 'Harga', 'Link', 'Kondisi', 'Toko'])
datasetGTX.to_csv("result.csv", mode='a', index=False, header=False)

print(datasetRTX)
print(datasetRX)
print(datasetGTX)

# Kelemahan
# - Saat DFS dijalankan, tidak bisa membedakan mana stock kosong mana yang tersedia
# - Ketika terdapat barang yang identik dengan barang awal melebihi dari 10, maka akan langsung tereliminasi (Terkadang)
# - terhitung lama karena harus membuka browser satu persatu (Mode Headless tidak bekerja dengan baik)
