<template>
    <v-toolbar color="#003366" dark fixed app clipped-right dense>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn flat to="/">Index</v-btn>
        <v-btn flat to="/about">About</v-btn>
        <v-btn flat v-if="isAuthenticated" @click="logout">Logout</v-btn>
        <v-btn flat v-else to="/login">Login</v-btn>
      </v-toolbar-items>
    </v-toolbar>
</template>

<script>
import { mapGetters, mapActions} from 'vuex'

export default {
  name: 'ToolBar',
  data: () => ({
    title: 'Mixed Method Discourse Analysis'
  }),
  computed: {
    ...mapGetters({
      isAuthenticated: 'login/isAuthenticated'
    })
  },
  methods: {
    ...mapActions({
      clearJWT: 'login/clearJWT'
    }),
    logout () {
      this.clearJWT().then(() => {
        this.$router.push('/')
      })
    }
  }
}
</script>
