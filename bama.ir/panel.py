from fast_scan import fast_scan_main

class panel :
    def __init__(self) -> None:
        pass

    def do_fast_scan(self):
        fast_scan_main()
    
    def panel_menu(self):
        print('1. fast scan')
        print('2. deep scan')
        print('-1. quit')
      
        while True :
            choose = input('choose the scan type : ')
            if choose == '1' :
                self.do_fast_scan()
            elif choose == '2' :
                print('this part need to get fix')
            elif choose == '-1' :
                print("Exiting...")
                break
            else:
                print('wrong option !! retry')

if __name__ == '__main__' :
    crawler_panel = panel()
    crawler_panel.panel_menu()