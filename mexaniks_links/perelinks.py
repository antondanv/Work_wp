from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
import pymorphy3

def open_file(filename):
    df = pd.read_csv(filename, sep=';', encoding='utf-8', na_filter=False)
    link = df.loc[0, 'link']
    return link

def search_word(phrase):

    article_titles = [
        "Как выбрать хороший смартфон",
        "Подробное руководство по выбору ноутбука",
        "Секреты эффективного использования Python"
    ]

    # Функция для получения всех форм слова с использованием pymorphy2
    morph = pymorphy3.MorphAnalyzer()

    # Функция для получения всех форм слов в словосочетании
    def get_word_forms(phrase):
        words = phrase.split()
        all_forms = set()
        for word in words:
            parsed_word = morph.parse(word)[0]
            forms = {parsed_word.normal_form}
            forms.update({f.word for f in parsed_word.lexeme})
            all_forms.update(forms)
        return all_forms

    # Функция для поиска словосочетания и его форм в заголовках статей
    def find_article_by_phrase(phrase, article_titles):
        phrase_forms = get_word_forms(phrase)
        for title in article_titles:
            normalized_title = title.lower()  # Приводим к нижнему регистру для удобства сравнения
            found = False
            for form in phrase_forms:
                if form in normalized_title:
                    found = True
                    break
            if found:
                return title
        return None

    # Пример использования:
    article_to_link = find_article_by_phrase(phrase, article_titles)
    if article_to_link:
        print(f"Для слова '{phrase}' подходит статья '{article_to_link}'")
    else:
        print(f"Не удалось найти подходящую статью для словосочетания '{phrase}'")

search_word("смартфоны")

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


