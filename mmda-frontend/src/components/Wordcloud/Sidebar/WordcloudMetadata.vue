<template>
<v-expansion-panel-content>
  <div slot="header" v-if="!mini" >Metadata</div>
  <v-card v-if="!mini">
    <v-card-text>{{ analysis }}</v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'WordcloudMetadata',
  props: ['mini'],
  data: () => ({
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
