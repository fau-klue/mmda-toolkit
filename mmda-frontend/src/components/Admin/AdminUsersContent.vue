<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <p class="headline">Users ({{ users.length }})</p>
          <v-list v-if="users">
            <v-list-tile v-for="user in users" :key="user" avatar>
              <v-list-tile-avatar>
                <v-icon v-if="user === 'admin'" class="red--text">perm_identity</v-icon>
                <v-icon v-else class="grey--text">perm_identity</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>{{ user }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn v-if="user !== 'admin'" icon @click="removeUser(user)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
        </v-flex>
      </v-layout>
    </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AdminUsersContent',
  data: () => ({
    loading: false,
    error: null
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      users: 'admin/users'
    })
  },
  methods: {
    ...mapActions({
      getAllUsers: 'admin/getAllUsers',
      deleteUser: 'admin/deleteUser'
    }),
    loadUsers () {
      this.loading = true
      this.getAllUsers().then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
      this.loading = false
    },
    removeUser (name) {
      this.deleteUser(name).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.loadUsers()
  }
}

</script>
