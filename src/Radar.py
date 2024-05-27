# Radar.py

from .MGMService import get_request
from . import tools

_radar_details_cache = None

def _find_short_name(radar_name, radar_details):
    radar_name_formatted = radar_name.strip().capitalize()

    if radar_name_formatted in radar_details:
        return radar_name_formatted, radar_details[radar_name_formatted]['shortName']
    
    radar_name_lower = radar_name.strip().lower()
    for radar_name_key, details in radar_details.items():
        if details['shortName'] == radar_name_lower:
            return radar_name_key, radar_name_lower
        
    raise ValueError(f"Radar name '{radar_name}' not found.")

def _check_product_support(product, radar_details, radar_name):
    if product not in radar_details[radar_name]['supportedProductTypes']:
        raise ValueError(f"Product '{product}' is not supported for radar '{radar_name}'.")

def get_image(radar_name, product, number):
    global _radar_details_cache
    if _radar_details_cache is None:
        _radar_details_cache = get_details()
    radar_details = _radar_details_cache
    
    radar_name_key, short_name = _find_short_name(radar_name, radar_details)
    _check_product_support(product, radar_details, radar_name_key)

    if not isinstance(number, int) or not 1 <= number <= 15:
        raise ValueError("Image sequence number must be an integer between 1 and 15.")

    endpoint = f'FTPDATA/uzal/radar/{short_name}/{short_name}{product}{number}.jpg'
    return get_request(endpoint)

def get_details():
    endpoint = 'sondurum/radar.aspx'
    response = get_request(endpoint)
    radar_links = response.find(id='cph_body_pRadar').find_all('a')

    radar_details = {}
    for radar_link in radar_links:
        radar_url = f"{endpoint}{radar_link['href']}"
        radar_response = get_request(radar_url)

        radarName = radar_response.find(id='sfB').find('strong').text.strip()
        short_name = radar_response.find(id='cph_body_imgResim')["src"].split("/")[4]
        try:
            image_types_elements = radar_response.find(id='cph_body_pUrun').find_all('a',href=True)
            supported_product_types = [
                item.get("href").split("&")[2].split("=")[1].split("#")[0]
                for item in image_types_elements
            ]
        except:
            supported_product_types = ['ppi']

        radar_details[radarName] = {
            "shortName": short_name,
            "supportedProductTypes": supported_product_types
        }
    return radar_details
