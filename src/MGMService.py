# MGMService.py

import requests
from bs4 import BeautifulSoup


def get_data(endpoint, params=None):
    base_url = "https://servis.mgm.gov.tr/web/"
    headers = {"Origin": "https://www.mgm.gov.tr"}
    url = f"{base_url}{endpoint}"
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_request(endpoint, params=None):
    base_url = "https://www.mgm.gov.tr/"
    url = f"{base_url}{endpoint}"
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
