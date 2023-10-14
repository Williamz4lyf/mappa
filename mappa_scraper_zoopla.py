import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

import pandas as pd
import numpy as np
import time
from pathlib import Path

pgs = np.arange(0, 41, 1)

# %%
options = webdriver.ChromeOptions()
chrome_driver_path = '/Users/nnankewilliams/chromedriver_mac_arm64/chromedriver'
chrome_service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service, options=options)

for pg in pgs:
    if pg <= 0: # amend for any interruptions in code run
        pass
    else:
        # Sale Data
        driver = webdriver.Chrome(service=chrome_service, options=options)
        url1 = f'https://www.zoopla.co.uk/for-sale/property/london/?q=London&results_sort=newest_listings&search_source=home&added=24_hours&radius=40&pn={pg}'
        driver.get(url1)
        with open(f'zoopla_pages/zp_page_sale_{pg}.html', 'w+') as file:
            file.write(driver.page_source)
        time.sleep(5)
        driver.quit()

for pg in pgs:
    if pg in []: # amend for any interruptions in code run
        pass
    else:
        # Rent Data
        driver = webdriver.Chrome(service=chrome_service, options=options)
        url2 = f'https://www.zoopla.co.uk/to-rent/property/london/?price_frequency=per_month&q=London&results_sort=newest_listings&search_source=to-rent&added=24_hours&radius=40&pn={pg}'
        driver.get(url2)
        with open(f'zoopla_pages/zp_page_rent_{pg}.html', 'w+') as file:
            file.write(driver.page_source)
        time.sleep(5)
        driver.quit()

# %%
rent_urls = list()
rent_id = list()
rent_date_added = list()
rent_availability_1 = list()
for pg in pgs:
    with open(f'zoopla_pages/zp_page_rent_{pg}.html') as file:
        page = file.read()
        soup = BeautifulSoup(page, 'html.parser')
        soup_content = soup.find_all('div', class_='_1c58w6u0')
        # p_card_info contains the html information for the listing
        pcard_info = soup_content[0].find_all('div', class_='_1c58w6u2')
        # Parse Rent Data
        for i in range(len(pcard_info)):
            rent_id.append(pcard_info[i].get('id'))
            pcard_link = pcard_info[i].find('a', class_='rgd66w1').get('href')
            pcard_link_full = f'https://www.zoopla.co.uk{pcard_link}'
            rent_urls.append(pcard_link_full)
            try:
                rent_date_added.append(
                    [i.text for i in pcard_info[i].find('ul', class_='_65yptp0 _1dgm2fcb').find_all('li')[0]])
            except IndexError:
                rent_date_added.append(None)
            try:
                rent_availability_1.append(
                    [i.text for i in pcard_info[i].find('ul', class_='_65yptp0 _1dgm2fcb').find_all('li')[1]])
            except IndexError:
                rent_availability_1.append(None)
# %%

sale_urls = list()
sale_id = list()
sale_date_added = list()
sale_tenure_1 = list()
for pg in pgs:
    with open(f'zoopla_pages/zp_page_sale_{pg}.html') as file:
        page = file.read()
        soup = BeautifulSoup(page, 'html.parser')
        soup_content = soup.find_all('div', class_='_1c58w6u0')
        # p_card_info contains the html information for the listing
        pcard_info = soup_content[0].find_all('div', class_='_1c58w6u2')
        # Parse Rent Data
        for i in range(len(pcard_info)):
            sale_id.append(pcard_info[i].get('id'))
            pcard_link = pcard_info[i].find('a', class_='rgd66w1').get('href')
            pcard_link_full = f'https://www.zoopla.co.uk{pcard_link}'
            sale_urls.append(pcard_link_full)
            try:
                sale_tenure_1.append(pcard_info[i].find('ul', class_='_1rnkq5r0').text)
            except IndexError as e1:
                sale_tenure_1.append(None)
            except AttributeError as e2:
                sale_tenure_1.append(None)
            try:
                sale_date_added.append(pcard_info[i].find('li', class_='_65yptp1').text)
            except AttributeError as e3:
                sale_date_added.append('Added today')

# %%
# Get Property Listings
options = webdriver.ChromeOptions()
chrome_driver_path = '/Users/nnankewilliams/chromedriver_mac_arm64/chromedriver'
chrome_service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service, options=options)

# Page doesnt contain property listing
bad_pgs = [344, 555, 572, 573, 575, 576, 577, 651, 652]

for ind, url in enumerate(rent_urls):
    if ind not in bad_pgs:  # amend for interruptions in the code
        pass
    else:
        # Rent Data
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.minimize_window()
        driver.get(url)
        with open(f'zoopla_pages/zp_property_rent_{ind}.html', 'w+') as file:
            file.write(driver.page_source)
        driver.quit()

#%%
for ind, url in enumerate(sale_urls):
    if ind not in [161, 348]:  # amend for interruptions in the code
        pass
    else:
        # Sale Data
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.minimize_window()
        driver.get(url)
        with open(f'zoopla_pages/zp_property_sale_{ind}.html', 'w+') as file:
            file.write(driver.page_source)
        driver.quit()

