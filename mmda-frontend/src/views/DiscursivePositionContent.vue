<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscursivePositionHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscursivePositionContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import DiscursivePositionHeader from '@/components/DiscursivePosition/DiscursivePositionHeader.vue'
import DiscursivePositionContent from '@/components/DiscursivePosition/DiscursivePositionContent.vue'

export default {
  name: 'DiscursivePositionView',
  components: {
    DiscursivePositionHeader,
    DiscursivePositionContent
  }
}

</script>
