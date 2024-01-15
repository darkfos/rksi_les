from configparser import ConfigParser

file_ini = ConfigParser()
file_ini.read("secret.ini")

URL_RKSI_PREPODS=file_ini.get("rksi", "URL_RKSI_P")
URL_RKSI_MOBILE=file_ini.get("rksi", "URL_RKSI_MOBILE")
