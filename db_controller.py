import sqlite3

def deep_scan_db_table():
    """
    این تابع جدول مورد نیاز برای اجرای اسکن عمیق روی آگهی‌های خودرو در پایگاه داده SQLite ایجاد می‌کند.

    """
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
            ad_images TEXT
        )
    ''')
    conn.commit()
    conn.close()  

def fast_scan_db_table():
    """
    این تابع جدول مورد نیاز برای اجرای اسکن سریع روی آگهی‌های خودرو در پایگاه داده SQLite ایجاد می‌کند.

    """
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
