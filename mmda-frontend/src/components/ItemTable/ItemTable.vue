<template>
<v-layout v-if="collocation" row>
  <v-flex xs12 sm12>

    <v-card-title>
      Collocates (window: {{ windowSize }})
      <v-btn icon ripple>
        <v-icon class="grey--text text--lighten-1" title="download collocates list (.tsv)" @click="downloadCollocationCSV">file_copy</v-icon>
      </v-btn>
      <v-spacer/>
      <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details ></v-text-field>
    </v-card-title>
    
    <v-alert v-if="error" value="true" color="error" icon="priority_high" :title="error" outline @click="error=null">{{ error }}</v-alert>
    
    <div v-else-if="loadingCoordinates || loadingCollocates" class="text-md-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p v-if="loadingCoordinates">Loading Coordinates...</p>
      <p v-if="loadingCollocates">Loading Collocates...</p>
    </div>

    <v-data-table v-else :headers="headers" :items="transposedCoordinates" :search="search" :pagination.sync="pagination" class="elevation-1">
      
      <template slot="items" slot-scope="props">
        <td v-for="el in headers" :key="props.item.name+el.text" class="text-xs-center">
          <div v-if="el.value==='name'">
            <v-layout row>
              <v-btn @click="gotoConcordanceViewOf(props.item)" icon ripple :title="'show concordances of '+props.item.name">
                <v-icon class="grey--text text--lighten-1">info</v-icon>
              </v-btn>
              <div class="collocation-table-name">{{props.item.name}}</div>
            </v-layout>
          </div>
          <div v-else-if="props.item[el.value+'#Norm']===undefined"> {{props.item[el.value]}} </div>
          <div v-else>
            <div class="collocation-table-sphere" :style="'width:'+props.item[el.value+'#Norm']*2+'rem;'
                                                       +'height:'+props.item[el.value+'#Norm']*2+'rem;'
                                                       +'border-radius:'+props.item[el.value+'#Norm']+'rem;'">
              <div class="collocation-table-number">{{props.item[el.value]}}</div>
            </div>
          </div>
        </td>
      </template>
      
    </v-data-table>
  </v-flex>
</v-layout>
</template>

