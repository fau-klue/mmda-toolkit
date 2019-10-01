<template>
  <div>
  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout>
          <v-flex xs12 sm12>
            <v-text-field label="Search" prepend-inner-icon="search" v-model="search" clearable @click:clear="clearSearch"></v-text-field>

            <v-list two-line subheader>
              <v-list-tile v-for="position in filteredItems" :key="position.id" avatar :to="/discursive/ + position.id">
                <v-list-tile-avatar>
                  <v-icon class="grey lighten-1 white--text">question_answer</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ position.name }} (ID:{{ position.id }})</v-list-tile-title>
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
  name: 'DiscursivePositionList',
  data: () => ({
    search: ''
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      userPositions: 'discursive/userDiscursivePositions'
    }),
    filteredItems() {
      var F = []
      if(!this.userPositions) return [];
      if (!this.search) {
        F = this.userPositions
      } else {
        F = this.userPositions.filter(items => items.name.toLowerCase().search(this.search) >= 0 )
      }
      F.sort((x)=>x.id)
      return F;
    }
  },
  methods: {
    ...mapActions({
      getUserDiscursivePositions: 'discursive/getUserDiscursivePositions'
    }),
    clearSearch () {
      this.search = ''
    },
    loadPositions () {
      this.getUserDiscursivePositions(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.loadPositions()
  }
}

</script>
