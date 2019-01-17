<template>
<div>
  <h1 class="title">Add new user</h1>

  <v-form>
    <v-text-field v-model="newUser.username" label="Username" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
    <v-text-field v-model="newUser.first_name" label="First Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
    <v-text-field v-model="newUser.last_name" label="Last Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
    <v-text-field v-model="newUser.email" label="Email" :rules="[rules.required, rules.email, rules.counter]"></v-text-field>

    <v-text-field
      v-model="newUser.password"
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

    <v-btn color="success" @click="">Add User</v-btn>
  </v-form>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import rules from '@/utils/validation'

export default {
  name: 'AdminUsersNew',
  data: () => ({
    loading: false,
    error: null,
    rules: rules,
    newPasswordRepeat: '',
    showPassword: false,
    newUser: {
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      password: '',
    }
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
    })
  },
  methods: {
    invalid () {
      if (!this.newUser.password || !this.newPasswordRepeat) {
        return true
      }
      if (this.newUser.password === this.newPasswordRepeat) {
        return false
      }
      return true
    },
    addNewUser () {
      this.loading = true
      this.loading = false
    }
  }
}

</script>
