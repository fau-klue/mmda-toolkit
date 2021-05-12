<template>
<div>
  <v-text-field label="Search" prepend-inner-icon="search" v-model="search"></v-text-field>
  <v-data-table v-if="userDiscoursemes" :headers="headers" :items="userDiscoursemes" :search="search" :pagination.sync="pagination" class="elevation-1">
    <template v-slot:items="props">
      <router-link :to="/discourseme/ + props.item.id" tag="tr" :style="{ cursor: 'pointer'}">
        <td class="text-xs-left">{{ props.item.id }}</td>
        <td class="text-xs-left">{{ props.item.name }}</td>
        <td class="text-xs-left">{{ props.item.items }}</td>
      </router-link>
    </template>
  </v-data-table>
</div>
</template>

  <script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'DiscoursemeList',
  data: () => ({
    search: '',
    // dialogDelete: false,
    headers: [
      {text: 'ID', value: 'id', align: 'left'},
      {text: 'name', value: 'name', align: 'left'},
      {text: 'items', value: 'items', align: 'left'},
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
      userDiscoursemes: 'discourseme/userDiscoursemes'
    }),
    // filteredItems() {
    //   var F = [];
    //   if(!this.userDiscoursemes) return [];
    //   if (!this.search) {
    //     F = this.userDiscoursemes

    //   } else {
    //     F = this.userDiscoursemes.filter(items =>
    //                                         items.name.toLowerCase().search(this.search.toLowerCase()) >= 0 ||
    //                                         items.items.join().toLowerCase().search(this.search.toLowerCase()) >= 0
    //                                        )}
    //   F.sort((x)=>x.id); //sort by latest creation-date //i.e. ~ id
    //   return F;
    // }
  },
  methods: {
    ...mapActions({
      getUserDiscoursemes: 'discourseme/getUserDiscoursemes'
    }),
    clearSearch () {
      this.search = ''
    },
    loadDiscoursemes () {
      this.getUserDiscoursemes(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.loadDiscoursemes()
  }
}

</script>
