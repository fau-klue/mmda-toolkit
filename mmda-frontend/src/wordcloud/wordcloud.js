//import * as d3 from "./d3.js";
import "./svg.min.js";
import {
  mul2,
  sub2,
  add2,
  scale2,
  div2,
  rand2,
  lerp2,
  lerp,
  len2,
  normalize2,
  dot2,
  cross2,
  min2,
  max2,
  inf2,
  negInf2,
  abs2,
  sign2,
  nan2
} from "./util_math.js";
import {
  hex_color_from_array,
  oneOf,
  random_color,
  //  hsv_to_rgb,
  fwdEvent,
  domSet,
  domSetEL,
} from "./util_misc.js";

import {
  Minimap
} from "./element_minimap.js";
import {
  WordElement
} from "./word_element.js";
import {
  WordGroup
} from "./word_group.js";
import * as layout from "./layout_generation.js";
import {
  SelectionBox
} from "./selection_box.js";
import {
  WordCanvas
} from "./word_canvas.js";

///////////////////////////////////////
//
//    Error Message
//
///////////////////////////////////////

class ErrorMessage {
  constructor(window) {
    this.window = window;

    this.el = document.createElement("div");
    this.el.classList.add("wordcloud_error_container");
    this.window.el.appendChild(this.el);
  }
  clear() {
    this.set("","");
    //if (!this.content) this.el.removeChild(this.content);
    //this.content = undefined;
  }
  set(msg, title) {
    if (!this.content){
      //this.el.removeChild(this.content);
      this.content = document.createTextNode("");
      this.el.appendChild(this.content);
    }
    

    domSetEL(this.content,'textContent',msg?"🔵 " + msg:'');
    domSetEL(this.el,'title',title);
    //if (this.content) this.el.removeChild(this.content);
    //this.content = document.createTextNode("⚠ " + msg);
    //this.el.appendChild(this.content);
  }
}

///////////////////////////////////////
//
//    Wordcloud Window
//
///////////////////////////////////////

class WordcloudWindow {
  constructor(content_div, component) {
    this.el = content_div;
    this.component = component;

    this.Map = new Map();
    this.selected_nodes = new Set();
    this.groups = new Set();
    this.groupMap = new Map();
    this.am_minmax = {};
    this.mouse = [0,0];

    this.options = {
      verbose: false,
      remap_tsne_positions: true,
      remap_standard_deviation_factor: 2,
      remap_standard_deviation_log: false,
      remap_standard_deviation_clamp: true,
      resolve_overlap: true,
      reposition_shown_by_color: false,
      reposition_shown_by_shadow: false,
      reposition_shown_by_line: false,
      word_trend_show: true,
      show_groups: true,
      relocation_by_group: 0.5, //0.5;
      multigroup_attraction: 0.1, //0.5;
      draw_group_schnoerkel: false,
      show_lexical_items_of_group: true
    };
    /*
        this.option_explained = {
          remap_tsne_positions: "Reduces the area according to the standard deviation of the contained items.",
          remap_standard_deviation_log: "Every item is repositioned according to a logarithmic-scale.",
          remap_standard_deviation_clamp: "Overflowing items are clamped to the border of the area.",
          resolve_overlap: "Prevents item overlaps by moving the smaller item away.",
          relocation_by_group: "The positions of words inside the group are scaled by this factor (at the group center of mass).",
          multigroup_attraction: "Words inside multiple groups are scaled towards them by this factor"
        };*/

    this.resize();

    this.container = document.createElement("div");
    this.container.classList.add("sw_container");
    this.el.appendChild(this.container);

    this._scale = 1;
    this._pos = [0, 0];

    this.minimap = new Minimap(this);
    this.error = new ErrorMessage(this);
    //    this.word_menu = new WordMenu(this);
    this.selectionBox = new SelectionBox(this);
    this.canvas = new WordCanvas(this);

    this.scale = this.scale;
    this.pos = this.pos;

    this.setupEventListeners();
  }

  destroy() {
    this.deleteEventListeners();
  }

  log(s) {
    if (this.options.verbose) {
      console.log(s);
    }
  }

  get WH() {
    //if(this._WH===undefined) 
    this._WH = [this.el.offsetWidth, this.el.offsetHeight];
    return this._WH;
  }

  ///////////////////////////////////////
  //
  //     Object and Dom-Object synchronicity getter and setter
  //
  /////////////////////////////////////// 

