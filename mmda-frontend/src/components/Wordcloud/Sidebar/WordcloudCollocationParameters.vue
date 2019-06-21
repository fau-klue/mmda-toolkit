<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Collocation Parameters</div>
  <v-card v-if="notMini">
    <v-card-text>
      <h3 class="body-2">Window Size</h3>
      <v-slider v-model="selectWindow" :max="analysis.max_window_size" :min="min" thumb-label="always"
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
      
      <v-layout class="my-4" row wrap>
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
            <v-checkbox v-for="discourseme in analysisDiscoursemes" :key="discourseme.id"
              v-model="secondOrderIDs"
              @change="setSOC"
              :label="discourseme.name"
              :value="discourseme.id"
              :title="'['+discourseme.items+']'"
              hide-details
              ></v-checkbox>
            <v-btn color="info" class="my-3 text-lg-right" @click="clearSOC">Topic Only</v-btn>
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
      <v-layout v-if="compare" row wrap class="my-3">
        <h3 class="my-3 body-2">Compare Collocations</h3>
          <v-flex xs12>
            <v-btn color="info" class="text-lg-right" title="Store above settings as reference." @click="storeCompare">Set Reference</v-btn>
            <!-- TODO:: format nicely-->
            <p v-if="collocatesCompare">
              Reference is {{collocatesCompare.am}} 
              in window-size {{collocatesCompare.ws}}.
            </p>
            <p v-if="collocatesCompare && collocatesCompare.discoursemes && collocatesCompare.discoursemes.length">
              With discourseme(s) {{collocatesCompare.discoursemes}}.
            </p>
            <v-list v-if="collocatesCompare">
              <v-list-tile>
                <v-list-tile-avatar>
                  <span style="font-size:200%;text-shadow:0.05rem 0.1rem 0.02rem black;color:goldenrod">⭑</span>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>not in reference</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile> 
              <v-list-tile>
                <v-list-tile-avatar>
                  <span style="text-decoration: line-through; color: #0006;">item</span>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>only in reference</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>  
              <v-list-tile>
                <v-list-tile-avatar>
                  <span style="font-size:100%;text-shadow:0.05rem 0.1rem 0.02rem black;color:forestgreen">⯅</span>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title title="more important than reference">more important</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile> 
              <v-list-tile>
                <v-list-tile-avatar>
                  <span style="font-size:100%;text-shadow:0.05rem 0.1rem 0.02rem black;color:darkred">⯆</span>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title title="less important than reference">less important</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile> 
            </v-list>
            <v-btn v-if="collocatesCompare" color="info" outline class="text-lg-right" @click="clearCompare">Stop Comparison</v-btn>
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
    compare: true,
    min: 2,
    am_value: null,
    am_value2: null,
    selectWindow: 3,
    selectWindow2: 3,
    secondOrderIDs:[],
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
      analysis: 'analysis/analysis',
      collocates: "analysis/collocates",
      notMini:   'wordcloud/rightSidebar',
      windowSize: 'wordcloud/windowSize',
      AM: 'wordcloud/associationMeasure',
      analysisDiscoursemes: 'analysis/discoursemes',
      SOC: 'wordcloud/secondOrderCollocationDiscoursemeIDs',
      collocatesCompare: 'wordcloud/collocatesToCompare',
    })
    /*,SOC_items(){
      var res = new Set();
      for(var id of this.SOC){
        var i = this.analysisDiscoursemes.findIndex((d)=>d.id==id);
        if(i!=-1){
          for(var it of this.analysisDiscoursemes[i].items ) res.add(it);
        }
      }
      console.log(Array.from(res));
      return Array.from(res);
    }*/
  },
  methods: {
    ...mapActions({
      setWindowSize: 'wordcloud/setWindowSize',
      _setAM : 'wordcloud/setAssociationMeasure',
      _setSOC : 'wordcloud/setSecondOrderCollocationDiscoursemeIDs',
    //  getSOCs: 'analysis/getAnalysisDiscoursemeCollocates',
      getCollocates: 'analysis/getAnalysisCollocates',
      setCompare:'wordcloud/setCollocatesToCompare',
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
      //this.requestSecondOrderCollocates();
      //console.log("Second order collocation with Discourseme ID:"+this.secondOrderIDs);
    },
    /*requestSecondOrderCollocates(){  //THIS is already done by WCContent
      let data = {
        username: this.user.username,
        analysis_id: this.analysis.id,
        window_size: this.windowSize,
        discourseme_items: this.SOC_items
      };
      if( this.SOC.length > 0 ){
        this.getSOCs(data).then((result)=>{
          this.error = null;

          //TODO:: if there are new collocates without position, 
          // -  fetch coordinates
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
    },*/
    SOCNames(){
      var result = "";
      var i = 0;
      for(var id of this.SOC){
        for(var d of this.analysisDiscoursemes){
          if(d.id == id){
            result += d.name;
            break;
          }
        }

        if(i<this.SOC.length-2){
          result+=", ";
        }else if(i==this.SOC.length-2){
          result+=" and ";
        }
        i++;
      }
      return result;
    },
    storeCompare(){
      this.setCompare({collocates:this.collocates, am:this.AM, ws:this.windowSize, discoursemes:this.SOCNames()});
    },
    clearCompare(){
      this.setCompare(null);
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
