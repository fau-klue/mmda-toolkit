<template>
  <div>
    <v-text-field label="Search" prepend-inner-icon="search" v-model="search"></v-text-field>
    <v-data-table v-if="userAnalysis" :headers="headers" :items="userAnalysis" :search="search" :pagination.sync="pagination" class="elevation-1">
      <template v-slot:items="props">
        <router-link :to="/analysis/ + props.item.id" tag="tr" :style="{ cursor: 'pointer'}">
          <td class="text-xs-left">{{ props.item.id }}</td>
          <td class="text-xs-left">{{ props.item.corpus }}</td>
          <td class="text-xs-left">{{ props.item.topic_discourseme.name }}</td>
          <td class="text-xs-left">{{ props.item.items }}</td>
        </router-link>
        <!-- <td> -->
        <!--   <v-btn icon @click="deleteAnalysis(props.item.id)"> -->
        <!--     <v-icon class="red--text text--lighten-1">delete</v-icon> -->
        <!--   </v-btn> -->
        <!-- </td> -->
      </template>
    </v-data-table>

  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AnalysisList',
  data: () => ({
    search: '',
    dialogDelete: false,
    headers: [
      {text: 'ID', value: 'id', align: 'left'},
      {text: 'corpus', value: 'corpus', align: 'left'},
      {text: 'discourseme', value: 'topic_discourseme.name', align: 'left'},
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
      userAnalysis: 'analysis/userAnalysis',
      isAuthenticated : 'login/isAuthenticated'
    })
  },
  methods: {
    ...mapActions({
      getUserAnalysis: 'analysis/getUserAnalysis',
      clearJWT: 'login/clearJWT',
      // deleteUserAnalysis: 'analysis/deleteUserAnalysis'
    }),
    clearSearch () {
      this.search = ''
    },
    loadAnalysis () {
      this.getUserAnalysis(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    // deleteAnalysis (id) {
    //   this.dialogDelete = false
    //   const data = {
    //     username: this.user.username,
    //     analysis_id: id
    //   }
    //   this.deleteUserAnalysis(data).then(() => {
    //     this.error = null
    //     this.$router.push('/analysis')
    //     this.dialogDelete = false
    //   }).catch((error) => {
    //     this.error = error
    //     this.dialogDelete = false
    //     this.loadAnalysis()
    //   })
    // },
  },
  created () {
    if(!this.user || !this.user.username){
      //fallback if user-token expired
      // Logout and go back to loginscreen
      this.clearJWT().then(() => {
        this.$router.push('/login')
      })
    }else{
      this.loadAnalysis()
    }
  }
}

</script>
