import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from pathlib import Path

pgs = np.arange(0, 24 * 42, 24)

# %%
# Scrape Rent Data
for pg in pgs:
    url = f'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&radius=40.0&index={pg}&propertyTypes=&maxDaysSinceAdded=14&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='
    page = requests.get(url)
    # Save relevant html on local drive to avoid flodding site with hits
    with open(f'rm_pages/rm_page_{pg}.html', 'w+') as file:
        file.write(page.text)

#%%
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

#%%
for pg in pgs:
    # Let's read htmls we saved to retrieve the following information:
    with open(f'rm_pages/rm_page_{pg}.html') as file:
        page = file.read()
        soup = BeautifulSoup(page, 'html.parser')
        soup_content = soup.find_all('div',
                                 class_='l-propertySearch-results propertySearch-results',
                                 id='propertySearch-results-container')
        # Parse Rent Data
        for item in soup_content:
            # On each html, there are 25 listings:
            for i in range(25):
                # p_card_info gives us the html information for the listing
                pcard_info = item.find_all(attrs={"data-test": f'propertyCard-{i}'})
                rent_id.append(pcard_info[0].find('a', class_='propertyCard-anchor').get('id'))
                rent_title.append(pcard_info[0].find('h2', class_='propertyCard-title').text)
                rent_agent_phone.append(pcard_info[0].find('a', class_="propertyCard-contactsPhoneNumber").text)
                rent_tag.append(pcard_info[0].find_all('span', class_='propertyCard-tagTitle')[1].text)
                rent_property_status.append(pcard_info[0].find('a', class_="linkBox-bodyLink", rel="nofollow").text)
                pcard_link = pcard_info[0].find('div', class_='propertyCard-description').find('a').get('href')
                pcard_link_full = f'https://www.rightmove.co.uk{pcard_link}'
                rent_urls.append(pcard_link_full)

rent_urls

#%%
for ind, url in enumerate(rent_urls):
    page = requests.get(url, headers={'User-agent': 'NWills'})
    if page.status_code == 200:
        with open(f'rm_pages/rm_property_{ind}.html', 'w+') as file:
                file.write(page.text)
    else:
        print(ind, page.status_code)
    if ind % 10 == 0:
        time.sleep(5)

#%%
# Parse Rent Data into DF
for i in range(1050):
    with open(f'rm_pages/rm_property_{i}.html') as file:
        url_page = file.read()
        url_soup = BeautifulSoup(url_page, 'html.parser')
        url_soup_content = url_soup.find_all('div', class_='_1kesCpEjLyhQyzhf_suDHz')

        rent_address.append(
            url_soup_content[0].find('h1', class_='_2uQQ3SV0eMHL1P6t5ZDo2q', itemprop='streetAddress').text)
        rent_country.append(url_soup_content[0].find('meta', itemprop='addressCountry').get('content'))
        rent_pry_price.append(url_soup_content[0].find('div', class_='_1gfnqJ3Vtd1z40MlC0MzXu').find('span').text)
        rent_sec_price.append(url_soup_content[0].find('div', class_='HXfWxKgwCdWTESd5VaU73').text)
        rent_agent_url.append(
            f'https://www.rightmove.co.uk{url_soup_content[0].find("a", class_="_2rTPddC0YvrcYaJHg9wfTP").get("href")}')
        rent_agent.append(url_soup_content[0].find("h3", class_="_3PpywCmRYxC0B-ShNWxstv").text)
        rent_agent_address.append(url_soup_content[0].find('p', class_="_1zJF3rohTQLpqNFDBD59qt").text)
        rent_date_added.append(url_soup_content[0].find('div', class_="_2nk2x6QhNB1UrxdI5KpvaF").text)
        rent_letting_details.append([i.text for i in url_soup_content[0].find('dl', class_="_2E1qBJkWUYMJYHfYJzUb_r").find_all('div', class_='_2RnXSVJcWbWv4IpBC1Sng6')])
        if len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 4:
            rent_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
            rent_beds.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1])
            rent_baths.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][2])
            rent_property_size.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][3])
        elif len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 3:
            rent_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
            rent_beds.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1])
            rent_baths.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][2])
            rent_property_size.append(None)
        elif len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 2:
            rent_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
            rent_beds.append(None)
            rent_baths.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1])
            rent_property_size.append(None)
        elif len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 1:
            rent_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
            rent_beds.append(None)
            rent_baths.append(None)
            rent_property_size.append(None)
        else:
            print(i, 'has no info for property, beds, baths')
            rent_property_type.append(None)
            rent_beds.append(None)
            rent_baths.append(None)
        try:
            rent_key_features.append([i.text for i in url_soup_content[0].find('ul', class_="_1uI3IvdF5sIuBtRIvKrreQ")])
        except TypeError: # where no key features in the listing
            rent_key_features.append(None)
        rent_description.append(url_soup_content[0].find('div', class_='STw8udCxUaBUMfOOZu0iL').text)


