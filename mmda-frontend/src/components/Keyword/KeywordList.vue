<template>
<div>
  <v-text-field label="Search" prepend-inner-icon="search" v-model="search"></v-text-field>
  <v-data-table v-if="userKeyword" :headers="headers" :items="userKeyword" :search="search" :pagination.sync="pagination" class="elevation-1">
    <template v-slot:items="props">
      <router-link :to="/keyword/ + props.item.id" tag="tr" :style="{ cursor: 'pointer'}">
        <td class="text-xs-left">{{ props.item.id }}</td>
        <td class="text-xs-left">{{ props.item.corpus }}</td>
        <td class="text-xs-left">{{ props.item.p }}</td>
        <td class="text-xs-left">{{ props.item.corpus_reference }}</td>
        <td class="text-xs-left">{{ props.item.p_reference }}</td>
      </router-link>
    </template>
  </v-data-table>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'KeywordList',
  data: () => ({
    search: '',
    headers: [
      {text: 'ID', value: 'id', align: 'left'},
      {text: 'corpus', value: 'corpus', align: 'left'},
      {text: 'p-att', value: 'p', align: 'left'},
      {text: 'reference corpus', value: 'name', align: 'left'},
      {text: 'p-att', value: 'p_reference', align: 'left'},
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
      userKeyword: 'keyword/userKeyword',
      isAuthenticated : 'login/isAuthenticated'
    })
  },
  methods: {
    ...mapActions({
      getUserKeyword: 'keyword/getUserKeyword',
      clearJWT: 'login/clearJWT'
    }),
    clearSearch () {
      this.search = ''
    },
    loadKeyword () {
      this.getUserKeyword(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
  },
  created () {
    if(!this.user || !this.user.username){
      // fallback if user-token expired
      // logout and go back to loginscreen
      this.clearJWT().then(() => {
        this.$router.push('/login')
      })
    }else{
      this.loadKeyword()
    }
  }
}

</script>
