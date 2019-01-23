<template>
<v-expansion-panel-content>
  <div slot="header" v-if="!mini" >Window Size</div>
  <v-card v-if="!mini">
    <v-card-text>
      <v-slider v-model="selectWindow" :max="analysis.window_size" :min="min" thumb-label="always" thumb-size="28" @change="setSize"></v-slider>
    </v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'WordcloudWindowsize',
  props: ['mini'],
  data: () => ({
    min: 2,
    selectWindow: 3
  }),
  computed: {
    ...mapGetters({
      analysis: 'analysis/analysis',
      windowSize: 'wordcloud/windowSize',
    })
  },
  methods: {
    ...mapActions({
      setWindowSize: 'wordcloud/setWindowSize'
    }),
    setSize () {
      this.setWindowSize(this.selectWindow)
    }
  }
}
</script>

<style>

</style>
