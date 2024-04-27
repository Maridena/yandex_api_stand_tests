#Весь чек-лист нужно писать в отдельном файле. Его можно назвать create_kit_name_kit_test.py .
import sender_stand_request
import data
import configuration
import pytest

# 1 создаем пользователя и получаем токен авторизации
# 2 создаем кит для этого пользователя
# 3 проверяем создался ли кит и если да, то есть ли отличия от ожидаемого результата

def test_positive_assert_1(kit_body):
    post_new_user_response = sender_stand_request.post_new_user(data.user_body);
    # Проверяется, что пользователь создался (ответ сервера == 201)
    assert post_new_user_response.status_code == 201
    print(post_new_user_response.status_code)
    print(post_new_user_response.json())


    #сохраняем токен авторизации
    auth_token_test = post_new_user_response.json()["authToken"]

    # Проверяется, что токен не пустой
    assert auth_token_test!= ""
    print(auth_token_test)

    # создаем кит для пользователя
    post_new_client_kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token_test)

    # Проверяется, что кит для пользователя создался (ответ сервера == 201)
    assert post_new_client_kit_response.status_code == 201
    print(post_new_client_kit_response.status_code)
    print(post_new_client_kit_response.json())

    dict = {"name": "a"}

test_positive_assert_1(dict)

