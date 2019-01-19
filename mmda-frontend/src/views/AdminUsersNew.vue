<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <NewUserForm/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import NewUserForm from '@/components/Admin/AdminUsersNew.vue'

export default {
  name: 'NewUser',
  components: {
    NewUserForm
  }
}

</script>
