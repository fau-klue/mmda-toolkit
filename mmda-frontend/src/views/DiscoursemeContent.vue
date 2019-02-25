<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscoursemeHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscoursemeContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import DiscoursemeHeader from '@/components/Discourseme/DiscoursemeHeader.vue'
import DiscoursemeContent from '@/components/Discourseme/DiscoursemeContent.vue'

export default {
  name: 'DiscoursemeView',
  components: {
    DiscoursemeHeader,
    DiscoursemeContent
  }
}

</script>
