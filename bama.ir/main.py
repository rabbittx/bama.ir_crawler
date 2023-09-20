from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


def get_ads_info(scroll_count=5 ,delay=3):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options,)

    driver.get('https://bama.ir/car')

    time.sleep(delay)

    scroll_count = scroll_count

    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    bama_ad_holder = soup.find_all('div', class_='bama-ad-holder')


    driver.quit()
    return bama_ad_holder


with open('html_source.txt',mode='r',encoding='utf-8') as file :
   ads_data = file.read()

ads_data = BeautifulSoup(ads_data, 'html.parser')


def ads_extraction(ad_suorce):

    bama_ad_holder = ad_suorce.find_all('div', class_='bama-ad-holder')
    for ad in bama_ad_holder :
        title = ad.find('a').attrs['title']
        link = ad.find('a').attrs['href']
        bama_ad__title_row = ad.find('div',{'class':'bama-ad__title-row'})
        bama_ad__detail_row =ad.find('div',{'class':'bama-ad__detail-row'})
        bama_ad__badges_row = ad.find('div',{'class':'bama-ad__badges-row'})
        bama_ad__price_row = ad.find('div',{'class':'bama-ad__price-row'})
        print(title)

ads_extraction(ads_data)