  get pos() {
    return this._pos;
  }
  set pos(p) {
    if (!p) return;
    if (!this.wWH) return (this._pos = p);

    var camDimToWorld = this.screenToWorld_vector(this.WH);

    //clamp position
    var screenspaceHalf = scale2(camDimToWorld, 0.5);
    var minPos = sub2(this.min, screenspaceHalf);
    var maxPos = sub2(this.max, screenspaceHalf);
    p = min2(maxPos, max2(minPos, p));

    //position world on screen
    var smin = div2(sub2(this.min, p), camDimToWorld);
    var smax = div2(sub2(this.max, p), camDimToWorld);
    domSet(this.container,'left', smin[0] * 100 + "%");
    domSet(this.container,'right', (1 - smax[0]) * 100 + "%");
    domSet(this.container,'top', smin[1] * 100 + "%");
    domSet(this.container,'bottom', (1 - smax[1]) * 100 + "%");
    domSet(this.container,'transition', this.transition ? "all ease .5s" : "none");

    //
    this._pos = p;
    this.minimap.reposition();
    return this._pos;
  }
  reposition_all() {
    //re-apply all word positions (see WordElement setter for .pos)
    for (var [_, W] of this.Map.entries()) {
      W.pos = W.pos;
    }
  }


  get scale() {
    return this._scale;
  }
  set scale(s) {
    if (!this.wWH) return (this._scale = s);
    this._scale = s;
    this.minimap.rescale();
    this.pos = this.pos; //apply position-changes, too
    this.canvas.resize();
    return this._scale;
  }

  resize() {

    //recalculate screen positions
    this.scale = this.scale;
    this.pos = this.pos;
    if(this.camera_centered) this.centerCamera();
  }


  set boxSelection(v) {
    this._boxSel = v;
    if (v) this.el.classList.add("box_selection");
    else this.el.classList.remove("box_selection");
    return v;
  }
  get boxSelection() {
    return this._boxSel;
  }

  ///////////////////////////////////////
  //
  //     Screen, World, Pixel and Container-Space Interoperation
  //
  /////////////////////////////////////// 

  get mouse_wpos() {
    return add2(scale2(this.mouse, 1 / this.scale), this.pos);
  }
  get worldPerScreen() {
    return 1 / this.scale;
  }
  worldToContainer(wpos) {
    if (!this.wWH) return wpos;
    return div2(sub2(wpos, this.min), this.wWH);
  }
  screenToWorld_vector(v2) {
    return scale2(v2, this.worldPerScreen);
  }
  screenToWorld(v2) {
    return add2(this.pos, this.screenToWorld_vector(v2));
  }
  worldToScreen(v2) {
    return scale2(sub2(v2, this.pos), 1 / this.worldPerScreen);
  }
  worldToPixel(v2) {
    return mul2(this.worldToScreen(v2), this.WH);
  }


  ///////////////////////////////////////
  //
  //     Single Item Management
  //
  /////////////////////////////////////// 

  getItemByName(name) {
    return this.Map.get(name);
  }

  addWord(word) {
    var W = new WordElement(word);
    if (this.Map.has(W.identifier)) {
      W = this.Map.get(W.identifier);
    } else {
      this.Map.set(W.identifier, W);
      W.link(this);
    }
    return W;
  }

  map_value(val){
    return Math.log(1 + Math.max(0,val));
  }

  getAMWS(data, am) { //}, ws) {
    if (!am || !this.am_minmax[am] || !this.collocates) return .5;
    if (!this.collocates[am][data.name]) return Number.NEGATIVE_INFINITY;//this.am_minmax[am].min; //TODO:  hide//-1;
    var val = this.collocates[am][data.name];
    val = Number.parseFloat(val);
    if(val!=val) return Number.NEGATIVE_INFINITY;
    if(val<=0) return Number.NEGATIVE_INFINITY;
    val = this.map_value(val);
    var v = (val - this.am_minmax[am].min) / (this.am_minmax[am].max - this.am_minmax[am].min);
    return v;
  }
  
