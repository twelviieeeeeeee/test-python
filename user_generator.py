import random
import string
from collections import namedtuple

User = namedtuple("User", ["name", "email", "password"])

def generate_random_user():
    first_names = ["Anton", "John", "Anna", "Kate", "Ivan"]
    last_names = ["Smith", "Johnson", "Trump", "Petrov", "Koval"]

    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@testmail.com"
    password = "12345678Aa"

    return User(name=name, email=email, password=password)

