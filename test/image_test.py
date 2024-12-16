from PIL import Image
import io

try:
    # 保存された画像を開く
    with Image.open("../static/images/61c469971aba4ddbab8136788fbde6a.jpg") as img:
        img.verify()  # 画像が破損していないか確認
        print("画像は正常です。")
except Exception as e:
    print("画像が破損しています:", e)
