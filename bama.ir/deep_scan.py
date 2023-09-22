import time 
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BA_MA_URL = 'https://bama.ir/car'
SCROLL_COUNT = 20
#
def get_selenium_driver(url, scroll_count=5):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    return driver

def calculate_date(date_string):
    now = datetime.now()
    if 'دقایقی پیش' in date_string or 'لحظاتی پیش' in date_string:
        return now.strftime('%Y-%m-%d')
    elif 'ساعت پیش' in date_string:
        hours_ago = int(date_string.split()[0])
        post_time = now - timedelta(hours=hours_ago)
        return post_time.strftime('%Y-%m-%d')

    elif 'روز پیش' in date_string:
        days_ago = int(date_string.split()[0])
        post_time = now - timedelta(days=days_ago)
        return post_time.strftime('%Y-%m-%d')

    elif 'دیروز' in date_string:
        post_time = now - timedelta(days=1)
        return post_time.strftime('%Y-%m-%d')

    elif 'سنجاق شده' in date_string:
        return now.strftime('%Y-%m-%d')
    return None


def deep_scan_extract(driver,cursor,conn):
    





    ad_elements = driver.find_elements(By.CLASS_NAME,'bama-ad-holder')
    for ad in ad_elements:
        ad_id = ad.find_element(By.TAG_NAME,'a').get_attribute('data-adcode')
        cursor.execute('SELECT ad_id FROM deep_scan WHERE ad_id = ?', (ad_id,))
        existing_id = cursor.fetchone()
        if existing_id is None:
            
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});", ad)
            ad.click()

            ad_warpper = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'bama-ad-detail-wrapper')))
            data_dic = {
                        'title': ad_warpper[0].find_element(By.TAG_NAME,'h1').text.strip(),
                        'link': ad.find_element(By.TAG_NAME,'a').get_attribute('href'),
                        'ad_id': ad.find_element(By.TAG_NAME,'a').get_attribute('data-adcode').strip(),
                        'model': ad_warpper[0].find_element(By.TAG_NAME,'h1').text.split('،')[0].strip(),
                        'date': calculate_date(ad_warpper[0].find_element(By.CLASS_NAME,'bama-ad-detail-title__ad-time').text),
                        'type': ad_warpper[0].find_element(By.TAG_NAME,'h1').text.split('،')[1].strip(),
                        'year': ad_warpper[0].find_element(By.CLASS_NAME,'bama-ad-detail-title__subtitle-holder').find_elements(By.TAG_NAME,'span')[0].text,
                        'used': ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-speed-outlined-bold').find_element(By.XPATH,'..').find_element(By.TAG_NAME,'p').text,
                        'gear': ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-gearbox-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'price': ad_warpper[0].find_element(By.CLASS_NAME,'bama-ad-detail-price__price-text').text,
                        'installment_price': '',
                        'monthly_price': '',
                        'city':  ad_warpper[0].find_element(By.CLASS_NAME,'address-text').text.split('/')[0],
                        'address':"N/A" ,
                        'fuel_type'  :ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-gas-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'body_condition':ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-car_body-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'body_color':ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-brush-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'interior_color':ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-seat-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'description' : '',
                        'Engine_volume':'',
                        'engine':'',
                        'acceleration':'',
                        'Combined_consumption':'',
                        'call_number':'',
                       }
            
            address_text = ad_warpper[0].find_element(By.CLASS_NAME,'address-text').text.split('/')
            if len(address_text) >= 2:
                data_dic['address'] = address_text[1].strip()
            else : 
                data_dic['address'] = 'N/A'

            try:             
                installment_price =ad_warpper[0].find_elements(By.CLASS_NAME,'bama-ad-detail-price__price-text--installment')
                data_dic['installment_price'] =installment_price[0].text
                data_dic['monthly_price'] =installment_price[1].text
            except : 
                data_dic['installment_price'] = ''
                data_dic['monthly_price'] = ''
            try :
                data_dic['description'] =  WebDriverWait(ad_warpper[0], 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'desc')))[0].text 
            except :
                data_dic['description'] = ''

            for item in ad_warpper[0].find_elements(By.CLASS_NAME,'bama-vehicle-detail-with-link__row'):
                if item.find_element(By.CLASS_NAME,'bama-vehicle-detail-with-link__row-title').text == 'حجم موتور':
                    data_dic['Engine_volume'] = item.find_element(By.CLASS_NAME,'bama-vehicle-detail-with-link__row-text').text
                elif item.find_element(By.CLASS_NAME,'bama-vehicle-detail-with-link__row-title').text == 'پیشرانه':
                    data_dic['engine'] = item.find_element(By.CLASS_NAME,'bama-vehicle-detail-with-link__row-text').text
                elif item.find_element(By.CLASS_NAME,'bama-vehicle-detail-with-link__row-title').text == 'شتاب':
                    data_dic['acceleration'] = item.find_element(By.CLASS_NAME,'bama-vehicle-detail-with-link__row-text').text
                elif item.find_element(By.CLASS_NAME,'bama-vehicle-detail-with-link__row-title').text == 'مصرف ترکیبی':
                    data_dic['Combined_consumption'] = item.find_element(By.CLASS_NAME,'bama-vehicle-detail-with-link__row-text').text




            phone_number_btn = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'bama-call-to-seller__button')))
            phone_number_btn[0].click()
            seller_phone_number_element = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'bama-call-to-seller__number-text')))
            data_dic['call_number'] = seller_phone_number_element[0].text


            print('===============================================')
            print(data_dic['title'])
            print(data_dic['link'])
            print(data_dic['ad_id'])
            print(data_dic['model'])
            print(data_dic['date'])
            print(data_dic['type'])
            print(data_dic['year'])
            print(data_dic['gear'])
            print(data_dic['city'])
            print(data_dic['address'])
            print(data_dic['price'])
            print(data_dic['used'])
            print(data_dic['fuel_type'])
            print(data_dic['Engine_volume'])
            print(data_dic['engine'])
            print(data_dic['acceleration'])
            print(data_dic['Combined_consumption'])
            print(data_dic['call_number'])
            print('===============================================')

            # extracn all data here 


            ad_close_btn = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'bama-ad-detail-modal__close-button')))
            ad_close_btn[0].click()
            time.sleep(1)
            # update table here 
            cursor.execute('''
            INSERT INTO deep_scan (title,link, ad_id,  model, date,type, year, used, gear,  price,installment_price,
            monthly_price, city, address,fuel_type,body_condition,body_color,interior_color,description,Engine_volume,
                           engine,acceleration,Combined_consumption,call_number)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (data_dic['title'],data_dic['ad_id'], data_dic['link'], data_dic['model'],data_dic['date'], data_dic['type'], data_dic['year'],
              data_dic['used'], data_dic['gear'],  data_dic['price'],data_dic['installment_price'],
              data_dic['monthly_price'], data_dic['city'], data_dic['address'],data_dic['fuel_type'],data_dic['body_condition'],
              data_dic['body_color'],data_dic['interior_color'],data_dic['description'],data_dic['Engine_volume'],data_dic['engine'],
              data_dic['acceleration'],data_dic['Combined_consumption'],data_dic['call_number']))
            

            
            conn.commit()    


def deep_scan_db_table():
    conn = sqlite3.connect('bama_ads.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deep_scan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            ad_id TEXT,
            model TEXT,
            date TEXT,
            type TEXT,
            year TEXT,
            used TEXT,
            gear TEXT,
            price TEXT,
            installment_price TEXT,
            monthly_price TEXT,
            city TEXT,
            address TEXT,
            fuel_type TEXT,
            body_condition TEXT,
            body_color TEXT,
            interior_color TEXT,
            description TEXT,
            Engine_volume TEXT,
            engine TEXT,
            acceleration TEXT,
            Combined_consumption TEXT,
            call_number TEXT,
        )
    ''')
    conn.commit()
    conn.close()  

def fast_scan_main():
    conn = sqlite3.connect('bama_ads.db')
    deep_scan_db_table()
    cursor = conn.cursor()
    driver = get_selenium_driver(BA_MA_URL, SCROLL_COUNT)
    deep_scan_extract(driver,cursor,conn)
    conn.close()

fast_scan_main()