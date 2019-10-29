import base64
# Encode the image
image = open('test.jpg', 'rb')
image_read = image.read()
req_encode = base64.encodebytes(image_read)
print(req_encode)
req_encode.decode(encoding="utf-8")
print(req_encode)
req_encode = bytes(req_encode, 'utf-8')
print(req_encode)
image_64_decode = base64.decodebytes(req_encode)
print(image_64_decode)