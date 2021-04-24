<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Second-Order Collocation</div>
  <v-card v-if="notMini">
    <v-card-text>
      <v-layout v-if="use_second_order_collocation" class="my-4" row wrap>
        <v-combobox v-model="secondOrderIDs" :items="analysisDiscoursemes" item-text="name" label="discoursemes" multiple chips @change="setSOC" ></v-combobox>
      </v-layout>
    </v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'WordcloudSecondOrder',
  data: () => ({
    use_second_order_collocation:true,
    compare: true,
    min: 2,
    am_value: null,
    am_value2: null,
    selectWindow: 3,
    selectWindow2: 3,
    secondOrderIDs: [],
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
      // console.log(this.am_value);
      this._setAM(this.am_value);
    },
    clearSOC(){
      this.secondOrderIDs=[];
      this.setSOC();
    },
    setSOC(){
        this._setSOC(this.secondOrderIDs.map(a=>a.id));
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
