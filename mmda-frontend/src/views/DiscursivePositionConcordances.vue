<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscursivePositionHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscursivePositionConcordancesExtraction/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import DiscursivePositionHeader from '@/components/DiscursivePosition/DiscursivePositionHeader.vue'
import DiscursivePositionConcordancesExtraction from '@/components/DiscursivePosition/DiscursivePositionConcordances.vue'

export default {
  name: 'DiscursivePosition',
  components: {
    DiscursivePositionHeader,
    DiscursivePositionConcordancesExtraction
  },
}

</script>
