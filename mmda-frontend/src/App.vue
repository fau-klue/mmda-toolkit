<template>
<v-app id="app">
  <SideBar v-if="isAuthenticated" />
  <ToolBar/>
    <v-content>
    <router-view/>
    </v-content>
</v-app>
</template>

<script>
// Central Entrypoint for the App
import { mapGetters } from 'vuex'

import ToolBar from '@/components/TheToolBar.vue'
import SideBar from '@/components/TheSideBar.vue'

export default {
  name: 'App',
  components: {
    ToolBar,
    SideBar
  },
  computed: {
    ...mapGetters({
      isAuthenticated: 'login/isAuthenticated'
    })
  }
}
</script>
