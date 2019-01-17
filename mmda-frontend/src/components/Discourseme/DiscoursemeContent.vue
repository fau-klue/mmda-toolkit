<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout justify-space-between row>
          <v-flex v-if="discourseme" xs12 sm12>
            <v-alert v-if="updated" value="true" dismissible color="success" icon="info" outline>Update Discoursemed</v-alert>
            <v-alert v-if="nodata" value="true" dismissible color="warning" icon="priority_high" outline>Missing Data</v-alert>

            <v-form>
              <!-- Better component for this? -->
              <v-alert v-if="discourseme.is_topic" value="true" color="info" icon="info" outline>This is a topic discourseme</v-alert>

              <v-text-field v-model="discourseme.name" label="Discourseme Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
              <v-combobox
                v-model="discourseme.items"
                :items="discourseme.items"
                label="Discourseme Items"
                :rules="[rules.required, rules.alphanum, rules.counter]"
                multiple
                chips
                ></v-combobox>
            </v-form>

            <v-btn color="success" class="text-lg-right" @click="updateDiscourseme">Update</v-btn>
            <v-btn color="error" v-if="discourseme.is_topic" disabled class="text-lg-right" @click="deleteDiscourseme">Delete</v-btn>
            <v-btn color="error" v-else outline class="text-lg-right" @click="deleteDiscourseme">Delete</v-btn>

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
    })
  },
  methods: {
    ...mapActions({
      updateUserDiscourseme: 'discourseme/updateUserDiscourseme',
      deleteUserDiscourseme: 'discourseme/deleteUserDiscourseme',
      getUserDiscourseme: 'discourseme/getUserDiscourseme'
    }),
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
