import requests

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

parameters = {'process_id':'b62a7d5e-b403-461e-8258-5ae811fa17bc'}
# res = client.get('http://localhost:8001/earkweb/search/order_status', params=parameters, headers = {'Referer':URL})
# print res.status_code

##### Place new order #####
payload = {'order_title':'AndreasPythonTestOrder', 'aip_identifiers':['urn:uuid:adb2b78e-c9c2-a35a-8cfa-f163612b3a08']}
res = client.post('http://localhost:8000/earkweb/search/submit_order/', json = payload, headers = {'Referer':URL})
print 'Status code:',res.status_code
print res.json()
