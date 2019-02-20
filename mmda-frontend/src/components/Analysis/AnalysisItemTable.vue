<template>
<v-layout row>
  <v-flex xs12 sm12>
    <h1 class="my-3 title">Collocation and Coordinates:</h1>
    <v-data-table
      v-if="coordinates"
      :headers="headers"
      :items="transposedCoordinates"
      class="elevation-1"
      >
      <template slot="items" slot-scope="props">
        <td v-for="el in headers" :key="props.item.name+el.text" 
          class="text-xs-center"
          >
          <div v-if="props.item[el.value+'#Norm']===undefined"> {{props.item[el.value]}} </div>
          <div v-else> 
            <div :style="
            'margin:auto;'
            +'width:'+props.item[el.value+'#Norm']*2+'rem;'
            +'height:'+props.item[el.value+'#Norm']*2+'rem;'
            +'border-radius:'+props.item[el.value+'#Norm']+'rem;'
            +'background-color:lightgrey;'
            +'position:relative;'">
              <div style="margin:auto;position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);text-shadow:0 0 .5rem white;">{{props.item[el.value]}}</div>
            </div>
          </div>
        </td>

        <!--
        <td>{{ props.item.name }}</td>
        <td class="text-xs-right">{{ props.item.MI }}</td>
        <td class="text-xs-right">{{ props.item['011'] }}</td>
        <td class="text-xs-right">{{ props.item['Dice'] }}</td>
        <td class="text-xs-right">{{ props.item['f2'] }}</td>
        <td class="text-xs-right">{{ props.item['simple.ll'] }}</td>
        <td class="text-xs-right">{{ props.item['t.score'] }}</td>
        <td class="text-xs-right">{{ props.item.tsne_x }}</td>
        <td class="text-xs-right">{{ props.item.tsne_y }}</td>
        <td class="text-xs-right">{{ props.item.user_x }}</td>
        <td class="text-xs-right">{{ props.item.user_y }}</td>-->
      </template>
  </v-data-table>
  </v-flex>
</v-layout>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AnalysisItemTable',
  data: () => ({
    search: '',
    error: null,
    loading: false,
    /*headers: [
      {
        text: 'Items',
        align: 'left',
        //sortable: false,
        value: 'name'
      },
      { text: 'MI', value: 'MI'},
      { text: '011', value: '011'},
      { text: 'Dice', value: 'Dice'},
      { text: 'f2', value: 'f2'},
      { text: 'simple.ll', value: 'simple.ll'},
      { text: 't.score', value: 't.score'},
      { text: 'x (t-SNE)', value: 'tsne_x' },
      { text: 'y (t-SNE)', value: 'tsne_y' },
      { text: 'x (User)', value: 'user_x' },
      { text: 'y (User)', value: 'user_y' },
    ],*/
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      coordinates: 'coordinates/coordinates',
      collocates: 'analysis/collocates',
      windowSize: "wordcloud/windowSize",
    }),
    minmaxAM () {
      var R = {};
      if(this.collocates){
        for(var am of Object.keys(this.collocates)){
          if(!R[am]){
            R[am] = {min:Number.POSITIVE_INFINITY,max:Number.NEGATIVE_INFINITY};
          }
          for(var w of Object.keys(this.collocates[am])){
            R[am].min = Math.min(R[am].min,this.collocates[am][w]);
            R[am].max = Math.max(R[am].max,this.collocates[am][w]);
          }
        }
      }
      return R;
    },
    transposedCoordinates () {
      //TODO: does this know, that it needs both this.coordinates and this.collocates?
      // and does it update, if any of them changes?
      var R = {};
      if(this.coordinates){
        for(var c of Object.keys(this.coordinates)){
          R[c] = {name:c};
          for(var x of Object.keys(this.coordinates[c])){
            var val = this.coordinates[c][x];
            R[c][x] = typeof val ==="number" ? val.toPrecision(3): val;
          }
        }
      }
      if(this.collocates){
        for(var am of Object.keys(this.collocates)){
          for(var w of Object.keys(this.collocates[am])){
            if(!R[w]) R[w] = { name: w };
            R[w][am] = this.collocates[am][w].toPrecision(2);
            R[w][am+'#Norm'] = this.map_range(this.collocates[am][w],this.minmaxAM[am]);
          }
        }
      }
      return Object.values(R);      
      //return Object.keys(items).map((key) => ( Object.assign(items[key], {name: key})))
    },
    headers () {
      var Coll = this.collocates ? Object.keys(this.collocates).map(k=>{return{text:k,value:k,align:'center'}}) : [];
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
      getCollocates:           "analysis/getAnalysisCollocates",
    }),
    map_range (value,minmax){
      return (value-minmax.min)/(minmax.max-minmax.min);
    },
    loadCoordinates () {
      const data = {
        username: this.user.username,
        analysis_id: this.id
      }
      this.getAnalysisCoordinates(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    loadCollocates( window_size ) {
      const request = {
        params: { window_size: window_size }
      };
      const data = {
        username: this.user.username,
        analysis_id: this.id,
        request: request
      };
      return this.getCollocates(data)
      
    },
  },
  created () {
    this.id = this.$route.params.id
    this.loadCoordinates()
    this.loadCollocates(this.windowSize)
  }
}

</script>
