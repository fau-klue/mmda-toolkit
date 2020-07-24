from backend.analysis.ccc import get_concordance, get_collocates
import pytest


@pytest.mark.conc
def test_get_concordance(germaparl):

    name = 'topic'
    conc = get_concordance(
        corpus_name=germaparl['corpus']['name'],
        topic_items=germaparl['discoursemes'][name],
        topic_name=name,
        s_context=germaparl['parameters']['s_context'],
        window_size=germaparl['parameters']['context'],
        s_show=[germaparl['corpus']['meta_s']]
    )
    print(conc)


@pytest.mark.conc
def test_get_concordance_dp(germaparl):

    name = 'topic'
    conc = get_concordance(
        corpus_name=germaparl['corpus']['name'],
        topic_items=germaparl['discoursemes'].pop(name),
        topic_name=name,
        s_context=germaparl['parameters']['s_context'],
        window_size=10,
        context=germaparl['parameters']['context'],
        additional_discoursemes=germaparl['discoursemes'],
        s_show=[germaparl['corpus']['meta_s']]
    )
    print(conc)


@pytest.mark.conc
def test_get_concordance_dp_2(germaparl):

    conc = get_concordance(
        corpus_name=germaparl['corpus']['name'],
        topic_items=['Merkel'],
        topic_name='topic',
        s_context=germaparl['parameters']['s_context'],
        window_size=5,
        context=germaparl['parameters']['context'],
        additional_discoursemes={'temp': ['Angela']},
        s_show=[germaparl['corpus']['meta_s']],
        cut_off=None
    )
    print(conc)


@pytest.mark.conc
def test_get_concordance_dp_3(germaparl):

    conc = get_concordance(
        corpus_name=germaparl['corpus']['name'],
        topic_items=['Merkel'],
        topic_name='topic',
        s_context=germaparl['parameters']['s_context'],
        window_size=7,
        additional_discoursemes={'temp': ['Angela']},
        s_show=[germaparl['corpus']['meta_s']],
        cut_off=None
    )
    print(conc)


@pytest.mark.coll
def test_get_collocates(germaparl):

    name = 'topic'
    coll = get_collocates(
        corpus_name=germaparl['corpus']['name'],
        topic_items=germaparl['discoursemes'][name],
        s_context=germaparl['parameters']['s_context'],
        window_size=5,
        context=germaparl['parameters']['context']
    )
    print(coll)


@pytest.mark.coll
def test_get_collocates_dp(germaparl):

    name = 'topic'
    coll = get_collocates(
        corpus_name=germaparl['corpus']['name'],
        topic_items=germaparl['discoursemes'][name],
        s_context=germaparl['parameters']['s_context'],
        window_size=5,
        context=germaparl['parameters']['context'],
        additional_discoursemes={'temp': ['Verhandlung']},
    )
    print(coll)
