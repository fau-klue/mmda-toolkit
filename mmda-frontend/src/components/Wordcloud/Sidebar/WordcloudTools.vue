<template>

      <v-card-text>
        <v-layout fill-height column ma-0>
        <v-flex shrink class="text-xs-right">
            <v-btn
              flat
              icon
              small
              ripple
              :value="i"
              v-for="(button,i) in tools"
              :key="button.icon"
              :title="button.title"
              @click="()=>{ if(button.call) wc[button.call](); if(button.call2) it[button.call2](); }"
              >
              <v-icon>{{button.icon}}</v-icon>
            </v-btn>
        </v-flex>
      </v-layout>
      </v-card-text>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "WordcloudTools",
  props:['wc'],
  data: () => ({
    it:null,
    tools: [
      {
        title: "view all",
        icon: "aspect_ratio",
        call: "centerCamera"
      },
      {
        title: "box selection [shift]",
        icon: "select_all",
        call: "startBoxSelection"
      },
      {
        title:
          "create new discourseme for selected items, or add selected items to selected discourseme [ctrl-g]",
        icon: "add_circle_outline",
        call: "groupSelected"
      },
      {
        title: "remove (selected items from) (selected) discourseme [del]",
        icon: "remove_circle_outline",
        call: "deleteSelection"
      },
      {
        title: "minimap (hide/show)",
        icon: "map",
        call: "toggleMinimap"
      },
    ]
  }),
  computed: {
    ...mapGetters({
      collocation: "collocation/collocation",
      windowSize: "wordcloud/windowSize",
      notMini: "wordcloud/rightSidebar"
    })
  },
  methods: {
    ...mapActions({
      setSidebar:"wordcloud/setRightSidebar"
    }),
  },
  mounted(){
    this.it=this;
  }
};
</script>

