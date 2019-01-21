<template>
<div>
  <v-container grid-list-md>
    <v-layout row wrap>
      <v-flex xs12>
        <p>
          Window Size {{ windowSize }}
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
  <WordcloudSidebar/>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
// import { finished } from 'stream'
// import { WordcloudWindow } from '@/wordcloud/wordcloud.js'
import rules from '@/utils/validation'
import WordcloudSidebar from '@/components/Wordcloud/WordcloudSidebar'
import styles from '@/wordcloud/wordcloud.module.css' // eslint-disable-line no-unused-vars

export default {
  name: 'WordcloudContent',
  components: {
    WordcloudSidebar
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
      concordances: 'corpus/concordances',
      windowSize: 'wordcloud/windowSize'
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
  },
  mounted () {
    // let WW = []
    // for (let A of document.getElementsByClassName(
    //   'structured_wordcloud_container'
    // )) {
    //   let W
    //   WW.push((W = new WordcloudWindow(A)))
    //   window.addEventListener('resize', (W => () => W.resize())(W))
    //   W.setupContent()
    // }
  }
}

</script>
