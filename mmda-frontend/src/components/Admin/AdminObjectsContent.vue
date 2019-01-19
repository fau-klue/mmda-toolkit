<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12>
          <p>
            {{ analysis  }}
          </p>
          <p>
            {{ discoursemes }}
          </p>
          <p>
            {{ positions }}
          </p>
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
      getAllPositions: 'admin/getAllPositions'
    }),
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
