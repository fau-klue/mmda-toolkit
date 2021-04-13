<template>
  <div>
  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout>
          <v-flex xs12 sm12>
            <v-text-field label="Search" prepend-inner-icon="search" v-model="search" clearable @click:clear="clearSearch"></v-text-field>

            <v-list two-line subheader>
              <v-list-tile v-for="constellation in filteredItems" :key="constellation.id" avatar :to="/constellation/ + constellation.id">
                <v-list-tile-avatar>
                  <v-icon class="grey lighten-1 white--text">question_answer</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ constellation.name }} (ID:{{ constellation.id }})</v-list-tile-title>
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

export default {
  name: 'ConstellationList',
  data: () => ({
    search: ''
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      userConstellations: 'constellation/userConstellations'
    }),
    filteredItems() {
      var F = []
      if(!this.userConstellations) return [];
      if (!this.search) {
        F = this.userConstellations
      } else {
        F = this.userConstellations.filter(items => items.name.toLowerCase().search(this.search) >= 0 )
      }
      F.sort((x)=>x.id)
      return F;
    }
  },
  methods: {
    ...mapActions({
      getUserConstellations: 'constellation/getUserConstellations'
    }),
    clearSearch () {
      this.search = ''
    },
    loadConstellations () {
      this.getUserConstellations(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.loadConstellations()
  }
}

</script>
