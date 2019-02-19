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
        <td class="text-xs-right">{{ props.item.user_y }}</td>
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
    headers: [
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
    ],
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      coordinates: 'coordinates/coordinates',
      collocates: 'analysis/collocates',
      windowSize: "wordcloud/windowSize",
    }),
    transposedCoordinates () {
      var R = {};
      for(var c of Object.keys(this.coordinates)){
        R[c] = {name:c};
        for(var x of Object.keys(this.coordinates[c])){
          var val = this.coordinates[c][x];
          R[c][x] = typeof val ==="number" ? val.toPrecision(3): val;
        }
      }

      for(var am of Object.keys(this.collocates)){
        for(var w of Object.keys(this.collocates[am])){
          if(!R[w]) R[w]={name:w};
          R[w][am] = this.collocates[am][w].toPrecision(2);
        }
      }
      return Object.values(R);      
      //return Object.keys(items).map((key) => ( Object.assign(items[key], {name: key})))
    }
  },
  methods: {
    ...mapActions({
      getAnalysisCoordinates: 'coordinates/getAnalysisCoordinates',
      getCollocates:           "analysis/getAnalysisCollocates",
    }),
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
