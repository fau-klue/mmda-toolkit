<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <AnalysisHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <AnalysisList/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import AnalysisHeader from '@/components/Analysis/AnalysisHeader.vue'
import AnalysisList from '@/components/Analysis/AnalysisList.vue'

export default {
  name: 'Analysis',
  components: {
    AnalysisList,
    AnalysisHeader
  },
  data: () => ({
  })
}

</script>
