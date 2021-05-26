<template>
<div>
  <v-text-field label="Search" prepend-inner-icon="search" v-model="search"></v-text-field>
  <v-data-table v-if="filteredItems" :headers="headers" :items="filteredItems" :search="search" :pagination.sync="pagination" class="elevation-1">
    <template v-slot:items="props">
      <router-link :to="/constellation/ + props.item.id" tag="tr" :style="{ cursor: 'pointer'}">
        <td class="text-xs-left">{{ props.item.id }}</td>
        <td class="text-xs-left">{{ props.item.name }}</td>
        <td class="text-xs-left">{{ props.item.discoursemes_names }}</td>
      </router-link>
    </template>
  </v-data-table>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'ConstellationList',
  data: () => ({
    search: '',
    headers: [
      {text: 'ID', value: 'id', align: 'left'},
      {text: 'name', value: 'name', align: 'left'},
      {text: 'discoursemes', value: 'discoursemes_names', align: 'left'},
      // {text: '', value: 'delete', align: 'center'}
    ],
    pagination: {
      sortBy: 'id',
      descending: true,
      rowsPerPage: 25
    }
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      userConstellations: 'constellation/userConstellations'
    }),
    filteredItems() {
      var F = []
      if(!this.userConstellations) return [];
      if (!this.search) {
        F = this.userConstellations
      } else {
        F = this.userConstellations.filter(items => items.name.toLowerCase().search(this.search) >= 0 )
      }
      F.sort((x)=>x.id)
      return F;
    }
  },
  methods: {
    ...mapActions({
      getUserConstellations: 'constellation/getUserConstellations'
    }),
    clearSearch () {
      this.search = ''
    },
    loadConstellations () {
      this.getUserConstellations(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.loadConstellations()
  }
}

</script>
