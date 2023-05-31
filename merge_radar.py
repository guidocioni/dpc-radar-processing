from definitions import logging
from glob import glob
import rioxarray as rxr
from tqdm import tqdm
import xarray as xr
import re
import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', help='Input files (as glob pattern), e.g. "/tmp/radar_SRI_20230530*.tiff"',
                    required=True)

parser.add_argument('-o', '--output', help='Output filename (netcdf file)',
                    required=True)

args = parser.parse_args()


def main():
    input_glob = args.input
    output = args.output

    files = glob(input_glob)

    dss = []
    time = []
    logging.info("Reading files")
    for f in tqdm(files):
        try:
            dss.append(rxr.open_rasterio(f).squeeze())
            time.append(pd.Timestamp(re.findall(
                r"(?:_)(\d{12})(?:.tiff)", f)[0]))
        except Exception as e:
            print(
                f"Could not process {f}: {type(e).__name__}: {e}")

    logging.info("Concatenating")
    var_name = re.findall(r"(?:radar_)(.*)(?:_\d{12})(?:.tiff)", f)[0]
    dss = xr.concat(dss, dim=time).rename(var_name).rename({'concat_dim': 'time',
                                                            'x': 'lon', 'y': 'lat'}).drop(['band', 'spatial_ref'])
    dss = dss.where(dss != -9999., 0)
    dss = dss.sortby('time')

    comp = dict(zlib=True, complevel=9)
    encoding = {dss.name: comp}
    logging.info("Writing to disk")
    dss.to_netcdf(
        path=output,
        mode='w',
        format='NETCDF4',  # netcdf4 library needs to be installed
        engine='netcdf4',
        encoding=encoding,
        compute=True
    )


if __name__ == "__main__":
    main()
