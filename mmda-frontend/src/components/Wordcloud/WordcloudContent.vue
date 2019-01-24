<template>
  <div >
    <div class="structured_wordcloud_container"></div>

<!--
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
  -->
  <WordcloudSidebar/>
</div>
</template>

<style>
@import '../../wordcloud/wordcloud.module.css';
</style>

<script>
import { mapActions, mapGetters } from 'vuex'
import { WordcloudWindow } from '@/wordcloud/wordcloud.js'
import rules from '@/utils/validation'
import WordcloudSidebar from '@/components/Wordcloud/WordcloudSidebar'
import * as data from '@/wordcloud/example_1.js'

export default {
  name: 'WordcloudContent',
  components: {
    WordcloudSidebar
  },
  data: () => ({
    id: null,
    rules: rules,
    wc: null,
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
        if(this.wc) this.wc.setupContent2(this.collocates, this.coordinates, this.discoursemes);
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
    //this.fetchConcordances(['test', 'anothertest'])
    this.fetchCollocates(3)
  },
  mounted () {
    
    let WW = []
    for (let A of document.getElementsByClassName(
      'structured_wordcloud_container'
    )) {
      WW.push((this.wc = new WordcloudWindow(A)))
      window.addEventListener('resize', (W => () => W.resize())(this.wc))
      //wc.setupContent2(this.collocates, this.coordinates, this.discoursemes);
      break;
    }
  }
}

</script>