from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BagsWD:
    def init(self):
        
        print(Fore.RED + 'Chrome Web Driver '+Fore.YELLOW +self.catalog_link+Fore.RESET)
        chrome_options = webdriver.ChromeOptions()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-notifications")
        #chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def __init__(self, lc_catalog_link):
        self.catalog_link = lc_catalog_link
        self.init()

    def __del__(self):
        try:
            self.driver.quit()
            pass
        except: pass

    def Get_HTML(self, curl):
        self.driver.get(curl)
        return self.driver.page_source

    def Get_List_Of_Links_On_Goods_From_Catalog(self):
        ll = []
        self.Get_HTML(self.catalog_link)
        elements = self.driver.find_elements_by_class_name('product_img_link') 
        print('Количество товаров: ', len(elements))
        for element in elements:
            lc_item_link = element.get_attribute('href')
            print(lc_item_link)
            if lc_item_link not in ll:
                ll.append(lc_item_link)
        return ll


    def Write_To_File(self, cfilename):
        file = open(cfilename, "w", encoding='utf-8')
        file.write(self.driver.page_source)
        file.close()

