<template>
  <v-navigation-drawer
    right
    clipped
    disable-resize-watcher
    hide-overlay
    permanent
    app
    :mini-variant="!notMini">
    <!-- permanent -->
    <v-toolbar flat class="transparent">
      <v-list class="pa-0">
        <v-list-tile avatar>
          <v-list-tile-avatar>
            <v-btn icon v-if="!notMini" @click.stop="setMini(true)">
              <v-icon>chevron_left</v-icon>
            </v-btn>
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>
              <span class="subheading">Wordcloud Options</span>
            </v-list-tile-title>
          </v-list-tile-content>

          <v-list-tile-action>
            <v-btn icon @click.stop="setMini(false)">
              <v-icon>chevron_right</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-toolbar>

    <v-expansion-panel>
      <wordcloudKeywordTools v-bind:wc="wc"/>
      <WordcloudKeywordCollocationParameters/>
      <!-- <WordcloudKeywordSecondOrder/> -->
      <!-- <WordcloudKeywordComparison/> -->
      <WordcloudKeywordSearchItem v-bind:wc="wc"/>
    </v-expansion-panel>
  </v-navigation-drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import WordcloudKeywordTools from "@/components/WordcloudKeyword/Sidebar/WordcloudKeywordTools";
import WordcloudKeywordSearchItem from "@/components/WordcloudKeyword/Sidebar/WordcloudKeywordSearchItem";
import WordcloudKeywordCollocationParameters from "@/components/WordcloudKeyword/Sidebar/WordcloudKeywordCollocationParameters";
// import WordcloudKeywordSecondOrder from "@/components/WordcloudKeyword/Sidebar/WordcloudKeywordSecondOrder";
// import WordcloudKeywordComparison from "@/components/WordcloudKeyword/Sidebar/WordcloudKeywordComparison";

export default {
  name: "WordcloudKeywordSidebar",
  components: {
    WordcloudKeywordTools,
    WordcloudKeywordSearchItem,
    WordcloudKeywordCollocationParameters,
    // WordcloudKeywordComparison,
    // WordcloudKeywordSecondOrder
  },
  props:["wc"],
  data: () => ({
  }),
  computed: {
    ...mapGetters({
      user: "login/user",
      keyword: "keyword/keyword",
      notMini: "wordcloud/rightSidebar"
    })
  },
  methods: {
    ...mapActions({
      setMini: "wordcloud/setRightSidebar",
    }),
  }
};
</script>

<style>
</style>
