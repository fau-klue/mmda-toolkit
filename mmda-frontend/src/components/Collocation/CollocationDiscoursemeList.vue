<template>
<v-layout row>
  <v-flex xs12 sm12>
    <div>
      <v-container>
        <v-layout>
          <v-flex xs6 sm6>
            <v-card-title>Associated Discoursemes</v-card-title>
            <v-list two-line subheader v-if="collocationDiscoursemes.length > 0">
              <v-list-tile v-for="discourseme in collocationDiscoursemes" :key="discourseme.id" avatar>
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
              <h2 v-if="collocationDiscoursemes.length <= 0" class="subheading text-md-center">None</h2>
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
  name: 'CollocationDiscoursemeList',
  data: () => ({
    search: '',
    error: null,
    loading: false
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      collocationDiscoursemes: 'collocation/discoursemes',
      theCollocation: 'collocation/collocation',
      userDiscoursemes: 'discourseme/userDiscoursemes'
    }),
    discoursemeUnion () {
      const collocationDiscoursemeIDs = this.collocationDiscoursemes.map(d => d.id)
      if(this.theCollocation){
        // Add own topic discourseme, cause you cant add that
        collocationDiscoursemeIDs.push(this.theCollocation.topic_id)
      }
      return this.userDiscoursemes.filter(items => !collocationDiscoursemeIDs.includes(items.id)  )
    }
  },
  methods: {
    ...mapActions({
      getCollocationDiscoursemes: 'collocation/getCollocationDiscoursemes',
      getUserDiscoursemes: 'discourseme/getUserDiscoursemes',
      removeDiscoursemeFromCollocation: 'collocation/removeDiscoursemeFromCollocation',
      addDiscoursemeToCollocation: 'collocation/addDiscoursemeToCollocation',
    }),
    loadCollocationDiscoursemes () {
      const data = {
        username: this.user.username,
        collocation_id: this.id
      }

      this.getCollocationDiscoursemes(data).then(() => {
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
        collocation_id: this.id,
        discourseme_id: id
      }

      this.loading = true
      this.addDiscoursemeToCollocation(data).then(() => {
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
        collocation_id: this.id,
        discourseme_id: id
      }

      this.loading = true
      this.removeDiscoursemeFromCollocation(data).then(() => {
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
    this.loadCollocationDiscoursemes()
  }
}

</script>
