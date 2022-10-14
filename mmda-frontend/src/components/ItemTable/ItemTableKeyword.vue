<template>
<v-layout v-if="keyword" row>
  <v-flex xs12 sm12>
    
    <v-card-title>
      Keywords
      <v-btn icon ripple>
        <v-icon class="grey--text text--lighten-1" title="download keywords list (.tsv)" @click="downloadCollocationCSV">file_copy</v-icon>
      </v-btn>
      <v-spacer/>
      <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details ></v-text-field>
    </v-card-title>
    
    <v-alert v-if="error" value="true" color="error" icon="priority_high" :title="error" outline @click="error=null">{{ error }}</v-alert>
    
    <div v-else-if="loadingCoordinates || loadingKeywords" class="text-md-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p v-if="loadingCoordinates">Loading Coordinates...</p>
      <p v-if="loadingKeywords">Loading Keywords...</p>
    </div>

    <v-data-table v-else :headers="headers" :items="transposedCoordinates" :search="search" :pagination.sync="pagination" class="elevation-1">
      
      <template slot="items" slot-scope="props">
        <td v-for="el in headers" :key="props.item.name+el.text" class="text-xs-center">
          <div v-if="el.value==='name'">
            <v-layout row>
              <v-btn @click="gotoConcordanceViewOf(props.item)" icon ripple :title="'show concordances of '+props.item.name">
                <v-icon class="grey--text text--lighten-1">info</v-icon>
              </v-btn>
              <div class="keyword-table-name">{{props.item.name}}</div>
            </v-layout>
          </div>
          <div v-else-if="props.item[el.value+'#Norm']===undefined"> {{props.item[el.value]}} </div>
          <div v-else>
            <div class="keyword-table-sphere" :style="'width:'+props.item[el.value+'#Norm']*2+'rem;'
                                                       +'height:'+props.item[el.value+'#Norm']*2+'rem;'
                                                       +'border-radius:'+props.item[el.value+'#Norm']+'rem;'">
              <div class="keyword-table-number">{{props.item[el.value]}}</div>
            </div>
          </div>
        </td>
      </template>
      
    </v-data-table>
  </v-flex>
</v-layout>
</template>

<style>
  .keyword-table-name{
    margin: auto 0;
  }
  .keyword-table-sphere{
    margin:auto;
    background-color:lightgrey;
    position:relative;
  }
  .keyword-table-number{
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
  name: 'ItemTableKeyword',
  data: () => ({
    search: '',
    error: null,
    loading: false,
    loadingConcordances:false,
    loadingKeywords:false,
    loadingCoordinates:false,
    min: 1,
    pagination: {
      sortBy: 'Conservative LR',
      descending: true,
      rowsPerPage: 10
    }
  }),
  watch:{
    keyword(){
      this.init();
    }
  },
  computed: {
    ...mapGetters({
      user: 'login/user',
      keyword: 'keyword/keyword',
      coordinates: 'coordinates/coordinates',
      keywords: 'keyword/keywords'
    }),
    minmaxAM () {
      var R = {};
      if(this.keywords){
        for(var am of Object.keys(this.keywords)){
          if(!R[am]){
            R[am] = {min:Number.POSITIVE_INFINITY,max:Number.NEGATIVE_INFINITY};
          }
          for(var w of Object.keys(this.keywords[am])){
            var val = Number.parseFloat(this.keywords[am][w]);
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
      if(this.keywords){
        for(var am of Object.keys(this.keywords)){
          for(var w of Object.keys(this.keywords[am])){
            if(!R[w]) R[w] = { name: w };
            val = this.keywords[am][w];
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
      if(this.keywords){
        for(var am of Object.keys(this.keywords)){
          for(var w of Object.keys(this.keywords[am])){
            if(!R[w]) R[w] = { name: w };
            val = this.keywords[am][w];
            val = Number.parseFloat(val);
            R[w][am] = val.toPrecision(2);
            R[w][am.replace(/\./g,'_')] = val.toPrecision(2);
            R[w][am.replace(/\./g,'_')+'#Norm'] = this.map_range(this.map_value(val),this.minmaxAM[am]);
          }
        }
      }
      if(this.coordinates){
        for(var c of Object.keys(this.coordinates)){
          if(R[c]){
            for(var x of Object.keys(this.coordinates[c])){
              val = this.coordinates[c][x];
              R[c][x] = typeof val ==="number" ? val.toPrecision(3): val;
            }
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
        this.keywords 
      ? Object.keys(this.keywords).map(k=>{
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
      getKeywordCoordinates: 'coordinates/getKeywordCoordinates',
      getKeywordKeywords:  'keyword/getKeywordKeywords',
      getConcordances:        'keyword/getConcordances',
      resetConcordances:      'keyword/resetConcordances'
    }),
    error_message_for(error, prefix, codes){
      if( error.response ){
        let value = codes[ error.response.status ];
        if( value ) return this.$t( prefix+value );
      }
      return error.message;
    },
    downloadCollocationCSV(){
      downloadText("keywords.tsv",this.csvText.replace(/"/g,'&quot;'));
    },
    map_value(value){
      return Math.log(1 + Math.max(0,value));
    },
    map_range (value, minmax){
      return (value-minmax.min)/(minmax.max-minmax.min);
    },
    gotoConcordanceViewOf ( item ) {
      if(!this.keyword) return;
      this.loadingConcordances = true;
      this.getConcordances({
        username: this.user.username,
        keyword_id: this.id,
        // soc_items: undefined,
        items: [item.name]
      }).catch((e)=>{
        this.error = this.error_message_for(e,"keyword.concordances.",{400:"invalid_input",404:"not_found"});
      }).then(()=>{
        this.loadingConcordances = false;
      });
    },
    getKeywords(){
      this.loadingKeywords = true;
      this.getKeywordKeywords({
        username:     this.user.username, 
        keyword_id:  this.id
      }).catch((error)=>{
        this.error = this.error_message_for(error,"keyword.keywords.",{400:"invalid_input",404:"not_found"});
      }).then(()=>{
        this.loadingKeywords = false;
      })
    },
    init(){
      this.loadingCoordinates = true;
      if(this.keyword&&this.keyword.id==this.id){
        this.getKeywordCoordinates({
          username:     this.user.username, 
          keyword_id:  this.id
        }).catch((error)=>{
          this.error = this.error_message_for(error,"keyword.coordinates_request.",{404:"not_found"});
        }).then(()=>{
          this.loadingCoordinates = false;
        });
        this.getKeywords();
      }
    }
  },
  created () {
    this.id = this.$route.params.id
    // this.init();
  }
}

</script>
