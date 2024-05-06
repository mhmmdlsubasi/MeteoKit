import requests
from bs4 import BeautifulSoup
from datetime import datetime

link = "http://weather.uwyo.edu/cgi-bin/sounding"

def get_sounding(day,month,year,hour,istNo,region='europe',file_type='TEXT:LIST'):
    time = datetime(year,month,day,hour)
    if hour != 0 or hour != 12:
        raise ValueError('Geçersiz saat değeri.')
    day = str(time.day).zfill(2)
    hour = str(time.hour).zfill(2)
    params = {
        "region" : region,
        "TYPE" : file_type,
        "YEAR" : year,
        "MONTH" : month,
        "FROM" : day+hour,
        "TO" : day+hour,
        "STNM" : istNo
        }
    response = requests.get(link, params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    data = soup.find('pre').text
 
    parametres = soup.find('h3').find_next_sibling('pre').text
    lines = parametres.splitlines()
    del lines[0]
    result = {}
    for line in lines:
        key, value = map(str.strip, line.split(':'))
        result[key] = value
    return data,result

