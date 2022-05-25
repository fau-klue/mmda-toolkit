<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>

      <h1>MMDA toolkit Vignette</h1>
      <p/>

      <h3>Prerequisites and Background</h3>
      <p>The MMDA toolkit can be used in a specialized way to
        <ul>
          <li> query corpora using the Corpus Query Processor (CQP) of the IMS Open Corpus Workbench (CWB),</li>
          <li> to visualize keywords and collocation profiles via semantic maps,</li>
          <li>to create and store discoursemes (see below) in a consistent database, and</li>
          <li>to analyze discourseme constellations.</li>
        </ul>
        In principle, any corpus indexed with the CWB can be imported in the toolkit.  For all visualzations, word embeddings of the respective token-layer (for the given language and register) must be at hand.</p>

      <h3>Discoursemes and their Constellations</h3>
      <p>We call any set of words formed by the analyst a <b>discourseme</b> – they are the building blocks of CDA. In a simple setting, a discourseme is a disjunction of related lexical items, i.e. a set of words that the researcher decided that belong together. CDA researchers are typically interested in <b>constellations</b> of discoursemes: e.g. a topic discourseme <i>nuclear energy</i> and a further discourseme capturing an attitude or perspective towards the topic, such as its <i>risks</i> or its <i>potential</i>. </p>

      <h3>Collocation Analysis</h3>
      <p>A typical starting point of CDA is a <b>topic node</b>: a set of tokens or multi-token units on any positional annotation layer of the corpus. The available layers depend on the actual linguistic annotation of the corpus at hand, but for most corpora the two layers <i>word</i> and <i>lemma</i> should be available. A typical topic node is made up semantically similar lexical items such as <i>erneuerbare Energie</i>, <i>Windenergie</i>, <i>Solarenergie</i>, and <i>Wasserkraft</i>. Such discoursemes are a way to capture a specific topic you are interested in. For a topic in the sense of CDA, it is reasonable to query on the lemma layer, i.e. to set <i>p-query</i> and <i>p-collocation</i> to <i>lemma</i> in the <i>New Collocation Analysis</i> pane.</p>
      <p>The <i>context</i> and <i>context break</i> parameters determine the windows around the retrieved topic nodes that will be highlighted in concordance views and which will be used to determine the domain of collocate candidates. For most corpora, sentences (<i>s</i>) should be used as break points. Newspaper texts might also contain <i>article</i>' or <i>p</i>aragraphs; CMC data might contain <i>post</i> or alike; the most generic s-break value is <i>text</i>. Typical values for the window size are 3 to 10, although some researchers might be interested in values as low as 1 (essentially looking for trigrams), others in window sizes of 10 and above, looking for patterns across lexical items far away from one another.</p>

      <h3>Keyword Analysis</h3>
      <p>Another starting point for CDA research are keyword analyses: in this case, researchers are interested in the lexical items that are prominent in one (sub-)corpus compared to another.  The keywords are again grouped into discoursemes, which are intended to capture the semantic groups that are indicative for the corpus at hand.</p>

      <h3>Inspecting Analysis Results</h3>
      <p>The immediate result of such analyses is a summarization of the cotext of the topic node (or the corpus, respectively):
        <ul>
          <li>you can see the frequency breakdown of the query for collocation analyses,</li>
          <li>the associated discoursemes pane lets you associate discoursemes with the analysis, so that they are visualized in the semantic map and in concordance lines,</li>
          <li>the concordance lines show the query matches or discoursemes in KWIC view, and</li>
          <li>the collocation or keyword table presents the association candidates.</li>
          <!-- <li>the meta pain shows you the distribution of the matches across all annotated s-attributes.</li> -->
        </ul>
      </p>

      <h3>The Semantic Map</h3>
      <p>You can display a semantic map of the association candidates in the collocation and keyword tables. The initial map is a straightforward visualization: it uses a stochastic dimensionality reduction algorithm to place the lexical items in a semantically structured two-dimensional plane (especially trying to place semantically similar items next to one another). The size of each lexical item represents the association strength of the item with the topic node (or the corpus, respectively). The appearance of the semantic map can be changed by tweaking the association parameters.</p>

      <p>The semantic map is <i>interactive</i>, meaning that lexical items can be grouped together via drag & drop to form additional discoursemes. The map can also display second-order collocates of a selected discourseme in the same semantic map, i.e. lexical items that are highly associated with the co-occurrence of the topic discourseme and the selected discourseme. Clicking on items in the semantic cloud retrieves relevant concordances.</p>

      <h3>Forming Constellations</h3>
      <p>The easiest discourseme constellation that can be formed consists of a topic discourseme and one further a group of collocates. Such a constellation consists of the topic (realized by the topic discourseme) and a certain perspective that can be taken towards that topic (realized by the second discourseme). After creating a constellation, you can inspect pairwise textual associations and actual concordance lines of the constellation across corpora.</p>

    </v-flex>
  </v-layout>
</v-container>
</template>

<script>

export default {
  name: 'About'
}

</script>
