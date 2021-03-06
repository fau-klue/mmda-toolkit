from backend.analysis.ccc import ccc_concordance, ccc_collocates, ccc_keywords
from backend.analysis.ccc import ccc_constellation_association
import pytest


###############
# CONCORDANCE #
###############
@pytest.mark.conc
def test_ccc_simple_concordance(app, test_corpus):

    conc = ccc_concordance(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_discourseme={'topic': test_corpus['discoursemes']['topic']},
        filter_discoursemes={},
        additional_discoursemes={},
        s_context=test_corpus['parameters']['s_context'],
        window_size=test_corpus['parameters']['context'],
        s_show=test_corpus['parameters']['s_show']
    )
    print(conc)


@pytest.mark.conc
@pytest.mark.now
def test_ccc_constellation_concordance(app, test_corpus):

    conc = ccc_concordance(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_discourseme={'topic': test_corpus['discoursemes']['topic']},
        filter_discoursemes={},
        additional_discoursemes={},
        s_context=test_corpus['parameters']['s_context'],
        window_size=10,
        context=test_corpus['parameters']['context'],
        s_show=test_corpus['parameters']['s_show']
    )
    print(conc)


@pytest.mark.conc
def test_ccc_constellation_concordance_2(app, test_corpus):

    conc = ccc_concordance(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_discourseme={'topic': test_corpus['discoursemes']['topic']},
        filter_discoursemes={},
        additional_discoursemes={},
        s_context=test_corpus['parameters']['s_context'],
        window_size=5,
        context=test_corpus['parameters']['context'],
        s_show=test_corpus['parameters']['s_show'],
        cut_off=None
    )
    print(conc)


@pytest.mark.conc
def test_ccc_constellation_concordance_3(app, test_corpus):

    conc = ccc_concordance(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_discourseme={'topic': test_corpus['discoursemes']['topic']},
        filter_discoursemes={},
        additional_discoursemes={},
        s_context=test_corpus['parameters']['s_context'],
        window_size=7,
        s_show=test_corpus['parameters']['s_show'],
        cut_off=None
    )
    print(conc)


###############
# COLLLOCATES #
###############
@pytest.mark.coll
def test_ccc_simple_collocates(app, test_corpus):

    coll = ccc_collocates(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_items=test_corpus['discoursemes']['topic'],
        s_context=test_corpus['parameters']['s_context'],
        windows=[3, 5, 7]
    )
    print(coll)


@pytest.mark.coll
def test_ccc_constellation_collocates(app, test_corpus):

    coll = ccc_collocates(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        topic_items=test_corpus['discoursemes']['topic'],
        s_context=test_corpus['parameters']['s_context'],
        windows=test_corpus['parameters']['window_sizes'],
        context=test_corpus['parameters']['context'],
        additional_discoursemes={'disc1': test_corpus['discoursemes']['disc1']},
    )
    print(coll)


############
# KEYWORDS #
############
@pytest.mark.keywords
def test_ccc_keywords(app, test_corpus):

    kw = ccc_keywords(
        corpus=test_corpus['corpus_name'],
        corpus_reference=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH']
    )
    print(kw)


###############
# ASSOCIATION #
###############
@pytest.mark.associations
def test_ccc_constellation_association(app, test_corpus):

    assoc = ccc_constellation_association(
        corpus_name=test_corpus['corpus_name'],
        cqp_bin=app.config['CCC_CQP_BIN'],
        registry_path=app.config['CCC_REGISTRY_PATH'],
        data_path=app.config['CCC_DATA_PATH'],
        lib_path=app.config['CCC_LIB_PATH'],
        discoursemes=test_corpus['discoursemes2'],
        p_query=test_corpus['parameters']['p_query'],
        s_query=test_corpus['parameters']['s_query'],
        s_context=test_corpus['parameters']['s_context']
    )
    print(assoc)
