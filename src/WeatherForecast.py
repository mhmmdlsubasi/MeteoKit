from . import MGMService

def hourly(saatlikTahminIstNo):
    endpoint = 'tahminler/saatlik'
    params = {'istno': saatlikTahminIstNo}
    return MGMService.get_data(endpoint,params)

def daily(gunlukTahminIstNo):
    endpoint = 'tahminler/gunluk'
    params = {'istno': gunlukTahminIstNo}
    return MGMService.get_data(endpoint,params)[0]
