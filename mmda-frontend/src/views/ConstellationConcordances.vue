<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <ConstellationHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <ConstellationConcordancesExtraction/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import ConstellationHeader from '@/components/Constellation/ConstellationHeader.vue'
import ConstellationConcordancesExtraction from '@/components/Constellation/ConstellationConcordances.vue'

export default {
  name: 'Constellation',
  components: {
    ConstellationHeader,
    ConstellationConcordancesExtraction
  },
}

</script>
