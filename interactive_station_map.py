import folium
from folium.plugins import MarkerCluster, Fullscreen, MeasureControl
from src import StationInfo

opentopomap_url = "https://tile.opentopomap.org/{z}/{x}/{y}.png"
opentopomap_attr = "OpenTopoMap (https://opentopomap.org/)"

m = folium.Map(
    location=[38.9637, 35.2433],
    zoom_start=6,
    control_scale=True,
    attribution=opentopomap_attr,
)

folium.TileLayer(opentopomap_url, attr=opentopomap_attr).add_to(m)

# Haritayı tam ekran moduna geçir
Fullscreen(
    position="topright", title="Tam Ekran", title_cancel="Tam Ekrandan Çık"
).add_to(m)
# Kilometre işaretlerini ekleyerek haritayı ölçeklendir
MeasureControl(primary_length_unit="kilometers").add_to(m)


all_centers = StationInfo.all_province_centers()

for center in all_centers:
    province = center["il"]
    stations = StationInfo.all_province_stations(province)
    marker_cluster = MarkerCluster().add_to(m)
    for station in stations:
        istAd = station["istAd"]
        lat = station["enlem"]
        lon = station["boylam"]
        yukseklik = station["yukseklik"]
        istNo = station["istNo"]

        popup = f"{istAd}\n\nRakım: {yukseklik}m"
        folium.Marker(location=(lat, lon), popup=popup).add_to(marker_cluster)
m.save("test.html")
