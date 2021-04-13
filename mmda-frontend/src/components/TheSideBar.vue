<template>
<v-navigation-drawer v-model="sidebar" app permanent clipped >
  <v-toolbar flat class="transparent">
    <v-list class="pa-0">
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title class="title"> {{ user.username }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-toolbar>

  <v-list class="pt-0" dense>
    <v-divider></v-divider>

    <v-list-tile v-for="item in items" :key="item.title" router :to="item.route">
      <v-list-tile-action>
        <v-icon>{{ item.icon }}</v-icon>
      </v-list-tile-action>

      <v-list-tile-content>
        <v-list-tile-title>{{ item.title }}</v-list-tile-title>
      </v-list-tile-content>
    </v-list-tile>

    <v-list-group prepend-icon="build" v-if="isAdmin">
      <v-list-tile slot="activator">
        <v-list-tile-title>Administration</v-list-tile-title>
      </v-list-tile>

      <v-list-tile v-for="item in admins" :key="item.title" router :to="item.route">
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>

        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list-group>

  </v-list>
</v-navigation-drawer>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ProfileSidebar',
  data: () => ({
    sidebar: true,
    items: [
      { title: 'Analyses', icon: 'dashboard', route: '/analysis' },
      { title: 'Discoursemes', icon: 'subject', route: '/discourseme' },
      { title: 'Constellations', icon: 'question_answer', route: '/constellation' },
      { title: 'User Profile', icon: 'perm_identity', route: '/profile' },
    ],
    admins: [
      { title: 'Users', icon: 'subject', route: '/admin/users' },
      { title: 'Objects', icon: 'subject', route: '/admin/objects' }
    ]
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      isAdmin: 'login/isAdmin'
    })
  }
}
</script>

<style>

</style>
