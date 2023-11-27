import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# User Input
harga = input("Harga VGA nya (Angka saja -> satuan juta) = ")
# bekasOrBaru = input("Preferensi Bekas / Baru = ")

# Set url dengan harga asli dan harga 1 juta dibawahnya
url = "https://www.tokopedia.com/search?st=&q=VGA%20" + harga + "%20Juta"
urlMinus = "https://www.tokopedia.com/search?st=&q=VGA%20" + \
    str(int(harga) - 1) + "%20Juta"

# Penyimpanan Data
data1 = []
data2 = []


def crawlData(urlWhat):
    driver = webdriver.Chrome()
    driver.get(url if urlWhat == 0 else urlMinus)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    container = soup.findAll('div', attrs={'class': 'css-1asz3by'})
    for divContainer in container:
        nama_barang = divContainer.find(
            'div', attrs={'class': 'prd_link-product-name'}).text
        (data1 if urlWhat == 0 else data2).append((nama_barang))


for i in range(2):
    crawlData(i)

dataRTX = [item for item in data1 if "RTX" in item]
dataRX = [item for item in data1 if "RX" in item]

dfRTX = pd.DataFrame(dataRTX, columns=['RTX'])
dfRX = pd.DataFrame(dataRX, columns=['RX'])

print(dfRTX)
print("")
print(dfRX)
