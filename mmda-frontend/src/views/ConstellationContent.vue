<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <ConstellationHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <ConstellationContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import ConstellationHeader from '@/components/Constellation/ConstellationHeader.vue'
import ConstellationContent from '@/components/Constellation/ConstellationContent.vue'

export default {
  name: 'ConstellationView',
  components: {
    ConstellationHeader,
    ConstellationContent
  }
}

</script>
