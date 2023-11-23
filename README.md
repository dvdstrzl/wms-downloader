## WMS Downloader

Ermöglicht das Herunterladen von geografischen Rasterdaten von einem Web Map Service (WMS).
Der gewünschte Layer wird beim Herunterladen zunächst auf seperate Tiles/Kacheln aufgeteilt, anschließend zusammengeführt und als einzelnes GeoTIFF-Format gespeichert. 

Die Anzahl der erforderlichen Kacheln wird dabei automatisch berechnet – basierend auf den angegebenen Parametern wie Auflösung, Kachelgröße und dem gewünschten geografischen Bereich.

Das [WMS des Thünen Instituts](https://atlas.thuenen.de/geoserver/ows?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0) dient als Beispiel.
Teste z.b. mit folgenden Layern: 
> "geonode:levl_1999_lau2" mit BoundingBox für CRS="EPSG:31467" --> minx="5233180.5" miny="3277167.5" maxx="6107773.5" maxy="3924737.5"
> 
> "geonode:ctm_ger_2021_seg_v201" mit BoundingBox für CRS="EPSG:3035" --> minx="2682993.25" miny="4030317.75" maxx="3540651.75" maxy="4675025.0"
> 
> "geonode:CTM_GER_2021_rst_v201" mit BoundingBox für CRS="EPSG:3035" --> minx="2654919.6079648044" miny="4016026.3630416505" maxx="3554919.6079648044" maxy="4676026.3630416505"
> 
> siehe: https://atlas.thuenen.de/geoserver/ows?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0

### Voraussetzungen

- Python 3.x
- Erforderliche Python-Bibliotheken (`owslib`, `tqdm`, `rasterio`)

### Anwendung

1. Installiere ggf. die erforderlichen Python-Bibliotheken:

```bash
pip install -r requirements.txt
```

2. Passe das Skript `wms_downloader.py` an, um den Layer, CRS und die Tiling-Parameter anzugeben:

   - `wms_url` 
   -  `layer_name`, `crs`, `bbox`, `tile_size` und `resolution_factor`
   
3. Führe das Skript `wms_downloader.py` aus:

```bash
python wms_downloader.py
```

Das Skript stellt eine Verbindung zum spezifizierten WMS-Dienst her, lädt die Kacheln herunter, führt sie zusammen und speichert die resultierende GeoTIFF-Datei im Ordner `downloads`.

### Dateien

- `wms_downloader.py`: Enthält das Hauptskript für die Verbindung zum WMS-Dienst und den Download/Vereinigung von Daten.
- `functions.py`: Enthält die Funktionen, die von `wms_downloader.py` verwendet werden.

### Referenzen

- [OWSLib](https://geopython.github.io/OWSLib/)
- [TQDM](https://github.com/tqdm/tqdm)
- [Rasterio](https://rasterio.readthedocs.io/en/latest/)