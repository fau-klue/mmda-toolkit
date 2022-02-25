<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout>
              <v-flex xs12 sm12>
                <h1 class="display-1">New Discourseme Constellation</h1>
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
                <h1 class="title">{{ $t("constellation.new.helpTitle") }}</h1>
                <p>
                  {{ $t("constellation.new.helpText") }}
                </p>

                <h1 class="subheading">{{ $t("constellation.new.name") }}</h1>
                <p>
                  {{ $t("constellation.new.helpName") }}
                </p>

                <h1 class="subheading">{{ $t("constellation.new.discoursemes") }}</h1>
                <p>
                  {{ $t("constellation.new.helpDiscoursemes") }}
                </p>

              </v-flex>
              <v-flex xs6 sm6>
                <div v-if="loading" class="text-md-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>Generating Constellation ...</p>
                </div>
                <v-form v-else>
                  <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Please enter missing data</v-alert>
                  <v-alert v-if="error" value="true" color="error" icon="priority_high" outline>Error during Constellation creation</v-alert>

                  <v-text-field v-model="name" label="Constellation Name" :rules="[rules.required, rules.counter]"></v-text-field>
                  <v-combobox v-model="selectDiscoursemes" :items="userDiscoursemes" item-text="name" label="Discoursemes" multiple chips ></v-combobox>

                  <v-layout row>
                    <v-spacer/>
                    <v-btn color="info" class="text-lg-right" @click="clear">Clear</v-btn>
                    <v-btn color="success" class="text-lg-right" @click="addConstellation">Submit</v-btn>
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
  name: 'ConstellationNewContent',
  data: () => ({
    error: null,
    loading: false,
    name: '',
    nodata: false,
    selectDiscoursemes: [],
    rules: rules
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      userDiscoursemes: 'discourseme/userDiscoursemes'
    })
  },
  methods: {
    ...mapActions({
      addUserConstellation: 'constellation/addUserConstellation'
    }),
    clear () {
      this.error = null
      this.nodata = false
      this.name = ''
      this.selectDiscoursemes = []
    },
    addConstellation () {
      this.nodata = false

      if (!this.name || this.selectDiscoursemes.length === 0) {
        this.nodata = true
        return
      }

      const data = {
        username: this.user.username,
        name: this.name,
        discoursemes: this.selectDiscoursemes.map(item => item.id)
      }

      this.loading = true
      this.addUserConstellation(data).then(() => {
        this.error = null
        this.$router.push('/constellation')
      }).catch((error) => {
        this.error = error
      }).then(() => {
        this.loading = false
      })
    }
  }
}

</Script>
