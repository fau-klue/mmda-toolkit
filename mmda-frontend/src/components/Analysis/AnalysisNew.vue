<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout>
              <v-flex xs12 sm12>
                <h1 class="display-1"> {{ $t("analysis.newAnalysis") }} </h1>
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
                <h1 class="title">{{ $t("analysis.new.helpTitle") }}</h1>
                <p>
                  {{ $t("analysis.new.helpText") }}
                </p>

                <h1 class="subheading">Name</h1>
                <p>
                  {{ $t("analysis.new.helpName") }}
                </p>

                <h1 class="subheading">Corpus</h1>
                <p>
                  {{ $t("analysis.new.helpCorpus") }}
                </p>

                <h1 class="subheading">Items</h1>
                <p>
                  {{ $t("analysis.new.helpItems") }}
                </p>

                <h1 class="subheading">Window Size</h1>
                <p>
                  {{ $t("analysis.new.helpWindowSize") }}
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
                  <v-container>
                    <h1 class="title">Advanced Options</h1>

                    <!-- <AnalysisPosTagsSelection/>  -->
                  </v-container>
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
//import AnalysisPosTagsSelection from "@/components/Analysis/AnalysisPosTagsSelection";

export default {
  name: 'AnalysisNewContent',
  components:{
    //AnalysisPosTagsSelection
  },
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
    selectWindow: 3,
    rules: rules,
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
      this.selectWindow = 3
    },
    addAnalysis () {
      this.nodata = false

      if (!this.name || this.selectItems.length === 0 || !this.selectCorpus) {
        this.nodata = true
        return
      }

      this.loading = true
      const data = {
        username: this.user.username,
        name: this.name,
        items: this.selectItems,
        window_size: this.selectWindow,
        corpus: this.selectCorpus
      }

      this.addUserAnalysis(data).then(() => {
        this.error = null
        this.$router.push('/analysis')
      }).catch((error) => {
        this.error = error
      }).then(() => {
        this.loading = false
      })

    }
  },
  created () {
    this.getCorpora().then(() => {
      this.error = null
    }).catch((error) => {
      this.error = error
    }).then(() => {
      this.loading = false
    })
  }
}

</Script>
