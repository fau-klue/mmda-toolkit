<template>
<div>
  <v-text-field label="Search" prepend-inner-icon="search" v-model="search"></v-text-field>
  <v-data-table v-if="userCollocation" :headers="headers" :items="userCollocation" :search="search" :pagination.sync="pagination" class="elevation-1">
    <template v-slot:items="props">
      <router-link :to="/collocation/ + props.item.id" tag="tr" :style="{ cursor: 'pointer'}">
        <td class="text-xs-left">{{ props.item.id }}</td>
        <td class="text-xs-left">{{ props.item.corpus }}</td>
        <td class="text-xs-left">{{ props.item.topic_discourseme.name }} (ID: {{ props.item.topic_discourseme.id }})</td>
        <!-- <td class="text-xs-left">{{ props.item.items }}</td> -->
      </router-link>
    </template>
  </v-data-table>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'CollocationList',
  data: () => ({
    search: '',
    // dialogDelete: false,
    headers: [
      {text: 'ID', value: 'id', align: 'left'},
      {text: 'corpus', value: 'corpus', align: 'left'},
      {text: 'discourseme', value: 'topic_discourseme.name', align: 'left'},
      // {text: 'items', value: 'items', align: 'left'},
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
      userCollocation: 'collocation/userCollocation',
      isAuthenticated : 'login/isAuthenticated'
    })
  },
  methods: {
    ...mapActions({
      getUserCollocation: 'collocation/getUserCollocation',
      clearJWT: 'login/clearJWT',
    }),
    clearSearch () {
      this.search = ''
    },
    loadCollocation () {
      this.getUserCollocation(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
  },
  created () {
    if(!this.user || !this.user.username){
      this.clearJWT().then(() => {
        this.$router.push('/login')
      })
    }else{
      this.loadCollocation()
    }
  }
}

</script>
