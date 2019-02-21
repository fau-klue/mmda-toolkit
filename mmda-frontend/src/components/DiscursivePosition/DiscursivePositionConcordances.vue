<template>
<div>
  <DiscursivePositionSelection/>

  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout>
          <v-flex xs12 sm12>
            <v-tabs color="cyan darken-2" dark slider-color="yellow">
              <v-tab v-for="n in 3" :key="n"ripple>
                Item {{ n }}
              </v-tab>
              <v-tab-item
                v-for="n in 3"
                :key="n"
                >
                <v-card flat>
                  <v-card-text>Lorem Ipsum</v-card-text>
                </v-card>
              </v-tab-item>
            </v-tabs>

          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
  </div>
</template>

<script>
import DiscursivePositionSelection from '@/components/DiscursivePosition/DiscursivePositionCorporaSelection.vue'

import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'DiscursivePositionConcordances',
  components: {
    DiscursivePositionSelection
  },
  data: () => ({
    search: ''
  }),
  computed: {
    ...mapGetters({
      user: 'login/user'
    })
  },
  methods: {
  }
}

</script>
