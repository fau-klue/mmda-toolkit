<template>
  <div>
  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout>
          <v-flex xs12 sm12>
            <v-text-field label="Search" prepend-inner-icon="search" v-model="search" clearable @click:clear="clearSearch"></v-text-field>

            <v-list two-line subheader>
              <v-list-tile v-for="analysis in filteredItems" :key="analysis.id" avatar :to="/analysis/ + analysis.id">
                <v-list-tile-avatar>
                  <v-icon class="grey lighten-1 white--text">dashboard</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ analysis.name }} (ID:{{ analysis.id }})</v-list-tile-title>
                  <v-list-tile-sub-title>{{ analysis.items }}</v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AnalysisList',
  data: () => ({
    search: '',
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      userAnalysis: 'analysis/userAnalysis',
      isAuthenticated : 'login/isAuthenticated'
    }),
    filteredItems() {
      var F = [];
      if(!this.userAnalysis) return [];
      if (!this.search) {
        F = this.userAnalysis
      } else {
        F = this.userAnalysis.filter(items => items.name.toLowerCase().search(this.search.toLowerCase()) >= 0 )
      }
      F.sort((x)=>x.id); //sort by latest creation-date //i.e. ~ id
      return F;
    }
  },
  methods: {
    ...mapActions({
      getUserAnalysis: 'analysis/getUserAnalysis',
      clearJWT: 'login/clearJWT'
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
    }
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
