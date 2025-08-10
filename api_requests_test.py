import pytest
import allure
from boba_framework.biba_framework import ApiClient
from faker import Faker

def test_api_product_list():
    ApiClient().verify_get_products_list()

def test_post_product_details():
    ApiClient().verify_post_products_list_returns_405()

def test_get_all_brands_list():
    ApiClient().verify_get_all_brands_list()

def test_put_to_all_brands_list():
    ApiClient().verify_put_to_all_brands_list_returns_405()

def test_post_search_product():
    ApiClient().verify_search_product("tshirt")

def test_post_to_search_products_without_search_product_parameter():
    ApiClient().verify_post_without_search_product_param()

def test_create_and_verify_login_delete():
    client = ApiClient()
    email, password = client.post_create_account()
    client.verify_login_with_valid_details(email=email, password=password)
    client.delete_account(email=email, password=password)

def test_login_without_email():
    client = ApiClient()
    client.verify_login_without_email(password="somepassword123")

def test_verify_login_wrong_method():
    client = ApiClient()
    client.verify_login_wrong_method(email="gagaga", password="123123")

def test_verify_login_with_wrong_credentials():
    client = ApiClient()
    client.verify_login_with_wrong_credentials(email="gagaga", password="123123")

def test_create_update_delete_user_account():
    client = ApiClient()
    email, password = client.post_create_account()
    updated_data = {
        "name": client.fake.first_name(),
        "email": email,
        "password": password,
        "title": client.fake.random_element(elements=("Mr", "Mrs", "Miss")),
        "birth_date": str(client.fake.random_int(min=1, max=28)),
        "birth_month": client.fake.month_name(),
        "birth_year": str(client.fake.random_int(min=1950, max=2005)),
        "firstname": client.fake.first_name(),
        "lastname": client.fake.last_name(),
        "company": client.fake.company(),
        "address1": client.fake.street_address(),
        "address2": client.fake.secondary_address(),
        "country": client.fake.country(),
        "zipcode": client.fake.postcode(),
        "state": client.fake.state(),
        "city": client.fake.city(),
        "mobile_number": client.fake.phone_number(),
    }
    client.put_update_account(**updated_data)
    client.delete_account(email=email, password=password)

def test_get_user_detail_by_email():
    client = ApiClient()

    email, password = client.post_create_account()

    data = client.verify_get_user_detail_by_email(email=email)

    assert data["user"]["email"] == email

    client.delete_account(email=email, password=password)


