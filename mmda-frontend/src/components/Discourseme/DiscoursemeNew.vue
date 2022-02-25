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
                <h1 class="title">{{ $t("discourseme.new.helpTitle") }}</h1>
                <p>
                  {{ $t("discourseme.new.helpText") }}
                </p>

                <h1 class="subheading">{{ $t("discourseme.new.name") }}</h1>
                <p>
                  {{ $t("discourseme.new.helpName") }}
                </p>

                <h1 class="subheading">{{ $t("discourseme.new.items") }}</h1>
                <p>
                  {{ $t("discourseme.new.helpItems") }}
                </p>

              </v-flex>

              <v-flex xs6 sm6>
                <div v-if="loading" class="text-md-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>Generating Discourseme...</p>
                </div>
                <v-form v-else>
                  <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Please enter missing data</v-alert>
                  <v-alert v-if="error" value="true" color="error" icon="priority_high" outline>Error during Discourseme creation</v-alert>
                  <v-text-field v-model="name" label="name" :rules="[rules.required, rules.counter]"></v-text-field>
                  <v-combobox v-model="select" :items="items" label="items" :rules="[rules.required, rules.counter]" multiple chips ></v-combobox>
                  <v-layout row>
                    <v-spacer/>
                    <v-btn color="info" class="text-lg-right" @click="clear">Clear</v-btn>
                    <v-btn color="success" class="text-lg-right" @click="addDiscourseme">Submit</v-btn>
                  </v-layout>
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
  name: 'DiscoursemeNewContent',
  data: () => ({
    error: null,
    loading: false,
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
    clear () {
      this.error = null
      this.select = []
      this.name = ''
    },
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

      this.loading = true
      this.addUserDiscourseme(data).then(() => {
        this.error = null
        this.$router.push('/discourseme')
      }).catch((error) => {
        this.error = error
      }).then(() => {
        this.loading = false
      })
    }
  }
}

</script>
