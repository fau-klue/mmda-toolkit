<template>
<v-container grid-list-md>
  <!-- heading -->
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
  <!-- content -->
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout justify-space-between row>
              <v-flex xs5 sm5>
                
                <!-- left box: explanations -->
                <h1 class="title">{{ $t("analysis.new.helpTitle") }}</h1>
                <p>
                  {{ $t("analysis.new.helpText") }}
                </p>

                <h1 class="subheading">{{ $t("analysis.new.name") }}</h1>
                <p>
                  {{ $t("analysis.new.helpName") }}
                </p>

                <h1 class="subheading">{{ $t("analysis.new.corpus") }}</h1>
                <p>
                  {{ $t("analysis.new.helpCorpus") }}
                </p>

                <h1 class="subheading">{{ $t("analysis.new.items") }}</h1>
                <p>
                  {{ $t("analysis.new.helpItems") }}
                </p>

                <h1 class="subheading">{{ $t("analysis.new.pquery") }}</h1>
                <p>
                  {{ $t("analysis.new.helpPQuery") }}
                </p>

                <h1 class="subheading">{{ $t("analysis.new.sbreak") }}</h1>
                <p>
                  {{ $t("analysis.new.helpSBreak") }}
                </p>

                <h1 class="subheading">{{ $t("analysis.new.windowSize") }}</h1>
                <p>
                  {{ $t("analysis.new.helpWindowSize") }}
                </p>

              </v-flex>

              <!-- right box: input field -->
              <v-flex xs6 sm6>
                <div v-if="loading" class="text-md-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>... querying corpus and creating semantic space ...</p>
                </div>
                <v-form v-else>
                  <v-alert v-if="error" value="true" color="error" icon="priority_high" outline>{{ error }}</v-alert>

                  <v-combobox
                    class="col-5"
                    v-model="selectDiscourseme"
                    :items="userDiscoursemes"
                    label="discourseme"
                    item-text="name"
                    :rules="[rules.required]"
                    ></v-combobox>
                  <v-autocomplete
                    v-model="selectCorpus"
                    clearable
                    :items="corpora"
                    item-value="name_api"
                    item-text="name"
                    label="corpus"
                    ></v-autocomplete>
                  <v-combobox
                    v-model="selectItems"
                    :items="items"
                    label="items"
                    :rules="[rules.required, rules.counter]"
                    multiple
                    chips
                    ></v-combobox>
                  <v-layout row>
                    <v-combobox
                      class="col-5"
                      v-model="pQuery"
                      :items="pQueries"
                      label="query layer (p-att)"
                      :rules="[rules.required, rules.alphanum, rules.counter]"
                      ></v-combobox><v-spacer/>
                    <v-combobox
                      class="col-5"
                      v-model="sBreak"
                      :items="sBreaks"
                      label="context break (s-att)"
                      :rules="[rules.required, rules.alphanum, rules.counter]"
                      ></v-combobox>
                  </v-layout>
                  <v-slider
                    v-model="selectWindow"
                    :max="max"
                    :min="min"
                    thumb-label="always"
                    label="context"
                    ></v-slider>
                  <v-btn color="success" class="text-lg-right" @click="addAnalysis">Submit</v-btn>
                  <v-btn color="info" class="text-lg-right" @click="clear">Clear</v-btn>
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
    min: 1,
    max: 25,
    name: 'untitled',           // TODO: make configurable
    pQuery: '',
    sBreak: '',
    pQueries: [],
    sBreaks: [],
    selectCorpus: '',
    selectItems: [],
    selectWindow: 10,
    selectDiscourseme: '',
    rules: rules,
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      corpora: 'corpus/corpora',
      analysis: 'analysis/analysis',
      userDiscoursemes: 'discourseme/userDiscoursemes',
    })
  },
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
    }
  },
  methods: {
    ...mapActions({
      getCorpora: 'corpus/getCorpora',
      getUserDiscoursemes: 'discourseme/getUserDiscoursemes',
      addUserAnalysis: 'analysis/addUserAnalysis'
    }),
    error_message_for(error, prefix, codes){
      ///// short for:
      //if(error.response){
      //  switch(error.response.status){
      //    case 400: this.error = this.$t("analysis.new.invalid_input"); break;
      //    case 404: this.error = this.$t("analysis.new.no_collocates"); break;
      //    default: this.error = error.message;
      //  }
      //}else this.error = error.message
      if( error.response ){
        let value = codes[ error.response.status ];
        if( value ) return this.$t( prefix+value );
      }
      return error.message;
    },
    clear () {
      this.error = null
      this.items = []
      this.pQuery = 'word'
      this.sBreak = 's'
      this.selectCorpus = ''
      this.selectItems = []
      this.selectWindow = 10,
      this.selectDiscourseme = ''
    },
    addAnalysis () {
      this.error = null;

      if ( this.selectItems.length === 0 || !this.selectCorpus) {
        this.error = this.$t("analysis.new.missing_data")
        return
      }

      this.loading = true
      const data = {
        username: this.user.username,
        name: this.name,
        items: this.selectItems,
        context: this.selectWindow,
        p_query: this.pQuery,
        s_break: this.sBreak,
        corpus: this.selectCorpus,
        discourseme: this.selectDiscourseme
      }

      this.addUserAnalysis(data).then(() => {
        this.error = null
        this.$router.push('/analysis')
      }).catch((error) => {
        this.error = this.error_message_for(error,"analysis.new.",{
          400:"invalid_input",
          404:"no_collocates",
          "TODO":"no_topic"
          });
      }).then(() => {
        this.loading = false
      })
    },
    getParametersFromRoute(){
      let r = this.$route.query
      if(r.discourseme) {
        this.selectDiscourseme = this.userDiscoursemes.find(
          (o)=>o.id == r.discourseme
        )
      }
      if(r.window) this.selectWindow = Number.parseInt(r.window)
      if(r.corpus) this.selectCorpus = r.corpus
      if(r.item){
        if(typeof r.item === 'string') this.selectItems = [r.item]
        else                           this.selectItems = r.item
      }
    }
  },
  created () {
    this.getUserDiscoursemes(this.user.username)
    this.getCorpora().then(() => {
      this.error = null
      this.getParametersFromRoute();
    }).catch((error) => {
      this.error = this.error_message_for(error,"",{});
    }).then(() => {
        this.loading = false
    })
  }
}

</script>
