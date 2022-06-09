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


# TODO
# rename show in surface

# disentangle
# cqp_query = items_query + p_query + flags_query + escape_query (+ s_query)
# and
# items_show = context + (p_show + flags_show + escape_show)

# allow cqp expressions to be passed

# disentangle
# matches = discourseme + corpus
# and
# collocation = query + context and collocation parameters


# query

# no linguistic analysis
# ...
# - meta distribution (words don't play a role)
# - breakdown (summary of surface realization of the matches) → linked to kwic
# - kwic (surface realization of the matches in context) → read 1 by 1
# - collocation analysis (summary of the surface realization of the context) → linked to kwic
# - generalized usage fluctuation analysi, → linked to kwic
# ...
# very linguistic analysis


# keyword analysis

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
        'items': ['Grippe',
                  '#Grippe',
                  'normal Grippe',
                  'leicht Grippe',
                  '#Erkältung',
                  'normal Erkältung',
                  'leicht Erkältung']
    },
    # {
    #     'name': 'Handelnde',
    #     'items': []
    #     # dahinter steck*,
    #     # kontrolliert [von,durch],
    #     # unter {ART} Kontrolle,
    # },
    # {
    #     'name': 'AktionProzess',
    #     'items': []
    #     # gegen {ART} (_{A})? [Bevölkerung,Volk,Menschen,Deutschen,Leute,Weltbevölkerung],
    #     # heimlich*,
    #     # versteckt*,
    #     # Krieg,
    #     # Kriegszustand,
    #     # dritte* Weltkrieg,
    #     # ist in [Wahrheit,Wirklichkeit],
    #     # soll eigentlich,
    #     # lüg*,
    #     # zuf?ll*,
    #     # Menschenverstand
    # },
    # {
    #     'name': 'Medium',
    #     'items': []
    #     # Notwehr,
    #     # Diktatur,
    #     # Befreiungskampf,
    #     # Widerstand,
    #     # Bürgerpflicht,
    #     # ist in [Wahrheit,Wirklichkeit],
    #     # soll eigentlich,
    #     # lüg*,
    #     # zuf?ll*,
    #     # Recht
    # },
    # {
    #     'name': 'Intention',
    #     'items': []
    #     # um * Kontrolle,
    #     # Massenkontrolle,
    #     # Massenvernichtung,
    #     # Vernichtung,
    #     # Auslöschung
    # },
    # {
    #     'name': 'Betroffene',
    #     'items': []
    #     # Kontrolle über uns*,
    #     # Kontrolle über {ART} (_{A})? [Bevölkerung,Volk,Menschen,Deutschen,Leute,Weltbevölkerung],
    #     # um uns* (_{N})? zu,
    # },
    # {
    #     'name': 'AmbivalenterDritter',
    #     'items': []
    #     # Verrat,
    #     # Verräter*,
    #     # Puppe*,
    #     # Marionette*,
    #     # unterwander*,
    #     # Sumpf,
    #     # lüg*,
    #     # zuf?ll*,
    #     # zens**r*,
    #     # Einheitspresse,
    #     # Mainstream,
    #     # Systemmedien,
    #     # Einheitsbrei,
    #     # gleichgeschaltet*
    # }
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
