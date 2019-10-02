import requests
import base64

# Used this to test because I had no data
url = 'http://127.0.0.1:5000/check'
myobj = {'process': 'run'}
print(myobj)
x = requests.post(url, json = myobj)
