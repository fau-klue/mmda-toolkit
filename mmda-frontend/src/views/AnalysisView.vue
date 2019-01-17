<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <AnalysisHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <AnalysisContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import AnalysisHeader from '@/components/Analysis/AnalysisHeader.vue'
import AnalysisContent from '@/components/Analysis/AnalysisContent.vue'

export default {
  name: 'AnalysisView',
  components: {
    AnalysisHeader,
    AnalysisContent
  }
}

</script>
