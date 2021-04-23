<template>
  <div class="wordcloud-minimap-preview" :style="minimapStyle">
  <div  class="title">{{label}}</div>
    <div v-for="c in coords" class="item" :style="c.style" :title="c.title" :key="c.title"/>
  </div>
</template>

<style>
.wordcloud-minimap-preview{
  /*background-color: antiquewhite; */
  overflow: hidden;
  position: relative;
  max-width: 100%;
  left: 50%;
  transform: translate(-50%,0);
  background-color: #aaa7;
  box-shadow: 0 0 1rem #0002;
  border: 0.2rem solid #0001;
  /*border-top-left-radius: 0.5rem;*/
}
.wordcloud-minimap-preview .item{
  width: 0.3rem;
  height: 0.3rem;
  position: absolute;
  border-radius: 0.15rem;
  background-color: #000a;
  transform: translate(-50%,-50%);
}
.wordcloud-minimap-preview .title{
  position: absolute;
  left:50%;
  top:50%;
  transform: translate(-50%,-50%);
}
</style>

<script>
import { mapGetters } from "vuex";
import {min2,max2,sub2,div2} from "@/wordcloud/util_math.js";

export default {
  name: "WordcloudMinimap",
  components: {},
  props:['label','height'],
  data: () => ({}),
  computed: {
    ...mapGetters({
      user: "login/user",
      analysis: "analysis/analysis",
      coordinates: "coordinates/coordinates",
    }),
    aspect(){
      var b = this.bounds;
      var D = sub2(b.max,b.min);
      var res = D[0] / D[1];
      if(isNaN(res)) return 1;
      return res;
    },
    minimapStyle(){
      return "width:"+this.aspect *this.height+"rem; height:"+ this.height+"rem;";
    },
    coords(){
      var res = [];
      if(!this.coordinates) return res;
      var b = this.bounds;
      var D = sub2(b.max,b.min);
      var a = this.aspect;
      var h = this.height;
      function toClipSpace(p){return div2(sub2(p,b.min), D);}
      function styleForPosition(p){
        var x = toClipSpace(p);
        return "left:" + x[0] * h *a     + "rem;"
          + "top:" + x[1] * h  + "rem;";
      }
      for(var c of Object.keys(this.coordinates)){
        var d = this.coordinates[c];
        res.push({title:c, style:styleForPosition([d.x,d.y])});
      }
      return res;
    },
    bounds(){
      var b = {
        min:[Number.POSITIVE_INFINITY,Number.POSITIVE_INFINITY],
        max:[Number.NEGATIVE_INFINITY,Number.NEGATIVE_INFINITY]
      }
      if(!this.coordinates) return b;
      for(var c of Object.keys(this.coordinates)){
        var d = this.coordinates[c];
        b.min = min2([d.x,d.y],b.min);
        b.max = max2([d.x,d.y],b.max);
      }
      return b;
    }
  },
};
</script>
