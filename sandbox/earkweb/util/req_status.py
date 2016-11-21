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

jobid = sys.argv[1]
res = client.get('http://localhost:8000/earkweb/search/jobstatus/' + jobid, headers = {'Referer':URL})
print 'Status code:',res.status_code
print res.json()


