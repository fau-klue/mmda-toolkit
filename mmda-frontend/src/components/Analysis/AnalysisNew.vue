<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout>
              <v-flex xs12 sm12>
                <h1 class="display-1">New Analysis</h1>
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
                <h1 class="title">What is an Analysis?</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>

                <h1 class="subheading">Name</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>


                <h1 class="subheading">Corpus</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>

                <h1 class="subheading">Items</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>

                <h1 class="subheading">Window Size</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>

              </v-flex>

              <v-flex xs6 sm6>
                <div v-if="loading" class="text-md-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>Generating Analysis...</p>
                </div>
                <v-form v-else>
                  <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Please enter missing data</v-alert>
                  <v-alert v-if="error" value="true" color="error" icon="priority_high" outline>Error during Analysis creation</v-alert>

                  <v-text-field v-model="name" label="Analysis Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
                  <v-autocomplete v-model="selectCorpus" clearable :items="corpora" item-value="name_api" item-text="name" label="Corpus"></v-autocomplete>
                  <v-combobox
                    v-model="selectItems"
                    :items="items"
                    label="Topic Items"
                    :rules="[rules.required, rules.alphanum, rules.counter]"
                    multiple
                    chips
                    ></v-combobox>

                  <v-slider v-model="selectWindow" :max="max" :min="min" thumb-label="always" label="Window Size"></v-slider>

                  <v-btn color="success" class="text-lg-right" @click="addAnalysis">Submit</v-btn>
                  <v-btn color="info" outline class="text-lg-right" @click="clear">Clear</v-btn>
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
  name: 'AnalysisNewContent',
  data: () => ({
    error: null,
    items: [],
    loading: false,
    min: 2,
    max: 20,
    name: '',
    nodata: false,
    selectCorpus: '',
    selectItems: [],
    selectWindow: 8,
    rules: rules
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      corpora: 'corpus/corpora'
    })
  },
  methods: {
    ...mapActions({
      getCorpora: 'corpus/getCorpora',
      getUserAnalysis: 'analysis/getUserAnalysis',
      addUserAnalysis: 'analysis/addUserAnalysis'
    }),
    clear () {
      this.error = null
      this.nodata = false
      this.items = []
      this.name = ''
      this.selectCorpus = ''
      this.selectItems = []
      this.selectWindow = 8
    },
    addAnalysis () {
      this.nodata = false

      if (!this.name || this.selectItems.length === 0 || !this.selectCorpus) {
        this.nodata = true
        return
      }

      const data = {
        username: this.user.username,
        name: this.name,
        items: this.selectItems,
        window_size: this.selectWindow,
        corpus: this.selectCorpus
      }

      this.loading = true
      this.addUserAnalysis(data).then(() => {
        this.error = null
        this.$router.push('/analysis')
      }).catch((error) => {
        this.error = error
      })
      this.loading = false
    }
  },
  created () {
    this.getCorpora().then(() => {
      this.error = null
    }).catch((error) => {
      this.error = error
      })
  }
}

</Script>
