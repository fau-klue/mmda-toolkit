<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Second-Order Collocation</div>
  <v-card v-if="notMini">
    <v-card-text>
      <v-layout v-if="use_second_order_collocation" class="my-4" row wrap>
        <v-combobox v-model="secondOrderIDs" :items="collocationDiscoursemes" item-text="name" label="discoursemes" multiple chips @change="setSOC" ></v-combobox>
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
      setCompare: 'wordcloud/setCollocatesToCompare',
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
    },
    SOCNames(){
      var result = "";
      var i = 0;
      for(var id of this.SOC){
        for(var d of this.collocationsDiscoursemes){
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
