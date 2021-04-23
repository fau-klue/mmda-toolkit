<template>
<div>
  <v-card flat>
    <v-card-title>Discourseme </v-card-title>
    <v-card-text>
      <v-container>
        <v-layout justify-space-between row>
          <v-flex v-if="discourseme" xs12 sm12>

            <v-alert v-if="updated" value="true" dismissible color="success" icon="info" outline>
              Updated Discourseme
            </v-alert>
            <v-alert v-if="nodata" value="true" dismissible color="warning" icon="priority_high" outline>
              Missing Data
            </v-alert>

            <v-form>
              
              <v-layout row>
                <v-text-field
                  v-model="discourseme.name"
                  label="Name"
                  :rules="[rules.required, rules.counter]"
                >
                </v-text-field>
                &nbsp;
                <v-text-field
                  v-model="discourseme.id"
                  :value="discourseme.id"
                  label="ID"
                  box readonly
                  >
                </v-text-field>
              </v-layout>
              
              <v-combobox
                v-model="discourseme.items"
                :items="discourseme.items"
                label="Items"
                :rules="[rules.required, rules.counter]"
                multiple
                chips
                ></v-combobox>

            </v-form>

            <v-btn color="success" outline class="text-lg-right" @click="updateDiscourseme">Update</v-btn>
            <v-btn color="error" outline class="text-lg-right" @click="deleteDiscourseme">Delete</v-btn>
            <v-btn color="success" outline class="text-lg-right" @click="createAnalysis">analyze</v-btn>

          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
  <v-card flat>
    <v-card-text>
      <v-card-title>Analyses</v-card-title>
      <v-container>
        <v-layout>
          <v-flex xs12 sm12>
            <v-list two-line subheader>
              <v-list-tile v-for="analysis in filteredAnalyses" :key="analysis.id" avatar :to="/analysis/ + analysis.id">
                <v-list-tile-avatar>
                  <v-icon class="grey lighten-1 white--text">dashboard</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title> Analysis in Corpus "{{ analysis.corpus }}" (Analysis ID: {{ analysis.id }}, name: {{ analysis.name }})</v-list-tile-title>
                  <v-list-tile-sub-title>items: {{ analysis.items }} </v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import rules from '@/utils/validation'

export default {
  name: 'DiscoursemeContent',
  data: () => ({
    id: null,
    error: null,
    updated: false,
    nodata: false,
    rules: rules
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      discourseme: 'discourseme/discourseme',
      analyses: 'analysis/userAnalysis'
    }),
    filteredAnalyses() {
      var F = [];
      if(!this.analyses) return [];
      F = this.analyses.filter(item => item.topic_id === this.discourseme.id );
      F.sort((x)=>x.id);     // sort by latest creation-date = id
      return F;
    },
  },
  methods: {
    ...mapActions({
      updateUserDiscourseme: 'discourseme/updateUserDiscourseme',
      deleteUserDiscourseme: 'discourseme/deleteUserDiscourseme',
      getUserDiscourseme: 'discourseme/getUserDiscourseme'
    }),
    // CREATE ANALYSIS
    createAnalysis () {
      if(!this.discourseme) return;
      var q = "?discourseme="+this.discourseme.id;
      for(var i of this.discourseme.items) q+="&item="+i;
      this.$router.push('/analysis/new'+q);
    },
    // LOAD DISCOURSEME
    loadDiscourseme () {

      const data = {
        username: this.user.username,
        discourseme_id: this.id
      }

      this.getUserDiscourseme(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })

    },
    // DELETE DISCOURSEME
    deleteDiscourseme () {

      const data = {
        username: this.user.username,
        discourseme_id: this.id
      }

      this.deleteUserDiscourseme(data).then(() => {
        this.error = null
        this.$router.push('/discourseme')
      }).catch((error) => {
        this.error = error
      })
    },
    // UPDATE
    updateDiscourseme () {
      this.nodata = false
      this.updated = false

      if (!this.discourseme.name || this.discourseme.items.length <= 0) {
        this.nodata = true
        return
      }

      const data = {
        discourseme_id: this.id,
        name: this.discourseme.name,
        items: this.discourseme.items,
        username: this.user.username
      }

      this.updateUserDiscourseme(data).then(() => {
        this.error = null
        this.updated = true
      }).catch((error) => {
        this.error = error
      })
    }
  },


  created () {
    this.id = this.$route.params.id
    this.loadDiscourseme()
  }

}

</script>
