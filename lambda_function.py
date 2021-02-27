import datetime
import sys
import time
from random import choice
from threading import Thread

import requests
from bs4 import BeautifulSoup

from m_token import bot, mi_id, group_id

def main():
    # References
    codewars = "https://www.codewars.com"
    search = "/kata/search/"
    level_ref = "?q=&r[]=-"
    cat_ref = "&tags="
    opts = "&beta=false&order_by=popularity+desc"
    kata_class = "list-item kata bg-ui-section p-4 rounded-lg shadow-md"
    
    parser = 'html.parser'

    # Level selection basaed on week day
    wd = datetime.datetime.today().weekday()
    level = abs(int(wd/2)-7)

    body = BeautifulSoup(requests.get(f"{codewars}{search}{level_ref}{level}{opts}").content, parser)
    cats = [cat.find("a")["href"] for cat in body.find_all(attrs={"class":"py-5px"})]                                   # All categories
    cat = choice(cats).split('=')[-1]                                                                                   # Random category selected
    body = BeautifulSoup(requests.get(f"{codewars}{search}{level_ref}{level}{cat_ref}{cat}{opts}").content, parser)
    katas = [kata.find("a")["href"] for kata in body.find_all(attrs={"class": kata_class})]                             # Some katas from that category
    mensaje = f"{codewars}{choice(katas)}"                                                                              # Random kata selected
    bot.send_message(group_id, mensaje)

    bot.polling()

def lambda_handler(event, context):
    main_thread = Thread(target=main)
    main_thread.daemon = True
    main_thread.start()
    time.sleep(10)
    sys.exit()



