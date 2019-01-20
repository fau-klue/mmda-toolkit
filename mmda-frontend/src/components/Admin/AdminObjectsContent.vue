<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <p class="headline">Analysis</p>
          <v-list two-line subheader v-if="analysis">
            <v-list-tile v-for="item in analysis" :key="item.name" avatar>
              <v-list-tile-avatar>
                <v-icon class="grey--text">dashboard</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>{{ item.name }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon @click="removeObject('analysis', item)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>

          <p class="headline">Discoursemes</p>
          <v-list two-line subheader v-if="discoursemes">
            <v-list-tile v-for="item in discoursemes" :key="item.name" avatar>
              <v-list-tile-avatar>
                <v-icon class="grey--text">subject</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>{{ item.name }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon @click="removeObject('discourseme', item)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>

          <p class="headline">Discursive Positions</p>
          <v-list two-line subheader v-if="positions">
            <v-list-tile v-for="item in positions" :key="item.name" avatar>
              <v-list-tile-avatar>
                <v-icon class="grey--text">question_answer</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>{{ item.name }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon @click="removeObject('discursiveposition', item)">
                  <v-icon class="red--text text--lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>

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
