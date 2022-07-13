from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import sqlite3
from os import system
from my_library import *
import sys
from bags_good import *
from bags_driver import BagsWD
import colorama
from colorama import Fore, Back, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#def unload_one_good(lc_link_on_good: str):
#    print(Fore.YELLOW + 'Товар: ' + Fore.BLACK + Back.LIGHTWHITE_EX + lc_link_on_good + Fore.RESET + Back.RESET)
#    lo_good = ob_good(lc_link_on_good)
#    print(Fore.YELLOW + "Артикул: " + Fore.LIGHTGREEN_EX, lo_good.article, Fore.RESET)
#    print(Fore.YELLOW + "Название:" + Fore.LIGHTGREEN_EX, lo_good.name, Fore.RESET)
#    print(Fore.YELLOW + "Размеры:" + Fore.LIGHTGREEN_EX, lo_good.size_list, Fore.RESET)
#    print(Fore.YELLOW + "Цена:" + Fore.LIGHTGREEN_EX, lo_good.price, Fore.RESET)
#    print(Fore.YELLOW + "Цены:" + Fore.LIGHTGREEN_EX, lo_good.prices, Fore.RESET)
#    print(Fore.YELLOW + "Цвета:" + Fore.LIGHTGREEN_EX, lo_good.colors, Fore.RESET)
    #print(Fore.YELLOW + "Описание:" + Fore.LIGHTGREEN_EX, lo_good.description, Fore.RESET)
    #print(Fore.YELLOW + "Картинки:" + Fore.LIGHTGREEN_EX, lo_good.pictures, Fore.RESET)

def unload_item_by_link_into_price(lc_item_link:str, lo:BagsWD, price:Price):
    print(Fore.LIGHTWHITE_EX+'----------------------------------------------------------------------')
    print(Fore.LIGHTYELLOW_EX+'Товар:' + lc_item_link)
    lo.Get_HTML(lc_item_link)
    lo.Write_To_File('item.html')

    try: lc_name = lo.driver.find_element(by=By.TAG_NAME, value='h1').text
    except: lc_name = ''
    print(Fore.LIGHTGREEN_EX+'Название:', Fore.LIGHTCYAN_EX + lc_name)

    try: lc_article = lo.driver.find_element(by=By.CLASS_NAME, value='editable').text
    except: lc_article = ''
    print(Fore.LIGHTGREEN_EX+'Артикул:', Fore.LIGHTCYAN_EX + lc_article)

    try: lc_price = lo.driver.find_element(by=By.ID, value='our_price_display').text.replace('руб','').replace(' ','')
    except: lc_price = ''
    print(Fore.LIGHTGREEN_EX+'Цена:', Fore.LIGHTCYAN_EX + lc_price)

    try: lc_description = lo.driver.find_element(by=By.CLASS_NAME, value='rte').text.replace('\t', ' ').replace('\n',' ').replace(';',' ').replace('"'," ").replace("'",'"')
    except: lc_description = ''
    print(Fore.LIGHTGREEN_EX+'Описание:', Fore.LIGHTCYAN_EX + lc_description)

    ll_pictures = []
    pictures_section = lo.driver.find_element(by=By.ID, value = 'thumbs_list_frame')
    picture_links = pictures_section.find_elements(by=By.TAG_NAME, value='a')
    for picture in picture_links:
        picture_link = picture.get_attribute('href')
        if picture_link not in ll_pictures:
            ll_pictures.append(picture_link)
    print(Fore.LIGHTGREEN_EX+'Картинки:', Fore.LIGHTCYAN_EX, ll_pictures)

    if is_price_have_link(price.file_name, lc_item_link):
        print(Fore.LIGHTRED_EX, 'Товар уже имеется в прайсе:', Fore.YELLOW, g, Fore.RESET)
    else:
        price.add_good('',
                        prepare_str(lc_article).strip() + ' ' + prepare_str(lc_name).strip(),
                        prepare_str(lc_description),
                        prepare_str(lc_price).replace(',', '.'),
                        '15',
                        prepare_str(lc_item_link),
                        prepare_for_csv_non_list(ll_pictures),
                        '')
        price.write_to_csv(price.file_name)  



def unload_catalog_bags(catalog_link:str, lc_filename:str):
    print(Fore.LIGHTWHITE_EX+'======================================================================')
    print(Fore.LIGHTWHITE_EX+'Каталог:' + catalog_link, '  Файл:', lc_filename)
    print(Fore.LIGHTWHITE_EX+'======================================================================',Fore.RESET)
    price = Price(lc_filename+'.csv')
    lo = BagsWD(catalog_link)
    ll_list_links_on_goods = lo.Get_List_Of_Links_On_Goods_From_Catalog()
    ln_counter = 0
    for g in ll_list_links_on_goods:
        ln_counter += 1
        print(Fore.LIGHTRED_EX+'Товар ', ln_counter, ' из ', len(ll_list_links_on_goods))
        unload_item_by_link_into_price(g, lo, price)

colorama.init()

if False:
    catalog_link='https://sumkispb.club/59-aksessuary?id_category=59&n=139&recaptchaResponse=03AGdBq27I5BUpT_jQe6oBhLtiYxQwikUiRaFON2gbsxZ8o3u68U2DLFmXt3sAehBu3axjORDmRWFB_i7p88JA3-MWLfyok0a2nZ8aCNJWdy6LzTe3vicm1lCgSUpqYxCdnZbhAQ1E3Yi9F845Kcm6yvLcCtXn72UlhRzeVBgpCHc1ClbKsRAI4Y5OSSDy1et3DlaYIm-NCKGITt1I6U09eHwmkKM7K_GTL60_Pn0p7hysW1ux5Z8mkTWh5Ih_92-zdcQ9REwY267lxrdDVs4JuU8T7XP3bL-uiiv50OEKvHl-HRfUZ5wc1MxfSlW3Sic4MqgyoeU_Fg-qb3ELhQaXFDQthg7uheNL7waLQgSOIO9mzA-3z0RR7vgUuYQk2f2oqnAeNLOa4OWAixYMrjQpA0PJ6X43xoPcPGEVLRwHT-0zrJ7Kq61_-S1oeCjsNlhfWrI6GVhirn6I5y2xHrJmeB8QyU5L5iFerg'
    lc_filename='g:\sumkiPY\csvs\test.csv'
    price = Price(lc_filename+'.csv')
    lo = BagsWD(catalog_link)
    unload_item_by_link_into_price('https://sumkispb.club/aksessuary/31406-02-002-0851-oblozhka-dpasport.html', lo, price)
    exit()



if sys.argv[1] == 'catalog':
    unload_catalog_bags(sys.argv[2], sys.argv[3])
