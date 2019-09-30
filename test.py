import requests
import base64

image = open('temp.jpg', 'rb')
image_read = image.read()
req_encode = base64.encodebytes(image_read)
url = 'http://127.0.0.1:5000/check'
myobj = {'student': str(req_encode)}
print(myobj)
print(req_encode)
x = requests.post(url, json = myobj)