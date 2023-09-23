from fast_scan import fast_scan_main
from deep_scan import deep_scan_main
# TODO add user agent 
# TODO add logging 
# TODO add docs 
class panel :
    def __init__(self):
        self.DEPP_SCAN_SCROLL =  1
        self.FAST_SCAN_SCROLL = 1
        self.BA_MA_URL = 'https://bama.ir/car'
    
    def do_fast_scan(self,url,scroll):
        fast_scan_main(url,scroll)
    
    def do_deep_scan(self,url,scroll):
        deep_scan_main(url,scroll)
    
    def panel_menu(self):
        
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
    crawler_panel = panel()
    crawler_panel.panel_menu()

