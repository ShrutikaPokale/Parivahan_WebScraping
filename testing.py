# -*- coding: utf-8 -*-
import requests
import pytesseract
from PIL import Image
import re
from selenium import webdriver
import selenium
from time import sleep
from selenium.webdriver.common.keys import Keys
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#selenium.common=r'C:\Users\Hp\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\selenium\chromedriver.exe'

def check():
    driver.save_screenshot('screenshot.png')
    im1 = Image.open('screenshot.png')
    alert = pytesseract.image_to_string(Image.open('screenshot.png')) 
    hidden=alert.find("No DL Details Found")
    return hidden
    
def current_status():
    element=driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt46"]')
    driver.execute_script("return arguments[0].scrollIntoView();", element)
    driver.save_screenshot('screenshot.png')
    im = Image.open('screenshot.png')
    detail = pytesseract.image_to_string(Image.open('screenshot.png')) 
    d=detail.find("Details")
    note=detail.find("Note")
    print(detail[d:note])
    driver.quit()

def get_captcha():
        
    driver.save_screenshot('screenshot.png')
    element=driver.find_element_by_xpath('//*[@id="form_rcdl:captchaPnl"]/div/div[2]/div/div[2]/table/tbody/tr/td[1]')
    location = element.location    
    size = element.size 
    im = Image.open('screenshot.png') # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    captcha_text = pytesseract.image_to_string(Image.open('screenshot.png'))
    n=captcha_text.find("me ws")
    cp=captcha_text[n+9:n+14].replace("€","e").replace("G","g").replace("P","p").replace("S","5").replace("F","r").replace("é","6").replace("qn","cw")
    return cp

def login():
    enterc=driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt34:CaptchaID"]')
    x=get_captcha()
    enterc.send_keys(x)
    #sleep(6)
    button = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt46"]')
    next=button.get_attribute('onclick')
    button.click()
    sleep(2)
    No_details=check()
    if No_details!=-1:
        print("No details found"+"\n"+"Check the Driving License Number and DoB and try again")
        driver.quit()
        return
    DL1=driver.find_element_by_xpath('//*[@id="form_rcdl:tf_dlNO"]')
    freeze=DL1.get_attribute('aria-disabled')
    
    if freeze=="false":
        error=driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt13"]/div/ul/li/span[2]')
        print(error.get_attribute("innerHTML"))
        error.click()
        driver.quit()
        return
    else:
        current_status()
        return

print("Enter the driving licence number in any of the following formats: DL-1420110012345 or DL14 20110012345"+"\n"+"Total number of input characters should be exactly 16 (including space or '-')."
    +"\n"+"If you hold an old driving license with a different format, please convert the format as per below rule before entering."+"\n"+
    "SS-RRYYYYNNNNNNN OR SSRR YYYYNNNNNNN"+"\n"+
    "Where"+"\n"+
    "SS - Two character State Code (like RJ for Rajasthan, TN for Tamil Nadu etc)"+"\n"+
    "RR - Two digit RTO Code"+"\n"+
    "YYYY - 4-digit Year of Issue (For Example: If year is mentioned in 2 digits, say 99, then it should be converted to 1999. Similarly use 2012 for 12."+"\n"+
"Rest of the numbers are to be given in 7 digits. If there are less number of digits, then additional 0's(zeros) may be added to make the total 7."+"\n"+
"For example: If the Driving Licence Number is RJ-13/DLC/12/ 123456 then please enter RJ-1320120123456 OR RJ13 20120123456.")
DL_num=input()
print("Enter Date of Birth in dd-mm-yyyy")
Date=input()
URL = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
page = requests.get(URL)
driver = webdriver.Chrome()
driver.set_window_position(-10000,0)
driver.get(URL)
#driver.maximize_window() 
DL=driver.find_element_by_xpath('//*[@id="form_rcdl:tf_dlNO"]')
DL.send_keys(DL_num)
DoB=driver.find_element_by_xpath('//*[@id="form_rcdl:tf_dob_input"]')
DoB.send_keys(Date)
login()
