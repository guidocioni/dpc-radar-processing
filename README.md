# DPC Radar processor
## Downloader
Use `download_radar.py` to download a specific TIFF file

## Merger
Use `merge_radar.py` to merge multiple TIFF files into a single compressed netcdf file

## Socket
Use `websocket_reciver.py` to listen to the websocket where new products are advertised.
Once a new product appears it gets written to a text file so that the file can be downloaded and/or processed