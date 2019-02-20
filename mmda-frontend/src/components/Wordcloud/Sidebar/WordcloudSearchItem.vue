<template>
<v-expansion-panel-content>
  <div slot="header" v-if="notMini" >Find</div>
  <div slot="header" v-else @click="openSidebar">
    <v-btn
              flat
              icon
              ripple
              title="search for discourseme or item"
            >
              <v-icon>search</v-icon>
    </v-btn>
  </div>
  <v-card v-if="notMini">
    <v-card-text>
        <v-layout>
          <v-flex xs12 sm12>
            <v-text-field label="Search" prepend-inner-icon="search" v-model="search" clearable @click:clear="clearSearch"></v-text-field>

            <v-list two-line subheader>
              <v-list-tile v-for="item in filteredItems" :key="item.name+(item.isGroup?'GROUP':'')" avatar @click="findElement(item)">
                <v-list-tile-avatar>
                  <v-icon v-if="!item.isItem" class="grey lighten-1 white--text">subject</v-icon>
                  <v-icon v-if="item.isItem" class="grey lighten-1 white--text">short_text</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ item.name }}</v-list-tile-title>
                  <v-list-tile-sub-title v-if="item.isGroup">{{ item.items }}</v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-flex>
        </v-layout>
    </v-card-text>
  </v-card>
</v-expansion-panel-content>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'WordcloudSearchItem',
  props:["wc"],
  data: () => ({
    min: 2,
    search:'',
  }),
  computed: {
    ...mapGetters({
      analysis: 'analysis/analysis',
      notMini:   'wordcloud/rightSidebar',
      coordinates: 'coordinates/coordinates',
    }),
    mappedCoordinates(){
        return Object.keys(this.coordinates).map(i=>{return{name:i, isItem:true};});
    },
    mappedDiscoursemes(){
        //TODO:: watch for changes in this.wc.groups, as they might not be updated yet
        if(!this.wc) return [];
        else return [...this.wc.groups].map(g=>{return {name:g.name||g.contentString, isGroup:true, g:g, items: g.item_names};});
    },
    filteredItems() {
      var R = [];
      if (!this.search) {
        R = this.mappedCoordinates.concat(this.mappedDiscoursemes);
      } else {
        R = this.mappedCoordinates.filter(items => items.name.toLowerCase().search(this.search.toLowerCase()) >= 0  )
        .concat( this.mappedDiscoursemes.filter(items => items.name.toLowerCase().search(this.search.toLowerCase()) >= 0 ||
                                                         items.items.join("").toLowerCase().search(this.search.toLowerCase()) >= 0 ));
                                       }
      R.sort((x)=>x.name)
      return R
    }
  },
  methods: {
    ...mapActions({
      setRightSidebar:"wordcloud/setRightSidebar"
    }),
    clearSearch(){
      this.search="";
    },
    openSidebar(){
      this.setRightSidebar(true);
    },
    findElement(item){
      if(item.isItem) this.wc.centerAtWord(item.name)
      else this.wc.centerAtGroup(item.g)
    }
  }
}
</script>

