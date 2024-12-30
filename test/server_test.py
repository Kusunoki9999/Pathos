import requests

url = "http://127.0.0.1:8080/api/submit"
image_path = "path/to/image.jpg"

with open(image_path, "rb") as img:
    files = {"image": img}
    data = {"title": "テストタイトル", "caption": "テストキャプション"}
    response = requests.post(url, data=data, files=files)

print(response.status_code)
print(response.json())
