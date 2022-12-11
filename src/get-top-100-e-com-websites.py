# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Create request for the list of shops
url = 'https://www.ehi.org/de/top-100-umsatzstaerkste-onlineshops-in-deutschland/'
response = requests.get(url)

# Create a soup object
soup = BeautifulSoup(response.text, 'html.parser')

# Empty list to store the data
shops = []

# Find the first table on the website
table = soup.find("table")

# Loop the table and get the shop information
for tr in table.find_all('tr')[1:]:
    tds = tr.find_all('td')
    if len(tds) > 0:
        shop = [tds[1].text, float(tds[2].text.replace(".", "").replace(",",".")), tds[3].text]
        shops.append(shop)

# Create dataframe from list
df = pd.DataFrame(shops, columns = ['url', 'e-com_net_rev_2021', 'main_product_segments'])

# Translate the main product segments column to english
translations = {'Bekleidung': 'clothing', 
                'Generalist': 'generalist', 
                'Unterhaltungselektronik': 'consumer_electronics', 
                'Möbel & Haushaltswaren': 'furniture and homewares', 
                'Drogerie & Gesundheit': 'drugstore and health', 
                'DIY, Garten & Tierbedarf': 'diy, garden and pet supplies', 
                'Hobby & Schreibwaren': 'hobby and writing materials', 
                'Sport & Outdoor': 'sports and outdoor', 
                'Lebensmittel & Getränke': 'groceries and drinks', 
                'Spielzeug & Baby': 'toys and baby',
                'Bücher, Filme, Musik & Games': 'books, movies, music and games', 
                'Haushaltsgeräte': 'home appliances', 
                'Taschen & Accessoires': 'bags and accessories'}                                                                                          

df = df.replace({"main_product_segments": translations}) 

# Save data as csv file    
df.to_csv('top_100_e-com_websites_by_revenue.csv', index=False)