<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <h1>Mixed Method Discourse Analysis</h1>

      <p>{{ $t("index.paragraph1") }}</p>

      <v-parallax src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-parallax>

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
