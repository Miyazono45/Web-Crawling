from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


#User Input
quer = input('whats your Searching = ')
pricemax = input('what is max price = ')
pricemin = input('what is min price = ')


urls = 'https://www.tokopedia.com'
# response = requests.get(urls)
# print(response)
# option =  Options()
# option.add_argument('--headless')\


driver = webdriver.Chrome()
driver.get(urls)
# Input User Search Query
driver.find_element(By.TAG_NAME,'input')
data_input = driver.find_element(By.CLASS_NAME,'css-3017qm')
ActionChains(driver)\
    .send_keys_to_element(data_input,quer)\
    .key_down(Keys.RETURN)\
    .perform()
time.sleep(4)
driver.current_url

# Shift it to highest or lowest(not yet done)
driver.find_element(By.CLASS_NAME,'css-1g467vj').click()
driver.find_elements(By.CLASS_NAME, 'e83okfj5')
driver.find_element(By.CSS_SELECTOR,'[data-item-text="Harga Tertinggi"]').click()
time.sleep(3)

driver.current_url

# Setting the value minimum
driver.find_element(By.CLASS_NAME, 'css-1cb34wj')
min = driver.find_element(By.NAME,'pmin')
ActionChains(driver)\
    .send_keys_to_element(min,'0')\
    .send_keys_to_element(min,pricemin)\
    .key_down(Keys.RETURN)\
    .perform()
time.sleep(3)

# setting the value maximum
driver.find_element(By.CLASS_NAME, 'css-1cb34wj')
max = driver.find_element(By.NAME,'pmax')
ActionChains(driver)\
    .send_keys_to_element(max,'0')\
    .send_keys_to_element(max,pricemax)\
    .key_down(Keys.RETURN)\
    .perform()
time.sleep(3)
driver.current_url
print(driver.current_url)


# then crawl the website data(not yet done)
def dfs_web_crawl():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    link = soup.findAll('div', attrs={'class': 'css-1asz3by'})
    print(link)


dfs_web_crawl()
