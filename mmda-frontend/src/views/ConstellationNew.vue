<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <ConstellationNewContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import ConstellationNewContent from '@/components/Constellation/ConstellationNew.vue'

export default {
  name: 'ConstellationNew',
  components: {
    ConstellationNewContent
  }
}

</script>
