<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Keyness Parameters</div>
  <v-card v-if="notMini">
    <v-card-text>
      <v-layout row wrap>
        <h3 class="body-2">Association Measure</h3>
          <v-flex xs12>
            <v-select :items="Object.keys(collocates)" v-model="am_value" @change="setAM"></v-select>
          </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'WordcloudKeywordCollocationParameters',
  data: () => ({
    min: 2,
    am_value: null,
    selectWindow: 3,
  }),
  watch:{
    AM(){
      this.am_value = this.AM;
    },
    windowSize(){
      this.selectWindow = this.windowSize;
    }
  },
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: 'keyword/keyword',
      collocates: "keyword/keywords",
      notMini:   'wordcloud/rightSidebar',
      windowSize: 'wordcloud/windowSize',
      AM: 'wordcloud/associationMeasure',
    })
  },
  methods: {
    ...mapActions({
      _setAM : 'wordcloud/setAssociationMeasure',
    }),
    setSize () {
      this.setWindowSize(this.selectWindow)
    },
    setAM (){
      this._setAM(this.am_value);
    },
  },
  mounted () {
    this.am_value = this.AM;
    this.selectWindow = this.windowSize;
  }
}
</script>

<style>

</style>
