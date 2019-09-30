import requests
import base64

# Used this to test because I had no data
image = open('temp.jpg', 'rb')
image_read = image.read()
req_encode = base64.encodebytes(image_read)
url = 'http://127.0.0.1:5000/check'
myobj = {'student': str(req_encode)}
image_64_decode = base64.decodebytes(req_encode)
image_result = open('temp.jpg','wb')
image_result.write(image_64_decode)
print(myobj)
print(req_encode)
x = requests.post(url, json = myobj)