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
        <td class="text-xs-right">{{ props.item.x }}</td>
        <td class="text-xs-right">{{ props.item.y }}</td>
        <td class="text-xs-right">{{ props.item.x_user }}</td>
        <td class="text-xs-right">{{ props.item.y_user }}</td>
      </template>
  </v-data-table>
  </v-flex>
</v-layout>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'KeywordDiscoursemeList',
  data: () => ({
    search: '',
    error: null,
    loading: false,
    headers: [
      {
        text: 'Coordinates',
        align: 'left',
        //sortable: false,
        value: 'name'
      },
      { text: 'x (auto)', value: 'x' },
      { text: 'y (auto)', value: 'y' },
      { text: 'x (user)', value: 'x_user' },
      { text: 'y (user)', value: 'y_user' },
    ],
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      keyword: 'keyword/keyword',
      coordinates: 'coordinates/coordinates'
    }),
    transposedCoordinates () {
      const items = this.coordinates
      return Object.keys(items).map((key) => ( Object.assign(items[key], {name: key})))
    }
  },
  methods: {
    ...mapActions({
      getKeywordCoordinates: 'coordinates/getKeywordCoordinates'
    }),
    loadCoordinates () {
      const data = {
        username: this.user.username,
        keyword_id: this.id
      }
      this.getKeywordCoordinates(data).then(() => {
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
