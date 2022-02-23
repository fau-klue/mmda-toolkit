<template>
  <div>

    <div class="structured_wordcloud_container"><!-- This is controlled by the wordcloud.js --></div>

    <WordcloudKeywordSidebar v-bind:wc="wc"/>

    <WordcloudKeywordBottomSheet ref="bottomSheet" v-bind:onclickitem="centerItemLocation" v-bind:sheetVisible="sheetVisible" v-bind:onchangevisibility="onChangeVisibility" />
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
import WordcloudKeywordSidebar from "@/components/WordcloudKeyword/WordcloudKeywordSidebar";
import WordcloudKeywordBottomSheet from "@/components/WordcloudKeyword/WordcloudKeywordBottomSheet";
var vm = null;

export default {
  name: "WordcloudKeywordContent",
  components: {
    WordcloudKeywordSidebar,
    WordcloudKeywordBottomSheet
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
      keyword: "keyword/keyword",
      discoursemes: "keyword/discoursemes",
      collocates: "keyword/keywords",
      coordinates: "coordinates/coordinates",
      concordances: "keyword/concordances",
      notMini:"wordcloud/rightSidebar",
      AM: "wordcloud/associationMeasure",
      showMinimap: "wordcloud/showMinimap",
      discourseme_ids: 'wordcloud/secondOrderCollocationDiscoursemeIDs',
      collocatesCompare: 'wordcloud/collocatesToCompare',
    }),
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
    error (){
      console.error("WordcloudKeywordContent")
      console.error(this.error);
    },
    collocatesCompare(){
      this.wc.changeAM();
    },
    sheetVisible(){
      // console.log("in WordcloudKeywordContent: " + this.sheetVisible)
    }
  },
  methods: {
    ...mapActions({
      getConcordances: "keyword/getConcordances",
      KeywordCancelConcordanceRequest:'keyword/cancelConcordanceRequest',
      getKeywordKeywords: "keyword/getKeywordKeywords",
      addUserDiscourseme: "discourseme/addUserDiscourseme",
      updateUserDiscourseme: "discourseme/updateUserDiscourseme",
      deleteUserDiscourseme: "discourseme/deleteUserDiscourseme",
      getUserDiscoursemes: "discourseme/getUserDiscoursemes",
      setUserCoordinatesKeyword: "coordinates/setUserCoordinatesKeyword",
      getKeywordCoordinates: "coordinates/getKeywordCoordinates",
      addDiscoursemeToKeyword: 'keyword/addDiscoursemeToKeyword',
      setAM: 'wordcloud/setAssociationMeasure',
      setShowMinimap: 'wordcloud/setShowMinimap',
      
    }),
      onChangeVisibility(x){
        this.sheetVisible=x
      },
    cancelConcordanceRequest(){
          this.KeywordCancelConcordanceRequest()
          this.getTopicConcordancesFromList([])
      },
    loadCoordinates() {
      if(!this.keyword) return;
      return this.getKeywordCoordinates({
        username:     this.user.username,
        keyword_id:  this.keyword.id
      }).catch((error)=>{
        this.error = error;
      })
    },
    loadCollocates() {
      if(!this.keyword) return;
      if(this.discourseme_ids && this.discourseme_ids.length){
        return this.getKeywordDiscoursemeCollocates({
          username:     this.user.username,
          keyword_id:  this.keyword.id,
          discourseme_ids:this.discourseme_ids
        }).catch((error)=>{
          this.error = error;
        });
      }else{
        return this.getKeywordKeywords({
          username:     this.user.username,
          keyword_id:  this.keyword.id,
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
        if(!this.keyword){reject(); return;}
        this.addUserDiscourseme({
          name: name,
          items: items,
          username: this.user.username
        }).catch(error => {
          reject(error);
        }).then(result =>{
          var id = result;
          this.addDiscoursemeToKeyword({
            username: this.user.username,
            keyword_id: this.keyword.id,
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
      if(!this.keyword) return;
      //console.log("Set User Coordinates");
      //obj: {<item2>:{user_x:<number>,user_y:<number>}, <item2>:{...}, ... }
      return this.setUserCoordinatesKeyword({
        username: this.user.username,
        keyword_id: this.keyword.id,
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
      if(!this.keyword) return;
        if( names.length==this.conc_request_cache.length
            && names.map((a,i)=>a==this.conc_request_cache[i] )
            .reduce((a,b)=>a&&b,true) ) return;
        this.conc_request_cache = names
      this.loadingConcordances = true;
      this.concordancesRequested = true;
      this.getConcordances({
        username :this.user.username,
        keyword_id: this.keyword.id,
        discourseme_ids: this.discourseme_ids,
        items: names
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
    if(!this.keyword) return this.$router.push('/keyword');  //fallback

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
  }
};
</script>
