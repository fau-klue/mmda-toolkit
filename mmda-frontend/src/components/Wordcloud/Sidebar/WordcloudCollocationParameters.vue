<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Collocation Parameters</div>
  <v-card v-if="notMini">
    <v-card-text>
      <v-slider v-model="selectWindow" :max="analysis.window_size" :min="min" thumb-label="always" 
      thumb-size="28" @change="setSize"
      label="Window Size"></v-slider>
      
      <v-layout row wrap>
          <v-flex xs12>
            <v-radio-group v-model="am_value" @change="setAM">
              <v-layout row wrap justify-space-between>
                <v-radio v-for="am in Object.keys(collocates)" :key="am"
                  :label="am"
                  :value="am"
                ></v-radio>
              </v-layout>
            </v-radio-group>
          </v-flex>
      </v-layout>

      <v-checkbox v-model="compare" label="compare to"></v-checkbox>
      <v-slider v-if="compare" v-model="selectWindow2" :max="analysis.window_size" :min="min" thumb-label="always" 
        thumb-size="28" @change="setSize2"
        color="secondary"
        label="Window Size"></v-slider>
      
      <v-layout v-if="compare" row wrap>
          <v-flex xs12>
            <v-radio-group v-model="am_value2" @change="setAM2">
              <v-layout row wrap justify-space-between>
                <v-radio v-for="am in Object.keys(collocates)" :key="am"
                  color="secondary"
                  :label="am"
                  :value="am"
                ></v-radio>
              </v-layout>
            </v-radio-group>
          </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'WordcloudCollocationParameters',
  data: () => ({
    compare: false,
    min: 2,
    am_value: null,
    am_value2: null,
    selectWindow: 3,
    selectWindow2: 3,
  }),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: 'analysis/analysis',
      collocates: "analysis/collocates",
      notMini:   'wordcloud/rightSidebar',
      windowSize: 'wordcloud/windowSize',
      //windowSize2: 'wordcloud/windowSizeCompare',
      AM: 'wordcloud/associationMeasure',
      //AM2: 'wordcloud/associationMeasureCompare',
    })
  },
  methods: {
    ...mapActions({
      setWindowSize: 'wordcloud/setWindowSize',
      //setWindowSize2: 'wordcloud/setWindowSizeCompare',
      _setAM : 'wordcloud/setAssociationMeasure',
      //_setAM2 : 'wordcloud/setAssociationMeasureCompare'
    }),
    setSize () {
      this.setWindowSize(this.selectWindow)
    },
    setSize2 () {
      //this.setWindowSize2(this.selectWindow2);
    },
    setAM (){
      this._setAM(this.am_value);
    },
    setAM2 (){
      //this._setAM2(this.am_value2);
    }
  },
  mounted () {
    //TODO:: update this once it changed ??
    this.am_value = this.AM;
    this.selectWindow = this.windowSize;
  }
}
</script>

<style>

</style>
