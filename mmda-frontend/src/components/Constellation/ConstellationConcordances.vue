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
            <td class="text-xs-left">{{ props.item.word }}</td>
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
    },
    clear () {
      this.error = null
      this.nodata = false
      this.requiredDiscoursemes = null
    },
  },
  created () {
    this.id = this.$route.params.id;
    this.filteredConcordances = this.concordances
    // console.log(this.concordances)
  }
}

</script>
