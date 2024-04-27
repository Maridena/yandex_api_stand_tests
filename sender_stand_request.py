# файл для POST-запросов

import configuration
import requests
import data

# Функция для POST-запроса на создание нового пользователя
# один параметр - body, для тела запроса
def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)


# Функция для POST-запроса на создание нового набора.
# Два параметра: kit_body — тело запроса, auth_token — токен авторизации.
def post_new_client_kit(kit_body, auth_token):
    # создаем новый заголовок для запроса с сохраненным ранее авторизационным токеном
    headers_new = data.headers.copy()
    headers_new["Authorization"] = "Bearer " + auth_token

    # возвращаем запрос
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_NEW_KIT,
                         json=kit_body,
                         headers=headers_new)