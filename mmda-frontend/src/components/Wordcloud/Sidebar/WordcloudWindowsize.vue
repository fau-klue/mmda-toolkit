<template>
<v-expansion-panel-content>
  <div slot="header" v-if="!mini" >Window Size</div>
  <v-card v-if="!mini">
    <v-card-text>
      <v-slider v-model="selectWindow" :max="max" :min="min" thumb-label="always" thumb-size="28"></v-slider>
    </v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'WordcloudWindowsize',
  props: ['mini'],
  data: () => ({
    min: 2,
    max: 20,
    selectedWindow: 2
  }),
  computed: {
    ...mapGetters({
      analysis: 'analysis/analysis'
    })
  }
}
</script>

<style>

</style>
