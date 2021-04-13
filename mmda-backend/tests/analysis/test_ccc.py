from backend.analysis.ccc import ccc_concordance, ccc_collocates
import pytest


@pytest.mark.conc
def test_ccc_concordance_simple(germaparl):

    name = 'topic'
    conc = ccc_concordance(
        corpus_name=germaparl['corpus']['name'],
        topic_items=germaparl['discoursemes'][name],
        topic_name=name,
        s_context=germaparl['parameters']['s_context'],
        window_size=germaparl['parameters']['context'],
        s_show=[germaparl['corpus']['meta_s']]
    )
    print(conc)


@pytest.mark.conc
def test_ccc_concordance_constellation(germaparl):

    name = 'topic'
    conc = ccc_concordance(
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
def test_ccc_concordance_constellation_2(germaparl):

    conc = ccc_concordance(
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
def test_ccc_concordance_constellation_3(germaparl):

    conc = ccc_concordance(
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
def test_ccc_collocates_simple(germaparl):

    name = 'topic'
    coll = ccc_collocates(
        corpus_name=germaparl['corpus']['name'],
        topic_items=germaparl['discoursemes'][name],
        s_context=germaparl['parameters']['s_context'],
        window_sizes=[3, 5, 7],
        context=germaparl['parameters']['context']
    )
    print(coll)


@pytest.mark.coll
def test_ccc_collocates_constellation(germaparl):

    name = 'topic'
    coll = ccc_collocates(
        corpus_name=germaparl['corpus']['name'],
        topic_items=germaparl['discoursemes'][name],
        s_context=germaparl['parameters']['s_context'],
        window_sizes=[3, 5, 7],
        context=germaparl['parameters']['context'],
        additional_discoursemes={'temp': ['Verhandlung']},
    )
    print(coll)
