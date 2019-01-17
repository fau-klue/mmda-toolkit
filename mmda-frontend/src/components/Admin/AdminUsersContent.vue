<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <h1 class="title">Users</h1>
          <v-list two-line subheader v-if="users">
            <v-list-tile v-for="user in users" :key="user" avatar>
              <v-list-tile-avatar>
                <v-icon class="grey--text">face</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>{{ user }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon @click="deleteUser(user)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
        </v-flex>

        <v-flex xs12>
        <AdminUsersNew/>
        </v-flex>

      </v-layout>
    </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import AdminUsersNew from '@/components/Admin/AdminUsersNew.vue'

export default {
  name: 'AdminUsersContent',
  components: {
    AdminUsersNew
  },
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
      getAllUsers: 'admin/getAllUsers'
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
    deleteUser (name) {
      // TODO call API
      console.log(name)
    }
  },
  created () {
    this.loadUsers()
  }
}

</script>
