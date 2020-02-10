from selenium import webdriver

import json 
import time
import threading

from misc.utils import get_links, get_page_list, next_page
from misc.miner_class import Miner
from settings import NUMBER_OF_THREADS, URL


def initialize_files():
    print('Initializing')
    with open('data/output_json.json', 'a') as output_file:
        output_file.write('[')

def closing_file():
    print('Closing')
    with open('data/output_json.json', 'a') as output_file:
        output_file.write(']')
        
'''handler function for all the multi threaded minners'''
def miner_handler(member_links):
    current_miners = []
    for member_link in member_links:
        miner = Miner()
        miner.setup(member_link)
        miner.start()
        current_miners.append(miner)
    x = 0
    while current_miners:
        for miner in current_miners:
            if miner.is_alive() != True:
                x = x+1
        if x == len(current_miners):
            print(x, "   ===   ", len(current_miners))
            break

'''main entry fucntion'''
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome('/home/lurayy/chromedriver', chrome_options=options)
    # driver = webdriver.Chrome('/home/lurayy/chromedriver')
    driver.get(URL)
    initialize_files()
    page_data = get_page_list(driver)
    n = NUMBER_OF_THREADS
    state = True
    try:
        while state:
            print('-------------------------Mining on page number: ',page_data['current_page'],'---------------------------')
            member_links = get_links(driver)
            while member_links:
                if len(member_links) > n:
                    process_links = member_links[:n]
                    member_links = member_links[n:]
                else:
                    process_links = member_links[:len(member_links)]
                    member_links = member_links[len(member_links):]
                miner_handler(process_links)
            page_data = get_page_list(driver)
            state = next_page(page_data, driver)
    except:
        print('Error on the main loop')
    finally:
        closing_file()
        driver.close()
