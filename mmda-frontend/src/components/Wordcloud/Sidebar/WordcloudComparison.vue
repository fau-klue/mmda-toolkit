<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Comparison</div>
  <v-card v-if="notMini">
    <v-card-text>
      <v-layout v-if="compare" row wrap class="my-3">
        Lock current collocation parameters (including second-order settings) as reference.
          <v-flex xs12>
            <v-btn color="info" class="text-lg-right" title="Store above settings as reference." @click="storeCompare">Lock Reference</v-btn>
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
            <v-btn v-if="collocatesCompare" color="info" outline class="text-lg-right" @click="clearCompare">Unlock Reference</v-btn>
          </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'WordcloudComparison',
  data: () => ({
    use_second_order_collocation:true,
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
      collocation: 'collocation/collocation',
      collocates: "collocation/collocates",
      notMini:   'wordcloud/rightSidebar',
      windowSize: 'wordcloud/windowSize',
      AM: 'wordcloud/associationMeasure',
      collocationDiscoursemes: 'collocation/discoursemes',
      SOC: 'wordcloud/secondOrderCollocationDiscoursemeIDs',
      collocatesCompare: 'wordcloud/collocatesToCompare',
    })
  },
  methods: {
    ...mapActions({
      setWindowSize: 'wordcloud/setWindowSize',
      _setAM : 'wordcloud/setAssociationMeasure',
      _setSOC : 'wordcloud/setSecondOrderCollocationDiscoursemeIDs',
      getCollocates: 'collocation/getCollocationCollocates',
      setCompare:'wordcloud/setCollocatesToCompare',
    }),
    setSize () {
      this.setWindowSize(this.selectWindow)
    },
    setAM (){
      // console.log(this.am_value);
      this._setAM(this.am_value);
    },
    clearSOC(){
      this.secondOrderIDs=[];
      this.setSOC();
    },
    setSOC(){
      this._setSOC(this.secondOrderIDs);
    },
    SOCNames(){
      var result = "";
      var i = 0;
      for(var id of this.SOC){
        for(var d of this.collocationDiscoursemes){
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
