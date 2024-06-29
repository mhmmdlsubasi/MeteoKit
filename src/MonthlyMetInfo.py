# MonthlyMetInfo.py

from .MGMService import get_request
from . import tools

from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")

endpoint = "veridegerlendirme/il-ve-ilceler-istatistik.aspx?"
all_months = [
    datetime.strptime(str(i), "%m").strftime("%B").capitalize() for i in range(1, 13)
]


class get:
    def __init__(self, province):
        province = province.strip().capitalize()
        if province == "Mersin":
            province = "İçel"  # Mersin ili, veri temin edilen adreste İçel olarak adlandırıldığı için if bloğu eklendi.
        self.province = tools.tr_to_eng(province)

    def general(self):
        params = {"k": "A", "m": self.province.upper()}
        response = get_request(endpoint, params)
        return self._parse_response(response)

    def seasonal_norms(self):
        params = {"k": "H", "m": self.province.upper()}
        response = get_request(endpoint, params)
        return self._parse_response(response)

    def _parse_response(self, response):
        try:
            rows = response.find_all("tbody")[0].find_all("tr")
            columns = response.find_all("thead")[0].find_all("th")
        except:
            raise AttributeError("Tablo bulunamadı.")

        columns = [th.text.strip() for th in columns]

        if len(columns) != 14:
            raise ValueError("Tablodaki sütun sayısı doğru değil.")

        if columns[-1] != "Yıllık":
            raise ValueError("Tablodaki son sütunun başlığı 'Yıllık' değil.")
        del columns[-1]

        if columns[0] != self.province.upper():
            raise ValueError("Tablodaki il bilgisi hatalı.")
        del columns[0]

        if columns != all_months:
            raise ValueError("Tablodaki sütun başlıkları uyumsuz.")

        df = {}
        for row in rows:
            keys = row.find_all("th")
            cells = row.find_all("td")
            if keys == []:
                continue
            key = (
                keys[0]
                .text.strip()
                .replace("\n", "")
                .replace("\r", "")
                .replace("                 ", "")
            )
            if len(cells) == 1:
                df["info"] = row.text.strip()
            if len(cells) == len(columns) + 1:
                del cells[-1]
                values_tuple = tuple(
                    map(
                        lambda x: (
                            "empty"
                            if not x.text.strip()  # Hücrede veri olmadığı durumda 'empty' döndür.
                            else float(x.text.replace(",", "."))
                        ),  # Hücredeki değeri ondalık sayıya dönüştür.
                        cells,
                    )
                )
                try:
                    title_tuple = tuple(map(lambda x: x["title"], cells))
                    values = tuple(zip(values_tuple, title_tuple))
                except:
                    values = values_tuple
                df[key] = dict(zip(columns, values))
        return df
