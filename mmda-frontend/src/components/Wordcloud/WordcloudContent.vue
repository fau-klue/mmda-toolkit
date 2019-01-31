<template>
  <div>
    <div class="structured_wordcloud_container">
      <v-layout fill-height column ma-0>
        <v-flex shrink class="text-xs-right">
          <v-btn-toggle class="wordcloud_tools" v-model="tool">
            <v-btn
              flat
              icon
              :color="button.color"
              :value="i"
              v-for="(button,i) in tools"
              :key="button.icon+button.color"
              :title="button.title"
              @click="(x)=>{if(button.call) button.call(x);}"
              @mousedown="()=>wc.clickedTools=true"
            >
              <v-icon>{{button.icon}}</v-icon>
            </v-btn>
            <!-- <v-btn flat icon color="gray" title="hide tools" @click="show_tools=!show_tools">
              <v-icon>chevron_right</v-icon>
            </v-btn>-->
          </v-btn-toggle>
        </v-flex>
      </v-layout>
    </div>

    <!--
  <v-container grid-list-md>
    <v-layout row wrap>
      <v-flex xs12>
        <p>
          Window Size {{ windowSize }}
        </p>
        <p>
          {{ coordinates }}
        </p>
        <p>
          {{ concordances }}
        </p>
        <p>
          {{ collocates }}
        </p>
      </v-flex>
    </v-layout>
  </v-container>
    -->
    <WordcloudSidebar/>
  </div>
</template>

<style>
@import "../../wordcloud/wordcloud.module.css";
</style>

<script>
import { mapActions, mapGetters } from "vuex";
import { WordcloudWindow } from "@/wordcloud/wordcloud.js";
import rules from "@/utils/validation";
import WordcloudSidebar from "@/components/Wordcloud/WordcloudSidebar";
//import * as data from '@/wordcloud/example_1.js'
var vm;
export default {
  name: "WordcloudContent",
  components: {
    WordcloudSidebar
  },
  data: () => ({
    id: null,
    rules: rules,
    tool: null,
    wc: null,
    tools: [
      {
        icon: "aspect_ratio",
        color: "gray",
        title: "view all",
        call: () => vm.wc.centerCamera()
      },
      //{ icon: "search", color: "gray", title: "find item" },
      {
        icon: "select_all",
        color: "gray",
        title: "box selection [shift]",
        call: () => (vm.wc.boxSelection = true)
      },
      {
        icon: "add_circle_outline",
        color: "gray",
        title:
          "create new discourseme for selected items, or add selected items to selected discourseme [ctrl-g]",
        call: () => vm.wc.groupSelected()
      },
      {
        icon: "remove_circle_outline",
        color: "gray",
        title: "remove selected items from (selected) discourseme [del]",
        call: () => vm.wc.deleteSelection()
      },
      { icon: "undo", color: "lightgray", title: "undo (not yet implemented)" },
      { icon: "redo", color: "lightgray", title: "redo (not yet implemented)" },
      /*{ icon: "cached", color: "green" },
      { icon: "thumb_up", color: "deep-orange" },
      { icon: "favorite", color: "pink" },
      { icon: "star", color: "indigo" }*/
      {
        icon: "map",
        color: "gray",
        title: "minimap",
        call: () => (vm.wc.minimap.shown = !vm.wc.minimap.shown)
      }
    ]
  }),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: "analysis/analysis",
      discoursemes: "analysis/discoursemes",
      collocates: "analysis/collocates",
      coordinates: "coordinates/coordinates",
      concordances: "corpus/concordances",
      windowSize: "wordcloud/windowSize"
    })
  },
  methods: {
    ...mapActions({
      getConcordances: "corpus/getConcordances",
      getCollocates: "analysis/getAnalysisCollocates"
    }),
    fetchCollocates(window_size) {
      const request = {
        params: { window_size: window_size }
      };
      const data = {
        username: this.user.username,
        analysis_id: this.id,
        request: request
      };
      this.getCollocates(data)
        .then(() => {
          this.error = null;
          if (this.wc)
            this.wc.setupContent2(
              this.collocates,
              this.coordinates,
              this.discoursemes
            );
        })
        .catch(error => {
          this.error = error;
        });
    },
    fetchConcordances(items) {
      let params = new URLSearchParams();
      // Concat item parameter
      items.forEach(function(item) {
        params.append("item", item);
      });
      const request = {
        params: params
      };
      const data = {
        corpus: this.analysis.corpus,
        request: request
      };
      this.getConcordances(data)
        .then(() => {
          this.error = null;
        })
        .catch(error => {
          this.error = error;
        });
    }
  },
  centerItemLocation(item_string) {
    this.wc.centerAtWord(item_string);
  },
  created() {
    this.id = this.$route.params.id;
    //this.fetchConcordances(['test', 'anothertest'])
    this.fetchCollocates(3);
  },
  mounted() {
    vm = this;
    let WW = [];
    for (let A of document.getElementsByClassName(
      "structured_wordcloud_container"
    )) {
      WW.push((this.wc = new WordcloudWindow(A)));
      window.addEventListener("resize", (W => () => W.resize())(this.wc));
      //wc.setupContent2(this.collocates, this.coordinates, this.discoursemes);
      break;
    }
  },
  beforeDestroy() {
    console.log("DESTROY!!");
    this.wc.destroy(); //removing event listeners from document for example
    delete this.wc;
  }
};
</script>