<template>
<v-container>
  <v-layout align-center justify-center>
    <v-flex xs12 sm8 md4>
      <v-card>
        <v-card-text>
          <v-form @keyup.native.enter="login">
            <v-text-field v-model="username"
                          prepend-icon="person" name="username" label="Username" type="text"></v-text-field>
            <v-text-field v-model="password"
                          prepend-icon="lock" name="password" label="Password" id="password" type="password"></v-text-field>
          </v-form>
        </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" :loading="loading" :disabled="loading" @click="login">Login</v-btn>
          </v-card-actions>
        </v-card>
        <v-alert v-model="unsuccessfull" dismissible type="error">Login unsuccessfull. {{ error }}</v-alert>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'LoginForm',
  data: () => ({
    username: null,
    password: null,
    unsuccessfull: false,
    error: '',
    loading: false
  }),
  methods: {
    ...mapActions({
      fetchJWT: 'login/fetchJWT',
      testJWT: 'login/testJWT',
      clearJWT: 'login/clearJWT'
    }),
    invalid () {
      if (this.username && this.password) {
        return false
      }
      return true
    },
    login () {
      this.unsuccessfull = false

      if (this.invalid()) {
        this.unsuccessfull = true
        this.password = null
        this.error = 'Please enter username and password.'
        return
      }

      // Get the JWT and redirect
      this.loading = true
      this.fetchJWT({ username: this.username, password: this.password }).then(() => {
        this.$router.push('/profile')
      }).catch((error) => {
        this.error = error
        this.password = null
        this.unsuccessfull = true
      })
      this.loading = false
    }
  }
}
</script>

<style>

</style>
