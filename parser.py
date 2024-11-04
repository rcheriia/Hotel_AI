import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url = "https://ostrovok.ru/hotel/russia/st._petersburg/?q=2042&dates=09.11.2024-10.11.2024&guests=2&price=one&sid=d54f245d-359f-4c24-88c0-e73d6f14e11d"

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8'
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
list_links = soup.find_all('a', class_="zen-hotelcard-name-link")

links = []

for i in list_links:
  lst = str(i).split()
  if len(lst) != 1:
    link = "https://ostrovok.ru" + lst[3][6:-1]
    links.append(link)

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

name_hot = open('dataset.txt', "a", encoding="utf-8")
for url in links:
    n = 0
    com = []
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find_all('h1', class_='HotelHeader_name__hWIU0')[0]
    name = name.prettify()[38:-7]
    num_com = soup.prettify().split('numReviews')
    num_com = int(num_com[1].split(',')[0][2:]) // 10
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    for i in range(num_com-1):
        html_text = soup.prettify()
        html = html_text.split('id"')
        for i in html:
            i = i[34:]
            if 'reviewPlus' in i and "reviewMinus" in i and "wDate" not in i:
                if "orderContext" in i:
                    i = i.replace('&quot;', '"').replace('\\n', '').replace('\\', '')
                    a = i.index('"o')
                    i = '{' + i[:a - 1] + '}'
                k = i.count('"')
                if k > 8:
                    l = i[15:].index('","') + 15
                    i = i[:15] + i[15:l-1].replace('"', '') + i[l - 1: l + 17] + i[l + 17:-1].replace('"', '') + '"}'
                if i[1] != '"':
                    i = '{"' + i[1:]
                i_dict = json.loads(''.join(i))
                if i_dict not in com:
                    com.append(i_dict)
        html_text = soup.prettify()
        ran = html_text.split('TotalRating_content__k5u6S')[3:]
        for i in ran:
            i = i[21:25].replace('\n', '').replace(' ', '')
            if ',' in i:
                i = i[0] + '.' + i[2]
            com[n]["rating"] = i
            n += 1
        button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[1]/div[4]/div[2]/div/div[3]/button')
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(button).click(button).perform()
    driver.close()
    rating = soup.find_all('span', class_='TotalRating_content__k5u6S')[0]
    rating = rating.prettify()[43:46]
    if ',' in rating:
        rating = rating[0] + '.' + rating[2]
    name_hot.write(name + ' | ' + str(rating) + "\n")
    name_file = name + '.txt'
    file = open(name_file, "w", encoding="utf-8")
    for k in range(len(com)-1, -1, -1):
        if "rating" in com[k]:
            file.write(com[k]["reviewPlus"] + com[k]["reviewMinus"] + ' | ' + com[k]["rating"] + '\n')
    file.close()
name_hot.close()