  getAMWSCompare(data) { //}, ws) {
    let comp = this.component.collocatesCompare;
    if(!comp) return .5;
    let am = comp.am;
    if (!am || !this.am_minmax[am] ) return .5;
    let coll = comp.collocates;
    if (!coll[am][data.name]) return -1;//this.am_minmax[am].min; //TODO:  hide//-1;
    var val = coll[am][data.name];
    val = Number.parseFloat(val);
    if(val!=val) return -1;
    if(val<0) return -1;
    val=this.map_value(val);
    var v = (val - this.am_minmax[am].min) / (this.am_minmax[am].max - this.am_minmax[am].min);
    v = Math.min(1,Math.max(0,v));
    return v;
  }

  getSizeOf(data) {
    return this.getAMWS(data, this.component.AM); //, this.ws);
  }
  getCompareSizeOf(data) {
    return this.getAMWSCompare(data); //, this.compare_ws);
  }


  ///////////////////////////////////////
  //
  //     Selection and Grouping
  //
  ///////////////////////////////////////

  clearSelection() {
    for (var s of this.selected_nodes) s.selected = false;
    //should already be empty at that point ( but to be sure)
    this.selected_nodes.clear();
  }

  groupSelected() {
    if (this.selected_nodes.size) this.groupSet(this.selected_nodes);
    this.clearSelection();
  }

  deleteSelection() {
    if (this.selected_nodes.size) this.deleteSet(this.selected_nodes);
    this.clearSelection();
  }

  groupSet(S) {
    //console.log("groupSet " + Array.from(S).map((s) => s.label ? s.label : ("(" + Array.from(s.items).map(n => n.label).join(",") + ")")));
    if(!S || S.size==0) return;

    var N = new Set();
    var G = new Set();
    //distinguish between selected group or single-item
    for (var n of S)(n.isgroup ? G : N).add(n);
    
    if(G.size==0 && N.size<1) return;

    if (G.size == 1) {
      G = Array.from(G)[0];
      for (var n of N) G.addItem(n);
      if(N.size>0) G.updateDatabase();
      return this.request("layout");
    }

    var any_group;
    for (var g of G) { 
      //Merge all selected groups (and delete all old ones, except one named group)
      //treat every element in selected group as selected
      for (var n of g.items) N.add(n);
      if (g.hasUsefulName && !any_group) any_group = g;
      else{
        g.deleteDatabase();
        g.delete();
      }
    }

    if(any_group){
      G = any_group;
      for (var n of N) G.addItem(n);
      G.updateDatabase();
    }else{
      G = new WordGroup(undefined, this);
      this.groups.add(G);
      for (var n of N) G.addItem(n);
      G.initDatabase();
    }
    this.request("layout");
  }

  deleteSet(S) {
    var G = new Set();
    var N = new Set();
    for (var i of S)(i.isgroup ? G : N).add(i);
    if (N.size == 0) {
      for (var g of G){
        g.deleteDatabase();
        g.delete();
      }
    } else if (G.size == 0) {
      for (var n of N) {
        if (!n.groups.size) n.pin.reset();
        for (var g of n.groups){
          g.removeItem(n);
          g.updateDatabase();
        }
      }
    } else {
      for (var g of G){
        for (var n of N) g.removeItem(n);
        g.updateDatabase();
      }
    }
    this.request("layout");
  }

  /*formGroupByNames(item_names) {
    var G = new WordGroup(undefined, this);
    this.groups.add(G);
    G.addItemsByName(item_names);

    for (var name of item_names) {
      var a = this.getItemByName(name);
      if (!a) return console.error("item '" + name + "' is grouped, but unknown");
      a.groups.add(G);
    }
    return G;
  }*/


  ///////////////////////////////////////
  //
  //     Immediate User Input
  //
  ///////////////////////////////////////

  setupEventListeners() {
    for (var v of ["mousedown", "mousemove", "mouseup"]) fwdEvent(this, this.el, v);

    function handleMouseWheel(t) {
      return e => {
        var wheel = e.wheelDelta / 40 || -e.detail;
        t.onzoom(e, wheel);
        e.preventDefault();
      };
    }
    this.el.addEventListener("mousewheel", handleMouseWheel(this)); //chrome
    this.el.addEventListener("DOMMouseScroll", handleMouseWheel(this), false); //firefox

    document.addEventListener("mouseup", (t => t.mouseupevent = e => t.onmouseupOutside(e))(this));
    document.addEventListener("keydown", (t => t.keydownevent = e => t.onkeydown(e))(this));
  }

