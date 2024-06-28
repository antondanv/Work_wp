# import requests
#
# # Адрес вашего сайта WordPress и путь к REST API
# base_url = 'http://example.com/wp-json/wp/v2/posts/'
# post_id = 123  # ID поста, который вы хотите отредактировать
#
# # Заголовки для авторизации и установки типа контента
# headers = {
#     'Authorization': 'Bearer ваш_токен_доступа',  # Или 'Authorization': 'Basic base64_строка_логин:пароль'
#     'Content-Type': 'application/json',
# }
#
# # Новые данные для поста
# new_post_data = {
#     'title': 'Новый заголовок поста',
#     'content': 'Новый текст поста',
# }
#
# # Отправка PATCH запроса для редактирования поста
# response = requests.patch(base_url + str(post_id), headers=headers, json=new_post_data)
#
# # Проверка успешности запроса
# if response.status_code == 200:
#     print('Пост успешно отредактирован.')
# else:
#     print('Ошибка при редактировании поста:', response.status_code)
#     print(response.text)
import requests
import re
from bs4 import BeautifulSoup
from colorama import init, Fore
import json

def posting(links_to_replace, post_id, count):
    # Функция для получения содержимого поста по id
    def get_post_content(post_id, base_url, headers):
        url = f"{base_url}/wp-json/wp/v2/posts/{post_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            post_data = response.json()
            return post_data.get('content', {}).get('rendered', '')
        else:
            print(f"Failed to retrieve post (ID: {post_id}). Status code: {response.status_code}")
            return None
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL21leGFuaWtzLnJ1IiwiaWF0IjoxNzE5NTU5OTE3LCJuYmYiOjE3MTk1NTk5MTcsImV4cCI6MTcyMDE2NDcxNywiZGF0YSI6eyJ1c2VyIjp7ImlkIjoiMSJ9fX0.zWRRKXbJCb5OnJipKcfBkkKPFKl1fYsG_2K2REtSgL0"
    def check_token_validity(token):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
        }
        response = requests.get('https://mexaniks.ru/wp-json/wp/v1', headers=headers)

        if response.status_code in (401, 403, 400):  # Обычно 401 код говорит о проблемах с аутентификацией
            print("Токен недействителен. Пожалуйста, поменяйте токен.")
            exit()
        else:
            pass


    # Функция для замены ссылок в содержимом поста
    # Функция для замены ссылок в содержимом поста с использованием BeautifulSoup
    def replace_links_in_post(post_content, links_to_replace):
        soup = BeautifulSoup(post_content, 'html.parser')
        for text, new_url in links_to_replace.items():
            # Находим все теги <a> с указанным текстом
            for tag in soup.find_all('a', text=text):
                # Заменяем значение атрибута href
                tag['href'] = new_url
        return str(soup)



    # Настройки вашего WordPress сайта
    base_url = 'https://mexaniks.ru'
     # ID вашего поста, который нужно обновить

    # Заголовки для авторизации или любой другой необходимой аутентификации
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
        # Добавьте сюда любые другие заголовки, необходимые для аутентификации или авторизации
    }

    # Словарь с текстами и новыми ссылками для замены
    # links_to_replace = {
    #     "животноводстве": "https://mexaniks.ru/kakie-sushhestvuyut-vidy-selskohozyajstvennyh-uslug/",
    #     "разведению коз": "https://mexaniks.ru/kakie-sushhestvuyut-vidy-selskohozyajstvennyh-uslug/",
    #     "соевых бобах": "https://mexaniks.ru/kakie-sushhestvuyut",
    #     "окунь": "https://mexaniks.ru/kakie-sushhestvuyut-vidy",
    #     "сома": "https://mexaniks.ru/kakie-kultury-vyrashhivayut-v-afrike/",
    # Получаем содержимое поста
    check_token_validity(token)
    post_content = get_post_content(post_id, base_url, headers)
    if post_content:
        # Заменяем ссылки в содержимом поста
        updated_post_content = replace_links_in_post(post_content, links_to_replace)
        # Новые данные для поста
        new_post_data = {
            'content': updated_post_content,
        }
        url = f"{base_url}/wp-json/wp/v2/posts/{post_id}"
        # Отправка PATCH запроса для редактирования поста
        response = requests.patch(url, headers=headers, json=new_post_data)

        # Проверка успешности запроса
        if response.status_code == 200:
            result_request = json.loads(response.text)
            print(Fore.GREEN + f'Пост {count} успешно отредактирован.', result_request["link"])
        else:
            print('Ошибка при редактировании поста:', response.status_code)
            print(response.text)
    else:
        print(f"Failed to get content for post ID {post_id}")