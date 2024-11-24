from pprint import pprint
import requests

URL = 'https://discosweb.esoc.esa.int'
token = 'IjIzOTM0ZWY4LWUwZmEtNDZhZC05ZmViLTE5YTNkY2Q3YTQwNiI.4YNLm_Y1rCJccv45t3BGvPFBN8g'


response = requests.get(
    f'{URL}/api/initial-orbits/{9254}',
    headers={
        'Authorization': f'Bearer {token}',
        'DiscosWeb-Api-Version': '2',
    },
    params={
        # 'fields': "eq(id,20920)",
        # 'sort': '-reentry.epoch',
    },
)

doc = response.json()
if response.ok:
    pprint(doc['data'])
else:
    pprint(doc['errors'])