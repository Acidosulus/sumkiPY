from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
from bags_driver import *
import colorama
from colorama import Fore, Back, Style


class ob_good:
    def __init__(self, ol:BagsWD, lc_link):
        lc_link = lc_link.replace(r'amp;', '')
        self.pictures = []
        self.sizes = []
        self.prices = []
        self.color = ''
        self.article = ''
        self.name = ''
        self.description= ''
        self.price = ''
        self.brand = ''
        print(Fore.LIGHTGREEN_EX, 'Товар: ', Fore.LIGHTBLUE_EX, lc_link, Fore.RESET)
        ol.Get_HTML(lc_link)
        self.name = ol.driver.find_element_by_xpath("//*[contains(@class,'h1_type_2 h1-back-type')]").text
        self.article = ol.driver.find_element_by_xpath("//*[contains(@class,'js-sku-prod')]").text
        self.brand = sx(sx(ol.driver.page_source, '<br>Бренд: <a itemprop="brand"', '/a>'), '>', '<')
        self.price = (sx(ol.driver.page_source, '<div itemprop="price" content="', '" class="g-none"></div>')+'|').replace('00|', '').replace('|', '')
        #self.price = ol.driver.find_element_by_xpath("//*[contains(@class,'price')]").text.replace('р./шт','').strip()
        self.description = sx(ol.driver.page_source, '<div class="text" itemprop="description">', '<').strip()



        #elements = ol.driver.find_elements_by_xpath("//*[contains(@class,'js-colbox-0 colorbox')]")
        #for element in elements:
        #    lc_picture_link = element.get_attribute('href')
        #    if lc_picture_link not in self.pictures:
        #        self.pictures.append(lc_picture_link)

        #print('Количество картинок:', ol.driver.page_source.count('<img data-colbox="'))

        for i in range(1,ol.driver.page_source.count('<img data-colbox="')+1):
            lc = sx(sx(ol.driver.page_source, '<img data-colbox="', '/>', i), 'src="', '"')
            self.pictures.append(lc)


        elements = ol.driver.find_elements_by_xpath("//*[contains(@class,'name_tb')]")
        #print('Количество размеров:', len(elements))
        for element in elements:
            lc_size = element.text
            if lc_size not in self.sizes and lc_size != 'Наименование':
                self.sizes.append(lc_size)

        for i in range(0, ol.driver.page_source.count('/ <span class="g-t-red">')):
            self.prices.append(sx(ol.driver.page_source, '/ <span class="g-t-red">', '</span>', i+1).replace('р.', '').strip())

        print(Fore.LIGHTGREEN_EX, 'Артикул: ', Fore.LIGHTCYAN_EX, self.article, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Название: ', Fore.LIGHTCYAN_EX, self.name, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Бренд: ', Fore.LIGHTCYAN_EX, self.brand, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Цена: ', Fore.LIGHTCYAN_EX, self.price, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Картинки: ', Fore.LIGHTCYAN_EX, self.pictures, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Описание: ', Fore.LIGHTCYAN_EX, self.description, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Размеры: ', Fore.LIGHTCYAN_EX, self.sizes, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Цены: ', Fore.LIGHTCYAN_EX, self.prices, Fore.RESET)
