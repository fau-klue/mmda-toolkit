<template>
<div>
  <v-card flat v-if="theConstellation">
    <v-card-text>
      <v-container>
        <v-layout justify-space-between row>
          <v-flex v-if="theConstellation" xs12 sm12>

            <v-alert v-if="updated" value="true" dismissible  color="success" icon="info" outline>Constellation Updated</v-alert>

            <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>
            
            <v-form>
              
              <v-layout row>
                <v-flex xs3 sm1>
                  <v-text-field v-model="theConstellation.id" :value="theConstellation.id" label="ID" box readonly />
                </v-flex>
                <v-flex xs3 sm11>
                  <v-text-field v-model="theConstellation.name" :value="theConstellation.name" label="name" :rules="[rules.required, rules.counter]" box background-color="white" />
                </v-flex>
              </v-layout>

              <v-layout row>
                <v-btn color="error" class="text-lg-right" @click="deleteConstellation">Delete</v-btn>
                <v-spacer/>
                <v-btn color="info" class="text-lg-right" @click="updateConstellation">Update</v-btn>
                <v-btn color="success" :to="/constellation/ + theConstellation.id + /concordances/" class="text-lg-right">Analyze</v-btn>
              </v-layout>

            </v-form>

          </v-flex>
        </v-layout>
      </v-container>

      <v-container>
        <ConstellationDiscoursemeList/>
      </v-container>
      
    </v-card-text>
  </v-card>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ConstellationDiscoursemeList from '@/components/Constellation/ConstellationDiscoursemeList.vue'

import rules from '@/utils/validation'

export default {
  name: 'ConstellationContent',
  components: {
    ConstellationDiscoursemeList
  },
  data: () => ({
    id: null,
    error: null,
    nodata: false,
    updated: false,
    rules: rules
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      theConstellation: 'constellation/constellation'
    })
  },
  methods: {
    ...mapActions({
      getUserSingleConstellation: 'constellation/getUserSingleConstellation',
      updateUserConstellation: 'constellation/updateUserConstellation',
      deleteUserConstellation: 'constellation/deleteUserConstellation'
    }),
    loadConstellation () {
      const data = {
        username: this.user.username,
        constellation_id: this.id
      }
      this.getUserSingleConstellation(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    updateConstellation () {
      this.nodata = false
      this.updated = false

      if (!this.theConstellation.name) {
        this.nodata = true
        return
      }

      const data = {
        constellation_id: this.id,
        username: this.user.username,
        name: this.theConstellation.name
      }

      this.updateUserConstellation(data).then(() => {
        this.error = null
        this.updated = true
      }).catch((error) => {
        this.error = error
      })
    },
    deleteConstellation () {
      const data = {
        username: this.user.username,
        constellation_id: this.id
      }
      this.deleteUserConstellation(data).then(() => {
        this.error = null
        this.$router.push('/constellation')
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadConstellation()
  }
}

</script>
