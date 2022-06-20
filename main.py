import urllib3
import requests
import time
import os
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)


TOKEN = cfg["telegram"]["TOKEN"]
chat_id = cfg["telegram"]["CHAT_ID"]
text = "Vietmy1.com is Online"
CHECK_EVERY_SECS = cfg["website"]["CHECK_EVERY_SECS"]
WEBSITE_URL = cfg["website"]["URL"]

number_of_check_offline = 0


def get_status_code():
    http = urllib3.PoolManager()
    r = http.request('GET', WEBSITE_URL)
    status_code = r.status
    return status_code


def bot_send_message():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
    # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url)
    print(r.json())


def get_pc_name():
    return os.environ['COMPUTERNAME']


if __name__ == '__main__':
    print("PHẦN MỀM KIỂM TRA TÌNH TRẠNG WEB SITE")
    pc_name = get_pc_name()

    while True:
        print('Checking vietmy1.com...', end=' ')
        status_code = get_status_code()
        print(status_code)

        if number_of_check_offline > 6:
            CHECK_EVERY_SECS = 86400

        if str(status_code) != '200':
            text = f'Vietmy1.com is now inaccessible, Status code: {status_code}, Send from: {pc_name}'
            number_of_check_offline += 1
            bot_send_message()
        else:
            number_of_check_offline = 0

        time.sleep(CHECK_EVERY_SECS)
