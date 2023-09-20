from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options,)

driver.get('https://bama.ir/car')

scroll_count = 5

for i in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2) 
    
soup = BeautifulSoup(driver.page_source, 'html.parser')

bama_ad_holder = soup.find_all('div', class_='bama-ad-holder')

print(len(bama_ad_holder))

driver.quit()

