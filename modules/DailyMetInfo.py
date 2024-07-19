from modules.submodules import MGMService
from modules import tools
from datetime import datetime, timedelta
from modules.submodules.log import logger


class get:
    def __init__(self, day=None, month=None, year=None):
        if day and month and year:
            self.date = datetime(year, month, day)
            logger.info(f"Tarih set edildi: {self.date}")
        else:
            self.date = None
            logger.info("Tarih set edilmedi")

    def _get_weather_data(
        self, endpoint, update_hour, update_minute, sort_order="descending"
    ):
        now = datetime.now()
        self._control_date(now, update_hour, update_minute)
        params = {"tarih": datetime.strftime(self.date, "%Y-%m-%d")}
        try:
            data = MGMService.get_data(endpoint, params)
            logger.info(f"Veri başarıyla alındı: {endpoint}, Tarih: {self.date}")
            return tools.sorter(data, sort_order, "deger")
        except Exception as e:
            logger.error(f"Veri alınırken bir hata oluştu: {e}")
            raise ValueError(f"Veri alınırken bir hata oluştu: {e}")

    def _control_date(self, now, update_hour, update_minute):
        if self.date:
            if self.date > now:
                logger.error("Belirtilen tarih gelecekte bir tarihtir.")
                raise ValueError("Belirtilen tarih gelecekte bir tarihtir.")
            elif now - self.date > timedelta(days=8):
                logger.error("Geçerli tarih aralığı son 1 hafta ile sınırlıdır.")
                raise ValueError("Geçerli tarih aralığı son 1 hafta ile sınırlıdır.")
        if self.date is None:
            if self._is_before(now, update_hour, update_minute):
                self.date = now - timedelta(days=1)
            else:
                self.date = now
            logger.info(f"Tarih otomatik olarak set edildi: {self.date}")
        elif self.date.date() == now.date() and self._is_before(
            now, update_hour, update_minute
        ):
            logger.error("Belirtilen tarihe ait veri henüz yayınlanmadı.")
            raise ValueError("Belirtilen tarihe ait veri henüz yayınlanmadı.")

    def _is_before(self, now, hour, minute):
        return now.hour < hour or (now.hour == hour and now.minute < minute)

    def highest_temp(self, sort_order="descending"):
        logger.info("En yüksek sıcaklık verisi çekiliyor")
        return self._get_weather_data("sondurumlar/enyuksek", 21, 37, sort_order)

    def lowest_temp(self, sort_order="ascending"):
        logger.info("En düşük sıcaklık verisi çekiliyor")
        return self._get_weather_data("sondurumlar/endusuk", 9, 37, sort_order)

    def lowest_soil_temp(self, sort_order="ascending"):
        logger.info("En düşük toprak sıcaklığı verisi çekiliyor")
        return self._get_weather_data("sondurumlar/toprakustu", 10, 0, sort_order)

    def total_precipitation(self, sort_order="descending"):
        logger.info("Toplam yağış verisi çekiliyor")
        return self._get_weather_data("sondurumlar/toplamyagis", 9, 37, sort_order)

    def extreme_values(self, merkezid: int):
        logger.info(f"Aşırı değerler verisi çekiliyor, Merkez ID: {merkezid}")
        month = self.date.month
        day = self.date.day
        endpoint = "ucdegerler"
        params = {"merkezid": merkezid, "ay": month, "gun": day}
        try:
            data = MGMService.get_data(endpoint, params)
            if not data or len(data) == 0:
                logger.error("Aşırı değerler verisi boş döndü.")
                raise ValueError("Aşırı değerler verisi boş döndü.")
            logger.info("Aşırı değerler verisi başarıyla alındı")
            return data[0]
        except Exception as e:
            logger.error(f"Aşırı değerler verisi alınırken bir hata oluştu: {e}")
            raise ValueError(f"Aşırı değerler verisi alınırken bir hata oluştu: {e}")
