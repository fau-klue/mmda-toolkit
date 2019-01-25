<template>
    <v-toolbar color="#003366" dark fixed app clipped-right dense>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-menu offset-y>
          <v-btn flat slot="activator" class="white--text">
            <v-icon dark left>language</v-icon>
            {{ $i18n.locale }}
          </v-btn>
        <v-list>
          <v-list-tile v-for="(lang, i) in langs" :key="i" @click="changeLang(lang)">
            <v-list-tile-title>{{ lang }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
        </v-menu>
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
    title: 'Mixed Method Discourse Analysis',
    langs: ['de', 'en']
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
    },
    changeLang (lang) {
      this.$i18n.locale = lang
    }
  }
}
</script>
