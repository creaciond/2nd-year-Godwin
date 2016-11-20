import requests
import json


parameters = {'user_id': '92283380', 'v': '5.52'}
response = requests.get('https://api.vk.com/method/users.get', params=parameters)
print('1) Status code: ' + str(response.status_code))
print('\r\n2) response.json():')
print(response.json())
print('\r\n2.5) response.json() построчно')
for each in response.json()['response']:
    for eachItem in each:
        print('%s: %s' % (eachItem, each[eachItem]))
print('\r\n3) Headers:')
for header in response.headers:
    print(header + ': ' + response.headers[header])
print('\r\n4) response.text:' + response.text)