  deleteEventListeners() {
    document.removeEventListener("keydown", this.keydownevent);
    document.removeEventListener("mouseup", this.mouseupevent);
  }

  onmousedown(e) {
    this.mouse_downpoint = this.mouse;
    this.mouse_down_wpos = this.mouse_wpos;
    this.window_downpos = this.pos;
    this.dragging = false;
    this.el.classList.remove("dragging");
    //    this.boxSelection = false;
    e.preventDefault();
  }
  onmouseupOutside(e){
    if(this.pressed_node){
      this.pressed_node.dragging = false;
    }
    if(this.dragging) this.request("layout");
    this.pressed_node = false;
    this.dragging = false;
    this.dragging_camera = false;
    this.el.classList.remove("dragging");
    this.window_downpos = null;
  }
  clickEmptySpace(){
    this.component.cancelConcordanceRequest();
    this.clearSelection();
  }
  clickNode(n, e){
    n.selected = e.shiftKey ?  !n.selected : true;
    if(n.getConcordances) n.getConcordances();
  }
  dragEnd(){
    this.component.cancelConcordanceRequest();
  }

  onmouseup(e) {
    if (!this.dragging && !this.dragging_camera && !this.clickedTools) {
      // this.word_menu.shown = false;
      if (!e.shiftKey && !this.boxSelection) {
        if (this.pressed_node){
          if(this.pressed_node.selected) {
          //this.openWordMenuAt(this.pressed_node);
          } else {
            this.clickEmptySpace();
          }
        }else{
          this.clickEmptySpace();
        }
      }
      if (this.pressed_node) this.clickNode(this.pressed_node, e);
    }
    if (this.dragging) {
      this.dragEnd()
      //if dragging node ends:
      this.request("layout");
    }
    if(this.dragging_camera){
      this.dragEnd();
    }
    if (this.boxSelection) {
      this.selectionBox.hide();
    }
    if (this.pressed_node && this.dragging) {
      let n = this.pressed_node;
      if (this.hover_node) {
        n.dropAt(this.hover_node);
      }else{
        n.drop();
      }
      n.dragging = false;
    }
    this.pressed_node = null;
    this.hover_node = null;
    this.dragging = false;
    this.el.classList.remove("dragging");
    this.dragging_camera = false;
    this.window_downpos = null;
    this.boxSelection = false;
    this.clickedTools = false;
  }

  onmousemove(e) {
    this.boxSelection |= e.shiftKey;

    var R = this.el.getBoundingClientRect();
    //offset   = elemRect.top - bodyRect.top;
    this.mouse = [e.pageX - R.left, e.pageY - R.top];
    //    this.mouse = [e.pageX - this.el.offsetLeft, e.pageY - this.el.offsetTop];
    if (this.pressed_node) {
        // dragging node
      var minimal_drag_mouse_movement = 10;
      if(len2(sub2(this.mouse, this.mouse_downpoint))> minimal_drag_mouse_movement || this.dragging){
        this.dragging = true;
        this.el.classList.add("dragging");
        //      this.word_menu.shown = false;
        this.pressed_node._pos = this.pressed_node.pos = sub2(
          this.mouse_wpos,
          this.pressed_offset
        );
        this.pressed_node.user_defined_position = this.pressed_node.pos;
        this.pressed_node.dragging = true;
      }
    } else if (this.window_downpos) {
      //this.word_menu.shown = false;
      if (this.boxSelection) {
        this.selectionBox.show(this.mouse_down_wpos, this.mouse_wpos);
      } else {
        this.dragging_camera = true;
        this.camera_centered = false;
        // dragging camera
        this.pos = sub2(
          this.window_downpos,
          scale2(sub2(this.mouse, this.mouse_downpoint), 1 / this.scale)
        );
      }
      //this.redraw();
    }
    //e.preventDefault();
  }

  onzoom(e, wheel) {
    this.log(wheel);
    this.camera_centered=false;
    //    this.word_menu.shown = false;
    var wpos = this.mouse_wpos;
    var sf = 1;
    if (wheel > 0) {
      sf = 1 / 1.05;
    } else {
      sf = 1.05;
    }
    this.scale *= sf;
    this.pos = add2(wpos, scale2(sub2(this.pos, wpos), 1 / sf));
    this.reposition_all();
    this.timeout("layout");
  }

