<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <h2>{{ $t("index.headline1") }}</h2>

      <p>{{ $t("index.paragraph1") }}</p>

      <p>
        <v-parallax src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-parallax>
      </p>

      <p>{{ $t("index.paragraph2") }}</p>

      <p>{{ $t("index.paragraph3") }}</p>

    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
export default {
  name: 'Index'
}
</script>
