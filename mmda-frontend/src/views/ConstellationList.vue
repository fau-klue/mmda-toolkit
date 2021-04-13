<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <ConstellationHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <ConstellationList/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import ConstellationHeader from '@/components/Constellation/ConstellationHeader.vue'
import ConstellationList from '@/components/Constellation/ConstellationList.vue'

export default {
  name: 'Constellation',
  components: {
    ConstellationHeader,
    ConstellationList
  },
}

</script>
