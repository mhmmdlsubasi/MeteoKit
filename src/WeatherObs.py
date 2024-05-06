# WeatherObs.py

from . import MGMService
from . import tools

def weather_by_istno(ist_no):
    endpoint = 'sondurumlar'
    params = {'istno': ist_no}
    return MGMService.get_data(endpoint, params)

def weather_by_merkezid(merkezid):
    endpoint = 'sondurumlar'
    params = {'merkezid': merkezid}
    return MGMService.get_data(endpoint, params)

def weather_by_plaka(plaka):
    endpoint = 'sondurumlar/ilTumSondurum'
    params = {'ilPlaka': plaka}
    return MGMService.get_data(endpoint,params)

def all_province_centers():
    endpoint = 'sondurumlar/ilmerkezleri'
    return MGMService.get_data(endpoint)

def all_province_stations(province):
    endpoint = 'merkezler/ililcesi'
    params = {'il': province.title()}
    return MGMService.get_data(endpoint, params)

def snow_heights(sort_order='descending'):
    endpoint = 'sondurumlar/kar'
    data = MGMService.get_data(endpoint)
    return tools.sorter(data,sort_order,'karYukseklik')

# from . import StationInfo

# def all_stations():
#     all_stations = StationInfo.all_stations()
#     for province,district in all_stations.items():
#         for district,value in district.items():
#             all_province_stations()
#             all_stations[province][district] = 


    # province_district_stations = {}
    # for station in all_province_centers():
    #     province_name = station['il']
    #     province_stations = all_province_stations(province_name)
    #     province_district_stations[province_name] = {}
    #     for district_station in province_stations:
    #         district_name = district_station['ilce']
    #         province_district_stations[province_name][district_name] = district_station

    # return province_district_stations
