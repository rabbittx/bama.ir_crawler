import sqlite3
from db_controller import fast_scan_db_table
from global_config import calculate_date , get_soup_with_selenium

def extract_ad_data(ad,cursor):
    """
    این تابع اطلاعات یک آگهی خودرو را از یک تگ BeautifulSoup استخراج کرده و در یک دیکشنری ذخیره می‌کند. همچنین اطلاعات آگهی را در پایگاه داده SQLite ذخیره می‌کند.

    ورودی:

    ad (Tag): تگ Beautiful Soup حاوی اطلاعات آگهی.
    cursor (sqlite3.Cursor): کرسور برای ارتباط با پایگاه داده SQLite.
    خروجی:

    یک دیکشنری حاوی اطلاعات آگهی خودرو.
        
    
    """
    data_dic = {
        'title': ad.find('a').attrs['title'],
        'link': 'https://bama.ir' + ad.find('a').attrs['href'],
        'id': ad.find('a').attrs['data-adcode'],
        'model': 'N/A',
        'date': 'N/A',
        'type': 'N/A',
        'year': 'N/A',
        'used': 'N/A',
        'gear': 'N/A',
        'badges': 'N/A',
        'price': 'N/A',
        'installment_price': 'N/A',
        'monthly_price': 'N/A',
        'city': 'N/A',
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
    """
    این تابع اطلاعات آگهی‌های خودرو را از منبع صفحه وب‌سایت استخراج می‌کند و در پایگاه داده SQLite ذخیره می‌کند.

    ورودی:
        ad_source (BeautifulSoup): شیء Beautiful Soup حاوی منبع صفحه وب‌سایت.
        cursor (sqlite3.Cursor): کرسور برای ارتباط با پایگاه داده SQLite.
    خروجی:
        بدون خروجی (None).

    
    """
    bama_ad_holders = ad_source.find_all('div', class_='bama-ad-holder')
    for ad in bama_ad_holders:
        extract_ad_data(ad,cursor)

def fast_scan_main(BA_MA_URL, SCROLL_COUNT):
    """
    این تابع اجرای اصلی برای انجام عملیات اسکن سریع روی آگهی‌های خودرو است. این تابع داده‌ها را استخراج کرده و در پایگاه داده SQLite ذخیره می‌کند.

    ورودی:

        BA_MA_URL (str): آدرس وب‌سایت Bama.ir.
        SCROLL_COUNT (int): تعداد باری که صفحه وب را پایین می‌کشیم تا اطلاعات بیشتری استخراج شود.
    خروجی:

        بدون خروجی (None).
    
    
    """

    fast_scan_db_table()
    conn = sqlite3.connect('bama_ads.db')
    cursor = conn.cursor()
    soup = get_soup_with_selenium(BA_MA_URL, SCROLL_COUNT)
    ads_fast_scan_extraction(soup, cursor)
    conn.commit()
    conn.close()

