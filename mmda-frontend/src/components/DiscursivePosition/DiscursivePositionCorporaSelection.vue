<template>
<div>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout justify-space-between row>
              <v-flex xs5 sm5>
                <h1 class="title">Discursive Position Collocate Extraction</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
                <h1 class="subheading">Corpora</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>
                <h1 class="subheading">Analysis</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>

              </v-flex>
              <v-flex xs6 sm6>
                <v-form>
                  <v-select
                    v-model="selectedCorpora"
                    :items="corpora"
                    label="Corpora"
                    item-value="name_api"
                    item-text="name"
                    multiple
                    chips
                    persistent-hint
                    ></v-select>

                  <v-autocomplete v-model="selectedAnalysis" clearable :items="userAnalysis" item-text="name" label="Analysis"></v-autocomplete>

                  <v-btn color="success" class="text-lg-right">Submit</v-btn>
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
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'DiscursivePositionCorporaSelection',
  data: () => ({
    error: null,
    loading: false,
    nodata: false,
    selectedCorpora: [],
    selectedAnalysis: null
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      corpora: 'corpus/corpora',
      userAnalysis: 'analysis/userAnalysis',
    })
  },
  methods: {
    ...mapActions({
      getCorpora: 'corpus/getCorpora',
      getUserAnalysis: 'analysis/getUserAnalysis'
    }),
    clear () {
      this.error = null
      this.nodata = false
      this.selectedAnalysis = null,
      this.selectedCorpora = []
    },
    clearSearch () {
      this.search = ''
    },
    loadAnalysis () {
      this.getUserAnalysis(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    loadCorpora () {
      this.getCorpora().then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.loadAnalysis()
    this.loadCorpora()
  }
}

</script>
