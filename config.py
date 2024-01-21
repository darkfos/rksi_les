from configparser import ConfigParser

# Конфигурация проекта

file_ini = ConfigParser()
file_ini.read("secret.ini")

URL_RKSI_PREPODS = file_ini.get("rksi", "URL_RKSI_P")
URL_RKSI_MOBILE = file_ini.get("rksi", "URL_RKSI_MOBILE")

API_KEY_TG = file_ini.get("bot", "API_KEY")