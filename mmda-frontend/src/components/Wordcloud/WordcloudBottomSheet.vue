<template>
  <v-bottom-sheet hide-overlay v-model="sheet">
    <ConcordancesKeywordInContextList/>
  </v-bottom-sheet>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'

export default {
  name: "WordcloudBottomSheet",
  components: {
    ConcordancesKeywordInContextList,
  },
  data: () => ({
    sheet:true,
  }),
  computed: {
    ...mapGetters({
      concordances: 'corpus/concordances'
    })
  },
  watch:{
    concordances(){
      this.sheet=true;
    }
  },
  methods: {
    ...mapActions({
    }),
  }
};
</script>

<style>
</style>
