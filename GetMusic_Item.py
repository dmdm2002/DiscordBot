from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("headless")


def get_item(key):
    url = f'https://www.youtube.com/results?search_query={key}'

    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    datas = soup.select('a#video-title')

    name_list = []
    url_list = []

    for i in range(5):
        name_list.append(datas[i].text.strip())
    for i in range(5):
        temp = datas[i]
        url_list.append(f"https://www.youtube.com{temp.get('href')}")

    youtubeDic = {
        '제목': name_list,
    }

    youtubeDf = pd.DataFrame(youtubeDic)
    print(youtubeDf)

    return youtubeDf, url_list
