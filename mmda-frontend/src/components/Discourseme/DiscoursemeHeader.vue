<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-layout wrap row>
        <v-flex xs6>
          <h1 class="display-1">Discoursemes</h1>
        </v-flex>
        <v-flex xs6 class="text-xs-right">
          <v-btn color="success" class="text-lg-right" to="/discourseme/new"> New Discourseme</v-btn>
        </v-flex>
      </v-layout>
    </v-card-text>
    </v-card>
  </div>
</template>

<script>

export default {
  name: 'DiscoursemeHeader',
  data: () => ({
})
}

</script>
