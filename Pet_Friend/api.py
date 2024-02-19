import json.decoder

import requests
import os

class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""
    def __init__(self):
        self.base_url ="https://petfriends.skillfactory.ru/"


    def get_api_key(self,email: str, password: str) ->json:
        """Метод делает запрос к API сервера  по указанным email и паролю и в случае валидных данных
        возвращает статус и результат запроса с уникальным ключом (в формате JSON)"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result= res.text
        return status, result
    def get_list_of_pets(self, auth_key: json, filter: str= "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
            со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
            либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
            собственных питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод -POST отправляет  на сервер данные о добавляемом питомце (в данном случае имя, тип животного,
         возраст и фотографию) и возвращает статус запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # объявляем параметры для выполнения функции (из Swagger в данном случае POST "Add information about new pet"
        # параметрам name, animal type, age, pet_photo присваеваем переменную data
        data =  {
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        }
        # Данные в формате json

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        # также библиотека requests позволяет загружать файли в байтовом формате

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        result = ""


        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        """

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def add_pet_simple_wythout_foto(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод -POST отправляет  на сервер данные о добавляемом питомце (в данном случае имя, тип животного,
         возраст без фотографии) и возвращает статус запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # объявляем параметры для выполнения функции (из Swagger в данном случае POST "Add information about new pet"
        # параметрам name, animal type, age, pet_photo присваеваем переменную data
        data =  {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        # Данные в формате json

        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
