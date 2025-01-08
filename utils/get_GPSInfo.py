from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PIL.TiffImagePlugin import IFDRational
import io

def convert_exif_value(value):
    if isinstance(value, IFDRational):
        return float(value)
    elif isinstance(value, (list, tuple)):
        return [convert_exif_value(v) for v in value]
    return value

async def extract_gps_from_image(image):
    gps_data = {}
    
    with Image.open(io.BytesIO(image)) as img:
        exif_data = img._getexif()
        print(exif_data)
        
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)  # タグ番号を名前に変換(第二引数はdefaltのReturn値)
                if tag_name == "GPSInfo": # GPSInfoは辞書型でありbytes型ではない
                    for gps_tag, gps_value in value.items(): # GPSはタグ名付きの辞書に変換
                        gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                        if gps_tag_name == "GPSLatitude":
                            gps_data["GPSLatitude"] = [
                                float(v) if isinstance(v, IFDRational) else v
                                for v in gps_value
                            ]
                        elif gps_tag_name == "GPSLongitude":
                            gps_data["GPSLongitude"] = [
                                float(v) if isinstance(v, IFDRational) else v
                                for v in gps_value
                            ]
    return gps_data