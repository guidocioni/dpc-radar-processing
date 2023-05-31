from definitions import logging
import argparse
from dpc_api import download_product
import pandas as pd

logging.getLogger('urllib3').setLevel(logging.CRITICAL)

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--product_type', help='Product type',
                    required=True, choices=["CAPPI4", "CAPPI6", "CAPPI8", "SRT6",
                                            "CAPPI2", "VMI", "HRD", "CAPPI5", "TEMP",
                                            "SRT1", "SRT3", "RADAR_STATUS", "CAPPI7",
                                            "SRT24", "CAPPI1", "SRI", "CAPPI3", "SRT12"])

parser.add_argument('-tr', '--time_radar',
                    help='Product time (epoch ns, e.g. 1685526600000)')

parser.add_argument('-tq', '--time_query',
                    help='Approximated time query to find closest radar product')

parser.add_argument('-o', '--output_folder', help='Output folder',
                    required=True)


args = parser.parse_args()


def main():
    product_type = args.product_type
    product_time = args.time_radar
    product_time_query = args.time_query
    folder = args.output_folder

    if product_time:
        logging.info(
            f"Downloading {product_type} at time {product_time} in folder {folder}")
        download_product(product_type, int(product_time), folder)
    elif product_time_query:
        product_time_query = pd.to_datetime(product_time_query, utc=True)
        product_time = int(product_time_query.replace(
            second=0, microsecond=0).timestamp() * 1000)
        logging.info(
            f"Downloading {product_type} at time {product_time} in folder {folder}")
        download_product(product_type, product_time, folder)


if __name__ == "__main__":
    main()
