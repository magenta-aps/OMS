import requests

URL = 'http://localhost:8000/earkweb/admin/login/'

client = requests.session()

# Make the GET request
# print 'cookie =', client.cookies['csrftoken']
res = client.get(URL)
csrftoken = client.cookies['csrftoken']
print 'csrftoken =',csrftoken
print res.status_code


#login_data = {'username':'eark', 'password':'eark', 'csrfmiddlewaretoken':csrftoken, 'next':'/hurra'}
login_data = {'username':'eark', 'password':'eark', 'csrfmiddlewaretoken':csrftoken}

res = client.post(URL, data = login_data, headers = {'Referer':URL})
print res.status_code

jar = client.cookies

# parameters = {'process_id':'7abd910e-a05e-4e51-9ca6-53dea71c9fb5'}
#parameters = {'process_id':'7abd910e-a05e-4e51-9ca6-53dea71c9faa'}
# res = client.get('http://localhost:8000/earkweb/search/order_status', params=parameters, headers = {'Referer':URL})
# print res.status_code

##### Place new order #####
payload = {'order_title':'AndreasPythonTestOrder', 'aip_identifiers':['0e54e9d5-256d-8e1d-6b6a-dbf5d417b61d']}
res = client.post('http://localhost:8000/earkweb/search/submit_order/', json = payload, headers = {'Referer':URL})
print res.status_code

