import requests
import sys

# Syntax: python req_index.py <identifier> (= dipID)

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

identifier = sys.argv[1]
payload = {'identifier': identifier}
print payload
res = client.post('http://localhost:8000/earkweb/earkcore/index_local_storage_ip', json = payload, headers = {'Referer':URL})
print 'Status code:',res.status_code
print res.json()
