<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <DiscoursemeNewContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import DiscoursemeNewContent from '@/components/Discourseme/DiscoursemeNew.vue'

export default {
  name: 'DiscoursemeNew',
  components: {
    DiscoursemeNewContent
  }
}

</script>