  onkeydown(e) {
    //not every ctrlKey- combination reaches here in chrome ...:(
    //if (e.ctrlKey && e.key == "b") {
    //  this.changeAM();
    //  e.preventDefault();
    //}
    if (e.ctrlKey && e.key == "g") {
      if (e.shiftKey) {
        //console.log("del");
        this.deleteSelection();
      } else {
        this.groupSelected();
      }
      e.preventDefault();
    }
    if (e.keyCode == 46) { //[del]
      this.deleteSelection();
      e.preventDefault();
    }
  }

  ///////////////////////////////////////
  //
  //   Button triggered User Input /  e.g. Camera Navigation
  //
  ///////////////////////////////////////

  centerCamera() {
    this.camera_centered = true;
    this.transition = true;
    //scale == screenPerWorld
    this.scale = Math.min(this.WH[0] / this.wWH[0], this.WH[1] / this.wWH[1]);

    var wBorder = [0, 0];
    if (this.screenBorder) {
      wBorder = this.screenToWorld_vector(this.screenBorder);
    }

    var worldDelta = add2(this.wWH, wBorder);
    this.scale = Math.min(
      this.WH[0] / worldDelta[0],
      this.WH[1] / worldDelta[1]
    );

    var rest = sub2(scale2(this.WH, 1 / this.scale), worldDelta);
    this.pos = sub2(sub2(this.min, scale2(wBorder, 0.5)), scale2(rest, 0.5));
    this.transition = false;
    this.timeout("layout");
  }

  centerAtWord(word) {
    if (typeof word === "string") {
      word = this.Map.get(word);
    }
    if(!word) return;
    this.transition = true;
    this.pos = sub2(word.pos, this.screenToWorld_vector(scale2(this.WH, .5)));
    this.transition = false;
  }
  
  centerAtGroup( g ) {
    this.transition = true;
    this.pos = sub2(g.pos, this.screenToWorld_vector(scale2(this.WH, .5)));
    this.transition = false;
  }


  startBoxSelection(){
    this.boxSelection = true;
  }

  toggleMinimap(){
    this.minimap.shown = !this.minimap.shown;
    this.component.setShowMinimap(this.minimap.shown);
  }

  ///////////////////////////////////////
  //
  //    Content setup
  //
  ///////////////////////////////////////




  changeAM(ws, am, cws, cam) {
    //this.compare_am = cam ? cam : this.am;
    //var AM = Object.keys(this.am_minmax);
    //this.am = am ? am : oneOf(AM);
    //console.log("CHANGE TO " + /*this.ws +*/ " " + this.am);
    for (var [_, a] of this.Map.entries()) {
      //a.shown = !a.hidden;
      a.normalized_size_invalidate();
      a.size = 1 + Math.max(0,Math.min(1,a.normalized_size)) * 1;
      a.trend.evaluate();
    }

    this.request("layout");
  }


  setupCollocates(collocates){
    //collocations may freely change ....
    // - always accept them
    // TODO:: a special case of collocates are the SOCs
    // - hold them and the compare-collocations always present in memory
    // - to be able to switch between them fast.

    var total_count = 0;
    var missing_coordinates = new Set();
    this.collocates = collocates;
    this.am_minmax = {};
    for (var am of Object.keys(collocates)) {
      if (!collocates[am]) continue;
      this.am_minmax[am] = {
        min: Number.POSITIVE_INFINITY,
        max: Number.NEGATIVE_INFINITY
      };

      var count = 0;
      for (var word of Object.keys(collocates[am])) {
        if(this.coordinates && !this.coordinates[word]){
          count++;
          missing_coordinates.add(word);
        }
        if (!collocates[am][word]) continue;
        var val = Number.parseFloat(collocates[am][word]);
        //console.log(collocates[am][word]);
        if(val!=val) continue;
        val = this.map_value(val);
        this.am_minmax[am].min = Math.min(this.am_minmax[am].min, val);
        this.am_minmax[am].max = Math.max(this.am_minmax[am].max, val);
      }
      //if(count) console.warn(count+" collocated items in '"+am+"' are not present in coordinates-list");
    }
    this.changeAM();
    if(missing_coordinates.size != 0){
      //console.warn("The following collocated items are not present in coordinates-list: " + new Array(...missing_coordinates) );
      //TODO:: reload Coordinates
      //console.warn("Reloading Coordinates");
      this.component.loadCoordinates();
    }
  }

