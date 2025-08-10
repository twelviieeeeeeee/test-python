import time

import random, string, os
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import pytest

class AutoExercise:
    def __init__(self, driver):
        self.driver = driver

    def generate_random_email(self):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(['example.com', 'testmail.com', 'mail.ru', "gmail.com", "aboba.com"])
        return f"{username}@{domain}"

    def generate_random_username(self):
        first_names = ['John', 'Mira', 'Anton', 'Luna', 'Markus', 'Elena', 'David', 'Sasha', 'Olga', 'Leo']
        last_names = ['Steel', 'Donnelly', 'Cabaleron', 'Foster', 'Ivanov', 'Kuznetsova', 'Torres', 'White', 'Chen',
                      'Ford']
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def open_and_verify (self):
        self.driver.get('https://automationexercise.com/')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='Website for automation practice']"))
        )
        assert self.driver.current_url == 'https://automationexercise.com/'

    def login_page_click_verify(self):
        login_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/login']"))
        )
        login_link.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="signup-form"]'))
        )

    def signup_new_user(self, name, email):
        name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@data-qa='signup-name']"))
        )
        name_field.click()
        name_field.send_keys(name)

        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@data-qa='signup-email']"))
        )
        email_field.click()
        email_field.send_keys(email)

        signup_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@data-qa='signup-button']"))
        )
        signup_button.click()

        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='title text-center']"))
        )
        text = element.text.strip()
        assert text == "ENTER ACCOUNT INFORMATION", f"Текст заголовка отличается: «{text}»"

    def fill_user_info(self, user):
        wait = WebDriverWait(self.driver, 10)
        first_name, last_name = user["name"].split()

        # Title
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='uniform-id_gender1']"))).click()

        # Password
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='password']")))
        password_field.click()
        password_field.send_keys("12345678Aa")

        # Birthdate
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='days']"))).send_keys("15", Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='months']"))).send_keys("Sep", Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='years']"))).send_keys("1984", Keys.ENTER)

        # Checkboxes
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='newsletter']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='optin']"))).click()

        # Address fields
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='first_name']"))).send_keys(first_name)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='last_name']"))).send_keys(last_name)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='company']"))).send_keys("Cabaleron Inc.")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='address1']"))).send_keys("st. Kyiv, д. 69")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='address2']"))).send_keys("st. Obolon, д. 37")

        # Country
        country_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='country']")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", country_field)
        country_field.send_keys("United States", Keys.ENTER)

        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='state']"))).send_keys("-")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='city']"))).send_keys("Sumi")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='zipcode']"))).send_keys("202017")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='mobile_number']"))).send_keys("+69 88 567 84 93")

        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-qa='create-account']"))).click()

        element2 = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='title text-center']"))
        )
        text = element2.text.strip()
        assert text == "ACCOUNT CREATED!", f"Текст заголовка отличается: «{text}»"

    def account_created(self, username):
        cont = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@data-qa='continue-button']"))
        )
        cont.click()

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='nav navbar-nav']"))
        )
        text = element.text.strip()
        assert username in text, f"Ожидали увидеть '{username}' в тексте, но получили: «{text}»"

    def delete_account(self):
        delete = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/delete_account']"))
        )
        delete.click()
        element = WebDriverWait(self.driver, 10).until(
           EC.presence_of_element_located((By.XPATH, "//*[@class='title text-center']"))
        )
        assert element.text.strip() == "ACCOUNT DELETED!", \
            f"Ожидали текст 'ACCOUNT DELETED!', но получили: «{element.text.strip()}»"

        cont = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@data-qa='continue-button']"))
        )
        cont.click()

    def login_into_account(self):
        login = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-email"]'))
        )
        login.click()
        login.send_keys("notidentifieduser@psina.com")

        password = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-password"]'))
        )
        password.click()
        password.send_keys("unidentifiedpassword000")

        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-button"]'))
        )
        login_button.click()

        error = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//p[contains(text(),"incorrect")]'))
        )

    def logout(self):
        logout = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/logout']"))
        )
        logout.click()

    def fill_email_and_name(self, email, name):
        fill_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="signup-name"]'))
        )
        fill_name.clear()
        fill_name.click()
        fill_name.send_keys(name)

        fill_email = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="signup-email"]'))
        )
        fill_email.clear()
        fill_email.click()
        fill_email.send_keys(email)

    def signup_button(self):
        signup = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="signup-button"]'))
        )
        signup.click()

    def contact_us_button(self):
        try:
            xpath = "//a[contains(text(), 'Contact us')]"
            contact = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", contact)

            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            ).click()

        except TimeoutException:
            raise AssertionError("❌ Кнопка 'Contact us' не найдена или не кликабельна.")

    def contact_us_mail(self, user):
        wait = WebDriverWait(self.driver, 10)

        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-qa="name"]'))).send_keys(user.name)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-qa="email"]'))).send_keys(user.email)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-qa="subject"]'))).send_keys("test if working")
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-qa="message"]'))).send_keys("test if working")

        wait.until(EC.presence_of_element_located((By.NAME, 'upload_file'))).send_keys(
            os.path.abspath(r"C:\Users\avere\PycharmProjects\test-selenium\utils\test_image.png")
        )

        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-qa="submit-button"]'))).click()

        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))).click()

    def login_button(self):
        login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@data-qa="login-button"]'))
        )
        login.click()

    def login_into_account_existing(self):
            login = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-email"]'))
            )
            login.click()
            login.send_keys("antoniobandera@gmail.com")

            password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-password"]'))
            )
            password.click()
            password.send_keys("12345678Aa")

    def error_user(self):
        error = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Email Address already exist")]')
            )
        )

        assert "Email Address already exist" in error.text

    def cases_test(self):
        cases = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/test_cases"]'))
        )
        cases.click()

    def products_test(self):
        products = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/products"]'))
        )
        products.click()

    def all_products_verified(self):
        all_products = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="title text-center"]'))
        )
        assert all_products.is_displayed(), "'All Products' title not visible"

    def details(self):
        scroll = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/product_details/21"]'))
        )

        self.driver.execute_script("""
                arguments[0].scrollIntoView({behavior: 'auto', block: 'start'});
                window.scrollBy(0, 100);
            """, scroll)

        view_product = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/product_details/18"]'))
        )
        view_product.click()

        name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Little Girls Mr. Panda Shirt')]"))
        )
        assert name.is_displayed(), "Product name is not displayed"

        category = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Category: Kids > Tops & Shirts')]"))
        )
        assert category.is_displayed(), "Category is not displayed"

        price = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Rs. 1200')]"))
        )
        assert price.is_displayed(), "Price is not displayed"

        availability = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//b[contains(text(), 'Availability')]"))
        )
        assert availability.is_displayed(), "Availability is not displayed"

        condition = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//b[contains(text(), 'Condition')]"))
        )
        assert condition.is_displayed(), "Condition is not displayed"

        brand = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//b[contains(text(), 'Brand')]"))
        )
        assert brand.is_displayed(), "Brand is not displayed"

    def fill_email_and_password(self, email, password):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-email"]'))
        )
        email_input.click()
        email_input.send_keys(email)  # <-- используем переданный параметр

        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-password"]'))
        )
        password_input.click()
        password_input.send_keys(password)  # <-- используем переданный параметр

        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-button"]'))
        )
        login_button.click()

    def search_products(self):
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_product"))
        )
        search_input.click()
        search_input.send_keys("Little Girls Mr. Panda Shirt")

        button_search = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit_search"))
        )
        button_search.click()

        searched_products = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="title text-center"]'))
        )
        assert searched_products.is_displayed(), "Search products is not displayed"

    def products(self):
        products_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_button.click()

    def scroll_to_footer(self):
        footer = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "footer-bottom"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", footer)

        subscription = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Subscription']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", subscription)

        email_address = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "susbscribe_email"))
        )
        email_address.click()
        email_address.send_keys(self.generate_random_email())

        submit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "subscribe"))
        )
        submit.click()

        successfully = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="alert-success alert"]'))
        )
        assert successfully.is_displayed(), 'You have been successfully subscribed!'

    def cart_button(self):
        cart_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/view_cart']"))
        )
        cart_button.click()

    def footer(self):
        footer = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "footer-bottom"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", footer)

    def subscription(self):
        subscription = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Subscription']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", subscription)

        email_address = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "susbscribe_email"))
        )
        email_address.click()
        email_address.send_keys("ilikehotgirls@trump.com")

        submit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "subscribe"))
        )
        submit.click()

        successfully = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="alert-success alert"]'))
        )
        assert successfully.is_displayed(),  'You have been successfully subscribed!'

    def product_add_to_cart(self):
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-product-id="1"]'))
        )
        add_to_cart_button.click()

        continue_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue Shopping"]'))  # пример
        )
        continue_button.click()

        second_product_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-product-id="2"]'))
        )
        second_product_button.click()

        view_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//u[text()="View Cart"]'))
        )
        view_cart_button.click()

        price = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="price"]'))
        )
        assert price.is_displayed(), 'Price'

        quantity = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="quantity"]'))
        )
        assert quantity.is_displayed(), 'Quantity'

        total = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="total"]'))
        )
        assert total.is_displayed(), 'Total'

    def view_cart_button(self):
        view_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//u[text()="View Cart"]'))
        )
        view_cart_button.click()

    def view_product_button(self):
        view_product_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/product_details/1']"))
        )
        view_product_button.click()

    def increase_quantity_to_4(self):
        increase_quantity_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "quantity"))
        )
        increase_quantity_button.click()
        increase_quantity_button.clear()
        increase_quantity_button.send_keys("4")

    def add_to_cart_button(self):
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]'))
        )
        add_to_cart_button.click()

    def verify_product_quantity(self, expected_quantity):
        quantity_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="cart_quantity"]'))
        )

        actual_quantity = quantity_element.text.strip()
        assert actual_quantity == str(
            expected_quantity), f'❌ Expected quantity: {expected_quantity}, but found: {actual_quantity}'

    def add_to_cart(self):
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-default cart"]'))
        )
        add_to_cart_button.click()

        view_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//u[text()="View Cart"]'))
        )
        view_cart_button.click()

    def click_on_white_space(self):
        white_space_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(white_space_button, 10, 10).click().perform()

    def verify_homepage(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='Website for automation practice']"))
        )
        assert self.driver.current_url == 'https://automationexercise.com/'

    def login_verify(self):
        login_verify = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h2[normalize-space()='Login to your account']")
            )
        )
        assert login_verify.is_displayed(), "'Login to your account' is not displayed"

    def account_deleted(self):
        element = WebDriverWait(self.driver, 10).until(
           EC.presence_of_element_located((By.XPATH, "//*[@class='title text-center']"))
        )
        assert element.text.strip() == "ACCOUNT DELETED!", \
            f"Ожидали текст 'ACCOUNT DELETED!', но получили: «{element.text.strip()}»"

    def proceed_to_checkout(self):
        proceed_to_checkout_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="btn btn-default check_out"]'))
        )
        proceed_to_checkout_button.click()

    def cart_verify(self):
        cart_verify = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li.active'))
        )
        assert cart_verify.is_displayed(), 'Cart is not displayed'

    def login_register_in_cart(self):
        login_register_in_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//u[text()="Register / Login"]'))
        )
        login_register_in_cart.click()

    def address_details(self):
        address_details = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2[contains(text(), "Address Details")]'))
        )
        assert address_details.is_displayed(), 'Address details is not displayed'

    def review_your_order(self):
        review_your_order_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2[contains(text(), "Review Your Order")]'))
        )
        assert review_your_order_button.is_displayed(), 'Review Your Order is not displayed'

    def comment(self):
        text_area = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.form-control'))
        )
        text_area.send_keys('Mord Ist Kunst')

    def card_details(self):
        card_details = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name_on_card"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_details)
        time.sleep(0.5)

        ActionChains(self.driver).move_to_element(card_details).click().perform()
        card_details.send_keys('Jeffrie Dahhmer')

        card_number = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'card_number'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_number)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "card_number")))
        card_number.click()
        card_number.send_keys('1234 4567 8910 1112')

        cvc = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'cvc'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cvc)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "cvc")))
        cvc.click()
        cvc.send_keys('123')

        expiration = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'expiry_month'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", expiration)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "expiry_month")))
        expiration.click()
        expiration.send_keys('12')

        expire_year = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'expiry_year'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", expire_year)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "expiry_year")))
        expire_year.click()
        expire_year.send_keys('2090')

    def button_pay(self):
        pay_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@data-qa="pay-button"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", pay_button)
        pay_button.click()

        try:
            successfully = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="alert-success alert"]'))
            )
            assert successfully.is_displayed(), 'Your order has been placed successfully!'
        except:
            print("Alert не отловлен, возможно, страница быстро перешла дальше")

        WebDriverWait(self.driver, 15).until(
            EC.url_contains("payment_done")
        )

    def add_to_cart_from_page(self):
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-default add-to-cart"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_button)
        add_to_cart_button.click()


    def place_order(self):
        place_order_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/payment"]'))
        )
        place_order_button.click()

    def x_from_cart(self):
        x =WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="cart_quantity_delete"]'))
        )
        x.click()

    def cart_empty(self):
        cart_empty = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Cart is empty!']"))
        )
        assert cart_empty.is_displayed(), "'Cart is empty!' is not displayed"

    def category(self):
        category = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2[text()="Category"]'))
        )
        assert category.is_displayed(), "'Category' is not displayed"

    def women_button(self):
        women_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#Women"]'))
        )
        women_button.click()

    def dress_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@href='/category_products/1']"))
        )

        dress_button = self.driver.find_element(By.XPATH, "//a[@href='/category_products/1']")
        dress_button.click()

    def dress_verify(self):
        dress_verify = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Women - Dress Products']"))
        )
        assert dress_verify.is_displayed(), "'Women - Dress Products' is not displayed"

    def men_category(self):
        men_category = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#Men"]'))
        )
        men_category.click()

    def t_shirts_menu(self):
        t_shirts_menu = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/category_products/3"]'))
        )
        t_shirts_menu.click()

    def t_shirts_verify(self):
        t_shirts_verify = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Men - Tshirts Products']"))
        )
        assert t_shirts_verify.is_displayed(), "'Tshirts Products' is not displayed"

    def login_into_account_that_got_created(self):
        login = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-email"]'))
        )
        login.click()
        login.send_keys("ilikehotgirls@trump.com")

        password = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-qa="login-password"]'))
        )
        password.click()
        password.send_keys("12345678Aa")

    def brands_verif(self):
        brands_verif = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2[text()="Brands"]'))
        )
        assert brands_verif.is_displayed(), "'Brands' is not displayed"

    def biba_brand(self):
        biba_brand = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/brand_products/Biba"]' ))
        )
        biba_brand.click()

    def biba_verify(self):
        biba_verify = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2[text()="Brand - Biba Products"]'))
        )
        assert biba_verify.is_displayed(), "'Brand' Biba is not displayed"

    def h_m_brand(self):
        h_m_brand = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/brand_products/H&M"]'))
        )
        h_m_brand.click()

    def h_m_verify(self):
        h_m_verify = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2[text()="Brand - H&M Products"]'))
        )
        assert h_m_verify.is_displayed(), "'H&M Products' is not displayed"

    def all_products_verify(self):
        all_products_verify = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2[text() = "All Products"]'))
        )
        assert all_products_verify.is_displayed(), "'All Products' is not displayed"

    def search_and_verify(self):
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_product"))
        )
        search_input.click()
        search_input.send_keys("Little Girls Mr. Panda Shirt")

        button_search = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit_search"))
        )
        button_search.click()

        searched_products_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="title text-center"]'))
        )
        assert searched_products_title.is_displayed(), "Search products title is not displayed"

        product_names = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="productinfo text-center"]/p'))
        )

        assert len(product_names) > 0, "No products found after search"

        for product in product_names:
            assert "panda" in product.text.lower(), f"Unexpected product: {product.text}"

    def verify_panda(self):
        verify_panda = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/product_details/18"]'))
        )
        assert verify_panda.is_displayed(), "'Panda' is not displayed"

    def cart_and_open(self):
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@data-product-id="18"]'))
        )
        add_to_cart_button.click()

        view_cart_popup_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//u[text()="View Cart"]'))
        )
        view_cart_popup_button.click()

    def review_on_product(self):
        name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'name'))
        )
        name.click()
        name.send_keys("Antoshka")

        email = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )
        email.click()
        email.send_keys("namaybytnee@zirki.com")

        review = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'review'))
        )
        review.click()
        review.send_keys("Hyita")

        submit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'button-review'))
        )
        submit.click()

    def thank_you_text(self):
        thank_you_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Thank you for your review."]'))
        )
        assert thank_you_text.is_displayed(), "'Thank you for your review.'"

    def scroll_to_bottom(self, pause_time=1.0):

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def add_from_recommendations(self):
        recommended_block = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='recommended_items']"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", recommended_block)

        add_button = recommended_block.find_element(By.CSS_SELECTOR, 'a[data-product-id="4"]')

        add_button.click()

    def verify_product_from_recommendations(self):
        verify_recommendations = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/product_details/4"]'))
        )
        assert verify_recommendations.is_displayed(), "'Stylish Dress is not displayed'"

    def verify_delivery_address_is_the_same(self):
        addresses = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'address_city'))
        )

        delivery_address = addresses[0].text.strip()
        billing_address = addresses[1].text.strip()

        assert delivery_address == billing_address, (
            f"❌ Адреса не совпадают!\nDelivery: {delivery_address}\nBilling: {billing_address}"
        )

        print("Delivery Address:", delivery_address)
        print("Billing Address:", billing_address)

        if delivery_address == billing_address:
            print("✅ Address of billing and delivery is the same")
        else:
            print("❌ Address of billing and delivery is not the same")

    def download_invoice(self):
        invoices = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/download_invoice/500"]'))
        )
        invoices.click()

    def continue_button(self):
        continue_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-qa="continue-button"]'))
        )
        continue_button.click()

    def verify_subscription(self):
        subscription = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Subscription']"))
        )
        assert subscription.is_displayed(), "'Subscription is not displayed'"

    def arrow_up(self):
        arrow_up = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#top"]'))
        )
        arrow_up.click()

    def verify_top(self):
        verify_top = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//h2[text()="Full-Fledged practice website for Automation Engineers"]')
            )
        )
        assert verify_top.is_displayed(), "'Full-fledged practice website for Automation Engineers is not displayed'"

    def scroll_up(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

        verify_top = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//h2[text()="Full-Fledged practice website for Automation Engineers"]')
            )
        )
        assert verify_top.is_displayed(), "'Full-fledged practice website for Automation Engineers is not displayed'"

    def verify_logged_in(self, expected_name: str):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='nav navbar-nav']"))
        )
        text = element.text.strip()
        assert expected_name in text, f"Expected username '{expected_name}' not found in: «{text}»"
