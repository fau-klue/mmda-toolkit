<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <div v-if="collocation">
          <p class="headline">Collocation Analyses ({{ collocation.length }})</p>
          <v-list>
            <v-list-tile v-for="item in collocation" :key="item.id" avatar>
              <v-list-tile-avatar>
                <v-icon class="grey--text">dashboard</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                  {{item.name}}
                  (ID: {{item.id}}, User: {{item.user_id}})
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon @click="removeObject('collocation', item)">
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

          <div v-if="constellations">
          <p class="headline">Constellations ({{ constellations.length }})</p>
          <v-list>
            <v-list-tile v-for="item in constellations" :key="item.id" avatar>
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
                <v-btn icon @click="removeObject('constellation', item)">
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
      collocation: 'admin/collocation',
      discoursemes: 'admin/discoursemes',
      constellations: 'admin/constellations'
    })
  },
  methods: {
    ...mapActions({
      getAllCollocation: 'admin/getAllCollocation',
      getAllDiscoursemes: 'admin/getAllDiscoursemes',
      getAllConstellations: 'admin/getAllConstellations',
      deleteObject: 'admin/deleteObject'
    }),
    removeObject (type, object) {
      const data = {
        object: type,
        object_id: object.id
      }

      this.loading = true
      // Collocation
      this.deleteObject(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
      this.loading = false
    },
    loadObjects () {
      this.loading = true
      // Collocation
      this.getAllCollocation().then(() => {
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
      // Constellations
      this.getAllConstellations().then(() => {
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
