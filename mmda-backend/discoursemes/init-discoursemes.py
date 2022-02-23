import requests
# import gzip
# import json

# with gzip.open("mmda-backend/discoursemes/dornseiff.ldjson.gz", "rt") as f:
#     for line in f:
#         disc = dict()
#         sachgruppe = json.loads(line)
#         disc['items'] = [val for sublist in sachgruppe['items'] for val in sublist]
#         disc['name'] = sachgruppe['meta']['name']
#         break


discoursemes = [
    {'name': 'Atomkraft',
     'items': ['Atomkraft', 'Atomenergie',
               'Kernkraft', 'Kernenergie',
               'Nuklearenergie', 'Nuklearkraft']},
    {'name': 'Klimawandel',
     'items': ["Klimawandel", "Klimaveränderung", "Klimaänderung",
               "Klimawechsel", "global Erwärmung", "Klimakrise"]},
    {'name': 'Kampf',
     'items': ["Bekämpfung", "Kampf", "aufhalten"]},
    {'name': 'Ressourcen',
     'items': ["Armut", "Hunger", "Dürre", "Ressourcenknappheit"]},
    {'name': 'Wetter',
     'items': ["Sturm", "Wetterereignis", "Naturkatastrophe"]},
    {'name': 'Anpassung',
     'items': ["Anpassungsmaßnahme", "Maßnahme", "bewältigen", "Anpassung"]}
]


# login and save token
response = requests.post(
    "http://localhost:5000/api/login/",
    json={"username": "admin", "password": "Squanchy1"},
)
access_token = response.json()['access_token']

# create discoursemes
for discourseme in discoursemes:
    response = requests.post(
        "http://localhost:5000/api/user/admin/discourseme/",
        json={'name': discourseme['name'],
              'items': discourseme['items']},
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )

# check stored discoursemes
response = requests.get(
    "http://localhost:5000/api/user/admin/discourseme/",
    headers={'Authorization': 'Bearer {}'.format(access_token)}
)
stored_discoursemes = response.json()
print(stored_discoursemes)