# %%
# Parse Rent Data into DF
rent_title = list()
rent_pry_price = list()
rent_sec_price = list()
rent_address = list()
rent_agent = list()
rent_agent_url = list()
rent_letting_details = list()
rent_beds = list()
rent_baths = list()
rent_epc_rating = list()
rent_key_features = list()
rent_description = list()
rent_availability = list()
rent_reception = list()
rent_property_size = list()

for i in range(len(rent_urls)):
    with open(f'zoopla_pages/zp_property_rent_{i}.html') as file:
        url_page = file.read()
        url_soup = BeautifulSoup(url_page, 'html.parser')

        check_page = url_soup.find('p', class_='_1dgm2fc4 _1y5q8ag0')
        if check_page is None:
            print(i, 'Bad Page')
            rent_pry_price.append(None)
            rent_sec_price.append(None)
            rent_address.append(None)
            rent_title.append(None)
            rent_agent.append(None)
            rent_agent_url.append(None)
            rent_availability.append(None)
            rent_letting_details.append(None)
            rent_beds.append(None)
            rent_baths.append(None)
            rent_epc_rating.append(None)
            rent_reception.append(None)
            rent_property_size.append(None)
            rent_key_features.append(None)
            rent_description.append(None)
        else:
            rent_pry_price.append(url_soup.find('p', class_='_1dgm2fc4 _1y5q8ag0').text)
            rent_sec_price.append(url_soup.find('p', class_='_1dgm2fc7').text)
            rent_title.append(url_soup.find('p', class_='_1dgm2fc7 _1y5q8ag1').text)
            rent_address.append(url_soup.find('address', class_='_1y5q8ag2 _1dgm2fc8').text)
            try:
                rent_agent_url.append(
                    f'https://www.zoopla.co.uk{url_soup.find("a", class_="xtkkei4").get("href")}')
            except AttributeError:
                rent_agent_url.append(None)
            rent_agent.append(url_soup.find("p", class_="xtkkei3 _1dgm2fc6").text)
            try:
                rent_availability.append(
                    url_soup.find('div', class_='_1p8nftv7 _1p8nftv1n _1p8nftv3z    ').find('p').text)
            except AttributeError as e1:
                rent_availability.append(None)
            rent_letting_details.append([i.text for i in url_soup.find('div', class_='_1k66bqh1').find_all('div')])
            try:
                rent_beds.append(
                    [i.text for i in url_soup.find('div', class_="_1y5q8ag4").find_all('div', class_="_1p8nftv0") if
                     'bed' in i.text][0])
            except (AttributeError, IndexError):
                rent_beds.append(None)
            try:
                rent_baths.append(
                    [i.text for i in url_soup.find('div', class_="_1y5q8ag4").find_all('div', class_="_1p8nftv0") if
                     'bath' in i.text][0])
            except (AttributeError, IndexError):
                rent_baths.append(None)
            try:
                rent_epc_rating.append(
                    [i.text for i in url_soup.find('div', class_="_1y5q8ag4").find_all('div', class_="_1p8nftv0") if
                     'rating' in i.text][0])
            except (AttributeError, IndexError):
                rent_epc_rating.append(None)
            try:
                rent_reception.append(
                    [i.text for i in url_soup.find('div', class_="_1y5q8ag4").find_all('div', class_="_1p8nftv0") if
                     'reception' in i.text][0])
            except (AttributeError, IndexError):
                rent_reception.append(None)
            try:
                rent_property_size.append(
                    [i.text for i in url_soup.find('div', class_="_1y5q8ag4").find_all('div', class_="_1p8nftv0") if
                     'ft' in i.text][0])
            except (AttributeError, IndexError):
                rent_property_size.append(None)
            try:
                rent_key_features.append([i.text for i in url_soup.find('ul', class_="swbww70").find_all('li')])
            except AttributeError:  # where no key features in the listing
                rent_key_features.append(None)
            rent_description.append(url_soup.find('div', class_='ru2q7m3').find('span').text)

# %%
# View Rent Data
rent_df = pd.DataFrame({
    'property_id': rent_id,
    'title': rent_title,
    'address': rent_address,
    'url': rent_urls,
    'primary price': rent_pry_price,
    'secondary price': rent_sec_price,
    'agent': rent_agent,
    'agent_url': rent_agent_url,
    'date_added': rent_date_added,
    'letting_details': rent_letting_details,
    'beds': rent_beds,
    'baths': rent_baths,
    'epc_rating': rent_epc_rating,
    'availability': rent_availability,
    'availability_1': rent_availability_1,
    'key_features': rent_key_features,
    'description': rent_description,
})

rent_df

# %%
filepath = Path(
    '/Users/nnankewilliams/Library/CloudStorage/OneDrive-Personal/Data Analytics/my_projects/mappa/zp_rent_df.csv')
rent_df.to_csv(filepath, index=False)

