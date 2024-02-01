from selenium import webdriver as wb
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.action_chains import ActionChains

# 마우스를 menu 요소 중앙으로 이동한 뒤 hidden_submenu 요소를 클릭하는 것을 실행


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
            pause_time = random.uniform(0.3, 0.6)
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


# f-string
options = Options()
key_count = 0
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
options.add_argument('User-Agent=' + user_agent)
options.add_argument('lang=ko_KR')

options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = wb.Chrome(options=options)

options.add_argument('--start-maximized')


base_url = 'https://m.kinolights.com/discover/explore/'


driver = wb.Chrome(options=options)


try:
    driver.get(base_url)
    time.sleep(2)
except:
    print('drivet.get')
    exit(1)

sample = driver.find_element(By.CSS_SELECTOR,'#contents > section > div.media-type-btn-wrap > div > div > div:nth-child(3) > button')
driver.execute_script("arguments[0].click();", sample)
time.sleep(1)
sample = driver.find_element(By.XPATH,"//*[@id='contents']/section/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/div/button[1]")
driver.execute_script("arguments[0].click();", sample)
time.sleep(1)
sample = driver.find_element(By.XPATH,"//*[@id='applyFilterButton']")
driver.execute_script("arguments[0].click();", sample)
time.sleep(1)

scroll()
movies=driver.find_elements(By.CLASS_NAME,"MovieItem")
print(len(movies))

title_list=[]
href_list=[]
element_list=[]


time.sleep(2)

for movie in movies: #영화리스트를 가져와서 해당 리스트의 영화제목  및 리뷰를 가져올 링크를 저장.

    item = movie.find_element(By.TAG_NAME,'a')
    title = item.get_attribute('title')
    href  = item.get_attribute('href') + '/reviews'
    title_list.append(title)
    href_list.append(href)
df = pd.DataFrame({'titles':title_list,'href':href_list})
df.to_csv('./data/movie_href_data.csv',index=False)

# for list in df['href']:
#     driver.get(list)
#     time.sleep(1.5)
#
#
#     print(30)
#     time.sleep(40)

    # for review in review_lists:
    #     link = review.find_element(By.TAG_NAME,'a')
    #     driver.execute_script("arguments[0].click();", link)
    #     ## 리뷰내용 저장후 back
    #     time.sleep(2)
    #     driver.back()
    #     time.sleep(1)



















#
#     keywords = ['요리']
#     key_num = [0,1, 2, 2, 2, 3, 4, 5, 5, 5, 5, 6]
#     key_label = ['music','game','sports','cook','pets','nature']
#
#     # print(text_list)
#     # for word in text_list:
#     #     class_list.append(word)
#     # random.shuffle(class_list)
#     # print(class_list)
#     #.find_elements(By.CLASS_NAME,'style-scope ytd-rich-grid-media')
#     for word in class_list:
#         if word.text in keywords:
#             label=key_label[key_num[keywords.index(word.text)]]
#             #ActionChains(driver).move_to_element(word).move_by_offset(random.uniform(-10,10),random.uniform(-5,5)).click().perform()
#             word.click()
#             time.sleep(random.uniform(2,3))
#
#             scroll()
#
#             dr_title =driver.find_elements(By.ID,'video-title-link')
#             titleList =[]
#             for list in dr_title:
#                 title = list.find_element(By.ID,'video-title').text
#                 title = re.compile('[^가-힣a-zA-Z]').sub(' ', title)
#                 titleList.append(title)
#
#
#             df_titles = pd.DataFrame()
#             df_section_title = pd.DataFrame(titleList, columns=['titles'])
#             df_section_title['category'] = label
#             df_titles = pd.concat([df_titles, df_section_title], axis='rows', ignore_index=True)
#             print(df_titles.head())
#             df_titles.to_csv('./predict_data/data_{}_{}_{}.csv'.format(label, random.Random(10000),i),index=False)
#             titleList = []
#
#     driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[1]/ytd-topbar-logo-renderer/a/div/ytd-logo/yt-icon/yt-icon-shape/icon-shape/div').click()
#     time.sleep(5)
# driver.close()
#         #     # # print(html)
#     #     #
#         # driver.close()
#         #
        # titleList = []
        # dr_title =driver.find_element(By.ID,'video-title').find_elements(By.CLASS_NAME,'style-scope ytd-rich-grid-media')
        # for content in dr_title:
        #     title = content.text
        #     title = re.compile('[^가-힣a-zA-Z]').sub(' ', title)
        #
        #     titleList.append(title)
        #
        # df_titles = pd.DataFrame()
        # df_section_title = pd.DataFrame(titleList, columns=['titles'])
        # df_section_title['category'] = label
        # df_titles = pd.concat([df_titles, df_section_title], axis='rows', ignore_index=True)
        # df_titles.to_csv('./predict_data/data_{}_{}.csv'.format(label, datetime.datetime.now().strftime('%Y%m%d')),
        #                  index=False)
        #
        # # print(label)






#
#
