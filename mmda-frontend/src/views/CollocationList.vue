<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <CollocationHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <CollocationList/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import CollocationHeader from '@/components/Collocation/CollocationHeader.vue'
import CollocationList from '@/components/Collocation/CollocationList.vue'

export default {
  name: 'Collocation',
  components: {
    CollocationList,
    CollocationHeader
  },
  data: () => ({
  })
}

</script>
