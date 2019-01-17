<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <DiscursivePositionNewContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import DiscursivePositionNewContent from '@/components/DiscursivePosition/DiscursivePositionNew.vue'

export default {
  name: 'DiscursivePositionNew',
  components: {
    DiscursivePositionNewContent
  }
}

</script>
