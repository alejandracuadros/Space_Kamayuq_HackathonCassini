from pprint import pprint
import requests

URL = 'https://discosweb.esoc.esa.int'
token = 'IjIzOTM0ZWY4LWUwZmEtNDZhZC05ZmViLTE5YTNkY2Q3YTQwNiI.4YNLm_Y1rCJccv45t3BGvPFBN8g'


response = requests.get(
    f'{URL}/api/objects',
    headers={
        'Authorization': f'Bearer {token}',
        'DiscosWeb-Api-Version': '2',
    },
    params={
        'filter': "eq(objectClass,Payload)&gt(reentry.epoch,epoch:'2020-01-01')",
        'sort': '-reentry.epoch',
    },
)

doc = response.json()
if response.ok:
    pprint(doc['data'])
else:
    pprint(doc['errors'])