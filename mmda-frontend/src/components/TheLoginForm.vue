<template>
<v-container>
  <v-layout align-center justify-center>
    <v-flex xs12 sm8 md4>
      <v-card>
        <v-card-text>
          <v-form @keyup.native.enter="login">
            <v-text-field v-model="username" prepend-icon="person" name="username" label="Username" type="text">
              <template slot="label">
                {{ $t("login.username") }}
              </template>
            </v-text-field>
            <v-text-field v-model="password" prepend-icon="lock" name="password" id="password" type="password">
              <template slot="label">
                {{ $t("login.password") }}
              </template>
            </v-text-field>
          </v-form>
        </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" :loading="loading" :disabled="loading" @click="login">Login</v-btn>
          </v-card-actions>
        </v-card>
        <v-alert v-model="show_error" dismissible type="error">{{ error }} </v-alert>
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
    show_error: false,
    error: '',
    loading: false
  }),
  methods: {
    ...mapActions({
      fetchJWT: 'login/fetchJWT',
      testJWT: 'login/testJWT',
      clearJWT: 'login/clearJWT'
    }),
    error_message_for(error, prefix, codes){
      if( error.response ){
        let value = codes[ error.response.status ];
        if( value ) return this.$t( prefix+value );
      }
      return error.message;
    },
    invalid () {
      if (this.username && this.password) {
        return false
      }
      return true
    },
    login () {
      this.show_error = false

      if( this.invalid() ) {
        this.password = null
        this.show_error = true
        this.error = this.$t("login.missing_input") //'Please enter username and password.'
        return
      }

      // Get the JWT and redirect
      this.loading = true
      this.fetchJWT({ username: this.username, password: this.password }).then(() => {
        this.$router.push('/profile')
      }).catch((error) => {
        this.error = this.error_message_for(error,"login.",{400:"bad_request",401:"unauthorized"});
        this.password = null
        this.show_error = true
      }).then(() => {
        this.loading = false
      })
    }
  }
}
</script>

<style>

</style>
