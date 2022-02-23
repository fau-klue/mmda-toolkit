<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Metadata</div>
  <v-card v-if="notMini">
    <v-card-text>{{ collocation }}</v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'WordcloudMetadata',
  data: () => ({
  }),
  computed: {
    ...mapGetters({
      collocation: 'collocation/collocation',
      notMini: "wordcloud/rightSidebar"
    })
  }
}
</script>

<style>

</style>
