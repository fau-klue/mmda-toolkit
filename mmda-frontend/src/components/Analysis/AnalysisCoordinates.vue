<template>
<v-layout row>
  <v-flex xs12 sm12>
    <h1 class="my-3 title">Coordinates:</h1>
    <v-data-table
      v-if="coordinates"
      :headers="headers"
      :items="transposedCoordinates"
      class="elevation-1"
      >
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
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
  name: 'AnalysisDiscoursemeList',
  data: () => ({
    search: '',
    error: null,
    loading: false,
    headers: [
      {
        text: 'Coordinates',
        align: 'left',
        sortable: false,
        value: 'name'
      },
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
      coordinates: 'coordinates/coordinates'
    }),
    transposedCoordinates () {
      const items = this.coordinates
      return Object.keys(items).map((key) => ( Object.assign(items[key], {name: key})))
    }
  },
  methods: {
    ...mapActions({
      getAnalysisCoordinates: 'coordinates/getAnalysisCoordinates'
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
    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadCoordinates()
  }
}

</script>
