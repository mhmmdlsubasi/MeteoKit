# StationInfo.py

from . import MGMService

def get(province,district):
    endpoint = 'merkezler?'
    params = {
        'il' : province,
        'ilce' : district
        }
    return MGMService.get_data(endpoint,params)[0] 

def all_province_centers():
    endpoint = 'merkezler/iller'
    return tuple(MGMService.get_data(endpoint))

def all_province_stations(province):
    endpoint = 'istasyonlar/ilAdDetay'
    params = {'il': province.title()}
    return tuple(MGMService.get_data(endpoint,params))

def ski_centers():
    endpoint = 'istasyonlar/kayakMerkezleri'
    return MGMService.get_data(endpoint)


