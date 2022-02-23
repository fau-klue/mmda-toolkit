<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <KeywordHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <KeywordContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import KeywordHeader from '@/components/Keyword/KeywordHeader.vue'
import KeywordContent from '@/components/Keyword/KeywordContent.vue'

export default {
  name: 'KeywordView',
  components: {
    KeywordHeader,
    KeywordContent
  }
}

</script>
