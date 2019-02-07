<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <h2>{{ $t("about.headline1") }}</h2>
      <p>{{ $t("about.paragraph1_1") }}</p>
      <p>{{ $t("about.paragraph1_2") }}</p>

      <h3>{{ $t("about.headline2") }}</h3>
      <p>{{ $t("about.paragraph2_1") }}</p>
      <p>{{ $t("about.paragraph2_2") }}</p>

      <h3>{{ $t("about.headline3") }}</h3>
      <p>{{ $t("about.paragraph3_1") }}</p>
      <p>{{ $t("about.paragraph3_2") }}</p>

      <h3>{{ $t("about.headline4") }}</h3>
      <p>{{ $t("about.paragraph4_1") }}</p>

      <h2>{{ $t("about.headlinePublications") }}</h2>
      <ul>
        <li>2018. A Transnational Analysis of News and Tweets about Nuclear Phase-Outin the Aftermath of the Fukushima Incident</li>
      </ul>

    </v-flex>
  </v-layout>
</v-container>
</template>

<script>

export default {
  name: 'About'
}

</script>
