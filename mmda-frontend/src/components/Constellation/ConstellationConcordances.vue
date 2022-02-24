<template>
<div>

  <ConstellationSelection/>

  <v-container v-if="associations">
    <v-tabs color="blue" dark>

      <v-tab :key="1">Discourseme Associations</v-tab>
      <v-tab :key="2">Concordance Lines</v-tab>

      <v-tab-item :key="1">
        <v-text-field label="Search" prepend-inner-icon="search" v-model="search"></v-text-field>
        <v-data-table v-if="associations" :headers="associationHeaders" :items="associations" :search="search" :pagination.sync="associationPagination" class="elevation-1">
          <template v-slot:items="props">
            <td class="text-xs-left">{{ props.item.node }}</td>
            <td class="text-xs-left">{{ props.item.candidate }}</td>
            <td class="text-xs-left">{{ props.item.log_likelihood }}</td>
            <td class="text-xs-left">{{ props.item.dice }}</td>
            <td class="text-xs-left">{{ props.item.log_ratio }}</td>
            <td class="text-xs-left">{{ props.item.mutual_information }}</td>
            <td class="text-xs-left">{{ props.item.z_score }}</td>
            <td class="text-xs-left">{{ props.item.t_score }}</td>
            <td class="text-xs-left">{{ props.item.f }}</td>
            <td class="text-xs-left">{{ props.item.f1 }}</td>
            <td class="text-xs-left">{{ props.item.f2 }}</td>
            <td class="text-xs-left">{{ props.item.N }}</td>
          </template>
        </v-data-table>
      </v-tab-item>

      <v-tab-item :key="2">
        <v-container>
          <v-form>
            <v-layout row>
              <v-select v-model="requiredDiscoursemes" :items="discoursemes" item-value="id" item-text="name" label="required discoursemes" multiple chips persistent-hint />
              <v-btn color="info" class="text-lg-right" @click="clear">Clear</v-btn>
              <v-btn color="success" class="text-lg-right" @click="filterConcordances">Filter</v-btn>
            </v-layout>
          </v-form>
        </v-container>

        <v-data-table v-if="filteredConcordances" :headers="concordanceHeaders" :items="filteredConcordances" :pagination.sync="concordancePagination" class="elevation-1">
          <template v-slot:items="props">

            <td class="text-xs-center">
              <v-menu open-on-hover top offset-y>
                <span slot="activator">{{ props.item.id }}</span>
                <v-card>
                  <center>
                    <div v-html="props.item.meta"> </div>
                  </center>
                  <br/>
                </v-card>
              </v-menu>
            </td>

            <!-- <td class="text-xs-left">{{ props.item.text }}</td> -->
            <td class="text-xs-left">
              <template v-for="(el,idx) in props.item.text">
                <span :key="'t_'+idx"
                      @click="selectItem(el)"
                      :class="'concordance '+ el.role "
                      :style="el.style"
                      :title="el.lemma">
                  {{el.text}}
                </span>
              </template>
            </td> 
          </template>
        </v-data-table>

      </v-tab-item>
    </v-tabs>
  </v-container>
 
</div>
</template>

<script>
import ConstellationSelection from '@/components/Constellation/ConstellationCorporaSelection.vue'
import { mapActions, mapGetters } from 'vuex'
import { random_color, hex_color_from_array } from '@/wordcloud/util_misc.js'

export default {
  name: 'ConstellationConcordances',
  components: {
    ConstellationSelection
  },
  data: () => ({
    search: '',
    requiredDiscoursemes: [],
    filteredConcordances: [],
    associationPagination: {
      sortBy: 'log_likelihood',
      descending: true,
      rowsPerPage: 25
    },
    concordancePagination: {
      sortBy: 'ID',
      rowsPerPage: 50
    },
    associationHeaders: [
      {text: 'node', align: 'left', value: 'node'},
      {text: 'candidate', align: 'left', value: 'candidate'},
      {text: 'log likelihood', align: 'center', value: 'log_likelihood'},
      {text: 'Dice', align: 'center', value: 'dice'},
      {text: 'log ratio', align: 'center', value: 'log_ratio'},
      {text: 'MI', align: 'center', value: 'mutual_information'},     
      {text: 'z-score', align: 'left', value: 'z_score'},
      {text: 't-score', align: 'left', value: 't_score'},
      {text: 'f', align: 'center', value: 'f'},
      {text: 'f1', align: 'center', value: 'f1'},
      {text: 'f2', align: 'center', value: 'f2'},
      {text: 'N', align: 'center', value: 'N'},
    ],
    concordanceHeaders: [
      {text: 'ID', align:'left', value: 'id'},
      {text: 'word', align: 'left', value: 'word'}
    ]
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      concordances: 'constellation/concordances',
      associations: 'constellation/associations',
      discoursemes: 'constellation/discoursemes',
    })
  },
  methods: {
    ...mapActions({
      getConstellationConcordances: 'constellation/getConstellationConcordances',
      resetConstellationConcordances: 'constellation/resetConstellationConcordances',
      getConstellationAssociations: 'constellation/getConstellationAssociations'
    }),
    filterConcordances () {
      var required = this.requiredDiscoursemes;
      function checkDiscoursemes(disc) {
        var a = true;
        for (var i = 0; i < required.length; ++i) {
          var r = ["BOOL", required[i]].join("_");
          a = a & disc[r];
        }
        return a
      }
      this.filteredConcordances = this.concordances.filter(checkDiscoursemes)
      this.filteredConcordances = this.formatConcordances()
    },
    formatConcordances () {
      var C = [];
      if(!this.filteredConcordances) return C;
      for(var ci of Object.keys(this.filteredConcordances)){
        var c = this.filteredConcordances[ci]
        var r = { 
          match_pos: ci,
          text: []
        };
        Object.assign(r, c);
        for(var i=0; i<c.word.length; ++i){
          var el = {
            text:   c.word[i],
            role:   c.role[i]? c.role[i].join(" "): "None",
            lemma:  c.lemma[i]
          };

          for(var role of c.role[i]){

            if(!role) continue;
            var nr = Number.parseInt(role);
            if(nr!==nr) continue;
            var col = random_color(nr);

            el.style =  'text-decoration:  ' + hex_color_from_array(col) + " underline double;";
            col[3] = 0.1;
            el.style += 'background-color: ' + hex_color_from_array(col) + ";";
          }
          r.text.push(el);
        }
        C.push(r);
      }
      return C;
    },
    clear () {
      this.error = null
      this.nodata = false
      this.requiredDiscoursemes = []
    },
  },
  created () {
    this.id = this.$route.params.id;
    this.filteredConcordances = this.concordances
    this.filteredConcordances = this.formatConcordances()
  }
}

</script>
