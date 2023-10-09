import time 
import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db_controller import deep_scan_db_table
from global_config import calculate_date , get_selenium_driver
import sys
def deep_scan_extract(driver,cursor,conn):
    """
    این تابع اطلاعات آگهی‌های خودرو را با استفاده از درایور Selenium به صورت عمیق از صفحه وب‌سایت استخراج می‌کند و در پایگاه داده SQLite ذخیره می‌کند.

    ورودی:

        driver (webdriver.Chrome): درایور Selenium برای متصل شدن به وب‌سایت.
        cursor (sqlite3.Cursor): کرسور برای ارتباط با پایگاه داده SQLite.
        conn (sqlite3.Connection): اتصال به پایگاه داده SQLite.
    خروجی:

        بدون خروجی (None).
    """
    ad_elements = driver.find_elements(By.CLASS_NAME,'bama-ad-holder')
    for index ,ad in enumerate(ad_elements):
        sys.stdout.write(f"\rcar ads progress: {index+1}/{len(ad_elements)}")
        sys.stdout.flush()
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
                        'installment_price': 'N/A',
                        'monthly_price': 'N/A',
                        'city':  ad_warpper[0].find_element(By.CLASS_NAME,'address-text').text.split('/')[0],
                        'address':"N/A" ,
                        'fuel_type'  :ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-gas-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'body_condition':ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-car_body-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'body_color':ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-brush-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'interior_color':ad_warpper[0].find_element(By.CLASS_NAME,'bama-icon-seat-outlined-bold').find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'p')[0].text,
                        'description' : 'N/A',
                        'Engine_volume':'N/A',
                        'engine':'N/A',
                        'acceleration':'N/A',
                        'Combined_consumption':'N/A',
                        'call_number':'N/A',
                        'ad_images' : 'N/A'
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
                data_dic['installment_price'] = 'N/A'
                data_dic['monthly_price'] = 'N/A'
            try :
                data_dic['description'] =  WebDriverWait(ad_warpper[0], 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'desc')))[0].text 
            except :
                data_dic['description'] = 'N/A'

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
            try:
                seller_phone_number_element = WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'bama-call-to-seller__number-text')))
                data_dic['call_number'] = seller_phone_number_element[0].text
            except:
                data_dic['call_number'] ='N/A'
            ad_image_list = []
            for img in ad_warpper[0].find_elements(By.TAG_NAME,'img'):
                
                if img.get_attribute('src') not in ad_image_list:
                    ad_image_list.append(img.get_attribute('src'))
            data_dic['ad_images'] = ad_image_list
    
            ad_close_btn = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'bama-ad-detail-modal__close-button')))
            ad_close_btn[0].click()
            time.sleep(1)

            cursor.execute('''
            INSERT INTO deep_scan (title,link, ad_id,  model, date,type, year, used, gear,  price,installment_price,
            monthly_price, city, address,fuel_type,body_condition,body_color,interior_color,description,Engine_volume,
                           engine,acceleration,Combined_consumption,call_number,ad_images)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (data_dic['title'],data_dic['ad_id'], data_dic['link'], data_dic['model'],data_dic['date'], data_dic['type'], data_dic['year'],
              data_dic['used'], data_dic['gear'],  data_dic['price'],data_dic['installment_price'],
              data_dic['monthly_price'], data_dic['city'], data_dic['address'],data_dic['fuel_type'],data_dic['body_condition'],
              data_dic['body_color'],data_dic['interior_color'],data_dic['description'],data_dic['Engine_volume'],data_dic['engine'],
              data_dic['acceleration'],data_dic['Combined_consumption'],data_dic['call_number'],str(data_dic['ad_images'])))
            conn.commit()    

def deep_scan_main(BA_MA_URL, SCROLL_COUNT):
    """
    این تابع اجرای اصلی برای انجام عملیات اسکن عمیق روی آگهی‌های خودرو است. این تابع داده‌ها را استخراج کرده و در پایگاه داده SQLite ذخیره می‌کند.

    ورودی:

        BA_MA_URL (str): آدرس وب‌سایت Bama.ir.
    خروجی:

        بدون خروجی (None).
            
    """
    conn = sqlite3.connect('bama_ads.db')
    deep_scan_db_table()
    cursor = conn.cursor()
    driver = get_selenium_driver(BA_MA_URL, SCROLL_COUNT)
    deep_scan_extract(driver,cursor,conn)
    conn.close()

