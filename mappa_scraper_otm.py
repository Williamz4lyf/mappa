import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from pathlib import Path

pgs = np.arange(0, 42, 1)

# %%
# Scrape Rent Data
for pg in pgs:
    url = f'https://www.onthemarket.com/for-sale/property/london/?page={pg}&recently-added=7-days&view=grid'
    page = requests.get(url, headers={'User-agent': 'NWills'})

    with open(f'otm_pages/otm_page_sale_{pg}.html', 'w+') as file:
        file.write(page.text)

for pg in pgs:
    url = f'https://www.onthemarket.com/to-rent/property/london/?page={pg}&recently-added=7-days&view=grid'
    page = requests.get(url, headers={'User-agent': 'BReds'})

    with open(f'otm_pages/otm_page_rent_{pg}.html', 'w+') as file:
        file.write(page.text)

# %%
# DF Details - This is the information to be scraped from the site
rent_urls = list()
rent_id = list()
rent_title = list()
rent_property_status = list()
rent_tag = list()
rent_agent_phone = list()
rent_address = list()
rent_country = list()
rent_pry_price = list()
rent_sec_price = list()
rent_agent = list()
rent_agent_address = list()
rent_agent_url = list()
rent_date_added = list()
rent_letting_details = list()
rent_property_type = list()
rent_beds = list()
rent_baths = list()
rent_key_features = list()
rent_description = list()
rent_property_size = list()
rent_address_2 = list()
rent_key_info = list()
rent_epc = list()


sale_urls = list()
sale_id = list()
sale_title = list()
sale_tag = list()
sale_property_status = list()
sale_agent_phone = list()
sale_address = list()
sale_country = list()
sale_price = list()
sale_agent = list()
sale_agent_address = list()
sale_agent_url = list()
sale_date_added = list()
sale_property_type = list()
sale_beds = list()
sale_baths = list()
sale_tenure = list()
sale_key_features = list()
sale_description = list()
sale_property_size = list()
sale_address_2 = list()
sale_epc = list()
sale_key_info = list()

for pg in pgs:
    # Read saved htmls we to retrieve necessary information:
    # Rent Pages
    with open(f'otm_pages/otm_page_rent_{pg}.html') as file:
        page = file.read()
        soup = BeautifulSoup(page, 'html.parser')
        soup_content = soup.find_all('ul', class_='grid-list-tabcontent hasSpotlight')
        # p_card_info contains the html information for the listing
        pcard_info = soup_content[0].find_all('li', class_='otm-PropertyCard')

        # Parse Rent Data for the page - There are 23 listings on each page
        for i in range(23):
            if 'result' in pcard_info[i].find('div').get('id'):
                rent_id.append(pcard_info[i].find('div').get('id'))
                rent_title.append(
                    pcard_info[i].find('a', itemtype="http://schema.org/LocationFeatureSpecification").text)
                link = pcard_info[i].find("a").get("href")
                pcard_link = f'https://www.onthemarket.com{link}'
                rent_urls.append(pcard_link)
                rent_agent_phone.append(
                    pcard_info[i].find('div', class_="otm-Telephone text-link font-semibold flex items-center").text)
                rent_address.append(pcard_info[i].find('span', class_='address').find('a').text)
            else:
                pass

    # Sale Pages
    with open(f'otm_pages/otm_page_sale_{pg}.html') as file:
        page = file.read()
        soup = BeautifulSoup(page, 'html.parser')
        soup_content = soup.find_all('ul', class_='grid-list-tabcontent hasSpotlight')
        # p_card_info contains the html information for the listing
        pcard_info = soup_content[0].find_all('li', class_='otm-PropertyCard')

        # Parse Sale Data for the page - There are 23 listings on each page
        for i in range(23):
            if 'result' in pcard_info[i].find('div').get('id'):
                sale_id.append(pcard_info[i].find('div').get('id'))
                sale_title.append(
                    pcard_info[i].find('a', itemtype="http://schema.org/LocationFeatureSpecification").text)
                link = pcard_info[i].find("a").get("href")
                pcard_link = f'https://www.onthemarket.com{link}'
                sale_urls.append(pcard_link)
                sale_agent_phone.append(
                    pcard_info[i].find('div', class_="otm-Telephone text-link font-semibold flex items-center").text)
                sale_address.append(pcard_info[i].find('span', class_='address').find('a').text)
            else:
                pass

