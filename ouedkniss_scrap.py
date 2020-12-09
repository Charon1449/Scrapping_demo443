# coding=utf-8
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import re
from io import BytesIO
import pytesseract
from PIL import Image


def get_phone_number(link):
        Phone = pytesseract.image_to_string(Image.open(BytesIO(requests.get("https:"+str(BeautifulSoup((requests.get(link)).text,'html.parser').find('p',class_='Phone').find('img').get('src'))).content)))
        if  (Phone == "Phone"):
            return "None"
        else:
            return Phone

def scrap_one_page(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    soup = soup.find('div', id='page_middle')
    soup = soup.find_all('div', class_='annonce')
    for annonce in soup:
        DataFrame = pd.DataFrame(
            columns=['Type', 'Marque', 'Modele', 'Energie', 'Moteur', 'Transmission', 'Kilometrage', 'Annee', 'Couleur',
                     'Papier', 'Prix',
                     'Proprietaire', 'Vile', 'Numero'])
        try:
            list = str((annonce.find('li', class_='annonce_titre')).find('h2').text).split(' ')
            marque = list.pop(0)
            annee = list.pop(-1)
            version = str((annonce.find('li', class_='annonce_titre')).find('h2').text).replace(marque, "")
            version = version.replace(annee, "")
            DataFrame['Type'] = [annonce.find('span', class_="annonce_get_description").contents[0]]
            DataFrame['Marque'] = [marque]
            DataFrame['Modele'] = [version]
            DataFrame['Energie'] = ["".join(
                re.findall('\w+', str(annonce.find_all('span', {'class': re.compile(r'vehicule_energie')})))).replace(
                "spanclassvehicule_energie_", "").replace("span", "").replace("1", "").replace("2", "").replace("3",
                                                                                                                "")]
            DataFrame['Moteur'] = [annonce.find('span', id="version").text]
            DataFrame['Transmission'] = [
                "".join(str(annonce.find('span', class_="annonce_get_description").contents[11]).split(':')[1]).replace(
                    "</b>", "")]
            DataFrame['Kilometrage'] = [
                "".join(re.findall('\d+', str(annonce.find_all('span', class_="vehicule_kilometrage"))))]
            DataFrame['Annee'] = [annee]
            DataFrame['Couleur'] = [
                "".join(str(annonce.find('span', class_="annonce_get_description").contents[13]).split(':')[1])]
            DataFrame['Papier'] = [
                str(annonce.find('span', class_="annonce_get_description").contents[15]).replace('</b>', "").replace(
                    '<b>', "")]
            if annonce.find('span', class_='annonce_prix') is not None:
                DataFrame['Prix'] = [
                    "".join(re.findall('\d+', str(annonce.find('span', class_='annonce_prix').find('span'))))]
            DataFrame['Proprietaire'] = [annonce.find('a', class_='name').text]
            DataFrame['Vile'] = [annonce.find('span', class_="titre_wilaya").text]
            DataFrame['Numero'] = [get_phone_number("https://www.ouedkniss.com/"+str(annonce.find('li',class_='annonce_titre').find('a').get('href')))]
            DataFrame.to_sql('Vehicule', con=engine, if_exists='append')


        except Exception as ex:
            print('\n***********************')
            print (type(ex).__name__)
            print('***********************\n')

engine = create_engine("sqlite:///OuedKniss.db",echo=True)
for page in range(1,40):
    scrap_one_page("https://www.ouedkniss.com/automobiles/{page_nb}".format(page_nb=str(page)))
