<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscoursemeHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscoursemeList/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import DiscoursemeHeader from '@/components/Discourseme/DiscoursemeHeader.vue'
import DiscoursemeList from '@/components/Discourseme/DiscoursemeList.vue'

export default {
  name: 'Discourseme',
  components: {
    DiscoursemeList,
    DiscoursemeHeader
  }
}

</script>
