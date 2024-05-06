from src import StationInfo
from src import DailyMetInfo
from src import MonthlyMetInfo
from datetime import datetime

class get():
    def __init__(self,day,month,year):
        self.daily_weather = DailyMetInfo.get(day,month,year)
    
    def _get_province_center_codes(self):
        all_centers = StationInfo.all_province_centers()
        return tuple(
            17351 if center['sondurumIstNo'] == 19272 else # Merkez istasyon olarak tanımlanan Adana Seyhan istasyonu, Adana Bölge istasyonu olarak değiştirildi.
            17064 if center['sondurumIstNo'] == 17060 else # Merkez istasyon olarak tanımlanan İstanbul Atatürk Havalimanı istasyonu, İstanbul Bölge istasyonu olarak değiştirildi.
            center['sondurumIstNo']
            for center in all_centers
        )
    
    def _check_temp_type(self, temp_type):
        if temp_type not in {'En Düşük Sıcaklık (°C)', 'En Yüksek Sıcaklık (°C)'}:
            raise ValueError("Geçersiz sıcaklık türü. Sadece 'En Düşük Sıcaklık (°C)' veya 'En Yüksek Sıcaklık (°C)' olabilir.")
        return 'lowest_temp' if temp_type == 'En Düşük Sıcaklık (°C)' else 'highest_temp'

    def _print_date_header(self):
        date_str = datetime.strftime(self.daily_weather.date, '%d.%m.%Y')
        print(f'*{date_str}*')

    def _print_separator(self):
        print('-' * 23)
       
class Monthly(get):
    def __init__(self, day, month, year):
        super().__init__(day, month, year)
        self.istno_tuple = self._get_province_center_codes()

    def minTemp(self):
        return self._temp_control('En Düşük Sıcaklık (°C)')         
    def maxTemp(self):
        return self._temp_control('En Yüksek Sıcaklık (°C)')        
 
    def _get_record_temp(self, province, temp_type, month_str):
        try:
            monthly_data = MonthlyMetInfo.get(province).general()
            record_temp = monthly_data[temp_type][month_str]
            return record_temp[0], record_temp[1]
        except Exception as e:
            print(f'Error getting monthly record temperature for {province}: {e}')
            return None, None
    def _temp_control(self,temp_type):
        temp_method = self._check_temp_type(temp_type)
        temp_data = getattr(self.daily_weather, temp_method)()
        month_str = datetime.strftime(self.daily_weather.date,'%B')  
              
        center_temp_data = tuple(filter(lambda x: x['istNo'] in self.istno_tuple,temp_data))
            
        self._print_date_header()
        print(f'_*{month_str} Ayı {temp_type} Rekorunu Kıran İller*_')
        print('_*Tam Liste*_\n')
        
        for station in center_temp_data:
            province = station['il']
            value = station['deger'] 
            try:
                record_temp_value, record_temp_date = self._get_record_temp(province, temp_type, month_str)
                if record_temp_value is None:
                    continue
                if (temp_type == 'En Yüksek Sıcaklık (°C)' and value >= record_temp_value) or \
                   (temp_type == 'En Düşük Sıcaklık (°C)' and value <= record_temp_value):
                    print(f"*{province.upper()}* => {value} - {record_temp_value} = {round(value - record_temp_value, 2)} => {record_temp_date}")
            except Exception as e:
                print(f'Error processing temperature record for {province}: {e}')


class Daily(get):
    def __init__(self, day, month, year):
        super().__init__(day, month, year)
    
    def minTemp(self):
        return self._temp_control('En Düşük Sıcaklık (°C)')
    def maxTemp(self):
        return self._temp_control('En Yüksek Sıcaklık (°C)')
    
    def _temp_control(self,temp_type):
        temp_method = self._check_temp_type(temp_type)
        temp_data = getattr(self.daily_weather, temp_method)()
        self._print_date_header()
        self._print_separator()

        for station in temp_data:
            if (station['il'] == 'Malatya') and (station['ilce'] == 'Pötürge'):
                station['ilce'] = 'Pütürge'
            if (station['il'] == 'Malatya') and (station['ilce'] == 'Arapkir'):
                station['ilce'] = 'Arapgir'
            if (station['il'] == 'Zonguldak') and (station['ilce'] == 'Karadeniz Ereğli'):
                station['ilce'] = 'Ereğli'
            try:
                c = StationInfo.get(station['il'],station['ilce'])
            except:
                continue
            if c['sondurumIstNo'] == station['istNo']:
                try:
                    extreme = self.daily_weather.extreme_values(c['merkezId'])
                except:
                    continue                    
                if (temp_type == 'En Yüksek Sıcaklık (°C)' and station['deger'] >= extreme['max']) or \
                   (temp_type == 'En Düşük Sıcaklık (°C)' and station['deger'] <= extreme['min']):
                    print(f"{station['il']} {station['ilce']} - {station['istAd']}")
                    print(f"Ölçülen Sıcaklık: {station['deger']}")
                    if temp_type == 'En Yüksek Sıcaklık (°C)':
                        print(f"Uç Sıcaklık: {extreme['max']}")
                    else:
                        print(f"Uç Sıcaklık: {extreme['min']}")
                    self._print_separator()
        