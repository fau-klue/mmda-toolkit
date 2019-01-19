<template>
  <v-container grid-list-md>
    <v-layout wrap row>
      <v-flex xs12>
        <v-card flat>
          <v-card-text>
            <v-container>
              <v-layout>
                <v-flex xs12 sm12>
                  <h1 class="display-1">New User</h1>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout wrap row>
      <v-flex xs12>
        <v-card flat>
          <v-card-text>
            <v-container>
              <v-layout justify-space-between row>
                <v-flex xs12 sm12>
                  <v-form>
                    <v-alert v-model="warn" type="warning" dismissible outline>Passwords do not match.</v-alert>

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

                  <v-btn color="success" @click="addNewUser">Add User</v-btn>
                </v-form>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</v-container>

</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import rules from '@/utils/validation'

export default {
  name: 'AdminUserNew',
  data: () => ({
    loading: false,
    error: null,
    warn: false,
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
      user: 'login/user'
    })
  },
  methods: {
    ...mapActions({
      createNewUser: 'admin/createNewUser'
    }),
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
      this.warn = false

      if (this.invalid()) {
        this.warn = true
        this.newPassword = ''
        this.newPasswordRepeat = ''
        return
      }

      this.createNewUser(this.newUser).then(() => {
        this.error = null
        this.$router.push('/admin/users')
      }).catch((error) => {
        this.error = error
      })
    }
  }
}

</script>
