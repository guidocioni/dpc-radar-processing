import requests as r
from os.path import exists as exists_local
from datetime import datetime
from definitions import logging

base_url_dpc = 'https://radar-api.protezionecivile.it/wide/product'


def check_exists(product_type, product_time):
    """Check if a specific product type at a specific time exists

    Args:
        product_type (str): can be in [ "CAPPI4", "CAPPI6", "CAPPI8", "SRT6",
        "CAPPI2", "VMI", "HRD", "CAPPI5", "TEMP",
        "SRT1", "SRT3", "RADAR_STATUS", "CAPPI7", "SRT24",
        "CAPPI1", "SRI", "CAPPI3", "SRT12" ]
        product_time (int): epoch in milliseconds

    Returns:
        bool: True if exists, otherwise False
    """
    response = r.get(
        f'{base_url_dpc}/existsProduct?type={product_type}&time={product_time}')
    response.raise_for_status()

    return response.json()


def find_last(product_type):
    """Find last product timestamp by type

    Args:
        product_type (str): can be in [ "CAPPI4", "CAPPI6", "CAPPI8", "SRT6",
        "CAPPI2", "VMI", "HRD", "CAPPI5", "TEMP",
        "SRT1", "SRT3", "RADAR_STATUS", "CAPPI7", "SRT24",
        "CAPPI1", "SRI", "CAPPI3", "SRT12" ]

    Returns:
        json: directly the respone
    """
    response = r.get(
        f'{base_url_dpc}/findLastProductByType?type={product_type}')
    response.raise_for_status()

    return response.json()


def download_product(product_type, product_time, write_folder="."):
    """Download the product

    Args:
        product_type (str): can be in [ "CAPPI4", "CAPPI6", "CAPPI8", "SRT6",
        "CAPPI2", "VMI", "HRD", "CAPPI5", "TEMP",
        "SRT1", "SRT3", "RADAR_STATUS", "CAPPI7", "SRT24",
        "CAPPI1", "SRI", "CAPPI3", "SRT12" ]
        product_time (int): epoch in milliseconds
        write_folder (str, optional): The output folder. Defaults to ".".

    Returns:
        str: The path of the file as string
    """
    # Convert product_time to something better
    filename = f"{write_folder}/radar_{product_type}_{datetime.utcfromtimestamp(product_time / 1000.).strftime('%Y%m%d%H%M')}.tiff"
    # First check if the file exists locally, in this case
    # we don't need to download it
    if exists_local(filename):
        return filename
    # Then check if the product exists remotely
    exists = check_exists(product_type, product_time)
    if not exists:
        logging.warning(
            f'Not found product {product_type} at time {product_time}')
        return None
    # Otherwise proceed to download
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"productType":"%s","productDate":"%s"}' % (
        product_type, product_time)
    with open(filename, 'wb') as f:
        ret = r.post(f'{base_url_dpc}/downloadProduct',
                     headers=headers, data=data, stream=True)
        ret.raise_for_status()
        for d in ret.iter_content(1024):
            f.write(d)

    return filename
