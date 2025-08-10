from setuptools import setup, find_packages

setup(
    name="api_requests_framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pytest",
        "allure-pytest",
        "faker"
    ],
    author="AntonioBANdeRASS",
    description="Api framework python packages",
    url="https://gitlab.com/barbariki245/api-requests",
)

