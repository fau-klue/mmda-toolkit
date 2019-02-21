<template>
  <div>
    <div class="structured_wordcloud_container">
      <!--v-layout v-if="false && !notMini" fill-height column ma-0>
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
            <!- <v-btn flat icon color="gray" title="hide tools" @click="show_tools=!show_tools">
              <v-icon>chevron_right</v-icon>
            </v-btn>->
          </v-btn-toggle>
        </v-flex>
      </v-layout -->
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
    <WordcloudSidebar v-bind:wc="wc"/>
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
var vm=null;
export default {
  name: "WordcloudContent",
  components: {
    WordcloudSidebar
  },
  data: () => ({
    mini : true,
    error : null,
    id: null,
    rules: rules,
    wc: null,
    resizeEvent: null,
    has_data: false,
    /*tools: [
      {
        title: "view all",
        icon: "aspect_ratio",
        color: "gray",
        call: () => {
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
          vm.wc.boxSelection = true;
        }
      },
      {
        title:
          "create new discourseme for selected items, or add selected items to selected discourseme [ctrl-g]",
        icon: "add_circle_outline",
        color: "gray",
        call: () => {
          vm.wc.groupSelected();
        }
      },
      {
        title: "remove (selected items from) (selected) discourseme [del]",
        icon: "remove_circle_outline",
        color: "gray",
        call: () => {
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
    ]*/
  }),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: "analysis/analysis",
      discoursemes: "analysis/discoursemes",
      collocates: "analysis/collocates",
      coordinates: "coordinates/coordinates",
      concordances: "corpus/concordances",
      notMini:"wordcloud/rightSidebar",
      windowSize: "wordcloud/windowSize",
      AM: "wordcloud/associationMeasure",
      showMinimap: "wordcloud/showMinimap"
    })
  },
  watch:{
    AM () {
      this.wc.changeAM();
    },
    collocates () {
      vm.wc.setupCollocates(vm.collocates);
    },
    coordinates () {
      vm.wc.setupCoordinates(vm.coordinates);
    },
    discoursemes () {
      vm.wc.setupDiscoursemes(vm.discoursemes);
    },
    windowSize () {
      vm.loadCollocates(vm.windowSize);
    },
    error (){
      console.error(this.error);
    }
  },
  methods: {
    ...mapActions({
      getConcordances: "corpus/getConcordances",
      getAnalysisCollocates: "analysis/getAnalysisCollocates",
      addUserDiscourseme: "discourseme/addUserDiscourseme",
      updateUserDiscourseme: "discourseme/updateUserDiscourseme",
      deleteUserDiscourseme: "discourseme/deleteUserDiscourseme",
      getUserDiscoursemes: "discourseme/getUserDiscoursemes",
      setUserCoordinates: "coordinates/setUserCoordinates",
      getAnalysisCoordinates: "coordinates/getAnalysisCoordinates",
      addDiscoursemeToAnalysis: 'analysis/addDiscoursemeToAnalysis',
      setAM: 'wordcloud/setAssociationMeasure',
      setShowMinimap: 'wordcloud/setShowMinimap'
    }),
/*
    initializeData() {
      return Promise.all([
        this.loadCoordinates(),
        this.loadCollocates(this.windowSize),
        this.loadDiscoursemes()
      ]);
    },*/

    loadCoordinates() {
      return this.getAnalysisCoordinates({
        username:     this.user.username,
        analysis_id:  this.analysis.id
      }).catch((error)=>{
        this.error = error;
      })
    },
    loadCollocates(window_size) {
      return this.getAnalysisCollocates({
        username:     this.user.username,
        analysis_id:  this.analysis.id,
        window_size:  window_size
      }).catch((error)=>{
        this.error = error;
      });
    },
    loadDiscoursemes() {
      return this.getUserDiscoursemes(
        this.user.username
      ).catch(error => {
        this.error = error;
      });
    },

    addDiscourseme(name, items) {
      return new Promise((resolve,reject)=>{
        this.addUserDiscourseme({
          name: name,
          items: items,
          username: this.user.username
        }).catch(error => {
          reject(error);
        }).then(result =>{
          var id = result;

          this.addDiscoursemeToAnalysis({
            username: this.user.username,
            analysis_id: this.analysis.id,
            discourseme_id: id
          }).then(()=>{
            resolve( id );
          }).catch((error)=>{
            reject( error );
          })
        });
      }).catch(error=>{
        this.error = error;
      });
    },

    deleteDiscourseme(id) {
      return this.deleteUserDiscourseme({
        username: this.user.username,
        discourseme_id: id
      }).catch(error => {
        this.error = error;
      });
    },

    updateDiscourseme(id, name, items) {
      return this.updateUserDiscourseme({
        discourseme_id: id,
        name: name,
        items: items,
        username: this.user.username
      }).catch(error => {
        this.error = error;
      });
    },
    setCoordinates( obj ) {
      //obj: {<item2>:{user_x:<number>,user_y:<number>}, <item2>:{...}, ... }
      return this.setUserCoordinates({
        username: this.user.username,
        analysis_id: this.analysis.id,
        user_coordinates: obj
      }).catch(error => {
        this.error = error;
      });
    },   

    centerItemLocation(item_string) {
      this.wc.centerAtWord(item_string);
    }
  },
  created() {
    this.id = this.$route.params.id;
  },
  mounted() {
    vm=this;
    let A = document.getElementsByClassName("structured_wordcloud_container");
    this.wc = new WordcloudWindow(A[0], this);
    window.addEventListener(
      "resize",
      (this.resizeEvent = (W => () => W.resize())(this.wc))
    );

    //setup already present data
    this.wc.minimap.shown = this.showMinimap;
    if(this.coordinates) this.wc.setupCoordinates(this.coordinates);
    if(this.collocates)  this.wc.setupCollocates(this.collocates);
    if(this.discoursemes) this.wc.setupDiscoursemes(this.discoursemes);
    
    //fetch new data
    this.loadCoordinates();
    this.loadCollocates(this.windowSize).then(()=>{
      //TODO:: do we want to select any present AM or a static one (e.g. MI)
      var oneAM = this.collocates.MI?'MI':Object.keys(this.collocates)[0];
      this.setAM( oneAM || 'MI' );
    });
    this.loadDiscoursemes();
  },
  beforeDestroy() {
    //e.g. removing event listeners from document
    this.wc.destroy();
    delete this.wc;
    window.removeEventListener("resize", this.resizeEvent);
  }
};
</script>