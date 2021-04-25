<template>
<v-layout row>
  <v-flex xs12 sm12>
    <div>
      <v-container>
        <v-layout>
          <v-flex xs6 sm6>
            <v-card-title>Associated Discoursemes</v-card-title>
            <v-list two-line subheader v-if="analysisDiscoursemes.length > 0">
              <v-list-tile v-for="discourseme in analysisDiscoursemes" :key="discourseme.id" avatar>
                <v-icon v-if="discourseme.is_topic" color="orange">grade</v-icon>
                <v-list-tile-avatar>
                  <v-icon class="grey--text">subject</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ discourseme.name }}</v-list-tile-title>
                  <v-list-tile-sub-title>{{ discourseme.items }}</v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action >
                  <v-btn :loading="loading" icon ripple :to="/discourseme/ + discourseme.id">
                    <v-icon class="grey--text text--lighten-1">info</v-icon>
                  </v-btn>
            </v-list-tile-action>
                <v-list-tile-action>
                  <v-btn :loading="loading" icon @click="removeDiscourseme(discourseme.id)">
                    <v-icon class="red--text text--lighten-1">remove</v-icon>
                  </v-btn>
                </v-list-tile-action>
              </v-list-tile>
              <h2 v-if="analysisDiscoursemes.length <= 0" class="subheading text-md-center">None</h2>
            </v-list>
          </v-flex>
          <v-flex xs6 sm6>
            <v-card-title>Available Discoursemes</v-card-title>
            <v-list two-line subheader v-if="userDiscoursemes">
              <v-list-tile v-for="discourseme in discoursemeUnion" :key="discourseme.id" avatar>
                <v-icon v-if="discourseme.is_topic" color="orange">grade</v-icon>
                <v-list-tile-avatar>
                  <v-icon class="grey--text">subject</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ discourseme.name }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ discourseme.items }}</v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-btn :loading="loading" icon ripple :to="/discourseme/ + discourseme.id">
                    <v-icon class="grey--text text--lighten-1">info</v-icon>
                  </v-btn>
                </v-list-tile-action>
                <v-list-tile-action>
                  <v-btn :loading="loading" icon @click="addDiscourseme(discourseme.id)">
                    <v-icon class="green--text text--lighten-1">add</v-icon>
                  </v-btn>
                </v-list-tile-action>
              </v-list-tile>
            </v-list>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
  </v-flex>
</v-layout>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AnalysisDiscoursemeList',
  data: () => ({
    search: '',
    error: null,
    loading: false
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysisDiscoursemes: 'analysis/discoursemes',
      theAnalysis: 'analysis/analysis',
      userDiscoursemes: 'discourseme/userDiscoursemes'
    }),
    discoursemeUnion () {
      const analysisDiscoursemeIDs = this.analysisDiscoursemes.map(d => d.id)
      if(this.theAnalysis){
        // Add own topic discourseme, cause you cant add that
        analysisDiscoursemeIDs.push(this.theAnalysis.topic_id)
      }
      return this.userDiscoursemes.filter(items => !analysisDiscoursemeIDs.includes(items.id)  )
    }
  },
  methods: {
    ...mapActions({
      getAnalysisDiscoursemes: 'analysis/getAnalysisDiscoursemes',
      getUserDiscoursemes: 'discourseme/getUserDiscoursemes',
      removeDiscoursemeFromAnalysis: 'analysis/removeDiscoursemeFromAnalysis',
      addDiscoursemeToAnalysis: 'analysis/addDiscoursemeToAnalysis',
    }),
    loadAnalysisDiscoursemes () {
      const data = {
        username: this.user.username,
        analysis_id: this.id
      }

      this.getAnalysisDiscoursemes(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    loadDiscoursemes () {
      this.getUserDiscoursemes(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    addDiscourseme (id) {
      const data = {
        username: this.user.username,
        analysis_id: this.id,
        discourseme_id: id
      }

      this.loading = true
      this.addDiscoursemeToAnalysis(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      }).then(() => {
        this.loading = false
      })
    },
    removeDiscourseme (id) {
      const data = {
        username: this.user.username,
        analysis_id: this.id,
        discourseme_id: id
      }

      this.loading = true
      this.removeDiscoursemeFromAnalysis(data).then(() => {
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
    this.loadDiscoursemes()
    this.loadAnalysisDiscoursemes()
  }
}

</script>
