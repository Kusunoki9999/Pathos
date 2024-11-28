import base64

img_path = r"test_image.JPG"
save_path = r"encoded_text\save_encode.txt"

with open(img_path,'br') as f0:
    encode_data = base64.b64encode(f0.read())
    
with open(save_path,'wb') as f1:
    f1.write(encode_data)