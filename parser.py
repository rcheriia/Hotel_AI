import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.common.action_chains import ActionChains

urls = ['https://www.booking.com/searchresults.ru.html?aid=304142&label=gen173nr-1FCAsoAkIhaG9saWRheS1pbm4tZXhwcmVzcy1kdWJhaS1haXJwb3J0SCFYBGjCAYgBAZgBIbgBF8gBDNgBAegBAfgBAogCAagCA7gC3NSuuQbAAgHSAiQ3Zjc4YWMwNS0xYTI4LTRhOTUtODhjMS0xZmU0NTc4Y2E2YTnYAgXgAgE&sid=656000c26ead80e6573d4ccaa7c12cbd&city=-2334069&',
        'https://www.booking.com/searchresults.ru.html?aid=304142&label=gen173nr-1FCAsoAkIhaG9saWRheS1pbm4tZXhwcmVzcy1kdWJhaS1haXJwb3J0SCFYBGjCAYgBAZgBIbgBF8gBDNgBAegBAfgBAogCAagCA7gC3NSuuQbAAgHSAiQ3Zjc4YWMwNS0xYTI4LTRhOTUtODhjMS0xZmU0NTc4Y2E2YTnYAgXgAgE&sid=656000c26ead80e6573d4ccaa7c12cbd&city=-2334218&',
        'https://www.booking.com/searchresults.ru.html?aid=304142&label=gen173nr-1FCAsoAkIhaG9saWRheS1pbm4tZXhwcmVzcy1kdWJhaS1haXJwb3J0SCFYBGjCAYgBAZgBIbgBF8gBDNgBAegBAfgBAogCAagCA7gC3NSuuQbAAgHSAiQ3Zjc4YWMwNS0xYTI4LTRhOTUtODhjMS0xZmU0NTc4Y2E2YTnYAgXgAgE&sid=656000c26ead80e6573d4ccaa7c12cbd&sb=1&sb_lp=1&src=country&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fcountry%2Fkz.ru.html%3Faid%3D304142%26label%3Dgen173nr-1FCAsoAkIhaG9saWRheS1pbm4tZXhwcmVzcy1kdWJhaS1haXJwb3J0SCFYBGjCAYgBAZgBIbgBF8gBDNgBAegBAfgBAogCAagCA7gC3NSuuQbAAgHSAiQ3Zjc4YWMwNS0xYTI4LTRhOTUtODhjMS0xZmU0NTc4Y2E2YTnYAgXgAgE%26sid%3D656000c26ead80e6573d4ccaa7c12cbd&ss=%D0%A2%D0%B0%D1%88%D0%BA%D0%B5%D0%BD%D1%82%2C+%D0%A3%D0%B7%D0%B1%D0%B5%D0%BA%D0%B8%D1%81%D1%82%D0%B0%D0%BD&is_ski_area=&ssne=%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD&ssne_untouched=%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD&checkin_year=2024&checkin_month=11&checkin_monthday=10&checkout_year=2024&checkout_month=11&checkout_monthday=11&flex_window=0&efdco=1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&search_pageview_id=685286a99199064d&ac_suggestion_list_length=4&ac_suggestion_theme_list_length=0&ac_position=0&ac_langcode=ru&ac_click_type=b&ac_meta=GhA2ODUyODZhOTkxOTkwNjRkIAAoATICcnU6FNCj0LfQsdC10LrQuNGB0YLQsNC9QABKAFAA&dest_id=-2579372&dest_type=city&iata=TAS&place_id_lat=41.3167&place_id_lon=69.25&search_pageview_id=685286a99199064d&search_selected=true&ss_raw=%D0%A3%D0%B7%D0%B1%D0%B5%D0%BA%D0%B8%D1%81%D1%82%D0%B0%D0%BD']

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8'}

sp_p = []

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

links = []
for url in urls:
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    list_links = soup.find_all('a', {"class": "a78ca197d0"})
    html_text = soup.prettify()

    matches = html_text.split("https://www.booking.com/hotel/")
    for match in matches[1:]:
        if 'index.ru.html"' != match.split()[0] and '>' not in match.split()[0]:
            match = "https://www.booking.com/hotel/" + match.split()[0][:-1]
            links.append(match)

csvfile = open('dataset.csv', "a", newline='', encoding='utf-8')
fieldnames = ["review", "rating"]
writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
writer.writeheader()
t = 1
def rev(j):
    review = ''
    if 'Ответ администрации отеля:' in j:
        n = j.index('Ответ администрации отеля:')
    else:
        n = -2
    for i in j[9:n]:
        if 'нашел этот отзыв полезным.' not in i:
            review += ' ' + i
    if 'а' in review and review != 'В данном отзыве отсутствуют комментарии' and 'Показать перевод' not in review:
        return True, review.replace('&quot;', '"').replace('\\n', '').replace('\\', '')
    else:
        return False, None

for url in links:
    url += "#tab-reviews"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    lang = driver.find_element(By.CLASS_NAME, 'ebf4591c8e')
    select = Select(lang)
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    text_n_rev = soup.find('div', {"class": "abf093bdfe f45d8e4c32 d935416c47"}).text
    num_rev = int(''.join([i for i in list(text_n_rev) if i.isdigit()]))
    num_rev = num_rev // 20

    for i in range(num_rev):
        full_reviews = driver.find_elements(By.CLASS_NAME, "d799cd346c")
        for i in full_reviews:
            j = i.text.split('\n')
            if len(j[0]) == 1:
                j = j[1:]
            if 'Популярный отзыв' in j:
                del j[j.index('Популярный отзыв')]
            if '10' != j[8]:
                j[8] = j[8][0]
            if j[8].isdigit():
                rating = int(j[8])
                flag, review = rev(j)

                if flag:
                    list_rev = [{"review": review, "rating": rating}]
                    if list_rev not in sp_p:
                        writer.writerows(list_rev)
                        sp_p.append(list_rev)
        button = driver.find_element(By.XPATH, '//*[@id="reviewCardsSection"]/div[2]/div[1]/div/div/div[3]')
        driver.implicitly_wait(2)
        ActionChains(driver).move_to_element(button).click(button).perform()

    driver.close()
    print(t)
    t += 1
csvfile.close()