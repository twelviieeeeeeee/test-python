from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

import time

class YaPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get('https://ya.ru')
        print("penis")

    def get_body_text(self):
        return self.driver.find_element(By.XPATH, '/html/body').text

    def input_search(self, text):
        search_input = self.driver.find_element(By.XPATH, '//*[@class="search3__input mini-suggest__input"]')
        search_input.clear()
        search_input.send_keys(text)

    def mic(self):
        self.driver.get('https://ya.ru')

        mic_button = self.driver.find_element(By.XPATH,
                                         '//*[@class="Button VoiceInput search3__voice search3__voice_type_depot VoiceInput_futuris"]')
        mic_button.click()

    def svg_camera(self):
        svg_camera = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="search3__svg_camera"]'))
        )
        svg_camera.click()

    def image_url(self, url):
        url_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '(//*[@class="Textinput-Control"])[2]'))
        )
        url_input.clear()
        url_input.send_keys(url)

    def find_button(self):
        find_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="Button Button_view_action Button_width_auto Button_size_m CbirPanelMultimodalUrlForm-Button"]'))
        )
        find_button.click()

    def search_button(self):
        search_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="Button Button_view_action Button_width_auto Button_size_m CbirPanelMultimodalQuery-ButtonSearch"]'))
        )
        search_button.click()


    def perform_empty_search(self):
        search_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search3__input"))
        )
        search_input.clear()
        search_input.send_keys("\n")
        return search_input

    def error_message(self):
        txt_error = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="SnackbarTransitioned-Content"]'))
        )
        return txt_error.text

    def press_enter(self):
        search_input = self.driver.find_element(By.XPATH, '//*[@class="search3__input mini-suggest__input"]')
        search_input.send_keys(Keys.ENTER)

    def wait_for_search_results(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.serp-list'))
        )
        self.driver.quit()


    def mts_music_open_page(self):
        original_window = self.driver.current_window_handle

        mts_music_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(),"Слушать")]'))
        )
        mts_music_link.click()
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))

        for handle in self.driver.window_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                break

    def accept_cookies(self):
        try:
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class="button_wrapper__hyCP8 mtsds-c1-bold-upp-wide button_size__m__0hq4N button_alwaysWhite__HEPeo button_secondaryGray__IFHOC"]'))
            )
            accept_button.click()
        except:
            pass

    def sound_search_input(self, query):
        search_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[contains(@class, "input-search_input")]'))
        )
        search_input.click()
        search_input.clear()
        search_input.send_keys(query)

        try:
            search_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "input-search_icon__")]'))
            )
            search_button.click()
        except TimeoutException:
            search_input.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"track-row_track_cover_wrapper")]'))
        )

    def play_button(self):
        play_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '(//div[contains(@class, "track-row_track_cover_wrapper")])[1]'))
        )
        if play_buttons:
            play_buttons[0].click()
            time.sleep(6)

    def close_yandex_popup(self):
        try:
            not_now_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class="Button Distribution-Button Distribution-ButtonClose Distribution-ButtonClose_view_button Button_view_default Button_size_m"]'))
            )
            not_now_button.click()
        except:
            pass


    def close_mts_popup(self):
        try:
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "close_button")]'))
            )
            close_button.click()
        except:
            pass

    def esc_button(self):
        try:
            body = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            body.send_keys(Keys.ESCAPE)
        except:
            pass