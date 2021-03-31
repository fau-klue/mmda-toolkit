<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <div v-if="analysis">
          <p class="headline">Queries ({{ analysis.length }})</p>
          <v-list>
            <v-list-tile v-for="item in analysis" :key="item.id" avatar>
              <v-list-tile-avatar>
                <v-icon class="grey--text">dashboard</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                  {{item.name}}
                  (ID: {{item.id}}, User: {{item.user_id}})
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon @click="removeObject('analysis', item)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
          </div>

          <div v-if="discoursemes">
          <p class="headline">Discoursemes ({{ discoursemes.length }})</p>
          <v-list>
            <v-list-tile v-for="item in discoursemes" :key="item.id" avatar>
              <v-list-tile-avatar>
                <v-icon class="grey--text">subject</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>
                  {{item.name}}
                  (ID: {{item.id}}, User: {{item.user_id}})
                </v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon @click="removeObject('discourseme', item)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
          </div>

          <div v-if="positions">
          <p class="headline">Constellations ({{ positions.length }})</p>
          <v-list>
            <v-list-tile v-for="item in positions" :key="item.id" avatar>
              <v-list-tile-avatar>
                <v-icon class="grey--text">question_answer</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>
                  {{item.name}}
                  (ID: {{item.id}}, User: {{item.user_id}})
                </v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon @click="removeObject('discursiveposition', item)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
          </div>

        </v-flex>
      </v-layout>
    </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AdminObjectsContent',
  data: () => ({
    loading: false,
    error: null
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'admin/analysis',
      discoursemes: 'admin/discoursemes',
      positions: 'admin/positions'
    })
  },
  methods: {
    ...mapActions({
      getAllAnalysis: 'admin/getAllAnalysis',
      getAllDiscoursemes: 'admin/getAllDiscoursemes',
      getAllPositions: 'admin/getAllPositions',
      deleteObject: 'admin/deleteObject'
    }),
    removeObject (type, object) {
      const data = {
        object: type,
        object_id: object.id
      }

      this.loading = true
      // Analysis
      this.deleteObject(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
      this.loading = false
    },
    loadObjects () {
      this.loading = true
      // Analysis
      this.getAllAnalysis().then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
      // Discoursemes
      this.getAllDiscoursemes().then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
      // Positions
      this.getAllPositions().then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
      this.loading = false
    },
  },
  created () {
    this.loadObjects()
  }
}

</script>
