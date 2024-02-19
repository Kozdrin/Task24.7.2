import os
from api import PetFriends
from  settings import valid_email,valid_password


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Проверка запроса api ключа и в результате получаем key, отправляем данные email и пароль '''
    # сохраняем ответ со статусом кода от сервера в result
    status, result = pf.get_api_key(email,password)
    # сверяем полученные данные с ожидаемыми c помощью метода assert
    assert status == 200
    assert  'key' in result


def test_get_all_pets_with_valid_key(filter= ''):
    '''Проверка списка питомцев (питомцы есть, больше 0),
    значение параметра filter - 'my_pets' либо '''''

    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # запрашиваем используя полученный ключ список питомцев "pf.get_list_of_pets(auth_key, filter)"
    status, result = pf.get_list_of_pets(auth_key, filter)

    # сверяем полученные данные с ожидаемыми c помощью метода assert
    assert  status == 200
    print(result['pets'])
    assert  len(result['pets'])>0

def test_add_new_pet_with_valid_key(name='Федя', animal_type='кот', age='2', pet_photo= 'images/Fedya.jpeg'):
    '''Проверка возможности добавления питомца с корректными данными :name='', animal_type='', age='', pet_photo='папка/название файла' '''

    # Получаем путь до файла с картинкой "os.path.join(os.path.dirname(__file__), pet_photo)", сохраняем в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)
    # сверяем полученные данные по имени питомца (name) с ожидаемыми c помощью метода assert
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Fedya.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    print(my_pets)
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Fedor', animal_type='котопес', age=95):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Негативный тест на проверку ввода некорректных данных email и  password


def test_get_api_key_for_invalid_user(email="kooodff@ya.ru", password="3455387"):
    '''Проверка запроса api ключа и в результате получаем key, отправляем данные email и пароль '''
    # сохраняем ответ со статусом кода от сервера в result
    status, result = pf.get_api_key(email,password)
    # сверяем полученные данные с ожидаемыми c помощью метода assert
    assert status == 200
    assert  'key' in result
    #Выводится ошибка 403




def test_add_new_pet_with_age_letter(name='Федя', animal_type='кот', age='пять', pet_photo= 'images/Fedya.jpeg'):
    '''Проверка невозможности добавления питомца с некорректным вводом age не цифра а буква , этот тест в нашем случае проходит со
    мтатусом 200, поэтому в ожидаемых пезультатах мы написали не равно статусу 200 и не равно возрасту ЭТО БАГ API'''

    # Получаем путь до файла с картинкой "os.path.join(os.path.dirname(__file__), pet_photo)", сохраняем в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)
    # сверяем полученные данные по имени питомца (name) с ожидаемыми c помощью метода assert статус код должен быть 4ХХ , реализуем проверку через не равно 200
    assert status != 200
    assert result['age'] != age

def test_add_new_pet_without_argument_pet_photo(name='Вася', animal_type='Кот', age='5', pet_photo= ''):
    '''Проверка невозможности добавления питомца ,без аргумента pet_photo '''

    # Получаем путь до файла с картинкой "os.path.join(os.path.dirname(__file__), pet_photo)", сохраняем в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)
    # сверяем полученные данные по имени питомца (name) с ожидаемыми c помощью метода assert статус код должен быть 4ХХ , реализуем проверку через не равно 200

    assert status == 200
    assert result['name'] == name
    # Выводится ошибка: FileNotFoundError: [Errno 2] No such file or directory:

def test_add_new_pet_without_argument_name_animal_type_age(name='', animal_type='', age='', pet_photo= 'images/Fedya.jpeg'):
    '''Проверка невозможности добавления питомца ,без аргументов name, animal_type, age ,но с аргументом pet_photo
     В данном тесте присутствует БАГ - возможно добавить животное только с картинкой без других аргументов,'''

    # Получаем путь до файла с картинкой "os.path.join(os.path.dirname(__file__), pet_photo)", сохраняем в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)
    # сверяем полученные данные по имени питомца (name) с ожидаемыми c помощью метода assert статус код должен быть 4ХХ , реализуем проверку через не равно 200

    assert status != 200
    assert result['name'] != name




def test_add_pet_simple_wythout_foto(name='Гена', animal_type='крокодил', age='67'):
    '''Проверка добавления питомца без фотографии '''
    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_pet_simple_wythout_foto(auth_key, name, animal_type, age)
    # сверяем полученные данные по имени питомца (name) с ожидаемыми c помощью метода assert статус код должен быть 4ХХ , реализуем проверку через не равно 200

    assert status == 200
    assert result['name'] == name

def test_add_pet_simple_without_arg(name='', animal_type='', age=''):
    '''Проверка добавления питомца без фотографии  без ввода name, animal_type, age
    '''
    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_pet_simple_wythout_foto(auth_key, name, animal_type, age)
    # сверяем полученные данные по имени питомца (name) с ожидаемыми c помощью метода assert статус код должен быть 4ХХ , реализуем проверку через не равно 200
# В тесте присутствует БАГ - возможно дабавить животное без аргументов, поэтому в ожидаемых результатах делаю условие не равно
    assert status != 200
    assert result['name'] != name

def test_add_new_pet_with_another_format_data_images(name='Саша', animal_type='собака', age='38', pet_photo= 'images/sobak.gif'):
    '''Проверка возможности добавления питомца с некорректным форматом файла (gif) pet_photo корректными данными :name='', animal_type='', age='' '''

    # Получаем путь до файла с картинкой "os.path.join(os.path.dirname(__file__), pet_photo)", сохраняем в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)
    # тест проходит, картинка не отображается на сайте -Это БАГ, ожидаем данные ошибка 415 «неподдерживаемый тип данных»
    assert status == 415
    assert result['name'] == name























