<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout justify-space-between row>
          <v-flex v-if="theDiscursivePosition" xs12 sm12>

            <v-alert v-if="updated" value="true" dismissible  color="success" icon="info" outline>Updated Discursive Position </v-alert>
            <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>

            <v-form>
              <v-text-field v-model="theDiscursivePosition.name" :value="theDiscursivePosition.name" label="Discursive Position Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>

               <DiscursivePositionDiscoursemeList/>

              <v-btn color="success" class="text-lg-right" @click="updatePosition">Update Name</v-btn>
              <v-btn color="error" outline class="text-lg-right" @click="deletePosition">Delete</v-btn>

            </v-form>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import DiscursivePositionDiscoursemeList from '@/components/DiscursivePosition/DiscursivePositionDiscoursemeList.vue'

import rules from '@/utils/validation'

export default {
  name: 'DiscursivePositionContent',
  components: {
    DiscursivePositionDiscoursemeList
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
      theDiscursivePosition: 'discursive/discursivePosition'
    })
  },
  methods: {
    ...mapActions({
      getUserSingleDiscursivePosition: 'discursive/getUserSingleDiscursivePosition',
      updateUserDiscursivePosition: 'discursive/updateUserDiscursivePosition',
      deleteUserDiscursivePosition: 'discursive/deleteUserDiscursivePosition'
    }),
    loadPosition () {
      const data = {
        username: this.user.username,
        position_id: this.id
      }
      this.getUserSingleDiscursivePosition(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    updatePosition () {
      this.nodata = false
      this.updated = false

      if (!this.theDiscursivePosition.name) {
        this.nodata = true
        return
      }

      const data = {
        position_id: this.id,
        username: this.user.username,
        name: this.theDiscursivePosition.name
      }

      this.updateUserDiscursivePosition(data).then(() => {
        this.error = null
        this.updated = true
      }).catch((error) => {
        this.error = error
      })
    },
    deletePosition () {
      const data = {
        username: this.user.username,
        position_id: this.id
      }
      this.deleteUserDiscursivePosition(data).then(() => {
        this.error = null
        this.$router.push('/discursive')
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadPosition()
  }
}

</script>
