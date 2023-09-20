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


def ads_fs_extraction(ad_suorce):
    result_list = []
    data_dic = {'title': '',
                'link': '',
                'id': '',
                'model': '',
                'type': '',
                'year': '',
                'used': '',
                'gear': '',
                'badges': '',
                'price': '',
                'city': '',
                'address': ''
                }
    bama_ad_holder = ad_suorce.find_all('div', class_='bama-ad-holder')
    for ad in bama_ad_holder :
        data_dic['title'] = ad.find('a').attrs['title']
        data_dic['link'] = ad.find('a').attrs['href']
        data_dic['id'] = ad.find('a').attrs['data-adcode'] 
        data_dic['model'] = ad.find('div',{'class':'bama-ad__title-row'}).text.split('،')[0]
        data_dic['type'] = ad.find('div',{'class':'bama-ad__title-row'}).text.split('،')[1]

        data_dic['year'] =ad.find('div',{'class':'bama-ad__detail-row'}).find_all('span')[0].text
        data_dic['used'] =ad.find('div',{'class':'bama-ad__detail-row'}).find_all('span')[1].text
        data_dic['gear'] =ad.find('div',{'class':'bama-ad__detail-row'}).find_all('span')[2].text
     
        bama_ad_badges_row = ad.find('div', {'class': 'bama-ad__badges-row'})

        if bama_ad_badges_row:
            span_element = bama_ad_badges_row.find('span')
            if span_element:
                data_dic['badges'] = span_element.text
            else:
                data_dic['badges'] = 'N/A'
        else:
            data_dic['badges'] = 'N/A'

        data_dic['price'] = ad.find('div',{'class':'bama-ad__price-row'}).find('span').text
        data_dic['city'] = ad.find('div',{'class':'bama-ad__address'}).find('span').text.split('/')[0]
        bama_ad_address = ad.find('div', {'class': 'bama-ad__address'})

        if bama_ad_address:
            span_element = bama_ad_address.find('span')
            if span_element:
                address_text = span_element.text
                address_parts = address_text.split('/')
                if len(address_parts) >= 2:
                    data_dic['address'] = address_parts[1].strip()
                else:
                    data_dic['address'] = 'N/A'
            else:
                data_dic['address'] = 'N/A'
        else:
            data_dic['address'] = 'N/A'

        result_list.append(data_dic.copy())  
        
        
    return result_list
fast_scran_result = ads_fs_extraction(ads_data)

with open('fast_scran_result.txt',mode='w',encoding='utf-8') as file :
   file.write(str(fast_scran_result))