  setupCoordinates(coordinates){
    //TODO:: only accept new coordinates (that are not already present here)
    // - we do not assume others are changeing our data while we're at it.
    
    
    //check consistency,... only update when new data arrives.
    var data_consistent = true;
    for(var word of Object.keys(coordinates)){
      var el = this.Map.get(word);
      if(!el){ data_consistent=false; break;}
      if(! el.matches( coordinates[ word ] )){ data_consistent=false; break;};
    }
    if(data_consistent) return; //console.log("drop consistent wc setup");

    for(var [_,a] of this.Map.entries()) a.delete();
    this.Map = new Map();
    this.coordinates = coordinates;

    for (var word of Object.keys(coordinates)) {
      coordinates[word].name = word;
      this.addWord( coordinates[word] );
    }

    this.layoutTsnePositions();
    if(this.discoursemes){
      this.setupDiscoursemes(this.discoursemes);
    }
  }

  setupDiscoursemes(discoursemes){

    //TODO:: only accept new discoursemes (that are not already present here)
    // - we do not assume others are changeing our data while we're at it.

    for(var g of this.groups) g.delete(); //!! Do not delete groups from server, only locally
    this.groups.clear();

    this.discoursemes = discoursemes;
    for (var disc of discoursemes) {
      var avgX = 0, avgY = 0, avgC = 0;
      var unknownWords = [];
      var G = new WordGroup(undefined,this);
      for(var name of disc.items){
        var n = this.getItemByName(name);
        if(!n){
          unknownWords.push(name);
          continue;
        }
        G.addItem(n);
        avgX += n.data.x;
        avgY += n.data.y;
        avgC ++;
      }
      if(avgC){
        avgX /= avgC; avgY /= avgC;
      }
      for(var name of unknownWords){
        //TODO:: what coordinates should these words have??
        // place them at the average of the other words in the discourseme
        n = this.addWord({name:name, x:avgX ,y:avgY, x_user:null, y_user:null});
        G.addItem(n);
      }

      // Only give name, if naming is meaningful
      G.updateContentString();
      if(G.contentString!=disc.name){
        G.name = disc.name;
      }
      G.id = disc.id;
      G.color = random_color(G.id);
      this.groups.add(G);
    }
    
    this.timeout('layout');
  }



  ///////////////////////////////////////
  //
  //   Helper (To not waste performance)
  //
  ///////////////////////////////////////


  // request the execution of the function in the next frame,
  // !BUT! only once (even if requested multiple times)
  request(fncName) {
    if (!this.requested) this.requested = new Set();
    if (this.requested.has(fncName)) return;
    this.requested.add(fncName);
    if (fncName == "layout") {
      this.canvas.clearDebug();
    }
    requestAnimationFrame(
      ((t, fncName) => () => {
        t.requested.delete(fncName);
        t[fncName]();
      })(this, fncName)
    );
  }

  // request the execution of the function after duration ms,
  // !BUT! when requested again in that period the older request is canceled and another waiting period starts
  timeout(fncName, duration = 400) {
    if (!this.requestedTimeout) this.requestedTimeout = {};
    if (!this.requestedTimeout[fncName]) this.requestedTimeout[fncName] = 0;
    var rt = ++this.requestedTimeout[fncName];
    setTimeout(
      ((t, rt, fncName) => () => {
        if (rt != this.requestedTimeout[fncName]) return; //do not compute the layout, if another issue has been posted
        this.requestedTimeout[fncName] = 0;
        t[fncName]();
      })(this, rt, fncName),
      duration
    );
  }

  ///////////////////////////////////////
  //
  //    Layout
  //
  ///////////////////////////////////////

  layout(x) {
    this.debugClear();
      
    for (var [_, a] of this.Map.entries()) {
      a.normalized_size_invalidate();
    }
    
    //layout.layoutWordcloudFormGroupsHideOverlap(this);
    //
    var multigroups = false;
    if(multigroups){
      layout.layoutWordcloudFormGroups2ResolveOverlap(this);
    }else{
      layout.layoutWordcloudFormGroupsResolveOverlap(this);
      this.drawContainmentEdges();
      for (var g of this.groups) g.draw();
    }
    this.pos = this.pos;
    this.scale = this.scale;
  }

