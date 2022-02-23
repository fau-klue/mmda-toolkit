<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <CollocationNewContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import CollocationNewContent from '@/components/Collocation/CollocationNew.vue'

export default {
  name: 'CollocationNew',
  components: {
    CollocationNewContent
  }
}

</script>
