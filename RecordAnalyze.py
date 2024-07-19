import csv
from datetime import datetime

from modules import DailyMetInfo, MonthlyMetInfo, StationInfo
from modules.submodules.log import logger


class get:
    def __init__(self, day, month, year):
        self.daily_weather = DailyMetInfo.get(day, month, year)

    def _get_province_center_codes(self):
        all_centers = StationInfo.all_province_centers()
        return tuple(
            (
                17351
                if center["sondurumIstNo"]
                == 19272  # Merkez istasyon olarak tanımlanan Adana Seyhan istasyonu, Adana Bölge istasyonu olarak değiştirildi.
                else (
                    17064
                    if center["sondurumIstNo"]
                    == 17060  # Merkez istasyon olarak tanımlanan İstanbul Atatürk Havalimanı istasyonu, İstanbul Bölge istasyonu olarak değiştirildi.
                    else center["sondurumIstNo"]
                )
            )
            for center in all_centers
        )

    def _check_temp_type(self, temp_type):
        if temp_type not in {"En Düşük Sıcaklık (°C)", "En Yüksek Sıcaklık (°C)"}:
            raise ValueError(
                "Geçersiz sıcaklık türü. Sadece 'En Düşük Sıcaklık (°C)' veya 'En Yüksek Sıcaklık (°C)' olabilir."
            )
        return (
            "lowest_temp" if temp_type == "En Düşük Sıcaklık (°C)" else "highest_temp"
        )

    def _generate_date_header(self):
        date_str = datetime.strftime(self.daily_weather.date, "%d.%m.%Y")
        return f"*{date_str}*"

    def _generate_separator(self):
        return "-" * 23


class Monthly(get):
    def __init__(self, day, month, year):
        super().__init__(day, month, year)
        self.istno_tuple = self._get_province_center_codes()

    def minTemp(self):
        return self._temp_control("En Düşük Sıcaklık (°C)")

    def minTemp_to_csv(self):
        """Aylık minimum sıcaklık verilerini CSV dosyasına kaydeder."""
        data = self.minTemp()
        filename = self._generate_filename("minTemp")
        self.save_to_csv(data, filename)

    def maxTemp(self):
        return self._temp_control("En Yüksek Sıcaklık (°C)")

    def maxTemp_to_csv(self):
        """Aylık maksimum sıcaklık verilerini CSV dosyasına kaydeder."""
        data = self.maxTemp()
        filename = self._generate_filename("maxTemp")
        self.save_to_csv(data, filename)

    def _get_record_temp(self, province, temp_type, month_str):
        try:
            monthly_data = MonthlyMetInfo.get(province).general()
            record_temp = monthly_data[temp_type][month_str]
            return record_temp[0], record_temp[1]
        except Exception as e:
            logger.error(
                "Error getting monthly record temperature for %s: %s", province, e
            )
            return None, None

    def _temp_control(self, temp_type):
        temp_method = self._check_temp_type(temp_type)
        temp_data = getattr(self.daily_weather, temp_method)()
        month_str = datetime.strftime(self.daily_weather.date, "%B")

        center_temp_data = tuple(
            filter(lambda x: x["istNo"] in self.istno_tuple, temp_data)
        )

        result = {
            "date": self._generate_date_header(),
            "title": f"{month_str} Ayı {temp_type} Rekorunu Kıran İller",
            "list": [],
        }

        for station in center_temp_data:
            province = station["il"]
            value = station["deger"]
            district = station["ilce"]
            istNo = station["istNo"]
            lat = station["enlem"]
            lon = station["boylam"]
            try:
                record_temp_value, record_temp_date = self._get_record_temp(
                    province, temp_type, month_str
                )
                if record_temp_value is None:
                    continue
                if (
                    temp_type == "En Yüksek Sıcaklık (°C)"
                    and value >= record_temp_value
                ) or (
                    temp_type == "En Düşük Sıcaklık (°C)" and value <= record_temp_value
                ):
                    result["list"].append(
                        {
                            "province": province.upper(),
                            "district": district.upper(),
                            "istNo": istNo,
                            "lat": lat,
                            "lon": lon,
                            "current_temp": value,
                            "record_temp": record_temp_value,
                            "difference": round(value - record_temp_value, 2),
                            "record_date": record_temp_date,
                        }
                    )
            except Exception as e:
                logger.error(
                    "Error processing temperature record for %s: %s", province, e
                )

        return result

    def save_to_csv(self, data, filename):
        """Monthly verilerini CSV dosyasına kaydeder."""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Başlık satırı
            writer.writerow(
                [
                    "Province",
                    "District",
                    "Station No",
                    "Latitude",
                    "Longitude",
                    "Current Temperature",
                    "Record Temperature",
                    "Difference",
                    "Record Date",
                ]
            )

            # Verileri yaz
            for item in data["list"]:
                writer.writerow(
                    [
                        item["province"],
                        item["district"],
                        item["istNo"],
                        item["lat"],
                        item["lon"],
                        item["current_temp"],
                        item["record_temp"],
                        item["difference"],
                        item["record_date"],
                    ]
                )

    def _generate_filename(self, temp_type):
        """CSV dosyasının adını oluşturur."""
        date_str = datetime.strftime(self.daily_weather.date, "%Y-%m-%d")
        temp_type_str = "minTemp" if temp_type == "minTemp" else "maxTemp"
        return f"{date_str}_monthly_{temp_type_str}_record.csv"


