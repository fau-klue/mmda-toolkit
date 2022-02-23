<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <CollocationHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <CollocationContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import CollocationHeader from '@/components/Collocation/CollocationHeader.vue'
import CollocationContent from '@/components/Collocation/CollocationContent.vue'

export default {
  name: 'CollocationView',
  components: {
    CollocationHeader,
    CollocationContent
  }
}

</script>
