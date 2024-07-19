"""
MGM (Meteoroloji Genel Müdürlüğü) istasyon bilgilerini almak için modül.

Fonksiyonlar:
    - get(province: str, district: str) -> dict:
        Belirtilen il ve ilçeye ait merkez bilgilerini alır.

    - all_province_centers() -> list:
        Tüm illere ait merkez bilgilerini alır.

    - all_province_stations(province: str) -> list:
        Belirtilen ildeki tüm istasyon bilgilerini alır.

    - ski_centers() -> list:
        Tüm kayak merkezlerini alır.
"""

from modules.submodules import MGMService
from modules.submodules.log import logger


def get(province: str, district: str) -> dict:
    """
    Belirtilen il ve ilçeye ait merkez bilgilerini alır.

    Args:
        province (str): İlin adı.
        district (str): İlçenin adı.

    Returns:
        dict: İlin ve ilçenin merkez bilgileri.

    Raises:
        ValueError: İstek başarısız olduğunda tetiklenir.
    """
    endpoint = "merkezler?"
    params = {"il": province, "ilce": district}
    logger.info("İl ve ilçe merkez bilgileri alınıyor: %s, %s", province, district)
    try:
        data = MGMService.get_data(endpoint, params)
        return data[0] if data else None
    except ValueError as e:
        logger.error("Merkez bilgileri alınırken hata oluştu: %s", e)
        raise


def all_province_centers() -> list:
    """
    Tüm illere ait merkez bilgilerini alır.

    Returns:
        list: Tüm illerin merkez bilgileri.

    Raises:
        ValueError: İstek başarısız olduğunda tetiklenir.
    """
    endpoint = "merkezler/iller"
    logger.info("Tüm illere ait merkez bilgileri alınıyor")
    try:
        return MGMService.get_data(endpoint)
    except ValueError as e:
        logger.error("Tüm illerin merkez bilgileri alınırken hata oluştu: %s", e)
        raise


def all_province_stations(province: str) -> list:
    """
    Belirtilen ildeki tüm istasyon bilgilerini alır.

    Args:
        province (str): İlin adı.

    Returns:
        list: İldeki tüm istasyon bilgileri.

    Raises:
        ValueError: İstek başarısız olduğunda tetiklenir.
    """
    endpoint = "istasyonlar/ilAdDetay"
    params = {"il": province.title()}
    logger.info("İldeki tüm istasyon bilgileri alınıyor: %s", province)
    try:
        return MGMService.get_data(endpoint, params)
    except ValueError as e:
        logger.error("İldeki tüm istasyon bilgileri alınırken hata oluştu: %s", e)
        raise


def ski_centers() -> list:
    """
    Tüm kayak merkezlerini alır.

    Returns:
        list: Tüm kayak merkezlerinin bilgileri.

    Raises:
        ValueError: İstek başarısız olduğunda tetiklenir.
    """
    endpoint = "istasyonlar/kayakMerkezleri"
    logger.info("Tüm kayak merkezleri alınıyor")
    try:
        return MGMService.get_data(endpoint)
    except ValueError as e:
        logger.error("Kayak merkezleri bilgileri alınırken hata oluştu: %s", e)
        raise