# %%
sale_address = list()
sale_title = list()
sale_price = list()
sale_agent = list()
sale_agent_url = list()
sale_tenure = list()
sale_reception = list()
sale_beds = list()
sale_baths = list()
sale_epc_rating = list()
sale_key_features = list()
sale_description = list()
sale_property_size = list()
for i in range(len(sale_urls)):
    with open(f'zoopla_pages/zp_property_sale_{i}.html') as file:
        url_page = file.read()
        url_soup = BeautifulSoup(url_page, 'html.parser')

        check_page = url_soup.find('h1', id='listing-summary-details-heading')
        if check_page is None:
            print(i, 'Bad Page')
            sale_address.append(None)
            sale_title.append(None)
            sale_price.append(None)
            sale_agent_url.append(None)
            sale_agent.append(None)
            sale_tenure.append(None)
            sale_beds.append(None)
            sale_baths.append(None)
            sale_epc_rating.append(None)
            sale_reception.append(None)
            sale_property_size.append(None)
            sale_key_features.append(None)
            sale_description.append(None)
        else:
            sale_address.append(url_soup.find('address', class_='_1y5q8ag2 _1dgm2fc8').text)
            sale_title.append(url_soup.find('p', class_='_1dgm2fc7 _1y5q8ag1').text)
            sale_price.append(url_soup.find('p', class_='_1dgm2fc4 _1y5q8ag0').text)
            try:
                sale_agent_url.append(
                    f'https://www.zoopla.co.uk{url_soup.find("a", class_="xtkkei4").get("href")}')
            except AttributeError:
                sale_agent_url.append(None)
            sale_agent.append(url_soup.find("p", class_="xtkkei3 _1dgm2fc6").text)
            sale_tenure.append(url_soup.find('div', class_='_1p8nftv7 _1p8nftv1n').text)
            if url_soup.find('div', class_='_1y5q8ag4') is None:
                print(i, 'has no info for property, beds, baths')
                sale_beds.append(None)
                sale_baths.append(None)
                sale_reception.append(None)
                sale_property_size.append(None)
                sale_epc_rating.append(None)
            elif len([i.text for i in url_soup.find('div', class_='_1y5q8ag4')]) == 5:
                sale_beds.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][0])
                sale_baths.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][1])
                sale_reception.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][2])
                sale_property_size.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][3])
                sale_epc_rating.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][4])
            elif len([i.text for i in url_soup.find('div', class_='_1y5q8ag4')]) == 4:
                sale_beds.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][0])
                sale_baths.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][1])
                sale_reception.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][2])
                sale_epc_rating.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][3])
                sale_property_size.append(None)
            elif len([i.text for i in url_soup.find('div', class_='_1y5q8ag4')]) == 3:
                sale_beds.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][0])
                sale_baths.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][1])
                sale_reception.append([i.text if 'reception' in i.text else None for i in url_soup.find('div', class_='_1y5q8ag4')][2])
                sale_property_size.append(None)
                sale_epc_rating.append([i.text if 'rating' in i.text else None for i in url_soup.find('div', class_='_1y5q8ag4')][2])
            elif len([i.text for i in url_soup.find('div', class_='_1y5q8ag4')]) == 2:
                sale_beds.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][0])
                sale_baths.append([i.text if 'bath' in i.text else None for i in url_soup.find('div', class_='_1y5q8ag4')][1])
                sale_reception.append([i.text if 'reception' in i.text else None for i in url_soup.find('div', class_='_1y5q8ag4')][1])
                sale_property_size.append(None)
                sale_epc_rating.append(None)
            elif len([i.text for i in url_soup.find('div', class_='_1y5q8ag4')]) == 1:
                sale_beds.append([i.text for i in url_soup.find('div', class_='_1y5q8ag4')][0])
                sale_baths.append(None)
                sale_reception.append(None)
                sale_property_size.append(None)
                sale_epc_rating.append(None)
            try:
                sale_key_features.append([i.text for i in url_soup.find('div', class_="_1k66bqh1")])
            except TypeError:  # where no key features in the listing
                sale_key_features.append(None)
            sale_description.append(url_soup.find('section', class_='_179tqtag').text)

# %%
# View Rent Data
sale_df = pd.DataFrame({
    'property_id': sale_id,
    'title': sale_title,
    'url': sale_urls,
    'address': sale_address,
    'price': sale_price,
    'agent': sale_agent,
    'agent_url': sale_agent_url,
    'date_added': sale_date_added,
    'beds': sale_beds,
    'baths': sale_baths,
    'reception': sale_reception,
    'property_size': sale_property_size,
    'epc_rating': sale_epc_rating,
    'sale_tenure': sale_tenure,
    'sale_tenure_1': sale_tenure_1,
    'key_features': sale_key_features,
    'description': sale_description,

})

sale_df

# %%
filepath = Path(
    '/Users/nnankewilliams/Library/CloudStorage/OneDrive-Personal/Data Analytics/my_projects/mappa/zp_sale_df.csv')
sale_df.to_csv(filepath, index=False)
