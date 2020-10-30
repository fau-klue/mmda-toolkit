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
      <wordcloudTools v-bind:wc="wc"/>
      <WordcloudCollocationParameters/>
      <WordcloudSecondOrder/>
      <WordcloudComparison/>
      <WordcloudSearchItem v-bind:wc="wc"/>
    </v-expansion-panel>
  </v-navigation-drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import WordcloudTools from "@/components/Wordcloud/Sidebar/WordcloudTools";
import WordcloudSearchItem from "@/components/Wordcloud/Sidebar/WordcloudSearchItem";
import WordcloudCollocationParameters from "@/components/Wordcloud/Sidebar/WordcloudCollocationParameters";
import WordcloudSecondOrder from "@/components/Wordcloud/Sidebar/WordcloudSecondOrder";
import WordcloudComparison from "@/components/Wordcloud/Sidebar/WordcloudComparison";

export default {
  name: "WordcloudSidebar",
  components: {
    WordcloudTools,
    WordcloudSearchItem,
    WordcloudCollocationParameters,
    WordcloudComparison,
    WordcloudSecondOrder
  },
  props:["wc"],
  data: () => ({
  }),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: "analysis/analysis",
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
