import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
from scipy.interpolate import griddata

from src import StationInfo, WeatherObs

from lib import GeoDataHandler
from lib import colors

lats = []
lons = []
temps = []

# İstasyon merkezlerini al
centers = StationInfo.all_province_centers()
for center in centers:
    province, district = center['il'],center['ilce']
    stations = StationInfo.all_province_stations(province)
    for station in stations:
        istNo = station['istNo']
        lat = station['enlem']
        lon = station['boylam']
        try:
            temp = WeatherObs.weather_by_istno(istNo)[0]['sicaklik']
            if temp >-60:
                lats.append(lat)
                lons.append(lon)
                temps.append(temp)
        except:
            continue


# Grid oluşturma
grid_lats = np.linspace(min(lats), max(lats), 100)
grid_lons = np.linspace(min(lons), max(lons), 100)
grid_lats, grid_lons = np.meshgrid(grid_lats, grid_lons)

# Interpolasyon işlemi
grid_temps = griddata((lons, lats), temps, (grid_lons, grid_lats), method='linear')

# Figure oluştur
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

asd = GeoDataHandler.create_multipolygon(GeoDataHandler.get_leaf_values(GeoDataHandler.get_province_polygons('Turkey')))
feature = ShapelyFeature(asd, ccrs.PlateCarree(),facecolor='None', edgecolor="black", lw=1)
ax.add_feature(feature)

# Sıcaklık dağılımını contourf ile çiz
cmap = colors.get_cmap('temp.rgb')
contour = ax.contourf(grid_lons, grid_lats, grid_temps, cmap=cmap,levels=np.arange(-40,41,1))
plt.colorbar(contour, ax=ax, label='Sıcaklık',ticks=np.arange(-40,41,5))  # Renk skalası ekle
ax.set_xlabel('Boylam')
ax.set_ylabel('Enlem')
ax.set_title('Sıcaklık Dağılımı')

# Kıyı çizgilerini ekle
ax.coastlines()

fig.savefig('test.png',dpi=400)
