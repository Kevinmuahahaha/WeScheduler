#!/usr/bin/python3
from pyvirtualdisplay import Display
from selenium.webdriver import Firefox
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
from dateutil import parser
import os
import sys
import threading
from update_notifier import listen_update
from parsefile import parse_file

running_on_server = False # This will change the value returned from current_time()
browser = None
notify = False # Config File is Checked Only WHen notify=True

def current_time():
    global running_on_server
    if running_on_server:
        return datetime.now() + timedelta(hours=8)
    else:
        return datetime.now()

def time_end_of_day():
    global running_on_server
    today = current_time()

    return datetime(today.year, today.month, today.day) + timedelta(hours=24)

def locate_target_by_name( input_target_name ):
    global browser
    target_name = input_target_name
    target_object = None
    chat_targets = browser.find_elements_by_class_name("nickname")
    for item in chat_targets:
        if item.text == target_name:
            print("[+] Target [%s] Found: " % target_name )
            target_object = item
            break
    if target_object is None:
        print("[error] Counldn't Find Chat Target")

    return target_object

def service_loop( notify, q ):
    global browser
    msg_list = parse_file()
    while True:
        if not q.empty():
            notify = q.get()    # Clear Out the enqueued Contents 
            msg_list = parse_file() ######## Get Config Contents
            notify = False
            print("[debug] Config Rechecked.")

        index = 0

        while index < len(msg_list):
            target_time = msg_list[index]
            d_target = 0
            # Processing Timing...
            try:
                d_target = parser.parse( str(target_time) )
            except:
                index = index+3
                continue

            d_now    = current_time()
            time_diff = (d_now - d_target).total_seconds()
            if time_diff < 0 or time_diff > 1:
                index = index + 3
                continue
            

            target_name = msg_list[index+1].strip('\n')
            target_object = locate_target_by_name( target_name ) ######## Locate Target
            if target_object is None:
                print("[-]\tTarget [%s] Not Found. Trying Next..." % target_name )
                index = index + 3
                continue
            target_object.click()                                    ######## Switch to Chat Target

            send_content = msg_list[index+2].strip('\n')
            index = index + 3

            edit_area = browser.find_element_by_id("editArea")
            edit_area.click()
            edit_area.send_keys( send_content )
            send_button = browser.find_element_by_class_name("btn_send")
            send_button.click()
            print("[notice] " + str( current_time() ) + " SEND OK")


def main():
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    ######## Loading Args
    profile=webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 0) 
    print("[debug] Browser Options Fully Loaded")
    ########

    ######## Launching Browser
    global browser
    browser = webdriver.Firefox( profile )
    print("[debug] Browser Started")
    browser.get('https://wx.qq.com/')
    print("[debug] Connected to Login Page")
    #### Get Login QR Code
    time.sleep(3)
    qr_code = browser.find_element_by_class_name('img').get_attribute('src')
    print( "[debug] Fetching QR Code: " + qr_code )
    print( "[debug] QR Code Fetched" )
    qr_code_path = "./scan.jpg"
    os.system("wget " + qr_code + " -q -O " + qr_code_path )
    print("[debug] QR Code Saved to %s" % qr_code_path)
    #### Wait For Login
    print( "[debug] Waiting For Login" )
    while True:
        if browser.current_url != "https://wx.qq.com/":
        # Login Detection Method -- URL Change
        #   before: https://wx.qq.com/
        #   after: https://wx2.qq.com/
            break;
        time.sleep(3)
    print( "[debug] Logged In, Wait For Contents to Load" )
    time.sleep(5)
    ########
    



    #### Start Refreshing Loop
    global notify
    notify = True
    import queue # queue is used to communicate between threads
    thread_comm_queue = queue.Queue()
    notify_listener_thread = threading.Thread(target=listen_update, args=(notify, thread_comm_queue))
    if notify_listener_thread == None:
        print("[-] Fail to Start Config-Update Listener.")
        print("[-] Abort.")
        sys.exit(1)
    service_refresh_thread = threading.Thread( target=service_loop, args=(notify, thread_comm_queue))
    service_refresh_thread.start()
    print("[debug] Service Loop Started.")
    notify_listener_thread.start()
    print("[debug] Update Notification Listener Started.")
    notify_listener_thread.join()
    service_refresh_thread.join()


    #print("[+] Update Listener is Ready.")
    #print("[debug] Start Refreshing Config File")




# TODO:
# Detect Time in Day
# Auto Datetime in VPS

if __name__ == "__main__":
    main()
