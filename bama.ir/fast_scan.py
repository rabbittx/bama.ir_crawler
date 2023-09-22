import time 
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

BA_MA_URL = 'https://bama.ir/car'
SCROLL_COUNT = 1

def get_soup_with_selenium(url, scroll_count=5):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    page_source = driver.page_source
    driver.quit()
    return BeautifulSoup(page_source, 'html.parser')

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

def extract_ad_data(ad,cursor):
    data_dic = {
        'title': ad.find('a').attrs['title'],
        'link': 'https://bama.ir' + ad.find('a').attrs['href'],
        'id': ad.find('a').attrs['data-adcode'],
        'model': '',
        'date': '',
        'type': '',
        'year': '',
        'used': '',
        'gear': '',
        'badges': 'N/A',
        'price': '',
        'installment_price': '',
        'monthly_price': '',
        'city': '',
        'address': 'N/A'
    }

    title_row = ad.find('div', {'class': 'bama-ad__title-row'})
    if title_row:
        data_dic['model'] = title_row.find('p').text.split('،')[0]
        data_dic['type'] = title_row.find('p').text.split('،')[1]
        data_dic['date'] = calculate_date(title_row.find('span').text)
            
    detail_row = ad.find('div', {'class': 'bama-ad__detail-row'})
    if detail_row:
        spans = detail_row.find_all('span')
        if len(spans) >= 3:
            data_dic['year'] = spans[0].text
            data_dic['used'] = spans[1].text
            data_dic['gear'] = spans[2].text

    badges_row = ad.find('div', {'class': 'bama-ad__badges-row'})
    if badges_row:
        span_element = badges_row.find('span')
        if span_element:
            data_dic['badges'] = span_element.text

    price_row = ad.find('span', {'class': 'bama-ad__price'})
    if price_row:
        data_dic['price'] = price_row.text.replace(',','')
    else :
        price_element = ad.find('span', {'class': 'bama-ad__negotiable-price'})
                
        if price_element is not None:
            data_dic['price'] = price_element.text
        else:
            data_dic['installment_price'] = ad.find('div',{'class':'bama-ad__pre-price'}).find('span').text
            data_dic['monthly_price'] = ad.find('div',{'class':'bama-ad__monthly-price'}).find('span').text

    address_row = ad.find('div', {'class': 'bama-ad__address'})
    if address_row:
        address_text = address_row.find('span').text.split('/')
        if len(address_text) >= 2:
            data_dic['city'] = address_text[0].strip()
            data_dic['address'] = address_text[1].strip()
        else : 
            data_dic['city'] = address_row.find('span').text
            data_dic['address'] = 'N/A'

    cursor.execute('SELECT ad_id FROM fast_scan WHERE ad_id = ?', (data_dic['id'],))
    existing_id = cursor.fetchone()

    if existing_id is None:
        cursor.execute('''
            INSERT INTO fast_scan (title, ad_id, link, model, date,type, year, used, gear, badges, price,installment_price,
            monthly_price, city, address)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)
        ''', (data_dic['title'],data_dic['id'], data_dic['link'], data_dic['model'],data_dic['date'], data_dic['type'], data_dic['year'],
              data_dic['used'], data_dic['gear'], data_dic['badges'], data_dic['price'],data_dic['installment_price'],
              data_dic['monthly_price'], data_dic['city'], data_dic['address']))

    return data_dic

def ads_fast_scan_extraction(ad_source,cursor):
    bama_ad_holders = ad_source.find_all('div', class_='bama-ad-holder')
    for ad in bama_ad_holders:
        extract_ad_data(ad,cursor)

def fast_scan_db_table():
    conn = sqlite3.connect('bama_ads.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fast_scan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_id TEXT,
            title TEXT,
            link TEXT,
            model TEXT,
            date TEXT,
            type TEXT,
            year TEXT,
            used TEXT,
            gear TEXT,
            badges TEXT,
            price TEXT,
            installment_price TEXT,
            monthly_price TEXT,
            city TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()  

def fast_scan_main():
    fast_scan_db_table()
    conn = sqlite3.connect('bama_ads.db')
    cursor = conn.cursor()
    soup = get_soup_with_selenium(BA_MA_URL, SCROLL_COUNT)
    ads_fast_scan_extraction(soup, cursor)
    conn.commit()
    conn.close()

