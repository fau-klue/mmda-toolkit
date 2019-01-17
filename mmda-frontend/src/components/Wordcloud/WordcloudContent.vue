<template>
<v-container grid-list-md>
  <v-layout row wrap>
    <v-flex xs12>
      <h1>Super WordCloud</h1>
      <p>
        {{ analysis }}
      </p>
      <p>
        {{ coordinates }}
      </p>
      <p>
        {{ concordances }}
      </p>
      <p>
        {{ collocates }}
      </p>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import rules from '@/utils/validation'

export default {
  name: 'WordcloudContent',
  components: {
  },
  data: () => ({
    id: null,
    rules: rules
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      discoursemes: 'analysis/discoursemes',
      collocates: 'analysis/collocates',
      coordinates: 'coordinates/coordinates',
      concordances: 'corpus/concordances'
    })
  },
  methods: {
    ...mapActions({
      getConcordances: 'corpus/getConcordances',
      getCollocates: 'analysis/getAnalysisCollocates'
    }),
    fetchCollocates (window_size) {
      const request = {
        params: {'window_size': window_size}
      }

      const data = {
        username: this.user.username,
        analysis_id: this.id,
        request: request
      }

      this.getCollocates(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    fetchConcordances (items) {

      let params = new URLSearchParams()
      // Concat item parameter
      items.forEach(function(item) {
        params.append('item', item)
      })

      const request = {
        params: params
      }

      const data = {
        corpus: this.analysis.corpus,
        request: request
      }

      this.getConcordances(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.id = this.$route.params.id
    this.fetchConcordances(['test', 'anothertest'])
    this.fetchCollocates(3)
  }
}

</script>
