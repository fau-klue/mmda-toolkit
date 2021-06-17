<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <h2>{{ $t("index.headline1") }}</h2>
      <p>{{ $t("index.paragraph1") }}</p>
      <p>{{ $t("index.paragraph2") }}</p>
      <p> <v-img src= "mmda-in-action.png"></v-img> </p>
      <p>{{ $t("index.paragraph3") }}</p>
      <!-- <p>{{ $t("index.paragraph4") }}</p> -->
      <p>See the <a href="/mmda/about">Vignette</a> for further info or start with an <a href="/mmda/analysis/new">Analysis</a>.

      <h4>{{ $t("index.headlineAcknowledgements") }}</h4>
      <p>{{ $t("index.Acknowledgements") }}</p>

      <h4>Developers</h4>
      <p><a href="https://linguistik.uni-erlangen.de/projects/efe/team">EFE project group</a>, FAU Erlangen-Nürnberg</p>

      <!-- <h3>{{ $t("index.headlinePublications") }}</h3> -->
      <!-- <p> -->
        <!--   <ul> -->
      <!--     <li>Evert, Stefan and Philipp Heinrich (2019). Introducing MMDA: An interactive toolkit for CDA. 7th Göttingen/Hildesheim-Workshop on CL and DH.</li> -->
      <!--     <li>Heinrich, Philipp and Fabian Schäfer (2018). Extending Corpus-Based Discourse Analysis for Exploring Japanese Social Media. Proceedings of 4th Asia Pacific Corpus Linguistics Conference (APCLC2018), pages 135–140. Takamatsu, Japan.</li> -->
      <!--     <li>Heinrich, Philipp, Christoph Adrian, Olena Kalashnikova, Fabian Schäfer, and Stefan Evert (2018). A Transnational Analysis of News and Tweets about Nuclear Phase-Out in the Aftermath of the Fukushima Incident. In Proceedings of the LREC 2018 “Workshop on Computational Impact Detection from Text Data” (CIDTD 2018), pages 8–16. Miyazaki, Japan.</li> -->
      <!--   </ul> -->
      <!-- </p> -->
      
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
export default {
  name: 'Index'
}
</script>
