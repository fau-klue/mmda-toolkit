<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout>
              <v-flex xs12 sm12>
                <h1 class="display-1">New Discourseme</h1>
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
              <v-flex xs5 sm5>
                <h1 class="title">What is a Discourseme?</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>

                <h1 class="subheading">Name</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>

                <h1 class="subheading">Items</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>

              </v-flex>
              <v-flex xs6 sm6>
                <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>
                <v-form>
                  <v-text-field v-model="name" label="Discourseme Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
                  <v-combobox
                    v-model="select"
                    :items="items"
                    label="Discourseme Items"
                    :rules="[rules.required, rules.alphanum, rules.counter]"
                    multiple
                    chips
                    ></v-combobox>
                </v-form>
                <v-btn color="success" class="text-lg-right" @click="addDiscourseme">Submit</v-btn>
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
  name: 'DiscoursemeNewContent',
  data: () => ({
    error: null,
    items: [],
    name: '',
    nodata: false,
    select: [],
    rules: rules
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
    })
  },
  methods: {
    ...mapActions({
      addUserDiscourseme: 'discourseme/addUserDiscourseme'
    }),
    addDiscourseme () {
      this.nodata = false

      if (!this.name || this.select.length === 0) {
        this.nodata = true
        return
      }

      const data = {
        name: this.name,
        items: this.select,
        username: this.user.username
      }

      this.addUserDiscourseme(data).then(() => {
        this.error = null
        this.$router.push('/discourseme')
      }).catch((error) => {
        this.error = error
      })
    }
  }
}

</script>