#%%
# View Rent Data
rent_df = pd.DataFrame({
    'property_id': rent_id,
    'title': rent_title,
    'url': rent_urls,
    'address': rent_address,
    'country': rent_country,
    'tag': rent_tag,
    'property_status': rent_property_status,
    'primary price': rent_pry_price,
    'secondary price': rent_sec_price,
    'agent': rent_agent,
    'agent_address': rent_agent_address,
    'agent_phone': rent_agent_phone,
    'agent_url': rent_agent_url,
    'date_added': rent_date_added,
    'letting_details': rent_letting_details,
    'property_type': rent_property_type,
    'beds': rent_beds,
    'baths': rent_baths,
    'key_features': rent_key_features,
    'description': rent_description,
    'property_size': rent_property_size
})

rent_df

#%%
filepath = Path('/Users/nnankewilliams/Library/CloudStorage/OneDrive-Personal/Data Analytics/my_projects/mappa/rm_rent_df.csv')
rent_df.to_csv(filepath, index=False)

# %%
# Scrape Sale Data
for pg in pgs:
    url = f'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&radius=40.0&index={pg}&propertyTypes=&maxDaysSinceAdded=14&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='
    page = requests.get(url)

    with open(f'rm_pages/rm_page_sale_{pg}.html', 'w+') as file:
        file.write(page.text)

# %%
# DF Details
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

# %%
sale_urls = list()
for pg in pgs:
    with open(f'rm_pages/rm_page_sale_{pg}.html') as file:
        page = file.read()
        soup = BeautifulSoup(page, 'html.parser')
        soup_content = soup.find_all('div',
                                     class_='l-propertySearch-results propertySearch-results',
                                     id='propertySearch-results-container')
        # Parse Rent Data
        for item in soup_content:
            for i in range(25):
                pcard_info = item.find_all(attrs={"data-test": f'propertyCard-{i}'})
                sale_id.append(pcard_info[0].find('a', class_='propertyCard-anchor').get('id'))
                sale_title.append(pcard_info[0].find('h2', class_='propertyCard-title').text)
                sale_agent_phone.append(pcard_info[0].find('a', class_="propertyCard-contactsPhoneNumber").text)
                sale_tag.append(pcard_info[0].find_all('span', class_='propertyCard-tagTitle')[1].text)
                try:
                    sale_property_status.append(pcard_info[0].find('a', class_="linkBox-bodyLink", rel="nofollow").text)
                except AttributeError:
                    sale_property_status.append(pcard_info[0].find('a', class_="linkBox-bodyLink").text)
                pcard_link = pcard_info[0].find('div', class_='propertyCard-description').find('a').get('href')
                pcard_link_full = f'https://www.rightmove.co.uk{pcard_link}'
                sale_urls.append(pcard_link_full)

sale_urls
#%%
for ind, url in enumerate(sale_urls):
    page = requests.get(url, headers={'User-agent': 'BReds'})
    if page.status_code == 200:
        with open(f'rm_pages/rm_property_sale_{ind}.html', 'w+') as file:
            file.write(page.text)
    else:
        print(ind, page.status_code)
    if ind % 10 == 0:
        time.sleep(15)

