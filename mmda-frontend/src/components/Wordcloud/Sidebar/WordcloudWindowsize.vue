<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Window Size</div>
  <v-card v-if="notMini">
    <v-card-text>
      <v-slider v-model="selectWindow" :max="analysis.context" :min="min" thumb-label="always" thumb-size="28" @change="setSize"></v-slider>
    </v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'WordcloudWindowsize',
  data: () => ({
    min: 2,
    selectWindow: 3
  }),
  computed: {
    ...mapGetters({
      analysis: 'analysis/analysis',
      windowSize: 'wordcloud/windowSize',
      notMini:   'wordcloud/rightSidebar'
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
