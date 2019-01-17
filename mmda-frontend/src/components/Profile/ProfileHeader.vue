<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs12 class="text-xs-left">
          <h1 v-if="userProfile" class="display-1">{{ userProfile.first_name }} {{ userProfile.last_name }}</h1>
        </v-flex>
      </v-layout>
    </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ProfileHeader',
  data: () => ({
  }),
  computed: {
    ...mapGetters({
      userProfile: 'profile/userProfile',
      user: 'login/user'
    })
  }
}

</script>
