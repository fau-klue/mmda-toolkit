<template>
  <div>
    <div class="structured_wordcloud_container">
      <v-layout fill-height column ma-0>
        <v-flex shrink class="text-xs-right">
          <v-btn-toggle class="wordcloud_tools" v-model="tool">
            <v-btn
              flat
              icon
              style="z-index:500;"
              ripple
              :color="button.color"
              :value="i"
              v-for="(button,i) in tools"
              :key="button.icon+button.color"
              :title="button.title"
              @click="(x)=>{ if(button.call) button.call(x);}"
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
import { Promise, reject } from "q";
import { resolve } from 'path';
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
    resizeEvent: null,
    has_data: false,
    tools: [
      {
        title: "view all",
        icon: "aspect_ratio",
        color: "gray",
        call: () => {
          vm.tool = null;
          vm.wc.centerCamera();
        }
      },
      //{ icon: "search", color: "gray", title: "find item" },
      {
        title: "box selection [shift]",
        icon: "select_all",
        color: "gray",
        call: () => {
          //TODO:: on finished box selection tool=null;
          vm.tool = null;
          vm.wc.boxSelection = true;
        }
      },
      {
        title:
          "create new discourseme for selected items, or add selected items to selected discourseme [ctrl-g]",
        icon: "add_circle_outline",
        color: "gray",
        call: () => {
          vm.tool = null;
          vm.wc.groupSelected();
        }
      },
      {
        title: "remove (selected items from) (selected) discourseme [del]",
        icon: "remove_circle_outline",
        color: "gray",
        call: () => {
          vm.tool = null;
          vm.wc.deleteSelection();
        }
      },
      //{ icon: "undo", color: "lightgray", title: "undo (not yet implemented)" },
      //{ icon: "redo", color: "lightgray", title: "redo (not yet implemented)" },
      {
        title: "minimap (hide/show)",
        icon: "map",
        color: "gray",
        call: () => {
          vm.tool = null;
          vm.wc.minimap.shown = !vm.wc.minimap.shown;
        }
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
      getCollocates: "analysis/getAnalysisCollocates",
      addUserDiscourseme: "discourseme/addUserDiscourseme",
      updateUserDiscourseme: "discourseme/updateUserDiscourseme",
      deleteUserDiscourseme: "discourseme/deleteUserDiscourseme",
      getUserDiscoursemes: "discourseme/getUserDiscoursemes",
      setUserCoordinates: "coordinates/setUserCoordinates",
      getAnalysisCoordinates: "coordinates/getAnalysisCoordinates",
      addDiscoursemeToAnalysis: 'analysis/addDiscoursemeToAnalysis',
    }),

    initializeData() {
      return Promise.all([
        this.loadCoordinates(),
        this.loadCollocates(2),
        this.loadDiscoursemes()
      ]);
    },

    loadCoordinates() {
      const data = {
        username: this.user.username,
        analysis_id: this.id
      };
      return this.getAnalysisCoordinates(data);
    },
    loadCollocates(window_size) {
      const request = {
        params: { window_size: window_size }
      };
      const data = {
        username: this.user.username,
        analysis_id: this.id,
        request: request
      };
      return this.getCollocates(data);
    },
    loadDiscoursemes() {
      return this.getUserDiscoursemes(this.user.username).catch(error => {
        console.error(error);
      });
    },

    addDiscourseme(name, items) {
      return new Promise((resolve,reject)=>{
        const data = {
          name: name,
          items: items,
          username: this.user.username
        };
        this.addUserDiscourseme(data).catch(error => {
          reject(error);
        }).then((e)=>{
          var id = e;

          this.addToAnalysis(id).then(()=>{
            resolve(id);
          }).catch((error)=>{
            reject(error);
          })
        });
      }).catch((error)=>{
        console.error(error);
      });
    },
    addToAnalysis(discourseme_id){
        const data = {
          username: this.user.username,
          analysis_id: this.id,
          discourseme_id: discourseme_id
        }
        return this.addDiscoursemeToAnalysis(data);//.catch((error) => {
         // console.error( error );
        //});
    },

    deleteDiscourseme(id) {
      const data = {
        username: this.user.username,
        discourseme_id: id
      };
      return this.deleteUserDiscourseme(data).catch(error => {
        console.error(error);
      });
    },

    updateDiscourseme(id, name, items) {
      const data = {
        discourseme_id: id,
        name: name,
        items: items,
        username: this.user.username
      };
      return this.updateUserDiscourseme(data).catch(error => {
        console.error(error);
      });
    },
    setCoordinates( obj ) {
      //obj: {<item2>:{user_x:<number>,user_y:<number>}, <item2>:{...}, ... }
      const data = {
        username: this.user.username,
        analysis_id: this.id,
        user_coordinates: obj
      };
      return this.setUserCoordinates(data)
        .catch(error => {
          console.error(error);
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
    },
    

    setupContent() {
      if (this.has_data && this.wc) {
      }
    },

    centerItemLocation(item_string) {
      this.wc.centerAtWord(item_string);
    }
  },
  created() {
    this.id = this.$route.params.id;
    console.log("ID: " + this.id);
    //this.fetchConcordances(['test', 'anothertest'])
    this.initializeData()
      .then(() => {
        this.error = null;
        if (this.wc)
          this.wc.setupContent(
            this.collocates,
            this.coordinates,
            this.discoursemes
          );
      })
      .catch(e => {
        this.error = e;
        if (this.wc) this.wc.errors.set("No Data Available", "" + e);
        else console.error("Data Initialization Failed: " + e);
      });
  },
  mounted() {
    vm = this;
    let A = document.getElementsByClassName("structured_wordcloud_container");
    this.wc = new WordcloudWindow(A[0], this);
    window.addEventListener(
      "resize",
      (this.resizeEvent = (W => () => W.resize())(this.wc))
    );
  },
  beforeDestroy() {
    //e.g. removing event listeners from document
    this.wc.destroy();
    delete this.wc;
    window.removeEventListener("resize", this.resizeEvent);
  }
};
</script>