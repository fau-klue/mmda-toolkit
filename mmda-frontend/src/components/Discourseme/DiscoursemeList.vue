<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout>
          <v-flex xs12 sm12>
            <v-text-field label="Search" prepend-inner-icon="search" v-model="search" clearable @click:clear="clearSearch"></v-text-field>

            <v-list two-line subheader>
              <v-list-tile v-for="discourseme in filteredItems" :key="discourseme.id" avatar :to="/discourseme/ + discourseme.id">
                <v-icon v-if="discourseme.is_topic" color="orange">grade</v-icon>
                <v-list-tile-avatar>
                  <v-icon class="grey lighten-1 white--text">subject</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ discourseme.name }} (ID:{{ discourseme.id }})</v-list-tile-title>
                  <v-list-tile-sub-title>{{ discourseme.items }}</v-list-tile-sub-title>
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
  name: 'DiscoursemeList',
  data: () => ({
    search: ''
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      userDiscoursemes: 'discourseme/userDiscoursemes'
    }),
    filteredItems() {
      var F = [];
      if(!this.userDiscoursemes) return [];
      if (!this.search) {
        F = this.userDiscoursemes

      } else {
        F = this.userDiscoursemes.filter(items =>
                                            items.name.toLowerCase().search(this.search.toLowerCase()) >= 0 ||
                                            items.items.join().toLowerCase().search(this.search.toLowerCase()) >= 0
                                           )}
      F.sort((x)=>x.id); //sort by latest creation-date //i.e. ~ id
      return F;
    }
  },
  methods: {
    ...mapActions({
      getUserDiscoursemes: 'discourseme/getUserDiscoursemes'
    }),
    clearSearch () {
      this.search = ''
    },
    loadDiscoursemes () {
      this.getUserDiscoursemes(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.loadDiscoursemes()
  }
}

</script>
