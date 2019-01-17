<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <v-form v-if="userProfile">
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
      getUserProfile: 'profile/getUserProfile'
    }),
    loadProfile () {
      this.getUserProfile(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    updateProfile () {
      // const newProfile = {
      //   firstName: '',
      //   lastName: '',
      //   email: ''
      // }
    }
  },
  created () {
    this.loadProfile()
  }
}

</script>
