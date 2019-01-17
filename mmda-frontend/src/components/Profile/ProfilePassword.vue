<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <v-alert v-model="warn" type="warning" dismissible outline>Passwords do not match.</v-alert>
          <v-alert v-model="success" type="success" dismissible outline>Password changed.</v-alert>
          <v-alert v-model="error" type="error" dismissible>An error occured.</v-alert>

          <v-form v-if="userProfile">
            <v-text-field
              v-model="newPassword"
              :append-icon="showPassword ? 'visibility_off' : 'visibility'"
              :type="showPassword ? 'text' : 'password'"
              name="inputNewPassword"
              label="New Password"
              :rules="[rules.required, rules.minlength8]"
              counter @click:append="showPassword = !showPassword"
              ></v-text-field>

            <v-text-field
              v-model="newPasswordRepeat"
              :append-icon="showPassword ? 'visibility_off' : 'visibility'"
              :type="showPassword ? 'text' : 'password'"
              name="inputNewPasswordRepeat"
              label="Repeat new password"
              :rules="[rules.required, rules.minlength8]"
              counter @click:append="showPassword = !showPassword"
              ></v-text-field>
            <v-btn color="success" @click="changePassword">Change Password</v-btn>
          </v-form>
          <div v-else>
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
    warn: false,
    success: false,
    showPassword: false,
    newPassword: '',
    newPasswordRepeat: '',
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
      updateUserPassword: 'profile/updateUserPassword'
    }),
    invalid () {
      if (!this.newPassword || !this.newPasswordRepeat) {
        return true
      }
      if (this.newPassword === this.newPasswordRepeat) {
        return false
      }
      return true
    },
    changePassword () {
        this.warn = false
        this.success = false

      if (this.invalid()) {
        this.warn = true
        this.newPassword = ''
        this.newPasswordRepeat = ''
        return
      }

      const data = {
        username: this.user.username,
        password: this.newPassword
      }

      this.updateUserPassword(data).then(() => {
        this.error = null
        this.success = true
      }).catch((error) => {
        this.error = error
      })

      this.newPassword = null
      this.newPasswordRepeat = null

    }
  }
}

</script>
