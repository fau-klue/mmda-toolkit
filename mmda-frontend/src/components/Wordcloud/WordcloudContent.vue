<template>
  <div>

    <div class="structured_wordcloud_container"><!-- This is controlled by the wordcloud.js --></div>

    <WordcloudSidebar v-bind:wc="wc"/>

    <WordcloudBottomSheet ref="bottomSheet" v-bind:onclickitem="centerItemLocation" v-bind:sheetVisible="sheetVisible" v-bind:onchangevisibility="onChangeVisibility" />
    <v-layout style="position:absolute;height:calc(100vh - 48px);width:100%;pointer-events:none">
      <v-layout v-if="!sheetVisible" justify-center align-end>
        <v-btn color="info" style="pointer-events:all;z-index:9000" class="text-xs-center" @click="_getTopicConcordancesFromList">Concordance Lines</v-btn>
      </v-layout>
    </v-layout>

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
    has_data: false,
    conc_request_cache: ['test'],
    request_names: [],
    sheetVisible: true
  }),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: "analysis/analysis",
      discoursemes: "analysis/discoursemes",
      collocates: "analysis/collocates",
      coordinates: "coordinates/coordinates",
      concordances: "analysis/concordances",
      notMini:"wordcloud/rightSidebar",
      windowSize: "wordcloud/windowSize",
      AM: "wordcloud/associationMeasure",
      showMinimap: "wordcloud/showMinimap",
      discourseme_ids: 'wordcloud/secondOrderCollocationDiscoursemeIDs',
      collocatesCompare: 'wordcloud/collocatesToCompare',
    }),
    /*SOC_items(){
      var res = new Set();
      for(var id of this.discourseme_ids){
        var i = this.discoursemes.findIndex((d)=>d.id==id);
        if(i!=-1){
          for(var it of this.discoursemes[i].items ) res.add(it);
        }
      }
      return Array.from(res);
    }*/
  },
  watch:{
    discourseme_ids(){
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
    },
    sheetVisible(){
      // console.log("in WordcloudContent: " + this.sheetVisible)
    }
  },
  methods: {
    ...mapActions({
      getConcordances: "analysis/getConcordances",
      AnalysiscancelConcordanceRequest:'analysis/cancelConcordanceRequest',
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
      onChangeVisibility(x){
        this.sheetVisible=x
      },
      cancelConcordanceRequest(){
          this.AnalysiscancelConcordanceRequest()
          this.getTopicConcordancesFromList([])
      },
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
      if(this.discourseme_ids && this.discourseme_ids.length){
        return this.getAnalysisDiscoursemeCollocates({
          username:     this.user.username,
          analysis_id:  this.analysis.id,
          window_size:  this.windowSize,
          //discourseme_items: this.SOC_items,
          discourseme_ids:this.discourseme_ids
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
      obj[name] = {x_user:x, y_user:y};
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
      this.request_names=names;
    },
    _getTopicConcordancesFromList () {
      this.sheetVisible=true;
      let names=this.request_names;
      if(!this.analysis) return;
        if( names.length==this.conc_request_cache.length
            && names.map((a,i)=>a==this.conc_request_cache[i] )
            .reduce((a,b)=>a&&b,true) ) return;
        this.conc_request_cache = names
      this.loadingConcordances = true;
      this.concordancesRequested = true;
      this.getConcordances({
        username :this.user.username,
        analysis_id: this.analysis.id,
        discourseme_ids: this.discourseme_ids,
        items: names,
        window_size: this.windowSize
      }).catch((error)=>{
        this.$refs.bottomSheet.error = error.response.data.msg;
        //this.error = error
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
