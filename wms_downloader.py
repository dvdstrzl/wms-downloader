from owslib.wms import WebMapService

from functions import download_and_merge, download_folder

# Verbindung zum WMS-Dienst herstellen
wms_url = 'https://atlas.thuenen.de/geoserver/ows'
wms = WebMapService(wms_url, version='1.3.0')

# Parameter für den gewünschten Layer festlegen
layer_name = 'geonode:levl_1999_lau2'
crs = 'EPSG:31467'
bbox = (3277167.5, 5233180.5, 3924737.5, 6107773.5)  # Bounding Box: miny, minx, maxy, maxx
tile_size = 1000 # Größe der einzelnen Tiles
resolution_factor = 100  # Anteilige Auflösung

# Aufruf der Funktion zum Herunterladen und Zusammenführen der Teile
download_and_merge(wms, layer_name, crs, bbox, tile_size, resolution_factor, f'{download_folder}/{layer_name}_{crs}_r{resolution_factor}.tif' )
