<template>
  <v-expansion-panel-content>
    <div slot="header" v-if="!mini">Tools</div>
    <v-card>
      <v-card-text>
        <v-container fluid class="pa-0">
          <v-btn-toggle class="wordcloud_tools" v-model="tool" mandatory>
            <v-layout row wrap>
              <v-flex v-for="(button,i) in tools" :key="button.icon+button.color">
                <v-btn flat icon :color="button.color" :value="i">
                  <v-icon>{{button.icon}}</v-icon>
                </v-btn>
              </v-flex>
            </v-layout>
          </v-btn-toggle>
        </v-container>
      </v-card-text>
    </v-card>
  </v-expansion-panel-content>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "WordcloudTools",
  props: ["mini"],
  data: () => ({
    min: 2,
    tool: 0,
    tools: [
      { icon: "favorite", color: "pink" },
      { icon: "star", color: "indigo" },
      { icon: "cached", color: "green" },
      { icon: "thumb_up", color: "deep-orange" },
      { icon: "favorite", color: "pink" },
      { icon: "star", color: "indigo" },
      { icon: "star", color: "indigo" },
      { icon: "cached", color: "green" },
      { icon: "cached", color: "green" }
    ]
  }),
  computed: {
    ...mapGetters({
      analysis: "analysis/analysis",
      windowSize: "wordcloud/windowSize"
    })
  },
  methods: {
    ...mapActions({})
  }
};
</script>

