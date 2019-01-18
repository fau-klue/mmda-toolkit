<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <v-form v-if="userProfile">
            <v-alert v-if="updated" value="true" dismissible color="success" icon="info" outline>Updated Profile</v-alert>
            <v-alert v-if="error" value="true" dismissible color="warning" icon="priority_high" outline>Could not update Profile</v-alert>

            <v-text-field v-model="userProfile.id" box label="ID" readonly></v-text-field>
            <v-text-field v-model="userProfile.first_name" label="First Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
            <v-text-field v-model="userProfile.last_name" label="Last Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
            <v-text-field v-model="userProfile.email" label="Email" :rules="[rules.required, rules.email, rules.counter]"></v-text-field>

            <v-btn color="success" @click="updateProfile">Update profile</v-btn>
          </v-form>
          <div v-else>
            <v-alert v-model="error" type="error" dismissible>Could not load profile</v-alert>
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>
        </v-flex>
      </v-layout>
    </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import rules from '@/utils/validation'

export default {
  name: 'ProfileContent',
  data: () => ({
    error: null,
    updated: false,
    rules: rules
  }),
  computed: {
    ...mapGetters({
      userProfile: 'profile/userProfile',
      user: 'login/user'
    })
  },
  methods: {
    ...mapActions({
      getUserProfile: 'profile/getUserProfile',
      updateUserProfile: 'profile/updateUserProfile'
    }),
    loadProfile () {
      this.getUserProfile(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    updateProfile () {
      const data = {
        username: this.user.username,
        first_name: this.userProfile.first_name,
        last_name: this.userProfile.last_name,
        email: this.userProfile.email
      }
      this.updateUserProfile(data).then(() => {
        this.updated = true
        this.error = null
      }).catch((error) => {
        this.error = error
      })

    }
  },
  created () {
    this.loadProfile()
  }
}

</script>
