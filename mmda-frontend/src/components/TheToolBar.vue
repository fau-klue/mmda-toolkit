<template>
<v-toolbar color="#003366" dark fixed app clipped-right dense>
  <v-toolbar-title>{{ title }}</v-toolbar-title>
  <v-spacer></v-spacer>
  <v-toolbar-items>
    <v-btn flat to="/">{{ $t("toolbar.home") }}</v-btn>
    <v-btn flat to="/about">{{ $t("toolbar.about") }}</v-btn>
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
    <v-btn flat v-if="isAuthenticated" @click="logout">{{ $t("toolbar.logout") }}</v-btn>
    <v-btn flat v-else to="/login">{{ $t("toolbar.login") }}</v-btn>
  </v-toolbar-items>
</v-toolbar>
</template>

<script>
import { mapGetters, mapActions} from 'vuex'

export default {
  name: 'ToolBar',
  data: () => ({
    title: 'Mixed Methods Discourse Analysis',
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
