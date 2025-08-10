from pages.savefromhell.bibki_page import AutoExercise
from utils.user_generator import generate_random_user
import allure
import pytest

@allure.title("Test: Register New User And Delete Account")
@allure.description("Opens main page, signs up, verifies account creation, and deletes it")


def test_open_and_verify(driver):
    ae = AutoExercise(driver)

    with allure.step("Open main page"):
        ae.open_and_verify()

    with allure.step("Navigate to Signup/Login page"):
        ae.login_page_click_verify()

    with allure.step("Generate user and sign up"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        password = "12345678Aa"

        user = {
            "name": name,
            "email": email,
            "password": password
        }

        ae.signup_new_user(name, email)

    with allure.step("Fill user info"):
        ae.fill_user_info(user)

    with allure.step("Verify account created"):
        ae.account_created(name)

    with allure.step("Delete account after test"):
        ae.delete_account()

def test_login_with_valid_credentials(driver):
    ae = AutoExercise(driver)

    with allure.step("Open main page and navigate to signup"):
        ae.open_and_verify()
        ae.login_page_click_verify()

    with allure.step("Generate and register new user"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()

        user = {
            "name": name,
            "email": email,
            "password": "12345678Aa"
        }

        ae.signup_new_user(name, email)
        ae.fill_user_info(user)
        ae.account_created(name)

    with allure.step("Logout after registration"):
        ae.logout()

    with allure.step("Go to login page"):
        ae.login_page_click_verify()

    with allure.step("Login with the registered user"):
        ae.login_into_account_that_got_created(user)

    with allure.step("Verify successful login"):
        ae.verify_logged_in(name)

    with allure.step("Delete account after test"):
        ae.delete_account()

def test_incorrect_login(driver):
    ae = AutoExercise(driver)

    with allure.step("Login Page Verify"):
        ae.open_and_verify()

    with allure.step("Login Page Verify"):
        ae.login_page_click_verify()

    with allure.step("Login Into Account"):
        ae.login_into_account()

def test_logout_user(driver):
    ae = AutoExercise(driver)

    with allure.step("Open main page and navigate to signup"):
        ae.open_and_verify()
        ae.login_page_click_verify()

    with allure.step("Generate and register new user"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        password = "12345678Aa"

        user = {
            "name": name,
            "email": email,
            "password": password
        }

        ae.signup_new_user(name, email)
        ae.fill_user_info(user)
        ae.account_created(name)

    with allure.step("Logout after registration"):
        ae.logout()

    with allure.step("Go to login page for second login"):
        ae.login_page_click_verify()

    with allure.step("Login with the registered user"):
        ae.login_into_account_that_got_created(user)

    with allure.step("Verify user is logged in"):
        ae.verify_logged_in(user["name"])

    with allure.step("Delete the user account"):
        ae.delete_account()

def test_register_with_existing_email(driver):
    ae = AutoExercise(driver)

    with allure.step("Open main page and navigate to signup"):
        ae.open_and_verify()
        ae.login_page_click_verify()

    with allure.step("Generate and register new user"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        password = "12345678Aa"

        user = {
            "name": name,
            "email": email,
            "password": password
        }

        ae.signup_new_user(name, email)
        ae.fill_user_info(user)
        ae.account_created(name)

    with allure.step("Logout to enable new registration attempt"):
        ae.logout()

    with allure.step("Navigate to signup/login page again"):
        ae.login_page_click_verify()

    with allure.step("Attempt to register with existing user's email"):
        ae.fill_email_and_name(user["email"], user["name"])
        ae.signup_button()

    with allure.step("Verify error message about existing user"):
        ae.error_user()

    with allure.step("Cleanup - delete the user account"):
        ae.login_page_click_verify()
        ae.fill_email_and_password(user["email"], user["password"])
        ae.delete_account()

def test_contact_us(driver):
    ae = AutoExercise(driver)

    ae.open_and_verify()
    ae.contact_us_button()

    user = generate_random_user()

    ae.contact_us_mail(user)

def test_cases(driver):
    ae = AutoExercise(driver)

    with allure.step("Open Test Cases"):
        ae.open_and_verify()

    with allure.step("Cases Page Click"):
        ae.cases_test()

def test_verify_all_products(driver):
    ae = AutoExercise(driver)

    with allure.step("Open All Products"):
        ae.open_and_verify()

    with allure.step("All Products"):
        ae.products_test()

    with allure.step("All Products Details Verified"):
        ae.details()

def test_search_products(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Open  Products"):
        ae.products()

    with allure.step("Products Search"):
        ae.search_products()

def test_subscriptions(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Scroll to Footer and create subscription"):
        ae.scroll_to_footer()

def test_cart_subscription(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Cart"):
        ae.cart_button()

    with allure.step("Footer"):
        ae.footer()

    with allure.step("Subscribe"):
        ae.subscription()

def test_cart_total(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Products"):
        ae.products()

    with allure.step("Products Total"):
        ae.product_add_to_cart()

def test_verify_product_quantity(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("View Product"):
        ae.view_product_button()

    with allure.step(" Quantity"):
        ae.increase_quantity_to_4()

    with allure.step("Space"):
        ae.click_on_white_space()

    with allure.step("Add to cart"):
        ae.add_to_cart()

    with allure.step("Cart"):
        ae.cart_button()

    with allure.step("Verify Quantity"):
        ae.verify_product_quantity(4)

def test_register_while_checkout(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Add Product"):
        ae.add_to_cart_from_page()

    with allure.step("View"):
        ae.view_product_button()

    with allure.step(" Cart"):
        ae.cart_button()

    with allure.step("Checkout"):
        ae.proceed_to_checkout()

    with allure.step("Register"):
        ae.login_register_in_cart()

    with allure.step("Sign up"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        ae.signup_new_user(name, email)

        user = {
            "name": name,
            "email": email
        }

    with allure.step("user info"):
        ae.fill_user_info(user)

    with allure.step("Account created"):
        ae.account_created(name)

    with allure.step("View cart again"):
        ae.cart_button()

    with allure.step("Cart Verify"):
        ae.cart_verify()

    with allure.step("Checkout again"):
        ae.proceed_to_checkout()

    with allure.step("Verify Address"):
        ae.address_details()

    with allure.step("Verify Review"):
        ae.review_your_order()

    with allure.step("Comment"):
        ae.comment()

    with allure.step("Place order"):
        ae.place_order()

    with allure.step("Card Details"):
        ae.card_details()

    with allure.step("Pay"):
        ae.button_pay()

    with allure.step("Delete Account"):
        ae.delete_account()

def test_order_register_before_checkout(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Login"):
        ae.login_page_click_verify()

    with allure.step("Sign up"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        ae.signup_new_user(name, email)

        user = {
            "name": name,
            "email": email
        }

    with allure.step("User info"):
        ae.fill_user_info(user)

    with allure.step("Account created"):
        ae.account_created(name)

    with allure.step("View product"):
        ae.products()

    with allure.step("Add Product"):
        ae.add_to_cart_from_page()

    with allure.step("View cart "):
        ae.cart_button()

    with allure.step("Cart Verify"):
        ae.cart_verify()

    with allure.step("Checkout"):
        ae.proceed_to_checkout()

    with allure.step("Verify Address"):
        ae.address_details()

    with allure.step("Verify Review"):
        ae.review_your_order()

    with allure.step("Comment"):
        ae.comment()

    with allure.step("Place order"):
        ae.place_order()

    with allure.step("Card Details"):
        ae.card_details()

    with allure.step("Pay"):
        ae.button_pay()

    with allure.step("Delete Account"):
        ae.delete_account()

def test_login_before_checkout(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Login"):
        ae.login_page_click_verify()

    with allure.step("Sign up"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        password = "12345678Aa"  # обязательно добавить пароль!
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        ae.signup_new_user(name, email)

    with allure.step("User info"):
        ae.fill_user_info(user)

    with allure.step("Account created"):
        ae.account_created(name)

    with allure.step("Logout"):
        ae.logout()

    with allure.step("Login Page again"):
        ae.login_page_click_verify()

    with allure.step("Login into"):
        ae.login_into_account_that_got_created(user)

    with allure.step("Add to cart"):
        ae.add_to_cart_from_page()

    with allure.step("Cart"):
        ae.cart_button()

    with allure.step("Cart Verify"):
        ae.cart_verify()

    with allure.step("Checkout"):
        ae.proceed_to_checkout()

    with allure.step("Verify Address"):
        ae.address_details()

    with allure.step("Verify Review"):
        ae.review_your_order()

    with allure.step("Comment"):
        ae.comment()

    with allure.step("Place order"):
        ae.place_order()

    with allure.step("Card Details"):
        ae.card_details()

    with allure.step("Pay"):
        ae.button_pay()

    with allure.step("Delete Account"):
        ae.delete_account()

def test_remove_from_cart(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Add to cart"):
        ae.add_to_cart_from_page()

    with allure.step("View"):
        ae.view_product_button()

    with allure.step("Cart"):
        ae.cart_button()

    with allure.step("Cart Verify"):
        ae.cart_verify()

    with allure.step("Remove from cart"):
        ae.x_from_cart()

    with allure.step("Empty cart"):
        ae.cart_empty()

def test_view_category_products(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Category Verify"):
        ae.category()

    with allure.step("Women Category"):
        ae.women_button()

    with allure.step("Dress Category"):
        ae.dress_button()

    with allure.step("Category Verify Again"):
        ae.category()

    with allure.step("Dress verify"):
        ae.dress_verify()

    with allure.step("Men Category"):
        ae.men_category()

    with allure.step("Men T-shirts"):
        ae.t_shirts_menu()

    with allure.step("Men T-shirts verify"):
        ae.t_shirts_verify()

def test_view_cart_brand_products(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Products"):
        ae.products()

    with allure.step("Brand Verif"):
        ae.brands_verif()

    with allure.step("Brand Biba"):
        ae.biba_brand()

    with allure.step("Biba Verify"):
        ae.biba_verify()

    with allure.step("H&M brand"):
        ae.h_m_brand()

    with allure.step("H&M brand verify"):
        ae.h_m_verify()

def test_search_and_verify_cart_after_login(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Products"):
        ae.products()

    with allure.step("Verify Products"):
        ae.all_products_verify()

    with allure.step("Search Products"):
        ae.search_and_verify()

    with allure.step("Add to cart"):
        ae.add_to_cart_from_page()

    with allure.step("Cart"):
        ae.view_cart_button()

    with allure.step("Panda Verify"):
        ae.verify_panda()

    with allure.step("Login"):
        ae.login_page_click_verify()

    with allure.step("Sign up"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        password = "12345678Aa"

        user = {
            "name": name,
            "email": email,
            "password": password
        }
        ae.signup_new_user(name, email)

    with allure.step("User info"):
        ae.fill_user_info(user)

    with allure.step("Account created"):
        ae.account_created(name)

    with allure.step("Logout"):
        ae.logout()

    with allure.step("Login Page again"):
        ae.login_page_click_verify()

    with allure.step("Login into account"):
        ae.login_into_account_that_got_created(user)

    with allure.step("Cart again"):
        ae.cart_button()

    with allure.step("Cart Verify again"):
        ae.verify_panda()

def test_add_review_on_product(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Products"):
        ae.products()

    with allure.step("Products Verified"):
        ae.all_products_verify()

    with allure.step("Go directly to product page if needed"):
        ae.driver.get("https://automationexercise.com/products")

    with allure.step("View product"):
        ae.view_product_button()

    with allure.step("Add review"):
        ae.review_on_product()

    with allure.step("Review Verify"):
        ae.thank_you_text()

def test_add_from_recommendations(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Scroll to bottom"):
        ae.scroll_to_bottom()

    with allure.step("Add from recommendatios"):
        ae.add_from_recommendations()

    with allure.step("View cart"):
        ae.view_cart_button()

    with allure.step("Verify from recommendations"):
        ae.verify_product_from_recommendations()

def test_verify_address_details_in_checkout_page(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Sign up"):
        ae.login_page_click_verify()

    with allure.step("Generate and create user"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        password = "12345678Aa"
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        ae.signup_new_user(name, email)
        ae.fill_user_info(user)
        ae.account_created(name)

    with allure.step("Add to cart"):
        ae.add_to_cart_from_page()

    with allure.step("Cart"):
        ae.view_cart_button()

    with allure.step("Verify Cart"):
        ae.cart_verify()

    with allure.step("Proceed to checkout"):
        ae.proceed_to_checkout()

    with allure.step("Verify addresses"):
        ae.verify_delivery_address_is_the_same()

    with allure.step("Delete account"):
        ae.delete_account()


def test_download_invoice(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("Add product"):
        ae.add_to_cart_from_page()

    with allure.step("Cart button"):
        ae.view_cart_button()

    with allure.step("Verify cart"):
        ae.cart_verify()

    with allure.step("Proceed to checkout"):
        ae.proceed_to_checkout()

    with allure.step("Register-login"):
        ae.login_register_in_cart()

    with allure.step("Generate and sign up user"):
        name = ae.generate_random_username()
        email = ae.generate_random_email()
        password = "12345678Aa"
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        ae.signup_new_user(name, email)
        ae.fill_user_info(user)
        ae.account_created(name)

    with allure.step("Cart"):
        ae.cart_button()

    with allure.step("Proceed to checkout again"):
        ae.proceed_to_checkout()

    with allure.step("Verify address"):
        ae.address_details()

    with allure.step("Review your order verify"):
        ae.review_your_order()

    with allure.step("Enter description"):
        ae.comment()

    with allure.step("Place order"):
        ae.place_order()

    with allure.step("Card details"):
        ae.card_details()

    with allure.step("Pay"):
        ae.button_pay()

    with allure.step("Invoice download"):
        ae.download_invoice()

    with allure.step("Continue button"):
        ae.continue_button()

    with allure.step("Delete account"):
        ae.delete_account()


def test_scroll_up_using_arrow(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("scroll down"):
        ae.scroll_to_bottom()

    with allure.step("Subscription is visible"):
        ae.verify_subscription()

    with allure.step("Arrow"):
        ae.arrow_up()

    with allure.step("Verify top"):
        ae.verify_top()

def test_without_arrow(driver):
    ae = AutoExercise(driver)

    with allure.step("Open and Verify"):
        ae.open_and_verify()

    with allure.step("scroll down"):
        ae.scroll_to_bottom()

    with allure.step("Subscription is visible"):
        ae.verify_subscription()

    with allure.step("Scroll without arrow"):
        ae.scroll_up()

    with allure.step("Verify top"):
        ae.verify_top()