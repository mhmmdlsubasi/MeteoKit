# DailyMetInfo.py

from . import MGMService
from . import tools

from datetime import datetime, timedelta


class get:
    def __init__(self, day=None, month=None, year=None):
        if day and month and year:
            self.date = datetime(year, month, day)
        else:
            self.date = None

    def _get_weather_data(
        self, endpoint, update_hour, update_minute, sort_order="descending"
    ):
        now = datetime.now()

        self._control_date(now, update_hour, update_minute)

        params = {"tarih": datetime.strftime(self.date, "%Y-%m-%d")}
        try:
            data = MGMService.get_data(endpoint, params)
            return tools.sorter(data, sort_order, "deger")
        except Exception as e:
            raise ValueError("Veri alınırken bir hata oluştu: {}".format(e))

    def _control_date(self, now, update_hour, update_minute):
        if self.date:
            now = datetime.now()
            if self.date > now:
                raise ValueError("Belirtilen tarih gelecekte bir tarihtir.")
            elif now - self.date > timedelta(days=8):
                raise ValueError("Geçerli tarih aralığı son 1 hafta ile sınırlıdır.")

        if self.date is None:
            if self._is_before(now, update_hour, update_minute):
                self.date = now - timedelta(days=1)
            else:
                self.date = now
        elif self.date.date() == now.date() and self._is_before(
            now, update_hour, update_minute
        ):
            raise ValueError("Belirtilen tarihe ait veri henüz yayınlanmadı.")

    def _is_before(self, now, hour, minute):
        return now.hour < hour or (now.hour == hour and now.minute < minute)

    def highest_temp(self, sort_order="descending"):
        return self._get_weather_data("sondurumlar/enyuksek", 21, 37, sort_order)

    def lowest_temp(self, sort_order="ascending"):
        return self._get_weather_data("sondurumlar/endusuk", 9, 37, sort_order)

    def lowest_soil_temp(self, sort_order="ascending"):
        return self._get_weather_data("sondurumlar/toprakustu", 10, 0, sort_order)

    def total_precipitation(self, sort_order="descending"):
        return self._get_weather_data("sondurumlar/toplamyagis", 9, 37, sort_order)

    def extreme_values(self, merkezid: int):
        month = self.date.month
        day = self.date.day
        endpoint = "ucdegerler"
        params = {"merkezid": merkezid, "ay": month, "gun": day}
        return MGMService.get_data(endpoint, params)[0]
