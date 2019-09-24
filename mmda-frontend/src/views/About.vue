<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>

      <h3>{{ $t("about.headline2") }}</h3>
      <p>{{ $t("about.paragraph2_1") }}</p>
      <p>{{ $t("about.paragraph2_2") }}</p>

      <h3>{{ $t("about.headline3") }}</h3>
      <p>{{ $t("about.paragraph3_1") }}</p>
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
