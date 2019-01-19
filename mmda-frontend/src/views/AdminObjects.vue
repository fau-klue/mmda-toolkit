<template>
<v-container grid-list-md>
  <v-layout wrap row>
    <v-flex xs12>
      <AdminHeader/>
    </v-flex>
  </v-layout>
  <v-layout wrap row>
    <v-flex xs12>
      <AdminObjectsContent/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import AdminHeader from '@/components/Admin/AdminHeader.vue'
import AdminObjectsContent from '@/components/Admin/AdminObjectsContent.vue'

export default {
  name: 'AdminObjects',
  components: {
    AdminHeader,
    AdminObjectsContent
  }
}

</script>
