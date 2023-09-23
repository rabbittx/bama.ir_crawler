from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import time

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
    return now.strftime('%Y-%m-%d')

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
