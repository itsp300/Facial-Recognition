import base64

image = open('test.jpg', 'rb')
image_read = image.read()
req_encode = base64.encodebytes(image_read)
print(req_encode)


# Decode the image into temp image file
image_64_decode = base64.decodebytes(req_encode)
image_result = open('test.jpg','wb')
image_result.write(image_64_decode)