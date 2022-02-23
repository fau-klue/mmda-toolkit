<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>

      <h1>{{ $t("about.headline") }}</h1>
      <p/>

      <h3>{{ $t("about.headline1") }}</h3>
      <p>{{ $t("about.paragraph1_1") }}</p>

      <h3>Discoursemes and their Constellations</h3>
      <p>We call any set of words formed by the analyst a <b>discourseme</b> – they are the building blocks of CDA. Theoretically speaking, a discourseme is a disjunction of related lexical items. On its surface, it represents a simple list of words or words, which the researcher decided that belong together. The list of topic nodes form a special discourseme – the topic discourseme.</p>
      <p>CDA researchers are typically interested in constellations of discoursemes: e.g. a topic discourseme <i>nuclear energy</i> and a further discourseme capturing an attitude or perspective towards the topic, such as its <i>risks</i> or its <i>potential</i>. </p>

      <h3>Creating a Discourseme Collocation Analysis</h3>
      <p>{{ $t("about.paragraph1_2") }}</p>
      <p>{{ $t("about.paragraph1_3") }}</p>
      <h3>Inspecting Analysis Results</h3>
      <p>{{ $t("about.paragraph2_1") }}</p>

      <h3>The Semantic Map</h3>
      <p>{{ $t("about.paragraph2_2") }}</p>

      <p>{{ $t("about.paragraph3_2") }}</p>

      <h3>{{ $t("about.headline4") }}</h3>
      <p>{{ $t("about.paragraph4_1") }}</p>

    </v-flex>
  </v-layout>
</v-container>
</template>

<script>

export default {
  name: 'About'
}

</script>
