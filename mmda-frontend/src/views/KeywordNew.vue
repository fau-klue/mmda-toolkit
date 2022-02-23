<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <KeywordNewContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import KeywordNewContent from '@/components/Keyword/KeywordNew.vue'

export default {
  name: 'KeywordNew',
  components: {
    KeywordNewContent
  }
}

</script>
