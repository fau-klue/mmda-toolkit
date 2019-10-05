<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>

      <h1>{{ $t("about.headline") }}</h1>
      <p/>
      <h2>{{ $t("about.headline1") }}</h2>
      <p>{{ $t("about.paragraph1_1") }}</p>
      <h3>{{ $t("about.headline1_1") }}</h3>
      <p>{{ $t("about.paragraph1_2") }}</p>
      <p>{{ $t("about.paragraph1_3") }}</p>
      <p>{{ $t("about.paragraph1_4") }}</p>

      <h3>{{ $t("about.headline2") }}</h3>
      <p>{{ $t("about.paragraph2_1") }}</p>
      <p>{{ $t("about.paragraph2_2") }}</p>
      <p>{{ $t("about.paragraph2_3") }}</p>

      <h3>{{ $t("about.headline3") }}</h3>
      <p>{{ $t("about.paragraph3_1") }}</p>
      <p>{{ $t("about.paragraph3_2") }}</p>

    </v-flex>
  </v-layout>
</v-container>
</template>

<script>

export default {
  name: 'About'
}

</script>
