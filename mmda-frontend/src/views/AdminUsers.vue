<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <AdminHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <AdminUsersContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import AdminHeader from '@/components/Admin/AdminHeader.vue'
import AdminUsersContent from '@/components/Admin/AdminUsersContent.vue'

export default {
  name: 'AdminUsers',
  components: {
    AdminHeader,
    AdminUsersContent
  },
  data: () => ({
  })
}

</script>
