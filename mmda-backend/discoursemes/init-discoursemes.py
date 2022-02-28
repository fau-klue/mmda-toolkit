import requests
from pprint import pprint
import gzip
import json


DORNSEIFF_DISCOURSEMES = list()
with gzip.open("discoursemes/dornseiff.ldjson.gz", "rt") as f:
    for line in f:
        disc = dict()
        sachgruppe = json.loads(line)
        disc['items'] = [val for sublist in sachgruppe['items'] for val in sublist]
        disc['name'] = sachgruppe['meta']['name']
        DORNSEIFF_DISCOURSEMES.append(disc)


INFODEMIC_DISCOURSEMES = [
    {
        'name': 'Corona',
        'items': ['Corona',
                  'Coronavirus',
                  'Covid',
                  'Covid19',
                  'Covid-19',
                  '#Corona',
                  '#Coronavirus',
                  '#Covid',
                  '#Covid19',
                  '#Covid-19']
    },
    {
        'name': 'Grippe',
        'items': ['#Grippe',
                  'normal Grippe',
                  'leicht Grippe',
                  '#Erkältung',
                  'normal Erkältung',
                  'leicht Erkältung']
    },
]


KLIMAWANDEL_DISCOURSEMES = [
    {
        'name': 'Atomkraft',
        'items': ['Atomkraft',
                  'Atomenergie',
                  'Kernkraft',
                  'Kernenergie',
                  'Nuklearenergie',
                  'Nuklearkraft']
    },
    {
        'name': 'Ausbau',
        'items': ['Ausbau',
                  'ausbauen',
                  'Förderung',
                  'Steigerung die Anteil']
    },
    {
        'name': 'Ausstieg',
        'items': ['Ausstieg',
                  'aussteigen']
    },
    {
        'name': 'erneuerbare Energien',
        'items': ["erneuerbar Energie",
                  "regenerativ Energie",
                  "Windenergie",
                  "Sonnenenergie"]
    },
    {
        'name': 'fossile Energie',
        'items': ["fossil Energie",
                  "fossil Brennstoff",
                  "Braunkohle",
                  "Steinkohle",
                  "Erdgas",
                  "Erdöl",
                  "Mineralöl"]
    },
    {
        'name': 'Klimawandel',
        'items': ["Klimawandel",
                  "Klimaveränderung",
                  "Klimaänderung",
                  "Klimawechsel",
                  "global Erwärmung",
                  "Klimakrise"]
    },
    {
        'name': 'Kampf',
        'items': ["Bekämpfung",
                  "Kampf",
                  "aufhalten"]
    },
    {
        'name': 'Mangel',
        'items': ["Armut",
                  "Hunger",
                  "Dürre",
                  "Ressourcenknappheit"]
    },
    {
        'name': 'Wetter',
        'items': ["Sturm",
                  "Wetterereignis",
                  "Naturkatastrophe"]
    },
    {
        'name': 'Anpassung',
        'items': ["Anpassungsmaßnahme",
                  "Maßnahme",
                  "bewältigen",
                  "Anpassung"]
    }
]


# login and save token
def login(username='admin', password='Squanchy1'):
    response = requests.post(
        "http://localhost:5000/api/login/",
        json={"username": username, "password": password},
    )
    access_token = response.json()['access_token']
    return access_token


# create discoursemes
def create_discoursemes(access_token, discoursemes):
    for discourseme in discoursemes:
        requests.post(
            "http://localhost:5000/api/user/admin/discourseme/",
            json={'name': discourseme['name'],
                  'items': discourseme['items']},
            headers={'Authorization': 'Bearer {}'.format(access_token)}
        )


# check stored discoursemes
def list_discoursemes(access_token):
    response = requests.get(
        "http://localhost:5000/api/user/admin/discourseme/",
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    return response.json()


if __name__ == '__main__':

    token = login()
    create_discoursemes(token, INFODEMIC_DISCOURSEMES)
    # create_discoursemes(token, DORNSEIFF_DISCOURSEMES)
    pprint(list_discoursemes(token))
