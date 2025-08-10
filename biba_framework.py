from http.client import responses

import requests
import pytest
import allure
from faker import Faker

class ApiClient:
    BASE_URL = "https://automationexercise.com/api"
    fake = Faker()

    def get(self, endpoint, **kwargs):
        return requests.get(f"{self.BASE_URL}/{endpoint}", **kwargs)

    def post(self, endpoint, **kwargs):
        return requests.post(f"{self.BASE_URL}/{endpoint}", **kwargs)

    def put(self, endpoint, **kwargs):
        return requests.put(f"{self.BASE_URL}/{endpoint}", **kwargs)

    @allure.step("GET /productsList и проверка ответа")
    def verify_get_products_list(self):
        response = self.get("productsList")
        assert response.status_code == 200, f"Ожидали 200, а получили {response.status_code}"
        data = None
        try:
            data = response.json()
        except ValueError:
            pytest.fail("Ответ не является JSON")
        assert "products" in data, "Ключ 'products' отсутствует"
        assert isinstance(data["products"], list), "'products' должен быть списком"

    @allure.step("POST /productsList и проверка, что метод не поддерживается")
    def verify_post_products_list_returns_405(self):
        response = self.post("productsList", json={})
        assert response.status_code == 405 or "not supported" in response.text.lower(), \
            f"Ожидали 405 или текст ошибки, получили: {response.status_code}, тело: {response.text}"

    @allure.step("GET /brandsList и проверка структуры")
    def verify_get_all_brands_list(self):
        response = self.get("brandsList")
        assert response.status_code == 200, f"Ожидали 200, а получили {response.status_code}"
        try:
            data = response.json()
        except ValueError:
            pytest.fail("Ответ не является JSON")
        assert "brands" in data, "Ключ 'brands' отсутствует"
        assert isinstance(data["brands"], list), "'brands' должен быть списком"

    @allure.step("PUT /brandsList и проверка ошибки в теле ответа (responseCode 405)")
    def verify_put_to_all_brands_list_returns_405(self):
        response = self.put("brandsList")
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Ответ не является JSON. Текст: {response.text}")

        assert str(data.get("responseCode")) == "405", \
            f"Ожидали responseCode 405 в теле, получили: {data.get('responseCode')}, тело: {data}"

        assert "not supported" in data.get("message", "").lower(), \
            f"Ожидали сообщение об ошибке, получили: {data}"

    @allure.step("POST /searchProduct с валидным параметром")
    def verify_search_product(self, search_product):
        payload = {'search_product': search_product}
        response = self.post("searchProduct", data=payload)
        assert response.status_code == 200, f"Ожидали 200, а получили {response.status_code}"
        data = response.json()
        assert "products" in data, "Ключ 'products' отсутствует"
        assert isinstance(data["products"], list), "'products' должен быть списком"

    @allure.step("POST /searchProduct без параметров — проверка ошибки в теле (missing param)")
    def verify_post_without_search_product_param(self):
        response = self.post("searchProduct")

        try:
            data = response.json()
            code = data.get("responseCode")
        except ValueError:
            data = None
            code = None

        assert str(code) == "400" or "search_product parameter is missing" in response.text.lower(), \
            f"Ожидали ошибку 400 или текст об отсутствии параметра, получили: {response.text}"

    @allure.step("POST /verifyLogin — проверка успешного логина")
    def verify_login_with_valid_details(self, email, password):
        response = requests.post(f"{self.BASE_URL}/verifyLogin", data={
            "email": email,
            "password": password
        })

        data = response.json()

        assert data.get("responseCode") == 200, \
            f"VerifyLogin: ожидали responseCode 200, получили {data.get('responseCode')}"

        assert "user exists" in data.get("message", "").lower(), \
            f"VerifyLogin: ожидали 'User exists!', получили: {data.get('message')}"

    @allure.step("POST /createAccount — создание нового пользователя с фейковыми данными")
    def post_create_account(self):
        name = self.fake.first_name()
        email = self.fake.unique.email()
        password = self.fake.password()
        title = self.fake.random_element(elements=("Mr", "Mrs", "Miss"))
        birth_date = str(self.fake.random_int(min=1, max=28))
        birth_month = self.fake.month_name()
        birth_year = str(self.fake.random_int(min=1950, max=2005))
        firstname = self.fake.first_name()
        lastname = self.fake.last_name()
        company = self.fake.company()
        address1 = self.fake.street_address()
        address2 = self.fake.secondary_address()
        country = self.fake.country()
        zipcode = self.fake.postcode()
        state = self.fake.state()
        city = self.fake.city()
        mobile_number = self.fake.phone_number()

        response = requests.post(f"{self.BASE_URL}/createAccount", data={
            "name": name,
            "email": email,
            "password": password,
            "title": title,
            "birth_date": birth_date,
            "birth_month": birth_month,
            "birth_year": birth_year,
            "firstname": firstname,
            "lastname": lastname,
            "company": company,
            "address1": address1,
            "address2": address2,
            "country": country,
            "zipcode": zipcode,
            "state": state,
            "city": city,
            "mobile_number": mobile_number
        })

        data = None
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"CreateAccount: ответ не JSON. Текст: {response.text}")

        assert data.get("responseCode") == 201, \
            f"CreateAccount: ожидали responseCode 201, получили {data.get('responseCode')}"

        assert "user created" in data.get("message", "").lower(), \
            f"CreateAccount: ожидали 'User created!', получили: {data.get('message')}"
        return email, password

    @allure.step("DELETE /deleteAccount — удаление пользователя")
    def delete_account(self, email, password):
        response = requests.delete(f"{self.BASE_URL}/deleteAccount", data={
            "email": email,
            "password": password
        })
        data = None
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"DeleteAccount: ответ не JSON. Текст: {response.text}")

        assert data.get("responseCode") == 200, \
            f"DeleteAccount: ожидали responseCode 200, получили {data.get('responseCode')}"

        assert "account deleted" in data.get("message", "").lower(), \
            f"DeleteAccount: ожидали 'Account deleted!', получили: {data.get('message')}"

        return response

    @allure.step("POST /verifyLogin — проверка отсутствия email")
    def verify_login_without_email(self, password):
        response = requests.post(f"{self.BASE_URL}/verifyLogin", data={
            "password": password
        })
        data = None
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"VerifyLogin: ответ не JSON. Текст: {response.text}")

        assert data.get("responseCode") == 400, \
            f"VerifyLogin: ожидали responseCode 400, получили {data.get('responseCode')}"

        assert "parameter is missing" in data.get("message", "").lower(), \
            f"VerifyLogin: ожидали сообщение об отсутствии параметров, получили: {data.get('message')}"

    @allure.step("POST /verifyLogin — проверка неверного метода")
    def verify_login_wrong_method(self, email, password):
        response = requests.delete(f"{self.BASE_URL}/verifyLogin", data={
            "email": email,
            "password": password
        })

        data = response.json()

        assert data.get("responseCode") == 405, \
            f"VerifyLogin: ожидали responseCode 405, получили {data.get('responseCode')}"

        assert "This request method is not supported." in data.get("message", ""), \
            f"VerifyLogin: ожидали 'This request method is not supported!', получили: {data.get('message')}"

    @allure.step("POST /verifyLogin проверка невалидные данные")
    def verify_login_with_wrong_credentials(self, email, password):
        response = requests.post(f"{self.BASE_URL}/verifyLogin", data={
            "email": email,
            "password": password
        })
        data = None
        try:
            data = response.json()
        except ValueError:
            pytest.fail("Ответ не JSON")

        assert data.get("responseCode") == 404, \
            f"VerifyLogin: ожидали responseCode 404, получили {data.get('responseCode')}"

        assert "user not found" in data.get("message", "").lower(), \
            f"VerifyLogin: ожидали 'User not found!', получили: {data.get('message')}"

    @allure.step("PUT /updateAccount — обновление данных пользователя")
    def put_update_account(self, **kwargs):
        response = requests.put(f"{self.BASE_URL}/updateAccount", data=kwargs)
        data = None
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"UpdateAccount: ответ не JSON. Текст: {response.text}")

        assert data.get("responseCode") == 200, \
            f"UpdateAccount: ожидали responseCode 200, получили {data.get('responseCode')}"

        assert "user updated" in data.get("message", "").lower(), \
            f"UpdateAccount: ожидали 'User updated!', получили: {data.get('message')}"

        return response

    @allure.step("GET /getUserDetailByEmail — детали пользователя по email")
    def verify_get_user_detail_by_email(self, email):
        response = requests.get(f"{self.BASE_URL}/getUserDetailByEmail", params={"email": email})

        assert response.status_code == 200, f"Ожидали 200, а получили {response.status_code}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail("Ответ не является JSON")

        assert data.get("responseCode") == 200, \
            f"Ожидали responseCode 200, получили {data.get('responseCode')}"
        assert "user" in data, "Нет ключа 'user' в ответе"
        assert isinstance(data["user"], dict), "'user' должен быть словарём"

        return data