class Daily(get):
    def __init__(self, day, month, year):
        super().__init__(day, month, year)

    def minTemp(self):
        return self._temp_control("En Düşük Sıcaklık (°C)")

    def maxTemp(self):
        return self._temp_control("En Yüksek Sıcaklık (°C)")

    def minTemp_to_csv(self):
        """Günlük minimum sıcaklık verilerini CSV dosyasına kaydeder."""
        data = self.minTemp()
        filename = self._generate_filename("minTemp")
        self.save_to_csv(data, filename)

    def maxTemp_to_csv(self):
        """Günlük maksimum sıcaklık verilerini CSV dosyasına kaydeder."""
        data = self.maxTemp()
        filename = self._generate_filename("maxTemp")
        self.save_to_csv(data, filename)

    def _temp_control(self, temp_type):
        temp_method = self._check_temp_type(temp_type)
        temp_data = getattr(self.daily_weather, temp_method)()
        result = {
            "date": self._generate_date_header(),
            "separator": self._generate_separator(),
            "list": [],
        }

        for station in temp_data:
            if (station["il"] == "Malatya") and (station["ilce"] == "Pötürge"):
                station["ilce"] = "Pütürge"
            if (station["il"] == "Malatya") and (station["ilce"] == "Arapkir"):
                station["ilce"] = "Arapgir"
            if (station["il"] == "Zonguldak") and (
                station["ilce"] == "Karadeniz Ereğli"
            ):
                station["ilce"] = "Ereğli"
            try:
                c = StationInfo.get(station["il"], station["ilce"])
            except KeyError as e:
                logger.error("StationInfo.get failed for %s: %s", station["il"], e)
                continue
            if c["sondurumIstNo"] == station["istNo"]:
                try:
                    extreme = self.daily_weather.extreme_values(c["merkezId"])
                except ValueError as e:
                    logger.error(
                        "Failed to get extreme values for %s: %s", station["il"], e
                    )
                    continue
                if (
                    temp_type == "En Yüksek Sıcaklık (°C)"
                    and station["deger"] >= extreme["max"]
                ) or (
                    temp_type == "En Düşük Sıcaklık (°C)"
                    and station["deger"] <= extreme["min"]
                ):
                    result["list"].append(
                        {
                            "province": station["il"],
                            "district": station["ilce"],
                            "station_name": station["istAd"],
                            "measured_temp": station["deger"],
                            "extreme_temp": (
                                extreme["max"]
                                if temp_type == "En Yüksek Sıcaklık (°C)"
                                else extreme["min"]
                            ),
                        }
                    )
        return result

    def save_to_csv(self, data, filename):
        """Günlük verileri CSV dosyasına kaydeder."""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Başlık satırı
            writer.writerow(
                [
                    "Province",
                    "District",
                    "Station Name",
                    "Measured Temperature",
                    "Extreme Temperature",
                ]
            )

            # Verileri yaz
            for item in data["list"]:
                writer.writerow(
                    [
                        item["province"],
                        item["district"],
                        item["station_name"],
                        item["measured_temp"],
                        item["extreme_temp"],
                    ]
                )

    def _generate_filename(self, temp_type):
        """CSV dosyasının adını oluşturur."""
        date_str = datetime.strftime(self.daily_weather.date, "%Y-%m-%d")
        temp_type_str = "minTemp" if temp_type == "minTemp" else "maxTemp"
        return f"{date_str}_daily_{temp_type_str}.csv"
