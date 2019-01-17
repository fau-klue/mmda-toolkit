<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <ProfileHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <ProfileContent/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <ProfilePassword/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import ProfileHeader from '@/components/Profile/ProfileHeader.vue'
import ProfileContent from '@/components/Profile/ProfileContent.vue'
import ProfilePassword from '@/components/Profile/ProfilePassword.vue'

export default {
  name: 'Profile',
  components: {
    ProfileHeader,
    ProfileContent,
    ProfilePassword
  },
}

</script>
