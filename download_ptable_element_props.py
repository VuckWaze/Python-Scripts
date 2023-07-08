import requests
import re
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd


urls = [f'https://periodictable.com/Elements/{str(n).zfill(3)}/data.html' for n in range(1, 119)] 

def fetch_and_parse_url(url: requests.Response):
    try:
        now = time.time()
        if now - start_time > 3.0:
            print('Too soon to make another request.')
            print(f'Pausing for {now - start_time} seconds.')
            time.sleep(now-start_time)
    except:
        if 'start_time' not in globals():
        # Time stamp request execution
            start_time = time.time()
    finally:
        response = requests.get(url)
    
    soup = BeautifulSoup(response.text)

    prop_dict = {}

    for p in soup.find_all('tr'):
        prop = p.find('td', align='right')
        try:
            prop_dict[prop.find_next('a').text] = prop.find_next_sibling('td', align='left').text
        except AttributeError:
          Warning('Encountered None, skipping.')
    return prop_dict
# test 
data = fetch_and_parse_url(urls[0])


if __name__ == '__main__':
    p_table = {}
    for url in urls:
        element_property_dict = fetch_and_parse_url(url)
        p_table[element_property_dict['Name']] = element_property_dict
        print(f'Added {element_property_dict["Name"]} to the table.')
    df = pd.DataFrame(p_table)
    df.to_csv('periodic_table.csv')