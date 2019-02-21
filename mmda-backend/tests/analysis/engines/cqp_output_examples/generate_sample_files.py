from subprocess import Popen, PIPE
from os import getenv


def create_topic_discourseme_query_window(topic_items,
                                          discourseme_items,
                                          p_att,
                                          s_att,
                                          window_size):
    """
    Creates CQP query for a discourseme given a topic.
    Includes window_size breaks.

    :param str topic_items: topic items
    :param str discourseme_items: discourseme items
    :param str p_att: p-attribute to query (typically 'lemma')
    :param str s_att: s-attribute where to break (typically 's' or 'tweet')
    :return: topic-discourseme CQP query as string
    :rtype: str
    """
    query = '(({topic_query} []{{,{ws}}} @{discourseme_query}) ' +\
            '| (@{discourseme_query} []{{,{ws}}} {topic_query})) ' +\
            'within {s_att}'
    query = query.format(
        discourseme_query=create_cqp_query_from_items(discourseme_items, p_att),
        topic_query=create_cqp_query_from_items(topic_items, p_att),
        s_att=s_att,
        ws=window_size
    )

    return query


def create_cqp_query_from_items(items, p_att):
    """
    Creates CQP query from item-list

    :param list items: user input in interface (list of tokens)
    :parm p_att str: p-attribute to query
    :return: CQP query as string
    :rtype: str
    """

    query = '[{p_att}="{items}"]'.format(
        p_att=p_att,
        items='|'.join(items)
    )

    return query


REGISTRY_PATH = getenv(
    'MMDA_CQP_REGISTRY',
    default='/usr/local/cwb-3.4.13/share/cwb/registry'
)


test_settings = {

    'corpus_name': 'LTWBY2018',

    'cqp_query': 'show +tt_lemma; A=[tt_lemma="Natur"]; cat A;',

    'items1': ['Hessen', 'Bayern'],
    'items2': ['Angela', 'Merkel'],

    'cut_off_concordances': 10,
    'cut_off_collocates': 100,

    'association_settings': {
        'p_att': 'tt_lemma',
        's_att': 'tweet',
        'window_size': 5,
        'association_measures': [
            'am.Dice',
            'am.log.likelihood'
        ]  # all_ams = "am.%"
    }
}


def popen_cqp_query(corpus_name, cmd, p_out):
    """
    Lets CQP evaluate a command via Popen.

    :param str corpus_name: corpus to be queried
    :param str cmd: CQP command
    :return: decoded return value of CQP
    :rtype: str
    """

    start_cqp = [
        'cqp',
        '-c',
        '-r',
        REGISTRY_PATH,
        '-D',
        corpus_name.upper()
    ]

    cqp_process = Popen(start_cqp,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE)

    cqp_return = cqp_process.communicate(cmd.encode())[0]

    with open("/home/ausgerechnet/projects/efe/mmda/mmda-refactor/mmda-backend/tests/analysis/engine/cqp_output_examples/" + p_out, "wb") as f:
        f.write("\n".join(cqp_return.decode().split("\n")[:50]).encode())


# cqp_simple
popen_cqp_query(test_settings['corpus_name'],
                test_settings['cqp_query'],
                "cqp_simple")


# cqp settings
cqp_settings = 'set PrintOptions hdr;' +\
               'set ShowTagAttributes on;' +\
               'set PrintMode sgml;' +\
               'set Context 1 {s_att};'
cqp_settings = cqp_settings.format(
    s_att=test_settings['association_settings']['s_att']
)

cqp_settings_p_att = 'set PrintOptions hdr;' +\
           'set ShowTagAttributes on;' +\
           'set PrintMode sgml;' +\
           'set Context 1 {s_att};' +\
           'show -word +{p_att};'

cqp_settings_p_att = cqp_settings_p_att.format(
    p_att=test_settings['association_settings']['p_att'],
    s_att=test_settings['association_settings']['s_att']
)


# conc_simple
cqp_exec = 'A = {query}; cat A;'
cqp_exec = cqp_exec.format(
    query=create_cqp_query_from_items(
        test_settings['items1'],
        test_settings['association_settings']['p_att']
    )
)

popen_cqp_query(test_settings['corpus_name'],
                cqp_settings + cqp_exec,
                "concordance_simple")


# conc_simple_p_att
popen_cqp_query(test_settings['corpus_name'],
                cqp_settings_p_att + cqp_exec,
                "concordance_simple_p_att")


# conc_complex
cqp_exec = 'A = {query}; cat A;'
cqp_exec = cqp_exec.format(
    query=create_topic_discourseme_query_window(
        test_settings['items1'],
        test_settings['items2'],
        test_settings['association_settings']['p_att'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['window_size']
    )
)

popen_cqp_query(test_settings['corpus_name'],
                cqp_settings + cqp_exec,
                "concordance_complex")

# conc_complex_p_att
popen_cqp_query(test_settings['corpus_name'],
                cqp_settings_p_att + cqp_exec,
                "concordance_complex_p_att")
