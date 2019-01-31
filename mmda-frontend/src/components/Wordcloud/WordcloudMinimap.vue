<template>
  <div>
    <!-- TODO -->
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "WordcloudMinimap",
  components: {},
  data: () => ({}),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: "analysis/analysis"
    })
  }
};
</script>
