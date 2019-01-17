<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <AnalysisNewContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import AnalysisNewContent from '@/components/Analysis/AnalysisNew.vue'

export default {
  name: 'AnalysisNew',
  components: {
    AnalysisNewContent
  }
}

</script>
