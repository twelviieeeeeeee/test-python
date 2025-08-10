from pages.savefromhell.ya_page import YaPage
import time


def test_ya_ru(driver):
    ya = YaPage(driver)
    ya.open()

def test_microphone(driver):
    ya = YaPage(driver)
    ya.mic()



def test_svg_camera(driver):
    ya = YaPage(driver)
    ya.open()
    ya.svg_camera()

    url = 'https://www.ixbt.com/img/n1/news/2024/8/4/RTX5090-HERO-1-1200x624_large.jpg'
    ya.image_url(url)

    ya.find_button()

    ya.search_button()


# негативные тесты

def test_empty_search_query(driver):
    ya = YaPage(driver)
    ya.open()
    ya.perform_empty_search()

def test_invalid_image_url_returns_error(driver):
    ya = YaPage(driver)
    ya.open()
    ya.svg_camera()

    invalid_url = "https://www.gutenberg.org/cache/epub/76339/pg76339-images.html"
    ya.image_url(invalid_url)

    ya.find_button()
    ya.error_message()

def test_long_image_url(driver):
    ya = YaPage(driver)
    ya.open()
    ya.svg_camera()
    long_url = 'https://www.ixbt.com/img/n1/news/2024/8/4/RTX5090-HERO-1-1200x624_large.jpg' + "a" * 10000
    ya.image_url(long_url)
    ya.find_button()
    ya.error_message()

# Дальше идут просто тест-кейсы

def test_search(driver):
    ya = YaPage(driver)
    ya.open()
    ya.input_search("Гитлер моя война")
    ya.press_enter()
    ya.wait_for_search_results()

def test_mts_search(driver):
    ya = YaPage(driver)
    ya.open()
    ya.input_search("мтс музыка")
    ya.press_enter()
    ya.close_yandex_popup()
    ya.mts_music_open_page()
    ya.esc_button()
    ya.accept_cookies()
    ya.sound_search_input("korn open up")
    ya.play_button()






