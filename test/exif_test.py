from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
import pandas as pd

path = "decoded_image\decoded.jpg"

def load_exif(path):
    ifd_dict = {}
    with Image.open(path) as im:
        exif = im.getexif()
    ifd_dict["Exif"] = exif.get_ifd(0x8769) #0x8769がExifデータへのアクセスタグ番号
    ifd_dict["GPSInfo"] = exif.get_ifd(0x8825) #0x8825がGPSデータ
    return ifd_dict

ifd_dict = load_exif(path)
exif_sr = pd.Series(ifd_dict["Exif"]).rename(TAGS)
gps_sr = pd.Series(ifd_dict["GPSInfo"]).rename(GPSTAGS)

print(gps_sr)