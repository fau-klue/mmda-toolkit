<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <KeywordHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <KeywordList/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import KeywordHeader from '@/components/Keyword/KeywordHeader.vue'
import KeywordList from '@/components/Keyword/KeywordList.vue'

export default {
  name: 'Keyword',
  components: {
    KeywordHeader,
    KeywordList
  },
  data: () => ({
  })
}

</script>
