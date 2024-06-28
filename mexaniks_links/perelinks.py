from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
import pymorphy3
import csv
from Redact_WP import posting

def open_file_title(filename_title):
    try:
        # Читаем CSV-файл с помощью Pandas
        df = pd.read_csv(filename_title, delimiter=';', encoding='utf-8')

        # Создаем словарь из двух столбцов
        dictionary_title = dict(zip(df['title'], df['link']))

        # Выводим полученный словарь
        # print(dictionary)

    except pd.errors.EmptyDataError:
        print(f"Ошибка: файл {filename_title} пустой или не содержит данных.")
    except FileNotFoundError:
        print(f"Ошибка: файл {filename_title} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла {filename_title}: {e}")
    return dictionary_title

def open_file_keywords(filename_keywords):
    try:
        # Читаем CSV-файл с помощью Pandas
        df = pd.read_csv(filename_keywords, delimiter=';', encoding='utf-8')

        # Создаем словарь из двух столбцов
        dictionary_keywords = dict(zip(df['id'], df['keywords']))

        # Выводим полученный словарь


    except pd.errors.EmptyDataError:
        print(f"Ошибка: файл {filename_keywords} пустой или не содержит данных.")
    except FileNotFoundError:
        print(f"Ошибка: файл {filename_keywords} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла {filename_keywords}: {e}")
    return dictionary_keywords

def search_word(filename_title, filename_keywords):

    # article_titles = [
    #     "Как выбрать хороший смартфон",
    #     "Подробное руководство по выбору ноутбука",
    #     "Секреты эффективного использования Python"
    # ]
    dictionary_title = open_file_title(filename_title)
    dictionary_keywords = open_file_keywords(filename_keywords)

    # Получаем все заголовки статей из словаря
    article_titles = list(dictionary_title.keys())
    phrase_all = list(dictionary_keywords.values())

    def get_key(d, value):
        for k, v in d.items():
            if v == value:
                return k
    for phrase_str in phrase_all:
        slova = {}
        phrase_id = get_key(dictionary_keywords, phrase_str)
        phrase_list = phrase_str.split(",")
        count = 0
        for phrase in phrase_list:
            count += 1
            #Функция для получения всех форм слова с использованием pymorphy2
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
            if len(phrase.split(" ")) == 1:
                pass
            else:
                with open('keyword_question_mexaniks.csv', 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow(
                        [phrase_id, phrase])
            if article_to_link:
                print(f"Для слова '{phrase}' подходит статья '{article_to_link}'")
                slova[phrase] = dictionary_title[article_to_link]
            else:
                print(f"Не удалось найти подходящую статью для словосочетания '{phrase}'")
                with open('keyword_mexaniks.csv', 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow([phrase_id, phrase])
        posting(slova, phrase_id, count)


search_word('Title_Link.csv', 'ID_key.csv')
#
#
# def main(link):
#     driver = webdriver.Chrome()
#     driver.get("https://mexaniks.ru/chto-takoe-med/")
#     tag_a = driver.find_elements(By.XPATH, '//header[@class="entry-header "]/following-sibling::div//a')
#     spisok_word = []
#
#     for i in tag_a:
#         link_a = i.get_attribute("href")
#         if link_a == "https://mexaniks.ru/":
#             text = i.text
#             spisok_word.append(text)
#
#     if not spisok_word:
#         print("Слова не найдены")
#     else:
#         print(spisok_word)
#
#     for word in spisok_word:
#         driver.find_element(By.CLASS_NAME, "wp-block-search__input").click()
#         for char in word:
#             driver.find_element(By.CLASS_NAME, "wp-block-search__input").send_keys(char)
#             time.sleep(random.uniform(0.005, 0.20))
#         time.sleep(100)
# def open_file_title(filename_title):
#     try:
#         df = pd.read_csv(filename_title, delimiter=';', encoding='utf-8')
#         dictionary_title = dict(zip(df['title'], df['link']))
#         return dictionary_title
#     except pd.errors.EmptyDataError:
#         print(f"Ошибка: файл {filename_title} пустой или не содержит данных.")
#     except FileNotFoundError:
#         print(f"Ошибка: файл {filename_title} не найден.")
#     except Exception as e:
#         print(f"Произошла ошибка при чтении файла {filename_title}: {e}")
#     return {}
#
#
# def open_file_keywords(filename_keywords):
#     try:
#         df = pd.read_csv(filename_keywords, delimiter=';', encoding='utf-8')
#         dictionary_keywords = dict(zip(df['id'], df['keywords']))
#         return dictionary_keywords
#     except pd.errors.EmptyDataError:
#         print(f"Ошибка: файл {filename_keywords} пустой или не содержит данных.")
#     except FileNotFoundError:
#         print(f"Ошибка: файл {filename_keywords} не найден.")
#     except Exception as e:
#         print(f"Произошла ошибка при чтении файла {filename_keywords}: {e}")
#     return {}
#
#
# def search_word(phrase, filename_title, filename_keywords):
#     try:
#         # Читаем заголовки и ключевые слова из файлов
#         dictionary_title = open_file_title(filename_title)
#         dictionary_keywords = open_file_keywords(filename_keywords)
#
#         # Получаем все заголовки статей из словаря
#         article_titles = list(dictionary_title.keys())
#
#         # Функция для получения всех форм слова с использованием pymorphy2
#         morph = pymorphy3.MorphAnalyzer()
#
#         # Функция для получения всех форм слов в словосочетании
#         def get_word_forms(phrase):
#             words = phrase.split()
#             all_forms = set()
#             for word in words:
#                 parsed_word = morph.parse(word)[0]
#                 forms = {parsed_word.normal_form}
#                 forms.update({f.word for f in parsed_word.lexeme})
#                 all_forms.update(forms)
#             return all_forms
#
#         # Функция для поиска словосочетания и его форм в заголовках статей
#         def find_article_by_phrase(phrase, article_titles):
#             phrase_forms = get_word_forms(phrase)
#             for title in article_titles:
#                 normalized_title = title.lower()  # Приводим к нижнему регистру для удобства сравнения
#                 found = False
#                 for form in phrase_forms:
#                     if form in normalized_title:
#                         found = True
#                         break
#                 if found:
#                     return title
#             return None
#
#         # Пример использования:
#         article_to_link = find_article_by_phrase(phrase, article_titles)
#         if article_to_link:
#             link = dictionary_title.get(article_to_link)
#             keywords = dictionary_keywords.get(link)
#             print(f"Для слова '{phrase}' подходит статья '{article_to_link}' с ключевыми словами: {keywords}")
#         else:
#             print(f"Не удалось найти подходящую статью для словосочетания '{phrase}'")
#
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#
#
# # Пример использования функции search_word с указанием файлов
# search_word("эффективное использование Python", "titles.csv", "keywords.csv")

