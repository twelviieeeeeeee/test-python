FROM python:3.12-slim

# Установка утилит и Google Chrome
RUN apt-get update && \
    apt-get install -y wget curl gnupg unzip apt-transport-https jq git openssh-client \
        libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libappindicator3-1 \
        libasound2 libxtst6 libatk-bridge2.0-0 libgtk-3-0 default-jre && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Задаем переменные для токена GitLab и ветки
ARG GITLAB_API_TOKEN
ARG GITLAB_BRANCH=AntonioBANdeRASS

ENV GITLAB_GROUP_PATH=barbariki245
ENV GITLAB_API_TOKEN=glpat-KY81g4JLGxgjs1wr1CR6
ENV GITLAB_API_URL=https://gitlab.com/api/v4

# Установка рабочей директории
WORKDIR /projects

# Клонируем каждый нужный репозиторий в отдельную папку
RUN git clone --branch ${GITLAB_BRANCH} https://oauth2:${GITLAB_API_TOKEN}@gitlab.com/barbariki245/test-selenium.git test-selenium && \
    git clone --branch ${GITLAB_BRANCH} https://oauth2:${GITLAB_API_TOKEN}@gitlab.com/barbariki245/automation.framework.git automation_framework && \
    git clone --branch ${GITLAB_BRANCH} https://oauth2:${GITLAB_API_TOKEN}@gitlab.com/barbariki245/api-requests.git api_requests

# Установка зависимостей проекта
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /projects/test-selenium/requirements.txt

# Установка Allure CLI
RUN curl -o allure.zip -L https://github.com/allure-framework/allure2/releases/download/2.34.0/allure-2.34.0.zip && \
    unzip allure.zip -d /opt/ && \
    ln -s /opt/allure-2.34.0/bin/allure /usr/bin/allure && \
    rm allure.zip

# Устанавливаем PYTHONPATH для всех модулей
ENV PYTHONPATH="/projects/automation_framework:/projects/api_requests:/projects/test-selenium"

WORKDIR /projects/test-selenium

CMD ["pytest", "tests", "--alluredir=allure-results"]
