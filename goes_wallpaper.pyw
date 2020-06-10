import ctypes
from io import BytesIO
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

import requests


DATA_DIR = os.path.join(os.getenv("LocalAppData"), "GOES-16")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Constants
IMAGE_URL = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/latest.jpg"
WALLPAPER_PATH = os.path.join(DATA_DIR, 'wallpaper.jpg')
WALLPAPER_FILETYPE = 'JPEG'


# Setup logging
def setup_logging():
    log_handler = RotatingFileHandler(
                    os.path.join(DATA_DIR, 'log.txt'), # filename "C:\\temp\\goes\\log.txt", 
                    mode='a',
                    maxBytes=1024*1024, # 1MB
                    backupCount=0,
                    encoding=None,
                    delay=0
            )
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    # print_handler = logging.StreamHandler(sys.stdout)
    # print_handler.setLevel(logging.INFO)

    app_log = logging.getLogger()
    app_log.setLevel(logging.INFO)
    app_log.addHandler(log_handler)
    # app_log.addHandler(print_handler)

def change_wallpaper(img_path):
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_SENDWININICHANGE = 3

    # Convert string to unicode in Python 2 for calling 
    # Windows DLL function with 'W' type (rather than 'A')
    if sys.version_info.major == 2:
        img_path = unicode(img_path)
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_path, SPIF_SENDWININICHANGE)

def main():
    setup_logging()

    logging.info("Downloading from " + IMAGE_URL)
    img_req = requests.get(IMAGE_URL)
    if img_req.status_code != 200:
        logging.error("Unexpected status code: %d" % img_req.status_code)
        return
    if img_req.headers.get('content-type') != 'image/jpeg':
        logging.error("Unexpected content type: %s" % img_req.headers.get('content-type'))
        return

    logging.info("Saving to " + WALLPAPER_PATH)
    with open(WALLPAPER_PATH, "wb") as f:
        f.write(img_req.content)
    """
    with BytesIO(img_req.content) as img_bytes:
        with Image.open(img_bytes) as final_img:
            logging.info("Saving to " + WALLPAPER_PATH)
            final_img.save(WALLPAPER_PATH, WALLPAPER_FILETYPE)
    """

    logging.info("Changing wallpaper to " + str(WALLPAPER_PATH))
    change_wallpaper(WALLPAPER_PATH)

if __name__ == '__main__':
    try:
        main()
    except:
        logging.exception("Exception while running the program: ")

