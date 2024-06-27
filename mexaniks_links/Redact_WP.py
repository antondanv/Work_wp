import requests

# Адрес вашего сайта WordPress и путь к REST API
base_url = 'http://example.com/wp-json/wp/v2/posts/'
post_id = 123  # ID поста, который вы хотите отредактировать

# Заголовки для авторизации и установки типа контента
headers = {
    'Authorization': 'Bearer ваш_токен_доступа',  # Или 'Authorization': 'Basic base64_строка_логин:пароль'
    'Content-Type': 'application/json',
}

# Новые данные для поста
new_post_data = {
    'title': 'Новый заголовок поста',
    'content': 'Новый текст поста',
}

# Отправка PATCH запроса для редактирования поста
response = requests.patch(base_url + str(post_id), headers=headers, json=new_post_data)

# Проверка успешности запроса
if response.status_code == 200:
    print('Пост успешно отредактирован.')
else:
    print('Ошибка при редактировании поста:', response.status_code)
    print(response.text)