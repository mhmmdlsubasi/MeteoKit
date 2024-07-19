"""
MGM (Meteoroloji Genel Müdürlüğü) servisleri ile etkileşim için modül.

Fonksiyonlar:
    - get_data(endpoint: str, params: dict = None) -> dict:
        MGM servisinden JSON verisi alır.

    - get_request(endpoint: str, params: dict = None) -> BeautifulSoup:
        MGM web sitesinden HTML verisi çeker.
"""

import requests
from bs4 import BeautifulSoup
from modules.submodules.log import logger

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(
    total=5,
    read=5,
    connect=5,
    backoff_factor=0.1
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_data(endpoint: str, params: dict = None) -> dict:
    """
    MGM servisinden JSON verisi alır.

    Args:
        endpoint (str): Sorgulanacak endpoint.
        params (dict, optional): İsteğin parametreleri. Varsayılan: None.

    Returns:
        dict: MGM servisinden gelen JSON verisi.

    Raises:
        ValueError: Hatalı HTTP durum kodunda tetiklenir.
    """
    base_url = "https://servis.mgm.gov.tr/web/"
    headers = {"Origin": "https://www.mgm.gov.tr"}
    url = f"{base_url}{endpoint}"

    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        logger.info("Başarılı JSON veri alımı: %s", response.url)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", http_err)
        raise ValueError(f"HTTP error occurred: {http_err}") from http_err
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error occurred: %s", req_err)
        raise ValueError(f"Request error occurred: {req_err}") from req_err


def get_request(endpoint: str, params: dict = None) -> BeautifulSoup:
    """
    MGM web sitesinden HTML verisi çeker.

    Args:
        endpoint (str): Alınacak endpoint.
        params (dict, optional): İsteğin parametreleri. Varsayılan: None.

    Returns:
        BeautifulSoup: MGM web sitesinden alınan ayrıştırılmış HTML verisi.

    Raises:
        ValueError: Hatalı HTTP durum kodunda tetiklenir.
    """
    base_url = "https://www.mgm.gov.tr/"
    url = f"{base_url}{endpoint}"

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        soup = BeautifulSoup(response.text, "html.parser")
        logger.info("Web sayfası alındı: %s", response.url)
        return soup
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", http_err)
        raise ValueError(f"HTTP error occurred: {http_err}") from http_err
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error occurred: %s", req_err)
        raise ValueError(f"Request error occurred: {req_err}") from req_err