<style>
  .collocation-table-name{
    margin: auto 0;
  }
  .collocation-table-sphere{
    margin:auto;
    background-color:lightgrey;
    position:relative;
  }
  .collocation-table-number{
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
import { downloadText } from '@/wordcloud/util_misc.js'

export default {
  name: 'ItemTable',
  data: () => ({
    search: '',
    error: null,
    loading: false,
    loadingConcordances:false,
    loadingCollocates:false,
    loadingCoordinates:false,
    min: 1,
    pagination: {
      sortBy: 'log likelihood',
      descending: true,
      rowsPerPage: 10
    }
  }),
  watch:{
    windowSize(){
      this.getCollocates();
    },
    collocation(){
      this.init();
    }
  },
  computed: {
    ...mapGetters({
      user: 'login/user',
      collocation: 'collocation/collocation',
      coordinates: 'coordinates/coordinates',
      collocates: 'collocation/collocates',
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
            val = this.map_value(val);
            R[am].min = Math.min(R[am].min,val);
            R[am].max = Math.max(R[am].max,val);
          }
        }
      }
      return R;
    },
    transposedCoordinatesFullPrecision () {
      // TODO: does this know, that it needs both this.coordinates and this.collocates?
      // and does it update, if any of them changes?
      var R = {}, val;
      if(this.coordinates){
        for(var c of Object.keys(this.coordinates)){
          R[c] = {name:c};
          for(var x of Object.keys(this.coordinates[c])){
            val = this.coordinates[c][x];
            R[c][x] = val;
          }
        }
      }
      if(this.collocates){
        for(var am of Object.keys(this.collocates)){
          for(var w of Object.keys(this.collocates[am])){
            if(!R[w]) R[w] = { name: w };
            val = this.collocates[am][w];
            val = Number.parseFloat(val);
            R[w][am] = val;
            R[w][am.replace(/\./g,'_')] = val;
            R[w][am.replace(/\./g,'_')+'#Norm'] = this.map_range(this.map_value(val), this.minmaxAM[am]);
          }
        }
      }
      return Object.values(R);
    },
    transposedCoordinates () {
      // TODO: does this know, that it needs both this.coordinates and this.collocates?
      // and does it update, if any of them changes?
      var R={},val;
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
            R[w][am.replace(/\./g,'_')+'#Norm'] = this.map_range(this.map_value(val),this.minmaxAM[am]);
          }
        }
      }
      return Object.values(R);
    },
    csvText(){
      var H = this.headers;
      var colSeparator="\t";
      var rowSeparator="\n";
      var text = "";
      var X = this.transposedCoordinatesFullPrecision;

      var firstColumn = true;
      var h ;
      for(h of H){
        if(!firstColumn) text += colSeparator;
        text += h.text;
        firstColumn = false;
      }

      for(var x of X){
        text+=rowSeparator;
        firstColumn = true;
        for(h of H){
          if(!firstColumn) text += colSeparator;
          var val = x[h.value];
          if(val!==undefined && val!==null) text += val;
          firstColumn = false;
        }
      }
      return text;
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
        {text:'item',value:'name',align:'center'},
        ...Coll,
        { text: 'x (auto)', value: 'x', align:"center" },
        { text: 'y (auto)', value: 'y', align:'center' },
        { text: 'x (user)', value: 'x_user', align:'center' },
        { text: 'y (user)', value: 'y_user', align:'center' }
      ];
    }
  },
  methods: {
    ...mapActions({
      getCollocationCoordinates: 'coordinates/getCollocationCoordinates',
      getCollocationCollocates:  'collocation/getCollocationCollocates',
      getConcordances:        'collocation/getConcordances',
      resetConcordances:      'collocation/resetConcordances'
    }),
    error_message_for(error, prefix, codes){
      if( error.response ){
        let value = codes[ error.response.status ];
        if( value ) return this.$t( prefix+value );
      }
      return error.message;
    },
    downloadCollocationCSV(){
      downloadText("collocates.tsv",this.csvText.replace(/"/g,'&quot;'));
    },
    map_value(value){
      return Math.log(1 + Math.max(0,value));
    },
    map_range (value, minmax){
      return (value-minmax.min)/(minmax.max-minmax.min);
    },
    gotoConcordanceViewOf ( item ) {
      if(!this.collocation) return;
      this.loadingConcordances = true;
      this.getConcordances({
        username: this.user.username,
        collocation_id: this.id,
        // soc_items: undefined,
        items: [item.name], 
        window_size: this.windowSize
      }).catch((e)=>{
        this.error = this.error_message_for(e,"collocation.concordances.",{400:"invalid_input",404:"not_found"});
      }).then(()=>{
        this.loadingConcordances = false;
      });
    },
    getCollocates(){
      this.loadingCollocates = true;
      this.getCollocationCollocates({
        username:     this.user.username, 
        collocation_id:  this.id, 
        window_size:  this.windowSize
      }).catch((error)=>{
        this.error = this.error_message_for(error,"collocation.collocates.",{400:"invalid_input",404:"not_found"});
      }).then(()=>{
        this.loadingCollocates = false;
      })
    },
    init(){
      this.loadingCoordinates = true;
      if(this.collocation&&this.collocation.id==this.id){
        this.selectWindow = this.windowSize;
        this.getCollocationCoordinates({
          username:     this.user.username, 
          collocation_id:  this.id
        }).catch((error)=>{
          this.error = this.error_message_for(error,"collocation.coordinates_request.",{404:"not_found"});
        }).then(()=>{
          this.loadingCoordinates = false;
        });
        this.getCollocates();
      }
    }
  },
  created () {
    this.id = this.$route.params.id
    this.init();
  }
}

</script>
