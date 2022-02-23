<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout>
              <v-flex xs12 sm12>
                <h1 class="display-1">New Keyword Analysis</h1>
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
                
                <!-- left box: explanations -->
                <h1 class="title">{{ $t("keyword.new.title") }}</h1>
                <p>
                  {{ $t("keyword.new.helpTitle") }}
                </p>
                
                <h1 class="subheading">{{ $t("keyword.new.corpus") }}</h1>
                <p>
                  {{ $t("keyword.new.helpCorpus") }}
                </p>
                
                <h1 class="subheading">{{ $t("keyword.new.p") }}</h1>
                <p>
                  {{ $t("keyword.new.helpP") }}
                </p>
                
              </v-flex>
              
              <!-- right box: input field -->
              <v-flex xs6 sm6>
                <div v-if="loading" class="text-md-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>... comparing frequencies and creating semantic space ...</p>
                </div>
                <v-form v-else>
                  <v-alert v-if="error" value="true" color="error" icon="priority_high" outline>{{ error }}</v-alert>
                  
                  <v-layout row>
                    <v-flex xs6>
                      <v-autocomplete v-model="selectCorpus" clearable :items="corpora" item-value="name_api" item-text="name" label="target" :rules="[rules.required]"></v-autocomplete>
                      <v-combobox class="col-5" v-model="p" :items="pList" label="query layer (p-att)" :rules="[rules.alphanum, rules.counter]" ></v-combobox><v-spacer/>
                    </v-flex>
                    <v-flex xs6>
                      <v-autocomplete v-model="selectCorpusReference" clearable :items="corpora" item-value="name_api" item-text="name" label="reference" :rules="[rules.required]"></v-autocomplete>
                      <v-combobox class="col-5" v-model="pReference" :items="pListReference" label="query layer (p-att)" :rules="[rules.required, rules.alphanum, rules.counter]" ></v-combobox><v-spacer/>
                        </v-flex>
                  </v-layout>
                  <v-layout row>
                    <v-btn color="info" class="text-lg-right" @click="clear">Clear</v-btn>
                    <v-spacer/>
                    <v-btn color="success" class="text-lg-right" @click="addKeyword">Submit</v-btn>
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
  name: 'KeywordNewContent',
  data: () => ({
    error: null,
    loading: false,
    name: 'untitled',           // TODO: make configurable
    selectCorpus: '',
    selectCorpusReference: '',
    p: '',
    pList: [],
    pReference: '',
    pListReference: [],
    rules: rules,
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      corpora: 'corpus/corpora',
      keyword: 'keyword/keyword'
    })
  },
  watch: {
    selectCorpus(){
      let C = this.corpora.find((o)=>o.name_api == this.selectCorpus);
      if(C){
        this.pList = C.pQueries
      }
      this.p = this.pList[0]
    },
    selectCorpusReference(){
      let C = this.corpora.find((o)=>o.name_api == this.selectCorpusReference);
      if(C){
        this.pListReference = C.pQueries
      }
      this.pReference = this.pListReference[0]
    },
  },
  methods: {
    ...mapActions({
      getCorpora: 'corpus/getCorpora',
      getUserDiscoursemes: 'discourseme/getUserDiscoursemes',
      addUserKeyword: 'keyword/addUserKeyword'
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
      this.p = ''
      this.pReference = ''
      this.selectCorpus = ''
      this.selectCorpusReference = ''
    },
    addKeyword () {
      this.error = null;

      if ( !this.selectCorpusReference || !this.selectCorpus ) {
        this.error = this.$t("keyword.new.missing_data")
        return
      }

      this.loading = true
      const data = {
        username: this.user.username,
        p: this.p,
        p_reference: this.pReference,
        corpus: this.selectCorpus,
        corpus_reference: this.selectCorpusReference
      }

      this.addUserKeyword(data).then(() => {
        this.error = null
        this.$router.push('/keyword')
      }).catch((error) => {
        this.error = this.error_message_for(error, "");
      }).then(() => {
        this.loading = false
      })
    }
  },
  created () {
    this.getCorpora().then(() => {
      this.error = null
    }).catch((error) => {
      this.error = this.error_message_for(error,"",{});
    }).then(() => {
        this.loading = false
    })
  }
}

</Script>
