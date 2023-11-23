import os
from tqdm import tqdm
import rasterio
from rasterio.merge import merge

# Pfad zum Download-Ordner
download_folder = "downloads"

# Überprüfen, ob der Ordner existiert, andernfalls erstellen
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Der Ordner '{download_folder}' wurde erstellt.")
else:
    print(f"Der Ordner '{download_folder}' existiert bereits.")


# Funktion zum Herunterladen und Zusammenführen von Teilen
def download_and_merge(
    wms,
    layer_name,
    crs,
    full_bbox,
    tile_size,
    resolution_factor,
    output_file,
):
    minx, miny, maxx, maxy = full_bbox

    # Berechnung der Anzahl der Tiles basierend auf der Auflösung und der gewünschten Tile-Größe ("+1" als Puffer)
    num_tiles_x = int((maxx - minx) / (resolution_factor * tile_size)) + 1
    num_tiles_y = int((maxy - miny) / (resolution_factor * tile_size)) + 1

    # Gesamtzahl der Tiles berechnen
    total_tiles = num_tiles_x * num_tiles_y

    # Fortschrittsbalken erstellen
    progress = tqdm(total=total_tiles, desc="Downloading Tiles", unit=" Tile")

    # Liste für heruntergeladene Teile
    downloaded_parts = []

    # Schleifen für die Aufteilung in Teile
    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            # Berechnung der Bounding Box für jedes Tile
            tile_bbox = (
                minx + i * resolution_factor * tile_size,  # minx
                miny + j * resolution_factor * tile_size,  # miny
                minx + (i + 1) * resolution_factor * tile_size,  # maxx
                miny + (j + 1) * resolution_factor * tile_size,  # maxy
            )

            # Karte herunterladen (Geotiff)
            geotiff = wms.getmap(
                layers=[layer_name],
                srs=crs,
                bbox=tile_bbox,
                size=(tile_size, tile_size),
                format="image/geotiff",
                transparent=True,
            )

            # Dateinamen für den heruntergeladenen Teil
            part_file = f"downloads/{layer_name}_part_{i}_{j}.tif"

            # Teil speichern
            with open(part_file, "wb") as part_out:
                part_out.write(geotiff.read())

            # Zur Liste der heruntergeladenen Teile hinzufügen
            downloaded_parts.append(part_file)

            # Fortschritt aktualisieren
            progress.update(1)

    # Funktion: Alle heruntergeladenen Teile zusammenführen
    def merge_parts(parts):
        src_files_to_mosaic = [rasterio.open(part) for part in parts]
        mosaic, out_trans = merge(src_files_to_mosaic)

        out_meta = src_files_to_mosaic[0].meta.copy()
        out_meta.update(
            {
                "driver": "GTiff",
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": out_trans,
                "nodata": 0,
            }
        )  # Falls "Leerraum" im Merge entsteht, setze als "nodata"

        with rasterio.open(output_file, "w", **out_meta) as dest:
            dest.write(mosaic)

    # Aufruf der Funktion zum Zusammenführen der Teile
    merge_parts(downloaded_parts)

    # Funktion: Bounding Box Zuschnitt (entsprechend urspr. Bereich)
    def clip_to_bbox(input_file, output_file, bbox):
        with rasterio.open(input_file) as src:
            # Berechnung der Fenstergröße für den Zuschnitt
            window = src.window(*bbox)

            # Ausschneiden und in neue Datei speichern
            clipped = src.read(window=window)
            out_meta = src.meta.copy()
            out_meta.update(
                {
                    "height": window.height,
                    "width": window.width,
                    "transform": rasterio.windows.transform(window, src.transform),
                }
            )

            with rasterio.open(output_file, "w", **out_meta) as dest:
                dest.write(clipped)

    # Zuschnitt auf die eigentliche Bounding Box
    clip_to_bbox(output_file, output_file, full_bbox)

    # Funktion: Löschen der heruntergeladenen Tiles
    def delete_downloaded_tiles(parts):
        for part_file in parts:
            os.remove(part_file)

    # Löschen der heruntergeladenen Tiles
    delete_downloaded_tiles(downloaded_parts)

    # Schließen des Fortschrittsbalkens
    progress.close()

    # Erfolgsmeldung
    print(
        f"Der Prozess wurde erfolgreich abgeschlossen. Die Datei befindet sich unter: {output_file}"
    )
