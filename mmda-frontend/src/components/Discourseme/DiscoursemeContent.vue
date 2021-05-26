<template>
<div>

  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout justify-space-between row>
          <v-flex v-if="discourseme" xs12 sm12>
            <v-alert v-if="updated" value="true" dismissible color="success" icon="info" outline>Updated Discourseme</v-alert>
            <v-alert v-if="nodata" value="true" dismissible color="warning" icon="priority_high" outline>Missing Data</v-alert>

            <v-form>
              
              <v-layout row>
 
                <v-flex xs3 sm1>
                  <v-text-field v-model="discourseme.id" :value="discourseme.id" label="ID" box readonly />
                </v-flex>
                <v-flex xs3 sm11>
                  <v-text-field v-model="discourseme.name" label="name" :rules="[rules.required, rules.counter]" box background-color="white"/>
                </v-flex>

              </v-layout>
              
              <v-combobox v-model="discourseme.items" :items="discourseme.items" label="items" :rules="[rules.required, rules.counter]" multiple chips></v-combobox>

            </v-form>

            <v-layout row>
              <v-btn color="info" class="text-lg-right" @click="updateDiscourseme">Update</v-btn>
              <v-btn color="success" class="text-lg-right" @click="createAnalysis">Analyze</v-btn>
              <v-spacer/>
              <v-btn color="error" class="text-lg-right"  @click.stop="dialogDelete = true">Delete</v-btn>
            </v-layout>

            <v-dialog v-model="dialogDelete" max-width="290">
              <v-card>
                <v-card-title class="headline">Delete Discourseme?</v-card-title>
                <v-card-text>
                  You’re about to permanently delete this discourseme. Once deleted, it cannot be undone or recovered. Any associated analyses will be deleted with it.
		</v-card-text>
                <v-card-actions>
                  <v-spacer/>
                  <v-btn outline @click="dialogDelete = false">Close</v-btn>
                  <v-btn color="error" @click="deleteDiscourseme">Delete</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

          </v-flex>
        </v-layout>
      </v-container>

      <v-container v-if="discourseme">
        <v-card-title>Analyses</v-card-title>

        <v-text-field label="Search" prepend-inner-icon="search" v-model="search"></v-text-field>
        <v-data-table v-if="filteredAnalyses" :headers="headers" :items="filteredAnalyses" :search="search" :pagination.sync="pagination" class="elevation-1">
          <template v-slot:items="props">
            <router-link :to="/analysis/ + props.item.id" tag="tr" :style="{ cursor: 'pointer'}">
              <td class="text-xs-left">{{ props.item.id }}</td>
              <td class="text-xs-left">{{ props.item.corpus }}</td>
              <td class="text-xs-left">{{ props.item.items }}</td>
            </router-link>
            <!-- <td> -->
              <!--   <v-btn icon @click="deleteAnalysis(props.item.id)"> -->
                <!--     <v-icon class="red--text text--lighten-1">delete</v-icon> -->
                <!--   </v-btn> -->
              <!-- </td> -->
          </template>
        </v-data-table>

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
    search: '',
    error: null,
    updated: false,
    nodata: false,
    rules: rules,
    dialogDelete: false,
    headers: [
      {text: 'ID', value: 'id', align: 'left'},
      {text: 'corpus', value: 'corpus', align: 'left'},
      {text: 'items', value: 'items', align: 'left'}
    ],
    pagination: {
      sortBy: 'id',
      descending: true,
      rowsPerPage: 25
    }
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      discourseme: 'discourseme/discourseme',
      analyses: 'analysis/userAnalysis'
    }),
    filteredAnalyses() {
      var F = [];
      if(!this.analyses) return [];
      F = this.analyses.filter(item => item.topic_id === this.discourseme.id );
      F.sort((x)=>x.id);     // sort by latest creation-date = id
      return F;
    },
  },
  methods: {
    ...mapActions({
      updateUserDiscourseme: 'discourseme/updateUserDiscourseme',
      deleteUserDiscourseme: 'discourseme/deleteUserDiscourseme',
      getUserDiscourseme: 'discourseme/getUserDiscourseme'
    }),
    // CREATE ANALYSIS
    createAnalysis () {
      if(!this.discourseme) return;
      var q = "?discourseme="+this.discourseme.id;
      for(var i of this.discourseme.items) q+="&item="+i;
      this.$router.push('/analysis/new'+q);
    },
    // LOAD DISCOURSEME
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
    // DELETE DISCOURSEME
    deleteDiscourseme () {
      this.dialogDelete = false
      const data = {
        username: this.user.username,
        discourseme_id: this.id
      }

      this.deleteUserDiscourseme(data).then(() => {
        this.error = null
        this.$router.push('/discourseme')
        this.dialogDelete = false
      }).catch((error) => {
        this.error = error
        this.dialogDelete = false
      })
    },
    // UPDATE
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
