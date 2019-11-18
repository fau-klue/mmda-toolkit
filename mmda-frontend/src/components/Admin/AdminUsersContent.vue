<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12 v-if="users">
          <p class="headline">Users ({{ users.length }})</p>
          <v-list>
            <v-list-tile v-for="user in users" :key="user" avatar>
              <v-list-tile-avatar>
                <v-icon v-if="user === 'admin'" class="red--text">perm_identity</v-icon>
                <v-icon v-else class="grey--text">perm_identity</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>{{ user }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn v-if="user !== 'admin'" icon @click.stop="openDeleteDialog(user)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>

  <v-dialog v-model="dialogDelete" max-width="290">
    <v-card>
      <v-card-title class="headline">Delete User {{selectedUser}}?</v-card-title>
      <v-card-text>
        You’re about to permanently delete this User. Once deleted, it cannot be undone or recovered.                </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn outline @click="dialogDelete = false">Close</v-btn>
        <v-btn color="error" @click="removeUser">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AdminUsersContent',
  data: () => ({
    loading: false,
    error: null,
    selectedUser: null,
    dialogDelete: false
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
    openDeleteDialog (name) {
      this.dialogDelete = true
      this.selectedUser = name
    } ,
    removeUser () {
      this.deleteUser(this.selectedUser).then(() => {
        this.error = null
        this.dialogDelete = false
      }).catch((error) => {
        this.error = error
        this.dialogDelete = false
      })
    }
  },
  created () {
    this.loadUsers()
  }
}

</script>