  layoutTsnePositions() {
    var min = inf2();
    for (var [_, a] of this.Map.entries()) min = min2(min, a.computed_position);
    var max = negInf2();
    for (var [_, a] of this.Map.entries()) max = max2(max, a.computed_position);
    this.wWH = sub2(max, min);
    this.min = min;
    this.max = max;
    this.pos = min;
    this.centerCamera();
    this.screenBorder = [0, 0];

    for (var [_, a] of this.Map.entries()) {
      a._pos = a.computed_position;
      a.color = [0, 0, 0, 0.8];
      this.screenBorder = max2(a.WH, this.screenBorder);
    }

    this.timeout("centerCamera");
  }


  ///////////////////////////////////////
  //
  //    Drawing  and debugging
  //
  ///////////////////////////////////////

  debugClear() {
    if (!this.debug){
      //this.container.removeChild(this.debug);
      this.debug = document.createElement("div");
      this.container.appendChild(this.debug);
    }
    if (!this.canvas) return;
    this.canvas.clearDebug();
  }

  debugPoint(p) {
    var P = document.createElement("div");
    this.debug.appendChild(P);
    P.style.position = "absolute";
    P.style.width = "0.3rem";
    P.style.height = "0.3rem";
    P.style.backgroundColor = "#faaa";
    P.style.left =
      ((p[0] - this.min[0]) / (this.max[0] - this.min[0])) * 100 + "%";
    P.style.top =
      ((p[1] - this.min[1]) / (this.max[1] - this.min[1])) * 100 + "%";
  }


  debugRepositionLines() {
    var wordset = this;
    for (var [_, a] of wordset.Map.entries()) {
      a._pos = min2(max, a._pos);
      a._pos = max2(min, a._pos);
      if (wordset.options.reposition_shown_by_line) {
        wordset.canvas.debugLine(a._pos, a.layout_position, 2, [0, 0, 0, 0.1]);
      }
    }
  }

  debugRepositionColor() {
    var wordset = this;
    for (var [_, a] of wordset.Map.entries()) {
      if (wordset.options.reposition_shown_by_color) {
        a.color = [
          len2(a.offset) / (0.5 * wordset.wWH[1]),
          0, //a.my_ctr / wordset.Map.size,
          0, //a.user_defined_position ? 0.5 : 0,
          0.8
        ]; //[Math.random(), Math.random(), Math.random()];
      } else {
        a.color = [0, 0, 0, 0.8];
      }
    }
    //wordset.centerCamera();
  }


  drawContainmentEdges() {
    for (var [_, a] of this.Map.entries()) {
      if (!a.shown) continue;

      //TODO:: for every word, that is in multiple groups:
      if (this.options.show_lexical_items_of_group && a.groups.size > 1) {
        // draw a containment edge from the closest Group-Boundary-Point (lerp(Pi,Pi+1,0.5))
        // Pointing in normal direction
        // towards the center of the word, stopping at the word-boundary

        for (var G of a.groups) {
          //var closest = [0, 0];
          //var normal = [1, 0];
          var dist = Number.POSITIVE_INFINITY;
          var P = G.border_path;
          var ctr = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
          ];
          var d = (a.max[1] - a.min[1]) / 4;
          for (var k = 0; k < P.length; ++k) {
            var A = P[k];
            var B = P[(k + 1) % P.length];
            var point = lerp2(A, B, 0.5);
            var norm = sub2(B, A);
            norm = [norm[1], -norm[0]]; //orthogonal
            norm = normalize2(norm);
            var len = len2(sub2(a._pos, point));

            function test(target, tnorm) {
              var dist2 = len2(
                sub2(
                  add2(point, scale2(norm, len / 5)),
                  add2(target, scale2(tnorm, len / 5 - d))
                )
              );
              if (dist2 < dist) {
                dist = dist2;
                ctr = [
                  point,
                  add2(point, scale2(norm, len / 5)),
                  add2(target, scale2(tnorm, len / 5 - d)),
                  add2(target, scale2(tnorm, -d))
                ];
              }
            }
            test([a._pos[0], a.min[1]], [0, -1]);
            test([a._pos[0], a.max[1]], [0, 1]);
            test([a.min[0], a._pos[1]], [-1, 0]);
            test([a.max[0], a._pos[1]], [1, 0]);
          }
          this.canvas.debugSpline(ctr, 2, G.color);
        }
      }
    }
  }
}


export {
  WordcloudWindow
};
