<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Collocation Parameters</div>
  <v-card v-if="notMini">
    <v-card-text>
      <h3 class="body-2">Window Size</h3>
      <v-slider v-model="selectWindow" :max="analysis.window_size" :min="min" thumb-label="always"
      thumb-size="28" @change="setSize"></v-slider>

      <v-layout row wrap>
        <h3 class="body-2">Association Measure</h3>
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
      
      <v-layout row wrap>
        <h3 class="body-2">Second Order Collocation with:</h3>
        <v-flex xs12 sm4 md4>
          <!-- <v-radio-group v-model="secondOrderID" @change="setSOC">
            <v-radio
              :label="'Topic Only'"
              :value="-1"
              ></v-radio>
            <v-radio v-for="discourseme in analysisDiscoursemes" :key="discourseme.id"
              :label="discourseme.name"
              :value="discourseme.id"
              ></v-radio>
          </v-radio-group> -->
            <v-btn color="info" class="text-lg-right" @click="clearSOC">Topic Only</v-btn>
            <v-checkbox v-for="discourseme in analysisDiscoursemes" :key="discourseme.id"
              v-model="secondOrderIDs"
              @change="setSOC"
              :label="discourseme.name"
              :value="discourseme.id"
              :title="'['+discourseme.items+']'"
              hide-details
              ></v-checkbox>
        </v-flex>
       <!-- <v-list two-line subheader>
          <v-list-tile avatar>
            <v-list-tile-avatar>
              <v-btn icon ripple selected>
                <v-icon class="grey--text text--lighten-1">subject</v-icon>
              </v-btn>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>Topic Only</v-list-tile-title>
              <v-list-tile-sub-title>{{ analysis.topic_items }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
          <h3 class="body-1">Discourseme</h3>
          <v-list-tile v-for="discourseme in analysisDiscoursemes" :key="discourseme.id" avatar>
            <v-list-tile-avatar>
              <v-btn icon ripple :to="/discourseme/ + discourseme.id">
                <v-icon class="grey--text text--lighten-1">subject</v-icon>
              </v-btn>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ discourseme.name }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ discourseme.items }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>  -->
      </v-layout>
      <v-layout v-if="compare" row wrap>
        <h3 class="body-2">Compare Collocations</h3>
          <v-flex xs12>
        <v-btn color="info" class="text-lg-right" @click="storeCompare">Store Settings to compare with</v-btn>
        <v-btn color="error" outline class="text-lg-right" @click="clearCompare">Stop Comparison</v-btn>
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
    secondOrderIDs:[],
  }),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: 'analysis/analysis',
      collocates: "analysis/collocates",
      notMini:   'wordcloud/rightSidebar',
      windowSize: 'wordcloud/windowSize',
      AM: 'wordcloud/associationMeasure',
      analysisDiscoursemes: 'analysis/discoursemes',
      SOC: 'wordcloud/secondOrderCollocationDiscoursemeIDs',
    })
  },
  methods: {
    ...mapActions({
      setWindowSize: 'wordcloud/setWindowSize',
      _setAM : 'wordcloud/setAssociationMeasure',
      _setSOC : 'wordcloud/setSecondOrderCollocationDiscoursemeIDs',
      getSOCs: 'analysis/getAnalysisDisoursemeCollocates',
      getCollocates: 'analysis/getAnalysisCollocates'
    }),
    setSize () {
      this.setWindowSize(this.selectWindow)
    },
    setAM (){
      this._setAM(this.am_value);
    },
    clearSOC(){
      this.secondOrderIDs=[];
      this.setSOC();
    },
    setSOC(){
      this._setSOC(this.secondOrderIDs);
      this.requestSecondOrderCollocates();
      //console.log("Second order collocation with Discourseme ID:"+this.secondOrderIDs);
    },
    requestSecondOrderCollocates(){
      let data = {
        username: this.user.username,
        analysis_id: this.analysis.id,
        window_size: this.windowSize,
        discourseme_ids: this.SOC
      };
      if(this.SOC.length>0){
        this.getSOCs(data).then((result)=>{
          this.error = null;
        }).catch((error)=>{
          this.error = error;
        });
      }else{
        this.getCollocates(data).then((result)=>{
          this.error = null;
        }).catch((error)=>{
          this.error = error;
        });
      }
    },
    storeCompare(){
      //TODO:: store parameters (or collocation values) for later comparison
    },
    clearCompare(){
      //TODO:: clear comparation storage/ disable comparison
    }
  },
  mounted () {
    //TODO:: update this once it changed ??
    this.am_value = this.AM;
    this.selectWindow = this.windowSize;
    this.secondOrderIDs = this.SOC;
  }
}
</script>

<style>

</style>
