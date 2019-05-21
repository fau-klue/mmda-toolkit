<template>
  <div>
    <div class="structured_wordcloud_container">
      <!-- This is controlled by the wordcloud.js -->
    </div>

    <WordcloudSidebar v-bind:wc="wc"/>
    <WordcloudBottomSheet v-bind:onclickitem="centerItemLocation" />
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
import WordcloudBottomSheet from "@/components/Wordcloud/WordcloudBottomSheet";
var vm = null;

export default {
  name: "WordcloudContent",
  components: {
    WordcloudSidebar,
    WordcloudBottomSheet
  },
  data: () => ({
    mini : true,
    error : null,
    id: null,
    rules: rules,
    wc: null,
    resizeEvent: null,
    has_data: false
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
      showMinimap: "wordcloud/showMinimap",
      SOC: 'wordcloud/secondOrderCollocationDiscoursemeIDs',
      collocatesCompare: 'wordcloud/collocatesToCompare',
    }),
    SOC_items(){
      var res = new Set();
      for(var id of this.SOC){
        var i = this.discoursemes.findIndex((d)=>d.id==id);
        if(i!=-1){
          for(var it of this.discoursemes[i].items ) res.add(it);
        }
      }
      return Array.from(res);
    }
  },
  watch:{
    SOC(){
      vm.loadCollocates();
    },
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
      vm.loadCollocates();
    },
    error (){
      console.error("WordcloudContent")
      console.error(this.error);
    },
    collocatesCompare(){
      this.wc.changeAM();
    }
  },
  methods: {
    ...mapActions({
      getConcordances: "corpus/getConcordances",
      cancelConcordanceRequest:'corpus/cancelConcordanceRequest',
      getAnalysisCollocates: "analysis/getAnalysisCollocates",
      getAnalysisDiscoursemeCollocates: "analysis/getAnalysisDiscoursemeCollocates",
      addUserDiscourseme: "discourseme/addUserDiscourseme",
      updateUserDiscourseme: "discourseme/updateUserDiscourseme",
      deleteUserDiscourseme: "discourseme/deleteUserDiscourseme",
      getUserDiscoursemes: "discourseme/getUserDiscoursemes",
      setUserCoordinates: "coordinates/setUserCoordinates",
      getAnalysisCoordinates: "coordinates/getAnalysisCoordinates",
      addDiscoursemeToAnalysis: 'analysis/addDiscoursemeToAnalysis',
      setAM: 'wordcloud/setAssociationMeasure',
      setShowMinimap: 'wordcloud/setShowMinimap',
       
    }),
    loadCoordinates() {
      if(!this.analysis) return;
      return this.getAnalysisCoordinates({
        username:     this.user.username,
        analysis_id:  this.analysis.id
      }).catch((error)=>{
        this.error = error;
      })
    },
    loadCollocates() {
      if(!this.analysis) return;
      if(this.SOC.length){
        return this.getAnalysisDiscoursemeCollocates({
          username:     this.user.username,
          analysis_id:  this.analysis.id,
          window_size:  this.windowSize,
          discourseme_items: this.SOC_items,
        }).catch((error)=>{
          this.error = error;
        });
      }else{
        return this.getAnalysisCollocates({
          username:     this.user.username,
          analysis_id:  this.analysis.id,
          window_size:  this.windowSize
        }).catch((error)=>{
          this.error = error;
        });
      }
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

        if(!this.analysis){reject(); return;}

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
            this.loadDiscoursemes();
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
      }).then(()=>{
        this.loadDiscoursemes();
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
      }).then(()=>{
        this.loadDiscoursemes();
      });
    },
    setUserCoordinate(name,x,y){
      var obj = {};
      obj[name] = {user_x:x, user_y:y};
      this.setCoordinates(obj);
    },
    setCoordinates( obj ) {
      if(!this.analysis) return;
      //console.log("Set User Coordinates");
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
    },
    getTopicConcordancesFromList (names) {
      if(!this.analysis) return;
      this.loadingConcordances = true;
      this.concordancesRequested = true;
      this.getConcordances({
        corpus:           this.analysis.corpus,
        topic_items:      this.analysis.topic_discourseme.items,
        collocate_items:  names,
        window_size:      this.windowSize
      }).catch((error)=>{
        this.error = error
      }).then(()=>{
        this.loadingConcordances = false;
      });
    },
  },
  created() {
    this.id = this.$route.params.id;
  },
  mounted() {
    vm = this;
    if(!this.analysis) return this.$router.push('/analysis');  //fallback

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
    //this.loadCoordinates(); // this is already done in the analysis window?!
    this.loadCollocates().then(()=>{
      if(!this.collocates[this.AM]){
        var oneAM = this.collocates.MI?'MI':Object.keys(this.collocates)[0];
        this.setAM( oneAM || 'MI' );
      }
    });
    this.loadDiscoursemes();
  },
  beforeDestroy() {
    //e.g. removing event listeners from document
    if(this.wc){
      this.wc.destroy();
      delete this.wc;
    }
    window.removeEventListener("resize", this.resizeEvent);
  }
};
</script>
