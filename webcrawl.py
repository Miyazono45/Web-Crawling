import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://www.tokopedia.com/nanokomputer/product?perpage=20"
driver = webdriver.Chrome()
driver.get(url)

data = []
soup = BeautifulSoup(driver.page_source, "html.parser")
container = soup.findAll('div', attrs={'class': 'css-1asz3by'})
for divContainer in container:
    nama_barang = divContainer.find(
        'div', attrs={'class': 'prd_link-product-name'}).text
    data.append((nama_barang))

df = pd.DataFrame(data, columns=['Nama Barang'])
print(df)
