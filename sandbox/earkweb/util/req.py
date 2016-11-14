import requests
import sys

URL = 'http://localhost:8000/earkweb/admin/login/'

client = requests.session()

# Get CSRF token
print 'Get CSRF token...'
res = client.get(URL)
csrftoken = client.cookies['csrftoken']
print 'csrftoken =',csrftoken
print 'Status code:',res.status_code
print

# Login to Django
print 'Logging in...'
login_data = {'username':'eark', 'password':'eark', 'csrfmiddlewaretoken':csrftoken}
res = client.post(URL, data = login_data, headers = {'Referer':URL}, allow_redirects = False)
print 'Status code:',res.status_code
print

#parameters = {'process_id':'1459cece-a304-4648-9cd5-2ea9bf9f4dbe'}
#res = client.get('http://localhost:8000/earkweb/search/order_status', params=parameters, headers = {'Referer':URL})
#print 'Status code:',res.status_code

##### Place new order #####
order_title = sys.argv[1]
payload = {'order_title':order_title, 'aip_identifiers':['urn:uuid:adb2b78e-c9c2-a35a-8cfa-f163612b3a08']}
res = client.post('http://localhost:8000/earkweb/search/submit_order/', json = payload, headers = {'Referer':URL})
print 'Status code:',res.status_code
print res.json()