#%%
for i in range(1050):
    with open(f'rm_pages/rm_property_sale_{i}.html') as file:
        url_page = file.read()
        url_soup = BeautifulSoup(url_page, 'html.parser')
        url_soup_content = url_soup.find_all('div', class_='_1kesCpEjLyhQyzhf_suDHz')

        sale_address.append(
            url_soup_content[0].find('h1', class_='_2uQQ3SV0eMHL1P6t5ZDo2q', itemprop='streetAddress').text)
        sale_country.append(url_soup_content[0].find('meta', itemprop='addressCountry').get('content'))
        sale_price.append(url_soup_content[0].find('div', class_='_1gfnqJ3Vtd1z40MlC0MzXu').find('span').text)
        sale_agent_url.append(
            f'https://www.rightmove.co.uk/{url_soup_content[0].find("a", class_="_2rTPddC0YvrcYaJHg9wfTP").get("href")}')
        try:
            sale_agent.append(url_soup_content[0].find("h3", class_="_3PpywCmRYxC0B-ShNWxstv").text)
        except AttributeError:
            sale_agent.append(url_soup_content[0].find("h2", class_="ecNNU4kaFhDCkrVPGQ88A").text)
        sale_agent_address.append(url_soup_content[0].find('p', class_="_1zJF3rohTQLpqNFDBD59qt").text)
        try:
            sale_date_added.append(url_soup_content[0].find('div', class_="_2nk2x6QhNB1UrxdI5KpvaF").text)
        except AttributeError:
            sale_date_added.append('Added today')
        if len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 5:
            sale_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
            sale_beds.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1])
            sale_baths.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][2])
            sale_property_size.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][3])
            sale_tenure.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][4])
        elif len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 4:
            sale_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
            sale_beds.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1])
            sale_baths.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][2])
            sale_tenure.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][3])
            sale_property_size.append(None)
        elif len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 3:
            sale_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
            sale_beds.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1])
            sale_tenure.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][2])
            sale_property_size.append(None)
            sale_baths.append(None)
        elif len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 2:
            if 'ft.' in [i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1]:
                sale_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
                sale_property_size.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1])
                sale_beds.append(None)
                sale_baths.append(None)
                sale_tenure.append(None)
            else:
                sale_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
                sale_tenure.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][1])
                sale_beds.append(None)
                sale_baths.append(None)
                sale_property_size.append(None)
        elif len([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')]) == 1:
            sale_property_type.append([i.text for i in url_soup_content[0].find('div', class_="_4hBezflLdgDMdFtURKTWh").find_all('dd')][0])
            sale_beds.append(None)
            sale_baths.append(None)
            sale_property_size.append(None)
            sale_tenure.append(None)
        else:
            print(i, 'has no info for property, beds, baths')
            sale_property_type.append(None)
            sale_beds.append(None)
            sale_baths.append(None)
            sale_tenure.append(None)
        try:
            sale_key_features.append([i.text for i in url_soup_content[0].find('ul', class_="_1uI3IvdF5sIuBtRIvKrreQ")])
        except TypeError: # where no key features in the listing
            sale_key_features.append(None)
        sale_description.append(url_soup_content[0].find('div', class_='STw8udCxUaBUMfOOZu0iL').text)


#%%
# View Rent Data
sale_df = pd.DataFrame({
    'property_id': sale_id,
    'title': sale_title,
    'url': sale_urls,
    'address': sale_address,
    'tag': sale_tag,
    'property_status': sale_property_status,
    'country': sale_country,
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
    'tenure':sale_tenure,
    'key_features': sale_key_features,
    'description': sale_description,

})

sale_df

#%%
filepath = Path('/Users/nnankewilliams/Library/CloudStorage/OneDrive-Personal/Data Analytics/my_projects/mappa/rm_sale_df.csv')
sale_df.to_csv(filepath, index=False)

