import ctypes
import sys
import os
import requests
import json
from PIL import Image
from io import BytesIO
import logging

domain = 'https://rammb-slider.cira.colostate.edu'
lastest_path = domain + '/data/json/goes-16/conus/geocolor/latest_times.json'
zoom_level = 2
y_range = [1, 2]
x_range = [0, 1, 2]
dimensions = (3, 2)
save_path = os.path.join('C:\\', 'temp', 'goes', 'wallpaper.png')
file_type = 'PNG'

logging_config = {"filename": os.path.join('C:\\', 'temp', 'goes', 'log.txt'),
        "filemode": 'a',
        "format": '%(asctime)s %(levelname)s %(message)s',
        "level": logging.INFO}

def get_latest_time():
    resp = json.loads(str(requests.get(lastest_path).text))
    logging.debug("latest_times.json: " + str(resp))
    return resp['timestamps_int'][0]

def get_urls(curr_time):
    imagery_path = '%s/data/imagery/%08d/goes-16---conus/geocolor/%14d/%02d/%03d_%03d.png'
    for y in y_range:
        for x in x_range:
            yield imagery_path % (domain, int(str(curr_time)[:8]), curr_time, zoom_level, y, x)

def get_images(urls):
    for url in urls:
        logging.info("Retrieving url: " + str(url))
        yield Image.open(BytesIO(requests.get(url).content))

def stitch_images(imgs):
    first_img = next(imgs)
    first_width = first_img.width
    first_height = first_img.height
    final_img = Image.new("RGB", (first_width*dimensions[0], first_height*dimensions[1]))
    logging.info("Final dimensions: " + str(final_img.size))

    curr_width, curr_height = 0, 0
    logging.info("Pasting to image at (0, 0)")
    final_img.paste(first_img, (0, 0))
    for img in imgs:
        curr_width += 1
        if curr_width >= dimensions[0]:
            curr_width = 0
            curr_height += 1
            if curr_height >= dimensions[1]:
                break
        paste_loc = (curr_width*first_width, curr_height*first_height)
        logging.info("Pasting to image at " + str(paste_loc))
        final_img.paste(img, paste_loc)
    return final_img

def change_wallpaper(img_path):
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_SENDWININICHANGE = 3

    # Convert string to unicode in Python 2 for calling 
    # Windows DLL function with 'W' type (rather than 'A')
    if sys.version_info.major == 2:
        img_path = unicode(img_path)
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_path, SPIF_SENDWININICHANGE)

def main():
    logging.basicConfig(**logging_config)
    curr_time = get_latest_time()
    logging.info("Most recent image time: " + str(curr_time))
    urls = get_urls(curr_time)
    imgs = get_images(urls)
    final_img = stitch_images(imgs)
    logging.info("Saving to " + save_path)
    final_img.save(save_path, file_type)
    logging.info("Changing wallpaper to " + str(save_path))
    change_wallpaper(save_path)

if __name__ == '__main__':
    try:
        main()
    except:
        logging.exception("Exception while running the program: ")
