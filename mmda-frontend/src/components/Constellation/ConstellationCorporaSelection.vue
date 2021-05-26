<template>
<div>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout justify-space-between row>
              <v-flex xs5 sm5>
                <h1 class="title">{{ $t("constellation.extraction.helpTitle") }}</h1>
                <p>
                  {{ $t("constellation.extraction.helpText") }}
                </p>
                <h1 class="subheading">{{ $t("analysis.new.corpus") }}</h1>
                <p>
                  {{ $t("analysis.new.helpCorpus") }}
                </p>
                <h1 class="subheading">{{ $t("analysis.new.pQuery") }}</h1>
                <p>
                  {{ $t("analysis.new.helpPQuery") }}
                </p>
                <h1 class="subheading">{{ $t("analysis.new.sBreak") }}</h1>
                <p>
                  {{ $t("analysis.new.helpSBreak") }}
                </p>

              </v-flex>
              <v-flex xs6 sm6>
                <div v-if="loading" class="text-md-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>Collecting discoursemes in corpus ...</p>
                </div>

                <v-form v-else>
                  <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Please enter missing data</v-alert>
                  <v-alert v-if="error" value="true" color="error" icon="priority_high" outline>Error during Concordance extraction</v-alert>
                  
                  <v-autocomplete v-model="selectCorpus" clearable :items="corpora" item-value="name_api" item-text="name" label="corpus"></v-autocomplete>
                  <v-layout row>
                    <v-combobox class="col-5" v-model="pQuery" :items="pQueries" label="query layer (p-att)" :rules="[rules.alphanum, rules.counter]" ></v-combobox><v-spacer/>
                    <v-combobox class="col-5" v-model="sBreak" :items="sBreaks" label="context break (s-att)" :rules="[rules.required, rules.alphanum, rules.counter]" ></v-combobox>
                  </v-layout>
                  <v-layout row>
                    <v-btn color="info" class="text-lg-right" @click="clear">Clear</v-btn>
                    <v-spacer/>
                    <v-btn color="success" class="text-lg-right" @click="loadAssociations">Analyze</v-btn>
                  </v-layout>
                </v-form>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import rules from '@/utils/validation'

export default {
  name: 'ConstellationCorporaSelection',
  data: () => ({
    id: null,
    error: null,
    loading: false,
    nodata: false,
    selectCorpus: '',
    sBreak: '',
    sBreaks: [],
    pQuery: '',
    pQueries: [],
    rules: rules
  }),
  watch: {
    selectCorpus(){
      let C = this.corpora.find((o)=>o.name_api == this.selectCorpus);
      if(C){
        this.pQueries = C.pQueries
        this.sBreaks = C.sBreaks
        if(C.p_att){
          if(typeof C.p_att ==='string'){
            this.pQueries = [C.p_att];
          }else if(typeof C.p_att === 'object' && C.p_att[0]){
            this.pQueries = C.p_att;
          }
        }
        if(C.s_att){
          if(typeof C.s_att ==='string'){
            this.sBreaks = [C.s_att];
          }else if(typeof C.s_att === 'object' && C.s_att[0]){
            this.sBreaks = C.s_att;
          }
        }
      }
      this.pQuery = this.pQueries[0]
      this.sBreak = this.sBreaks[0]
    },
  },
  computed: {
    ...mapGetters({
      user: 'login/user',
      corpora: 'corpus/corpora'
    })
  },
  methods: {
    ...mapActions({
      getCorpora: 'corpus/getCorpora',
      getConstellationConcordances: 'constellation/getConstellationConcordances',
      getConstellationAssociations: 'constellation/getConstellationAssociations',
      resetConstellationConcordances: 'constellation/resetConstellationConcordances',
      resetConstellationAssociations: 'constellation/resetConstellationAssociations',
    }),
    clear () {
      this.error = null
      this.nodata = false
      this.selectCorpus = ''
      this.pQuery = ''
      this.sBreak = ''
    },
    loadCorpora () {
      this.getCorpora().then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    loadAssociations () {

      this.resetConstellationConcordances()
      this.resetConstellationAssociations()
      
      this.nodata = false

      if (this.selectCorpus.length === 0) {
        this.nodata = true
        return
      }
      this.loading = true

      const data = {
        username: this.user.username,
        constellation_id: this.id,
        pQuery: this.pQuery,
        sBreak: this.sBreak,
        corpus: this.selectCorpus
      }

      this.getConstellationConcordances(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })

      this.getConstellationAssociations(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      }).then(() => {
        this.loading = false
      })

    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadCorpora()
    this.resetConstellationConcordances()
    this.resetConstellationAssociations()
  }
}

</script>
