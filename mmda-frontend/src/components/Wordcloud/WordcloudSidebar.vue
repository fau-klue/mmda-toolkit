<template>
  <v-navigation-drawer v-model="sidebar" right app clipped :mini-variant.sync="mini">
    <v-toolbar flat class="transparent">
      <v-list class="pa-0">
        <v-list-tile avatar>
          <v-list-tile-avatar>
            <v-btn icon v-if="mini">
              <v-icon>chevron_left</v-icon>
            </v-btn>
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>
              <span class="subheading">Wordcloud Options</span>
            </v-list-tile-title>
          </v-list-tile-content>

          <v-list-tile-action>
            <v-btn icon @click.stop="mini = !mini">
              <v-icon>chevron_right</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-toolbar>

    <v-expansion-panel>
      <WordcloudMetadata v-bind:mini="mini"/>
      <WordcloudWindowsize v-bind:mini="mini"/>
      <!--<wordcloudTools v-bind:mini="mini"/>-->
    </v-expansion-panel>
  </v-navigation-drawer>
</template>

<script>
import { mapGetters } from "vuex";
import WordcloudMetadata from "@/components/Wordcloud/Sidebar/WordcloudMetadata";
import WordcloudWindowsize from "@/components/Wordcloud/Sidebar/WordcloudWindowsize";
import WordcloudTools from "@/components/Wordcloud/Sidebar/WordcloudTools";

export default {
  name: "WordcloudSidebar",
  components: {
    WordcloudMetadata,
    WordcloudWindowsize,
    WordcloudTools
  },
  data: () => ({
    sidebar: true,
    mini: true
  }),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: "analysis/analysis"
    })
  }
};
</script>

<style>
</style>
