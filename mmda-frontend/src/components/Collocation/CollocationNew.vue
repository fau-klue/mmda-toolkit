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
                <h1 class="display-1">New Collocation Analysis</h1>
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

                <h1 class="title">{{ $t("collocation.new.helpTitle") }}</h1>
                <p>
                  {{ $t("collocation.new.helpText") }}
                </p>

                <h1 class="subheading">{{ $t("collocation.new.corpus") }}</h1>
                <p>
                  {{ $t("collocation.new.helpCorpus") }}
                </p>

                <h1 class="subheading">{{ $t("collocation.new.name") }}</h1>
                <p>
                  {{ $t("collocation.new.helpName") }}
                </p>

                <h1 class="subheading">{{ $t("collocation.new.items") }}</h1>
                <p>
                  {{ $t("collocation.new.helpItems") }}
                </p>

                <h1 class="subheading">{{ $t("collocation.new.pQuery") }}</h1>
                <p>
                  {{ $t("collocation.new.helpPQuery") }}
                </p>

                <h1 class="subheading">{{ $t("collocation.new.pCollocation") }}</h1>
                <p>
                  {{ $t("collocation.new.helpPCollocation") }}
                </p>

                <h1 class="subheading">{{ $t("collocation.new.sBreak") }}</h1>
                <p>
                  {{ $t("collocation.new.helpSBreak") }}
                </p>

                <h1 class="subheading">{{ $t("collocation.new.windowSize") }}</h1>
                <p>
                  {{ $t("collocation.new.helpWindowSize") }}
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

                  <v-autocomplete v-model="selectCorpus" clearable :items="corpora" item-value="name_api" item-text="name" label="corpus" :rules="[rules.required]"></v-autocomplete>

                  <v-combobox class="col-5" v-model="selectDiscourseme" :items="userDiscoursemes" label="discourseme" item-text="name" :rules="[rules.required]"></v-combobox>

                  <v-combobox v-model="selectItems" :items="items" label="items" :rules="[rules.required, rules.counter]" multiple chips ></v-combobox>

                  <v-layout row>
                    <v-flex xs6>
                      <v-combobox class="col-6" v-model="pQuery" :items="pQueries" label="query layer (p-att)" :rules="[rules.alphanum, rules.counter]" ></v-combobox>
                    </v-flex>
                    <v-flex xs6>
                      <v-combobox class="col-6" v-model="pCollocation" :items="pCollocations" label="collocation layer (p-att)" :rules="[rules.required, rules.alphanum, rules.counter]" ></v-combobox>
                    </v-flex>                      
                  </v-layout>

                  <v-layout row>
                    <v-flex xs6>
                      <v-combobox class="col-6" v-model="sBreak" :items="sBreaks" label="context break (s-att)" :rules="[rules.required, rules.alphanum, rules.counter]" ></v-combobox>
                    </v-flex>
                    <v-flex xs6>
                      <v-slider v-model="selectWindow" inverse-label ticks="always" :min="min" :max="max" thumb-label="always" label="context" ></v-slider>
                    </v-flex>
                  </v-layout>

                  <v-layout row>
                    <v-spacer/>
                    <v-btn color="info" class="text-lg-right" @click="clear">Clear</v-btn>
                    <v-btn color="success" class="text-lg-right" @click="addCollocation">Submit</v-btn>
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
  name: 'CollocationNewContent',
  data: () => ({
    error: null,
    items: [],
    loading: false,
    min: 1,
    max: 25,
    name: 'untitled',           // TODO: make configurable
    pQuery: '',
    pCollocation: '',
    sBreak: '',
    pQueries: [],
    pCollocations: [],
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
      collocation: 'collocation/collocation',
      userDiscoursemes: 'discourseme/userDiscoursemes',
    })
  },
  watch: {
    selectCorpus(){
      let C = this.corpora.find((o)=>o.name_api == this.selectCorpus);
      if(C){
        this.pQueries = C.pQueries
        this.pCollocations = C.pQueries
        this.sBreaks = C.sBreaks
        if(C.p_att){
          if(typeof C.p_att ==='string'){
            this.pQueries = [C.p_att];
            this.pCollocations = [C.p_att];
          }else if(typeof C.p_att === 'object' && C.p_att[0]){
            this.pQueries = C.p_att;
            this.pCollocations = C.p_att;
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
      this.pCollocation = this.pCollocations[0]
      this.sBreak = this.sBreaks[0]
    },
    selectDiscourseme(){
      this.selectItems = this.selectDiscourseme.items
    }
  },
  methods: {
    ...mapActions({
      getCorpora: 'corpus/getCorpora',
      getUserDiscoursemes: 'discourseme/getUserDiscoursemes',
      addUserCollocation: 'collocation/addUserCollocation'
    }),
    error_message_for(error, prefix, codes){
      if( error.response ){
        let value = codes[ error.response.status ];
        if( value ) return this.$t( prefix+value );
      }
      return error.message;
    },
    clear () {
      this.error = null
      this.items = []
      this.pQuery = ''
      this.sBreak = ''
      this.pCollocation = ''
      this.selectCorpus = ''
      this.selectItems = []
      this.selectWindow = 10,
      this.selectDiscourseme = ''
    },
    addCollocation () {
      this.error = null;

      if ( this.selectItems.length === 0 || !this.selectCorpus) {
        this.error = this.$t("collocation.new.missing_data")
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
        p_collocation: this.pCollocation,
        corpus: this.selectCorpus,
        discourseme: this.selectDiscourseme
      }

      this.addUserCollocation(data).then(() => {
        this.error = null
        this.$router.push('/collocation')
      }).catch((error) => {
        this.error = this.error_message_for(error,"collocation.new.",{
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
