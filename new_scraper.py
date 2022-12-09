from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# Enlace a NASA Exoplanet
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Controlador web
options = webdriver.EdgeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
browser = webdriver.Edge(options=options)
browser.get(START_URL)

time.sleep(10)

page = requests.get(START_URL)

new_stars_data = []


soup = BeautifulSoup(page.content, "html.parser")

start_table = soup.find_all("table", attrs={"class": "wikitable sortable"})

temporal_list = []
tr_save = start_table[1].find_all("tr")

for scrap_temporal in tr_save:

    td_save = scrap_temporal.find_all('td')
    row = [i.text.rstrip() for i in td_save] 
    
    temporal_list.append(row)


# Crear 4 listas vacias en donde vas a guardar, nombre de la estrella, distancia, masa y radio
star_names = []
distance = []
mass = []
radius = []
# Ciclo for que con el range en el q vas a recorrer la longitud de la temporal_list y cuando lo recorras vas a ir guardando en cada lista q ya creaste arriba lo q le corresponde
#star_names.append(temporal_list[indice][0]) distance 5 masa 7 radio 8
for indice in range(1,len(temporal_list)):
    star_names.append(temporal_list[indice][0])
    distance.append(temporal_list[indice][5])
    mass.append(temporal_list[indice][7])
    radius.append(temporal_list[indice][8])

# crear los encabezados, convertirlo en un dataframe y lo conviertes en un archivo de csv
headers = ['star_names', 'distance', 'mass', 'radius']

new_star_df = pd.DataFrame(list(zip(star_names, distance, mass, radius)), columns = headers )
new_star_df.to_csv('new_scraped_data.csv', index=True, index_label="id")