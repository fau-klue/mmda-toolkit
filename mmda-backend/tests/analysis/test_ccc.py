from backend.analysis.ccc import ccc_concordance, ccc_collocates
import pytest


@pytest.mark.conc
def test_ccc_concordance_simple(app, test_corpus):

    conc = ccc_concordance(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_items=test_corpus['discoursemes']['topic'],
        topic_name='topic',
        s_context=test_corpus['parameters']['s_context'],
        window_size=test_corpus['parameters']['context'],
        s_show=test_corpus['parameters']['s_show']
    )
    print(conc)


@pytest.mark.conc
def test_ccc_concordance_constellation(app, test_corpus):

    name = 'topic'
    conc = ccc_concordance(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_items=test_corpus['discoursemes'].pop(name),
        topic_name=name,
        s_context=test_corpus['parameters']['s_context'],
        window_size=10,
        context=test_corpus['parameters']['context'],
        additional_discoursemes=test_corpus['discoursemes'],
        s_show=test_corpus['parameters']['s_show']
    )
    print(conc)


@pytest.mark.conc
def test_ccc_concordance_constellation_2(app, test_corpus):

    conc = ccc_concordance(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_items=test_corpus['discoursemes']['topic'],
        topic_name='topic',
        s_context=test_corpus['parameters']['s_context'],
        window_size=5,
        context=test_corpus['parameters']['context'],
        additional_discoursemes={'disc1': test_corpus['discoursemes']['disc1']},
        s_show=test_corpus['parameters']['s_show'],
        cut_off=None
    )
    print(conc)


@pytest.mark.conc
def test_ccc_concordance_constellation_3(app, test_corpus):

    conc = ccc_concordance(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_items=['Merkel'],
        topic_name='topic',
        s_context=test_corpus['parameters']['s_context'],
        window_size=7,
        additional_discoursemes={'disc1': test_corpus['discoursemes']['disc1']},
        s_show=test_corpus['parameters']['s_show'],
        cut_off=None
    )
    print(conc)


@pytest.mark.coll
def test_ccc_collocates_simple(app, test_corpus):

    coll = ccc_collocates(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_items=test_corpus['discoursemes']['topic'],
        s_context=test_corpus['parameters']['s_context'],
        window_sizes=[3, 5, 7],
        context=test_corpus['parameters']['context']
    )
    print(coll)


@pytest.mark.coll
def test_ccc_collocates_constellation(app, test_corpus):

    coll = ccc_collocates(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_items=test_corpus['discoursemes']['topic'],
        s_context=test_corpus['parameters']['s_context'],
        window_sizes=test_corpus['parameters']['window_sizes'],
        context=test_corpus['parameters']['context'],
        additional_discoursemes={'disc1': test_corpus['discoursemes']['disc1']},
    )
    print(coll)
