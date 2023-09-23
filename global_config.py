from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import time

USER_AGENTS = {
    "chrome": "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "firefox": "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"
}

def calculate_date(date_string):
    """
    این تابع یک رشته تاریخ دریافتی را تجزیه و تحلیل کرده و آن را به یک فرمت استاندارد تبدیل می‌کند.
    ورودی:

    date_string (str): رشته حاوی تاریخ در فرمت خاص.
    خروجی:

    یک رشته که تاریخ معتبر به فرمت YYYY-MM-DD را نمایش می‌دهد.

    """
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
    return now.strftime('%Y-%m-%d')

def get_selenium_driver(url, scroll_count=5, user_agent="chrome"):
    """
    این تابع یک درایور Selenium برای مرورگر ایجاد می‌کند و به وب‌سایت مورد نظر متصل می‌شود. سپس صفحه وب را به تعداد دفعات مشخصی پایین می‌کشد (scroll) تا اطلاعات بیشتری استخراج شود.

    ورودی:

    url (str): آدرس وب‌سایت برای متصل شدن.
    scroll_count (int): تعداد باری که صفحه وب را پایین می‌کشیم تا اطلاعات بیشتری استخراج شود (پیش‌فرض: 5).
    user_agent (str): نوع مرورگر برای شبیه‌سازی (مثلا، "chrome" یا "firefox").
    خروجی:

    یک نمونه از کلاس webdriver.Chrome که به وب‌سایت متصل شده است یا None اگر متصل نشد.
        
    """
    if user_agent not in USER_AGENTS:
        raise ValueError("Invalid user agent specified")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(USER_AGENTS[user_agent])
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        for _ in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        return driver
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.quit()
        return None

def get_soup_with_selenium(url, scroll_count=5, user_agent="chrome"):
    """

    این تابع از Selenium برای دریافت محتوای وب‌سایت و تبدیل آن به یک شیء Beautiful Soup استفاده می‌کند.

    ورودی:

    url (str): آدرس وب‌سایت برای متصل شدن.
    scroll_count (int): تعداد باری که صفحه وب را پایین می‌کشیم تا اطلاعات بیشتری استخراج شود (پیش‌فرض: 5).
    user_agent (str): نوع مرورگر برای شبیه‌سازی (مثلا، "chrome" یا "firefox").
    خروجی:

    یک شیء Beautiful Soup حاوی محتوای وب‌سایت یا None اگر متصل نشد.
        

    """
    driver = get_selenium_driver(url, scroll_count, user_agent)
    if driver is not None:
        try:
            page_source = driver.page_source
            driver.quit()
            return BeautifulSoup(page_source, 'html.parser')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            driver.quit()
    return None

