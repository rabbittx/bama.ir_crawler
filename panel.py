from fast_scan import fast_scan_main
from deep_scan import deep_scan_main

class panel :
    """
    این کلاس برای مدیریت عملیات اسکن سریع و عمیق روی آگهی‌های خودرو استفاده می‌شود. این کلاس دارای توابع زیر است:

    __init__(self, fast_scan_scroll=10, deep_scan_scroll=1): سازنده کلاس که مقادیر پیش‌فرض برای تعداد اسکرول در اسکن سریع و عمیق را تنظیم می‌کند.
    do_fast_scan(self, url, scroll): انجام عملیات اسکن سریع بر روی آگهی‌های خودرو.
    do_deep_scan(self, url, scroll): انجام عملیات اسکن عمیق بر روی آگهی‌های خودرو.
    run_panel(self): اجرای پنل مدیریتی برای انتخاب و اجرای نوع اسکن.
        
    """
    def __init__(self,fast_scan_scroll=10,deep_scan_scroll=1,):
        self.DEPP_SCAN_SCROLL =  deep_scan_scroll
        self.FAST_SCAN_SCROLL = fast_scan_scroll
        self.BA_MA_URL = 'https://bama.ir/car'
    
    def do_fast_scan(self,url,scroll):
        fast_scan_main(url,scroll)
    
    def do_deep_scan(self,url,scroll):
        deep_scan_main(url,scroll)
    
    def run_panel(self):
        
        while True :
            print('1. fast scan')
            print('2. deep scan')
            print('-1. quit')
            choose = input('choose the scan type : ')
            if choose == '1' :
                self.do_fast_scan(self.BA_MA_URL,self.FAST_SCAN_SCROLL)
            elif choose == '2' :
                self.do_deep_scan(self.BA_MA_URL,self.DEPP_SCAN_SCROLL)
            elif choose == '-1' :
                print("Exiting...")
                break
            else:
                print('wrong option !! retry')

if __name__ == '__main__' :
    crawler_panel = panel(fast_scan_scroll=100,deep_scan_scroll=50)
    crawler_panel.run_panel()
