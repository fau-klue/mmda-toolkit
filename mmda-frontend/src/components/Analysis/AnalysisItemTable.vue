<template>
<v-layout row>
  <v-flex xs12 sm12>
    <h1 class="my-3 title">Collocation and Coordinates:</h1>
    <v-alert v-if="error" value="true" color="error" icon="priority_high" :title="error" outline>An Error occured</v-alert>
    <div v-else-if="loadingCoordinates || loadingCollocates" class="text-md-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p v-if="loadingCoordinates">Loading Coordinates...</p>
      <p v-if="loadingCollocates">Loading Collocation...</p>
    </div>
    <v-data-table
      v-else
      :headers="headers"
      :items="transposedCoordinates"
      class="elevation-1"
      >
      <template slot="items" slot-scope="props">
        <td v-for="el in headers" :key="props.item.name+el.text" 
          class="text-xs-center"
          >
          <div v-if="el.value==='name'">
            <v-layout row>
              <v-btn @click="gotoConcordanceViewOf(props.item)" icon ripple :title="'show concordances of '+props.item.name">
                <v-icon class="grey--text text--lighten-1">info</v-icon>
              </v-btn>
              <div class="analysis-table-name">{{props.item.name}}</div>
            </v-layout>
          </div>
          <div v-else-if="props.item[el.value+'#Norm']===undefined"> {{props.item[el.value]}} </div>
          <div v-else> 
            <div class="analysis-table-sphere" :style="
            'width:'+props.item[el.value+'#Norm']*2+'rem;'
            +'height:'+props.item[el.value+'#Norm']*2+'rem;'
            +'border-radius:'+props.item[el.value+'#Norm']+'rem;'">
              <div class="analysis-table-number">{{props.item[el.value]}}</div>
            </div>
          </div>
        </td>
      </template>
  </v-data-table>
  </v-flex>
</v-layout>
</template>

<style>
  .analysis-table-name{
    margin: auto 0;
  }
  .analysis-table-sphere{
    margin:auto;
    background-color:lightgrey;
    position:relative;
  }
  .analysis-table-number{
    margin:auto;
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    text-shadow:0 0 .5rem white;
  }
</style>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AnalysisItemTable',
  data: () => ({
    search: '',
    error: null,
    loading: false,
    loadingConcordances:false,
    loadingCollocates:false,
    loadingCoordinates:false
  }),
  watch:{
    /* analysis(){
      this.requestData();
    },
    user(){
      if(!this.user){
        //TODO:: route to login
        return;
      }
      this.requestData();
    }
     minmaxAM(){
      console.log("MinmaxUpdate");
    },
    transposedCoordinates(){
      console.log("transposedUpdate");
    },
    headers(){
      console.log("headersUpdate");
    }*/
  },
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      coordinates: 'coordinates/coordinates',
      collocates: 'analysis/collocates',
      windowSize: 'wordcloud/windowSize',
    }),
    minmaxAM () {
      var R = {};
      if(this.collocates){
        for(var am of Object.keys(this.collocates)){
          if(!R[am]){
            R[am] = {min:Number.POSITIVE_INFINITY,max:Number.NEGATIVE_INFINITY};
          }
          for(var w of Object.keys(this.collocates[am])){
            var val = Number.parseFloat(this.collocates[am][w]);
            if(val!=val) continue;
            R[am].min = Math.min(R[am].min,val);
            R[am].max = Math.max(R[am].max,val);
          }
        }
      }
      return R;
    },
    transposedCoordinates () {
      //TODO: does this know, that it needs both this.coordinates and this.collocates?
      // and does it update, if any of them changes?
      var R = {}, val;
      if(this.coordinates){
        for(var c of Object.keys(this.coordinates)){
          R[c] = {name:c};
          for(var x of Object.keys(this.coordinates[c])){
            val = this.coordinates[c][x];
            R[c][x] = typeof val ==="number" ? val.toPrecision(3): val;
          }
        }
      }
      if(this.collocates){
        for(var am of Object.keys(this.collocates)){
          for(var w of Object.keys(this.collocates[am])){
            if(!R[w]) R[w] = { name: w };
            val = this.collocates[am][w];
            val = Number.parseFloat(val);
            R[w][am] = val.toPrecision(2);
            R[w][am.replace(/\./g,'_')] = val.toPrecision(2);
            R[w][am.replace(/\./g,'_')+'#Norm'] = this.map_range(val,this.minmaxAM[am]);
          }
        }
      }
      return Object.values(R);
    },
    headers () {
      var Coll = 
        this.collocates 
      ? Object.keys(this.collocates).map(k=>{
          return {
            text:k, 
            valueWithDot:k, 
            value:k.replace(/\./g,'_'), 
            align:'center'
          }
        }) 
      : [];
      return [
        {text:'Items',value:'name',align:'center'},
        ...Coll,
        { text: 'x (t-SNE)', value: 'tsne_x', align:"center" },
        { text: 'y (t-SNE)', value: 'tsne_y', align:'center' },
        { text: 'x (User)', value: 'user_x', align:'center' },
        { text: 'y (User)', value: 'user_y', align:'center' }
      ];
    }
  },
  methods: {
    ...mapActions({
      getAnalysisCoordinates: 'coordinates/getAnalysisCoordinates',
      getAnalysisCollocates:  'analysis/getAnalysisCollocates',
      getConcordances:        'corpus/getConcordances',
    }),
    map_range (value,minmax){
      return (value-minmax.min)/(minmax.max-minmax.min);
    },
    gotoConcordanceViewOf ( item ) {
      this.loadingConcordances = true;
      this.getConcordances({
        corpus:         this.analysis.corpus, 
        topic_items:    this.analysis.topic_discourseme.items, 
        collocate_items: [item.name], 
        window_size:    this.windowSize
      }).catch((e)=>{
        this.error = e;
      }).then(()=>{
        this.loadingConcordances = false;
      });
    },
  },
  created () {
    this.id = this.$route.params.id
    this.loadingCoordinates = true;
    this.loadingCollocates = true;
    this.getAnalysisCoordinates({
      username:     this.user.username, 
      analysis_id:  this.id
    }).catch((error)=>{
      this.error = error;
    }).then(()=>{
      this.loadingCoordinates = false;
    });

    this.getAnalysisCollocates({
      username:     this.user.username, 
      analysis_id:  this.id, 
      window_size:  this.windowSize
    }).catch((error)=>{
      this.error = error;
    }).then(()=>{
      this.loadingCollocates = false;
    })
  }
}

</script>
