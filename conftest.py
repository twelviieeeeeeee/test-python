import sys
import os
import random
import string
import tempfile
import shutil

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.options import Options

from utils.user_generator import generate_random_user
from boba_framework.biba_framework import ApiClient
from pages.savefromhell.bibki_page import AutoExercise

# Путь к корню PyCharmProjects
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Добавляем пути к фреймворкам
for subdir in ['automation_framework', 'api_requests']:
    full_path = os.path.join(base_path, subdir)
    if full_path not in sys.path:
        sys.path.insert(0, full_path)

print("sys.path:", sys.path)

# Фикстура для WebDriver
@pytest.fixture(scope="function")
def driver():
    user_data_dir = tempfile.mkdtemp()
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    yield driver

    driver.quit()
    shutil.rmtree(user_data_dir, ignore_errors=True)

# Фикстура для случайной почты
@pytest.fixture
def random_email():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(['example.com', 'testmail.com', 'mail.ru', 'gmail.com', 'aboba.com'])
    return f"{username}@{domain}"

# Фикстура для случайного имени
@pytest.fixture
def random_username():
    first_names = ['John', 'Mira', 'Anton', 'Luna', 'Markus', 'Elena', 'David', 'Sasha', 'Olga', 'Leo']
    last_names = ['Steel', 'Donnelly', 'Cabaleron', 'Foster', 'Ivanov', 'Kuznetsova', 'Torres', 'White', 'Chen', 'Ford']
    return f"{random.choice(first_names)} {random.choice(last_names)}"
