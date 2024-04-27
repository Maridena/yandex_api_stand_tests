# Отдельный файл для чек-листа

import sender_stand_request
import data
import configuration
import requests
import pytest

# функция для создания нового набора (kit) для пользователя с новым именем на основании словаря в data
# и имени из теста
def get_kit_body(name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_kit_body = data.kit_body.copy()
    # изменение значения в поле name
    current_kit_body["name"] = name
    # возвращается новый словарь с нужным значением name
    return current_kit_body


# функция для позитивных тестов (с ответом сервера 201)
def positive_assert(new_kit_name):

    # создаем нового пользователя с данными из data.user_body
    new_user_response = sender_stand_request.post_new_user(data.user_body)

    # сохраняем токен авторизации для нового пользователя
    auth_token = new_user_response.json()["authToken"]
    # проверяем что токен авторизации не пустой
    assert auth_token != ""

    # создаем новый кит для этого пользователя с новым именем набора
    kit_body = get_kit_body(new_kit_name)

    # отправляем запрос на сервер на создание нового набора
    new_kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)

    # проверяем, что код ответа сервера соответствует ожидаемому
    assert new_kit_response.status_code == 201


# функция для негативных тестов (с ответом сервера 400 или отсутствует обязательный параметр name)
def negative_assert(new_kit_name):

    # проверяем на наличие обязательного параметра
    assert new_kit_name != None

    # создаем нового пользователя с данными из data.user_body
    new_user_response = sender_stand_request.post_new_user(data.user_body)

    # сохраняем токен авторизации для нового пользователя
    auth_token = new_user_response.json()["authToken"]
    # проверяем что токен авторизации не пустой
    assert auth_token != ""

    # создаем новый кит для этого пользователя с новым именем набора
    kit_body = get_kit_body(new_kit_name)

    # отправляем запрос на сервер на создание нового набора
    new_kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)

    # проверяем, что код ответа сервера соответствует ожидаемому
    assert new_kit_response.status_code == 400

    # проверяем, что в теле ответа аттрибут code равен 400
    assert new_kit_response.json()["code"] == 400

    assert new_kit_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"


# Test1. Должен проходить.
# Допустимое количество символов в имени 1.
def test_create_user_1_letter_in_first_name_get_success_response():
    positive_assert("а")

# Test2. Должен проходить.
# Допустимое количество символов в имени 511.
def test_create_user_511_letter_in_first_name_get_success_response():
    positive_assert("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc"
            "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcda"
            "bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc"
            "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc"
            "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabC")

# Test3. Не должен проходить.
# Количество символов в имени меньше допустимого (0)
def test_create_user_amount_chars_is_zero_in_first_name_get_negative_response():
    negative_assert("")

# Test4. Не должен проходить.
# Количество символов в имени больше допустимого (512)
def test_create_user_amount_chars_is_bigger_in_first_name_get_negative_response():
    negative_assert("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab"
    "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabc"
    "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc"
    "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc"
    "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

# Test5. Должен проходить.
# Разрешены английские буквы
def test_create_user_english_chars_in_first_name_get_success_response():
    positive_assert("QWErty")

# Test6. Должен проходить.
# Разрешены русские буквы
def test_create_user_russian_chars_in_first_name_get_success_response():
    positive_assert("Мария")

# Test7. Должен проходить.
# Разрешены спецсимволы
def test_create_user_special_chars_in_first_name_get_success_response():
    positive_assert('"№%@","')

# Test8. Должен проходить.
# Разрешены пробелы
def test_create_user_spaces_in_first_name_get_success_response():
    positive_assert("Человек и КО ")

# Test9.Должен проходить.
# Разрешены цифры
def test_create_user_numbers_in_first_name_get_success_response():
    positive_assert("123")

# Test10. Не должен проходить.
# Параметр не передан в запросе
def test_create_user_without_transferred_parametr_in_first_name_get_negative_response():
    negative_assert()

# Test11. Не должен проходить.
# Передан другой тип параметра (число)
def test_create_user_send_number_in_first_name_get_negative_response():
    negative_assert(123)
