<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <DiscursivePositionHeader/>
    </v-flex>
    <v-flex xs12>
      <DiscursivePositionList/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import DiscursivePositionHeader from '@/components/DiscursivePosition/DiscursivePositionHeader.vue'
import DiscursivePositionList from '@/components/DiscursivePosition/DiscursivePositionList.vue'

export default {
  name: 'DiscursivePosition',
  components: {
    DiscursivePositionHeader,
    DiscursivePositionList
  },
}

</script>
