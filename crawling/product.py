from selenium                           import webdriver
from pathlib                            import Path
from apscheduler.schedulers.background  import BackgroundScheduler

import os
import sys
import pathlib
import bs4
import logging
import time
import django

FILE_DIR = os.path.abspath(os.path.join(os.path.realpath(__file__), os. pardir))
BASE_DIR = os.path.abspath(os.path.join(os.path.realpath(FILE_DIR), os.pardir))

sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "we_market.settings")
django.setup()

sched = BackgroundScheduler()

from post.models import Post, CrawlProduct

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('window_size=1920x1090')
options.add_argument('disable_gpu')

base_url='https://search.shopping.naver.com/search/all?query='

def Crawling(product):
    url     = base_url+product

    driver  = webdriver.Chrome('crawling/chromedriver', options=options)
    driver.get(url)
    product_source      = bs4.BeautifulSoup(driver.page_source, 'lxml')

    product_info        = product_source.find('div', {'class':"basicList_inner__eY_mq"})
    product_info_list   = product_info.find('ul', {'class':"basicList_mall_list__vIiQw"})
    
    product_info_image      = product_info.find('img')
    product_info_mall_list  = product_info_list.find_all('span', {'class':"basicList_mall_name__1XaKA"})
    product_info_price_list = product_info_list.find_all('span', {'class':"basicList_price__2r23_"})

    driver.close()
    
    CrawlProduct.objects.all().delete()

    if len(product_info_mall_list)<=5:
        MALL_NUM = len(product_info_mall_list)
    else:
        MALL_NUM = 5       

    for post in Post.objects.filter(product__isnull=False):
        for i in range(MALL_NUM):
            crawl, is_created = CrawlProduct.objects.get_or_create(
                    post_id = post.id,    
                    url     = product_info_image['src'],
                    mall    = product_info_mall_list[i].text,
                    price   = int(product_info_price_list[i].text.replace(',', ''))
                    )
            
            if not is_created:
                crawl.url     = product_info_image['src'],
                crawl.mall    = product_info_mall_list[i].text,
                crawl.price   = int(product_info_price_list[i].text.replace(',', ''))
        
products = [post.product for post in Post.objects.all()]

def CrawlingProduct():
    print('start')
    for product in products:
        if product != None:
            Crawling(product)
            print(f'{products.index(product)} is done')
    print('done')

sched.add_job(CrawlingProduct, 'cron', hour='14', minute='03', id='CrawlingProduct')

print('sched start')
sched.start()

while True:
    time.sleep(1)
