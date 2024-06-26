from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random

def open_file(filename):
    df = pd.read_csv(filename, sep=';', encoding='utf-8', na_filter=False)
    link = df.loc[0, 'link']
    return link


def main(link):
    driver = webdriver.Chrome()
    driver.get("https://mexaniks.ru/chto-takoe-med/")
    tag_a = driver.find_elements(By.XPATH, '//header[@class="entry-header "]/following-sibling::div//a')
    spisok_word = []

    for i in tag_a:
        link_a = i.get_attribute("href")
        if link_a == "https://mexaniks.ru/":
            text = i.text
            spisok_word.append(text)

    if not spisok_word:
        print("Слова не найдены")
    else:
        print(spisok_word)

    for word in spisok_word:
        driver.find_element(By.CLASS_NAME, "wp-block-search__input").click()
        for char in word:
            driver.find_element(By.CLASS_NAME, "wp-block-search__input").send_keys(char)
            time.sleep(random.uniform(0.005, 0.20))
        time.sleep(100)


main(" ")
