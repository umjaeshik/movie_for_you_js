from selenium import webdriver as wb
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.action_chains import ActionChains
import re
import random
import time
import pandas as pd


def scroll():
    try:
        # 페이지 내 스크롤 높이 받아오기
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # 임의의 페이지 로딩 시간 설정
            # PC환경에 따라 로딩시간 최적화를 통해 scraping 시간 단축 가능
            pause_time = random.uniform(0.5, 0.6)
            # 페이지 최하단까지 스크롤
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # 페이지 로딩 대기
            time.sleep(pause_time)
            # 무한 스크롤 동작을 위해 살짝 위로 스크롤(i.e., 페이지를 위로 올렸다가 내리는 제스쳐)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
            time.sleep(pause_time)
            # 페이지 내 스크롤 높이 새롭게 받아오기
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            # 스크롤을 완료한 경우(더이상 페이지 높이 변화가 없는 경우)
            if new_page_height == last_page_height:
                print("스크롤 완료")
                break

            # 스크롤 완료하지 않은 경우, 최하단까지 스크롤
            else:
                last_page_height = new_page_height

    except Exception as e:
        print("에러 발생: ", e)




# 속도 향상을 위한 옵션 해제




options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
options.add_argument('User-Agent=' + user_agent)
options.add_argument('lang=ko_KR')

options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}
options.add_experimental_option('prefs', prefs)



options.add_argument('--start-maximized')

movie_reviews = pd.DataFrame()
df = pd.read_csv('./data/movie_href_data.csv')




startnum = 33
review_list=[]

for idx,url in enumerate(df.loc[startnum:1000,'href']):
    driver = wb.Chrome(options=options)
    movie_reviews = pd.DataFrame()
    print(url)
    try:
        driver.get(url)
        time.sleep(1)
    except:
        print('drivet.get(url)')
        continue
    scroll()
    reviews = driver.find_elements(By.CLASS_NAME,'review-item')
    text =' '
    long_review_hrefs=[]

    for review in reviews:

        try:
            text = text + ' ' + review.find_element(By.CLASS_NAME, 'review-title').text
            review.find_element(By.CLASS_NAME, 'more-button-wrap')

        except:
            text = text + ' ' + review.find_element(By.CLASS_NAME, 'review-content').text
            continue
        long_review_hrefs.append(review.find_element(By.CLASS_NAME,'review-content-link').get_attribute('href'))
    print(len(long_review_hrefs))
    for href in long_review_hrefs:
        try:
            driver.get(href)
            time.sleep(0.5)
            text = text + ' ' + driver.find_element(By.CLASS_NAME, 'contents').find_element(By.TAG_NAME, 'p').text
        except:
            print('drivet.get(text)')
            continue
    movie_reviews.loc[idx, 'titles'] = df.loc[idx+startnum, 'titles']
    movie_reviews.loc[idx,'reviews'] = text



# df['reviews']= review_list
    movie_reviews.to_csv('./data/reviews{}.csv'.format(idx+startnum),index=False)
    driver.close()



