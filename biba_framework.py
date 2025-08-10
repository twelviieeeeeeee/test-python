import requests
import pytest
import allure
from faker import Faker
from helpers.searchID import SearchAPI

class ApiClient:
    BASE_URL = "https://automationexercise.com/api"
    fake = Faker()

    def get(self, endpoint, **kwargs):
        return requests.get(f"{self.BASE_URL}/{endpoint}", **kwargs)

    def post(self, endpoint, **kwargs):
        return requests.post(f"{self.BASE_URL}/{endpoint}", **kwargs)

    def put(self, endpoint, **kwargs):
        return requests.put(f"{self.BASE_URL}/{endpoint}", **kwargs)

    def delete(self, endpoint, **kwargs):
        return requests.delete(f"{self.BASE_URL}/{endpoint}", **kwargs)

    # ---------- PRODUCTS ----------
    @allure.step("GET /productsList — получение списка продуктов")
    def verify_get_products_list(self):
        response = self.get("productsList")
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
        try:
            data = response.json()
        except ValueError:
            pytest.fail("Ответ не JSON")
        assert "products" in data, "Нет ключа 'products'"
        assert isinstance(data["products"], list), "'products' должен быть списком"

    @allure.step("POST /productsList — проверка, что метод не поддерживается")
    def verify_post_products_list_returns_405(self):
        response = self.post("productsList")
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
        assert "405" in response.text, f"Ожидали '405' в ответе, получили {response.text}"
        assert "This request method is not supported." in response.text, \
            "Нет сообщения о неподдерживаемом методе"

    # ---------- BRANDS ----------
    @allure.step("GET /brandsList — получение списка брендов и поиск ID")
    def verify_get_all_brands_list(self):
        response = self.get("brandsList")
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

        # Используем SearchAPI
        search_instance = SearchAPI(response.text)
        found_ids = search_instance.search_id()
        allure.attach(str(found_ids), "Найденные ID брендов", allure.attachment_type.TEXT)

        try:
            data = response.json()
        except ValueError:
            pytest.fail("Ответ не JSON")

        assert "brands" in data, "Нет ключа 'brands'"
        assert isinstance(data["brands"], list), "'brands' должен быть списком"

    @allure.step("PUT /brandsList — проверка 405 в теле ответа")
    def verify_put_to_all_brands_list_returns_405(self):
        response = self.put("brandsList")
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Ответ не JSON. Текст: {response.text}")

        assert str(data.get("responseCode")) == "405", f"Ожидали 405, получили {data.get('responseCode')}"
        assert "not supported" in data.get("message", "").lower(), \
            f"Ожидали сообщение об ошибке, получили: {data}"

    # ---------- SEARCH ----------
    @allure.step("POST /searchProduct — поиск продукта")
    def verify_search_product(self, search_product):
        payload = {'search_product': search_product}
        response = self.post("searchProduct", data=payload)
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
        data = response.json()
        assert "products" in data, "Нет ключа 'products'"
        assert isinstance(data["products"], list), "'products' должен быть списком"

    @allure.step("POST /searchProduct без параметра — проверка ошибки")
    def verify_post_without_search_product_param(self):
        response = self.post("searchProduct")
        try:
            data = response.json()
            code = data.get("responseCode")
        except ValueError:
            pytest.fail("Ответ не JSON")

        assert str(code) == "400" or "search_product parameter is missing" in response.text.lower(), \
            f"Ожидали ошибку 400 или сообщение об отсутствии параметра, получили: {response.text}"

    # ---------- USERS ----------
    @allure.step("POST /createAccount — создание пользователя")
    def post_create_account(self):
        payload = {
            "name": self.fake.first_name(),
            "email": self.fake.unique.email(),
            "password": self.fake.password(),
            "title": self.fake.random_element(elements=("Mr", "Mrs", "Miss")),
            "birth_date": str(self.fake.random_int(min=1, max=28)),
            "birth_month": self.fake.month_name(),
            "birth_year": str(self.fake.random_int(min=1950, max=2005)),
            "firstname": self.fake.first_name(),
            "lastname": self.fake.last_name(),
            "company": self.fake.company(),
            "address1": self.fake.street_address(),
            "address2": self.fake.secondary_address(),
            "country": self.fake.country(),
            "zipcode": self.fake.postcode(),
            "state": self.fake.state(),
            "city": self.fake.city(),
            "mobile_number": self.fake.phone_number(),
        }

        response = self.post("createAccount", data=payload)
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Ответ не JSON. Текст: {response.text}")

        assert data.get("responseCode") == 201, f"Ожидали 201, получили {data.get('responseCode')}"
        assert "user created" in data.get("message", "").lower(), "Нет сообщения 'User created!'"
        return payload["email"], payload["password"]

    @allure.step("DELETE /deleteAccount — удаление пользователя")
    def delete_account(self, email, password):
        response = self.delete("deleteAccount", data={
            "email": email,
            "password": password
        })
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Ответ не JSON. Текст: {response.text}")

        assert data.get("responseCode") == 200, f"Ожидали 200, получили {data.get('responseCode')}"
        assert "account deleted" in data.get("message", "").lower(), \
            "Нет сообщения 'Account deleted!'"
        return response

    @allure.step("POST /verifyLogin — успешный логин")
    def verify_login_with_valid_details(self, email, password):
        response = self.post("verifyLogin", data={"email": email, "password": password})
        data = response.json()
        assert data.get("responseCode") == 200, f"Ожидали 200, получили {data.get('responseCode')}"
        assert "user exists" in data.get("message", "").lower(), "Нет сообщения 'User exists!'"

    @allure.step("POST /verifyLogin без email — проверка ошибки")
    def verify_login_without_email(self, password):
        response = self.post("verifyLogin", data={"password": password})
        data = response.json()
        assert data.get("responseCode") == 400, f"Ожидали 400, получили {data.get('responseCode')}"
        assert "parameter is missing" in data.get("message", "").lower(), \
            "Нет сообщения о пропущенном параметре"

    @allure.step("DELETE /verifyLogin — проверка неверного метода")
    def verify_login_wrong_method(self, email, password):
        response = self.delete("verifyLogin", data={"email": email, "password": password})
        data = response.json()
        assert data.get("responseCode") == 405, f"Ожидали 405, получили {data.get('responseCode')}"
        assert "not supported" in data.get("message", "").lower(), "Нет сообщения 'not supported'"

    @allure.step("POST /verifyLogin с неверными данными")
    def verify_login_with_wrong_credentials(self, email, password):
        response = self.post("verifyLogin", data={"email": email, "password": password})
        data = response.json()
        assert data.get("responseCode") == 404, f"Ожидали 404, получили {data.get('responseCode')}"
        assert "user not found" in data.get("message", "").lower(), "Нет сообщения 'User not found!'"

    @allure.step("PUT /updateAccount — обновление пользователя")
    def put_update_account(self, **kwargs):
        response = self.put("updateAccount", data=kwargs)
        data = response.json()
        assert data.get("responseCode") == 200, f"Ожидали 200, получили {data.get('responseCode')}"
        assert "user updated" in data.get("message", "").lower(), "Нет сообщения 'User updated!'"
        return response

    @allure.step("GET /getUserDetailByEmail — получение пользователя по email")
    def verify_get_user_detail_by_email(self, email):
        response = self.get("getUserDetailByEmail", params={"email": email})
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
        data = response.json()
        assert data.get("responseCode") == 200, f"Ожидали 200, получили {data.get('responseCode')}"
        assert "user" in data, "Нет ключа 'user'"
        assert isinstance(data["user"], dict), "'user' должен быть словарём"
        return data
