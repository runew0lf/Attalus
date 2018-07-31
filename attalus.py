import requests
import random
import ctypes
import os
import time
from PIL import Image
import os.path

screensize = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

default_dir = 'Wallpaper'


def resize_image(image_path, size):
    """
    Resizes the image to fit our current desktop resolution
    :param image_path:
    :param size:
    :returns False if image is < 1024:
    """
    original_image = Image.open(image_path)
    width, height = original_image.size
    if width < 1024:
        print("width too small")
        return False

    resized_image = original_image.resize(size, Image.ANTIALIAS)
    resized_image.save(image_path)


def set_wallpaper(imagePath):
    """
    Set the wallpaper that we have downloaded
    :param imagePath:
    :returns false if the image is <1024
    """
    dirpath = os.path.dirname(__file__)
    full_path = os.path.abspath(os.path.join(dirpath, imagePath))
    print((full_path))
    if resize_image(full_path, screensize) == False:
        return False
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, full_path, 0)


def download_wallpaper(url: str):
    """
    Download the wallpaper from the url specified
    :param url:
    :return: false if the wallpaper already exists
    """
    r = requests.get(url, allow_redirects=True)
    filename = url[url.rfind("/") + 1:]
    filename = f"{default_dir}\{filename}"
    if(os.path.exists(filename)):
        print(f"{filename} already exists")
        return False
    open(filename, 'wb').write(r.content)
    return filename


def get_reddit(subreddit: str):
    """
    Grab wallpapers from reddit
    :param subreddit:
    :return random wallpaper url:
    """
    headers = {
        'User-Agent': 'Attallus V0.1'
    }

    new_images = []
    valid_images = ['.png', '.jpg']
    r = requests.get(f'https://www.reddit.com/r/{subreddit}/new/.json?limit=100', headers=headers)
    data = r.json()
    for item in data['data']['children']:
        for extension in valid_images:
            if extension in item['data']['url']:
                if item['data']['ups'] > 1:
                    new_images.append(item['data']['url'])
    return random.choice(new_images)

def get_imgur(tags: str):
    """
    Grab wallpapers from imgur
    :param tags:
    :return random wallpaper url:
    """
    new_images = []
    headers = {'Authorization': 'Client-ID ' + os.environ.get('IMGUR_ID')}
    r = requests.get(f'https://api.imgur.com/3/gallery/t/{tags}', headers=headers)
    data = r.json()
    for album in data['data']['items']:
        if 'images' in album:
            for image in album['images']:
                if image['width'] > image['height']:
                    new_images.append(image['link'])
        else:
            if album['width'] > album['height']:
                new_images.append(album['link'])
    return random.choice(new_images)


while True:
    seconds = 60
    minutes = 60
    hours = 1
    if random.choice([True, False]):
        url = get_reddit('wallpapers')
    else:
        url = get_imgur('Wallpaper')
    wallpaper_file = download_wallpaper(url)
    if wallpaper_file != False:
        if set_wallpaper(wallpaper_file) != False:
            time.sleep(seconds * minutes * hours)
            print("Time to change wallpaper")
