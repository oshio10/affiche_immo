#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__, template_folder='templates')


# main.py
@app.route('/form', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lien = request.form['lien']
        dicoInfo = extract_property_info(lien)
        return render_template('result.html', **dicoInfo)
    return render_template('form.html')



def extract_property_info(url):
    # Envoyer une requête GET au site web
    response = requests.get(url)

    # Analyser le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupérer le titre du bien immobilier
    title = soup.select_one('h1.entry-title.entry-prop').text.strip()

    # Récupérer les informations du bien immobilier
    info = soup.select_one('div.wpestate_property_description').text.strip()

    # Récupérer tous les éléments div contenant les images de fond
    background_divs = soup.select('div.col-md-6.image_gallery.lightbox_trigger.special_border')

    # Récupérer le style du premier élément div
    style = background_divs[0]['style']

    # Utiliser une expression régulière pour extraire le lien de l'image de fond
    pattern = r"url\((.*?)\)"
    match = re.search(pattern, style)
    if match:
        image_url = match.group(1)
    else:
        image_url = ""

    # Récupérer le prix du bien immobilier
    price = soup.select_one('div.listing_detail.col-md-4.property_default_price').text.strip()

    # Récupérer la classe énergétique du bien immobilier
    energy_class_element = soup.select('div.indicator-energy')
    
    energy_class1 = energy_class_element[0].text.strip() if energy_class_element else 'NR'
    energy_class2 = energy_class_element[1].text.strip() if energy_class_element else 'NR'



    # Récupérer le logo de l'entreprise
    logo = soup.select_one('[src="https://yrsa-progedim.fr/wp-content/uploads/2022/11/logo_YRSA-PROGEDIM_white_web.webp"]')['src']

    # Retourner les informations extraites
    return {
        'title': title,
        'info': info,
        'image': image_url,
        'price': price,
        'energy_class1': energy_class1,
        'energy_class2': energy_class2,
        'logo': logo
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)