# %%
# Save individual listing htmls into local drive
for ind, url in enumerate(rent_urls):
    if ind <= 366:
        pass
    else:
        page = requests.get(url, headers={'User-agent': 'NWills'})
        if page.status_code == 200:
            with open(f'otm_pages/otm_property_rent_{ind}.html', 'w+') as file:
                file.write(page.text)
        else:
            print(ind, page.status_code)
        if ind % 10 == 0:
            time.sleep(5)

for ind, url in enumerate(sale_urls):
    page = requests.get(url, headers={'User-agent': 'BReds'})
    if page.status_code == 200:
        with open(f'otm_pages/otm_property_sale_{ind}.html', 'w+') as file:
            file.write(page.text)
    else:
        print(ind, page.status_code)
    if ind % 10 == 0:
        time.sleep(5)

# %%
# Parse Rent Data into DF
for i in range(924):
    if i in [673]:
        pass
    else:
        with open(f'otm_pages/otm_property_rent_{i}.html') as file:
            url_page = file.read()
            url_soup = BeautifulSoup(url_page, 'html.parser')
            url_soup_content = url_soup.find_all('section', class_='main-col')
            url_soup_content_2 = url_soup.find_all('div', class_='agent-info otm-new')
            try:
                rent_address_2.append(
                    url_soup_content[0].find('div', class_="text-slate h4 font-normal leading-none font-heading").text)
            except AttributeError:
                rent_address_2.append(None)
            try:
                rent_pry_price.append(url_soup_content[0].find('span', class_="mb-0 text-lg font-bold text-denim price").text)
            except AttributeError:
                rent_pry_price.append(None)
            try:
                rent_property_status.append(url_soup_content[0].find('h1', class_='h4 md:text-xl').text)
            except AttributeError:
                rent_property_status.append(None)
            rent_agent_url.append(url_soup_content[0].find('a', class_='flex items-center text-link pt-4 hover:underline').get('href'))
            rent_agent.append(url_soup_content_2[0].find("h2", class_="text-base2 font-body").text)
            rent_agent_address.append(url_soup_content_2[0].find('p', class_="text-sm text-slate").text)
            try:
                rent_date_added.append(
                    url_soup_content[0].find('div', class_="otm-LabelChip inline-block font-heading p-2 py-1 rounded-full bg-dove/40 text-demin inline-block").text)
            except AttributeError:
                rent_date_added.append('Added today')
            rent_property_type.append(
                url_soup_content[0].find('div', class_='otm-PropertyIcon flex items-center mr-6 py-0.5 mr-6 py-0.5').find('div').text)
            if len([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')]) == 4:
                rent_beds.append(
                    [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][0])
                rent_baths.append(
                    [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][1])
                rent_epc.append(
                    [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][2])
                rent_property_size.append(
                    [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][3])
            elif len([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')]) == 3:
                rent_beds.append(
                    [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][0])
                rent_baths.append(
                    [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][1])
                rent_epc.append(None)
                rent_property_size.append([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][2])
            elif len([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')]) == 2:
                rent_beds.append(
                    [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][0])
                rent_baths.append(
                    [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][1])
                rent_epc.append(None)
                rent_property_size.append(None)
            else:
                print(i, len([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')]))
                rent_beds.append(None)
                rent_baths.append(None)
                rent_epc.append(None)
                rent_property_size.append(None)
            try:
                rent_key_features.append(
                    [li.text for li in url_soup_content[0].find('ul', class_="ml-0 mt-6 gap-4 font-heading text-semibold text-md text-denim lg:grid lg:grid-cols-2")])
            except TypeError:
                rent_key_features.append(None)
            rent_key_info.append(
                [i.text for i in url_soup_content[0].find('div', class_='text-md space-y-1.5 mt-6 font-heading').find_all('span')])
            rent_description.append(url_soup_content[0].find('div', class_='description-truncate').find('div').text)

# Parse Sale Data into DF
for i in range(882):
    with open(f'otm_pages/otm_property_sale_{i}.html') as file:
        url_page = file.read()
        url_soup = BeautifulSoup(url_page, 'html.parser')
        url_soup_content = url_soup.find_all('section', class_='main-col')
        url_soup_content_2 = url_soup.find_all('div', class_='agent-info otm-new')
        try:
            sale_address_2.append(
                url_soup_content[0].find('div', class_="text-slate h4 font-normal leading-none font-heading").text)
        except AttributeError:
            sale_address_2.append(None)
        try:
            sale_price.append(url_soup_content[0].find('span', class_="mb-0 text-lg font-bold text-denim price").text)
        except AttributeError:
            sale_price.append(None)
        try:
            sale_property_status.append(url_soup_content[0].find('h1', class_='h4 md:text-xl').text)
        except AttributeError:
            sale_property_status.append(None)
        sale_agent_url.append(url_soup_content[0].find('a', class_='flex items-center text-link pt-4 hover:underline').get('href'))
        sale_agent.append(url_soup_content_2[0].find("h2", class_="text-base2 font-body").text)
        sale_agent_address.append(url_soup_content_2[0].find('p', class_="text-sm text-slate").text)
        try:
            sale_date_added.append(
                url_soup_content[0].find('div', class_="otm-LabelChip inline-block font-heading p-2 py-1 rounded-full bg-dove/40 text-demin inline-block").text)
        except AttributeError:
            sale_date_added.append('Added today')
        sale_property_type.append(
            url_soup_content[0].find('div', class_='otm-PropertyIcon flex items-center mr-6 py-0.5 mr-6 py-0.5').find('div').text)
        if len([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')]) == 4:
            sale_beds.append(
                [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][0])
            sale_baths.append(
                [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][1])
            sale_epc.append(
                [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][2])
            sale_property_size.append(
                [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][3])
        elif len([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')]) == 3:
            sale_beds.append(
                [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][0])
            sale_baths.append(
                [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][1])
            sale_epc.append(None)
            sale_property_size.append([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][2])
        elif len([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')]) == 2:
            sale_beds.append(
                [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][0])
            sale_baths.append(
                [i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')][1])
            sale_epc.append(None)
            sale_property_size.append(None)
        else:
            print(i, len([i.text for i in url_soup_content[0].find('div', class_="font-heading text-xs flex flex-wrap border-t border-b mb-6 md:text-md py-3 md:py-4 md:mb-9").find_all('div', class_='flex items-center mr-6 py-0.5')]))
            sale_beds.append(None)
            sale_baths.append(None)
            sale_epc.append(None)
            sale_property_size.append(None)
        try:
            sale_key_features.append(
                [li.text for li in url_soup_content[0].find('ul', class_="ml-0 mt-6 gap-4 font-heading text-semibold text-md text-denim lg:grid lg:grid-cols-2")])
        except TypeError:
            sale_key_features.append(None)
        try:
            sale_key_info.append(
                [i.text for i in url_soup_content[0].find('div', class_='text-md space-y-1.5 mt-6 font-heading').find_all('span')])
        except AttributeError:
            sale_key_info.append(None)
        sale_description.append(url_soup_content[0].find('div', class_='description-truncate').find('div').text)

# View Rent Data
# Remove value at index 673 in the following lists:
rent_id.pop(673)
rent_title.pop(673)
rent_urls.pop(673)
rent_address.pop(673)
rent_agent_phone.pop(673)

rent_df = pd.DataFrame({
    'property_id': rent_id,
    'title': rent_title,
    'url': rent_urls,
    'address': rent_address,
    'address_2': rent_address_2,
    'property_status': rent_property_status,
    'primary price': rent_pry_price,
    'agent': rent_agent,
    'agent_address': rent_agent_address,
    'agent_phone': rent_agent_phone,
    'agent_url': rent_agent_url,
    'date_added': rent_date_added,
    'property_type': rent_property_type,
    'beds': rent_beds,
    'baths': rent_baths,
    'key_features': rent_key_features,
    'description': rent_description,
    'property_size': rent_property_size,
    'epc_rating': rent_epc,
    'key_info': rent_key_info
})

# View Sale Data
sale_df = pd.DataFrame({
    'property_id': sale_id,
    'title': sale_title,
    'url': sale_urls,
    'address': sale_address,
    'address_2': sale_address_2,
    'property_status': sale_property_status,
    'price': sale_price,
    'agent': sale_agent,
    'agent_address': sale_agent_address,
    'agent_phone': sale_agent_phone,
    'agent_url': sale_agent_url,
    'date_added': sale_date_added,
    'property_type': sale_property_type,
    'beds': sale_beds,
    'baths': sale_baths,
    'property_size': sale_property_size,
    'key_features': sale_key_features,
    'description': sale_description,
    'epc_rating': sale_epc,
    'key_info': sale_key_info

})

filepath = Path(
    '/Users/nnankewilliams/Library/CloudStorage/OneDrive-Personal/Data Analytics/my_projects/mappa/otm_rent_df.csv')
rent_df.to_csv(filepath, index=False)

filepath = Path(
    '/Users/nnankewilliams/Library/CloudStorage/OneDrive-Personal/Data Analytics/my_projects/mappa/otm_sale_df.csv')
sale_df.to_csv(filepath, index=False)
