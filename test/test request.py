import json

import requests
_dat = {'order_type': 'pick'}
response = requests.post('http://51.158.120.193:8001/api/v1/orders/5/update-status?order_type=pick')
print(response)

