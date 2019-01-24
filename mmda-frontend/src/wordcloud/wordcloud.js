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
  intersectObjects,
  convexHull,
  GridAccelerationStructure
} from "./util_bounds_and_intersection.js";
import {
  hex_color_from_array,
  oneOf,
  random_color,
  //  hsv_to_rgb,
  fwdEvent
} from "./util_misc.js";

import { Minimap } from "./element_minimap.js";
import { WordElement } from "./word_element.js";
import { WordGroup } from "./word_group.js";
import { WordMenu } from "./word_menu.js";

import { callWorker }from "./layout_worker.js";
import * as layout from "./layout_generation.js";

///////////////////////////////////////
//
//    Box Selection
//
///////////////////////////////////////

class SelectionBox {
  constructor(window) {
    this.window = window;
    this.el = document.createElement("div");
    this.el.classList.add("selection_box");
    this.window.container.appendChild(this.el);
    this.selected = new Set();
    this.bounds = { min: [0, 0], max: [0, 0] };
    this.hide();
  }
  hide() {
    this.el.style.visibility = "hidden";
    //this.execute_selection();
    this.selected.clear();
  }
  execute_selection() {
    for (var s of this.selected) {
      s.onmouseout();
      s.selected = true;
    }
  }
  show(min, max) {
    this.el.style.visibility = "visible";
    //Sort Min max

    var wmin = min2(min, max);
    var wmax = max2(min, max);

    min = this.window.worldToContainer(wmin);
    max = this.window.worldToContainer(wmax);
    min = scale2(min, 100);
    max = scale2(sub2([1, 1], max), 100);

    this.el.style.left = min[0] + "%";
    this.el.style.top = min[1] + "%";
    this.el.style.right = max[0] + "%";
    this.el.style.bottom = max[1] + "%";

    //TODO: Select every contained this.window.Map-element

    this.newSelection = new Set();
    this.window.total_acceleration_grid.forEachIn(
      { min: wmin, max: wmax },
      (t => els => {
        for (var el of els) {
          if (intersectObjects(el, { bounds: { min: wmin, max: wmax } })) {
            if(el.shown) t.newSelection.add(el);
          }
        }
      })(this)
    );

    for (var el of this.newSelection) {
      if (!this.selected.has(el)) {
        el.selected = true;
        //el.onmouseover();
      } else {
        this.selected.delete(el);
      }
    }

    for (var el of this.selected) {
      el.selected = false;
    }

    this.selected = this.newSelection;

    this.bounds.max = wmax;
    this.bounds.min = wmin;
  }
}

class WordCanvas {
  constructor(window) {
    this.window = window;
    this.window.container.setAttribute("id", "window_container");
    this.svg_worldspace = SVG("window_container")  ;
    this.clearDebug();
  }
  resize() {
    this.svg_worldspace.attr("viewBox",this.window.min[0]+" "+this.window.min[1]+" "+(this.window.max[0]-this.window.min[0])+" "+(this.window.max[1]-this.window.min[1]))
  }
  remove(el) {
    var i = this.elements.findIndex(a => a == el);
    if (i != -1) {
      this.elements.splice(i, 1);
      el.remove();
    }
  }
  clearDebug() {
    if (this.elements) for (var p of this.elements) p.remove();
    this.elements = [];
  }
  debugLine(a, b, size, color) {
    this.elements.push(
      this.svg_worldspace.line(a[0], a[1], b[0], b[1]).stroke({
        width: size * this.window.worldPerScreen,
        color: hex_color_from_array(color)
      })
    );
  }
  pathElement(X, ...P) {
    var res = "" + X;
    for (var p of P) {
      res += p[0] + "," + p[1] + " ";
    }
    return res;
  }
  debugConvex(P, size, color, label) {
    var str = "";
    P = P.reverse();
    var s = lerp2(P[P.length - 1], P[0], 0.5);
    var schnoerkel = this.window.options.draw_group_schnoerkel;
    if (schnoerkel) {
      var a = lerp2(P[P.length - 1], P[0], 0.0);
      str += this.pathElement("M", a);
      str += this.pathElement("Q", a, s);
    } else {
      str += this.pathElement("M", s);
    }
    var longest = 0;
    var length = 0;

    for (var i in P) {
      var c = P[i];
      var p = P[(Number.parseInt(i) + 1) % P.length];
      var t = lerp2(c, p, 0.5);
      var d = sub2(p, c);
      var l = len2(d);
      if (length <= d[0] && d[1] >= 0 && d[0] > 0) {
        longest = i;
        length = d[0];
      }
      str += this.pathElement("Q", c, t);
    }

    var middlePercentage = ((Number.parseInt(longest) + 0.5) / P.length) * 100;
    //console.log(middlePercentage);
    middlePercentage = 5;

    var wid = size * this.window.worldPerScreen;

    var path = this.svg_worldspace
      .path(str)
      .stroke({
        width: wid,
        color: hex_color_from_array(color)
      })
      .attr({ fill: hex_color_from_array([...color, 0.1]) });

    var text = this.svg_worldspace
      .text(function(add) {
        add.tspan(label);
      })
      .font({
        family: "Helvetica",
        size: 6 * wid,
        weight: "bold"
        //anchor: "middle"
      })
      .attr({
        fill: hex_color_from_array([...color, 0.5]),
        "dominant-baseline": "hanging"
      })
      .path(str);
    text.textPath().attr({ startOffset: middlePercentage + "%" });

    var res = path;
    this.elements.push(res);
    this.elements.push(text);
    return { path, text };
  }
  debugSpline(P, size, color) {
    var str = this.pathElement("M", P[0]);
    P.splice(0, 1);
    if (P.length == 1) {
      str += this.pathElement("L", ...P);
    } else if (P.length == 2) {
      str += this.pathElement("Q", ...P);
    } else if (P.length == 3) {
      str += this.pathElement("C", ...P);
    }
    this.elements.push(
      this.svg_worldspace
        .path(str)
        .stroke({
          width: size * this.window.worldPerScreen,
          color: hex_color_from_array(color)
        })
        .attr({ fill: "none" })
    );
  }
}

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
    if (this.content) this.el.removeChild(this.content);
    this.content = undefined;
  }
  set(msg, title) {
    this.el.title = title;
    if (this.content) this.el.removeChild(this.content);
    this.content = document.createTextNode("⚠ " + msg);
    this.el.appendChild(this.content);
  }
}

///////////////////////////////////////
//
//    Wordcloud Window
//
///////////////////////////////////////

class WordcloudWindow {
  constructor(content_div) {
    this.el = content_div;

    this.Map = new Map();
    this.selected_nodes = new Set();

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
    this.option_explained = {
      remap_tsne_positions:
        "Reduces the area according to the standard deviation of the contained items.",
      remap_standard_deviation_log:
        "Every item is repositioned according to a logarithmic-scale.",
      remap_standard_deviation_clamp:
        "Overflowing items are clamped to the border of the area.",
      resolve_overlap:
        "Prevents item overlaps by moving the smaller item away.",
      relocation_by_group:
        "The positions of words inside the group are scaled by this factor (at the group center of mass).",
      multigroup_attraction:
        "Words inside multiple groups are scaled towards them by this factor"
    };

    this.resize();

    this.container = document.createElement("div");
    this.container.classList.add("sw_container");
    this.el.appendChild(this.container);

    this.minimap = new Minimap(this);

    this.error = new ErrorMessage(this);

    this.scale = 1;
    this.pos = [0, 0];

    for (var v of ["mousedown", "mousemove"]) fwdEvent(this, this.el, v);

    document.addEventListener("mouseup", (t => e => t.onmouseup(e))(this));

    function handleMouseWheel(t) {
      return e => {
        var wheel = e.wheelDelta / 40 || -e.detail;
        t.onzoom(e, wheel);
        e.preventDefault();
      };
    }
    this.el.addEventListener("mousewheel", handleMouseWheel(this)); //chrome
    this.el.addEventListener("DOMMouseScroll", handleMouseWheel(this), false); //firefox

    document.addEventListener(
      "keydown",
      (t => e => {
        t.onkeydown(e);
      })(this)
    );

    this.setupMenu();
    this.closeMenu();

    this.word_menu = new WordMenu(this);
    this.selectionBox = new SelectionBox(this);
    this.canvas = new WordCanvas(this);
  }

  openWordMenuAt(item) {
    this.log("add" + item);
    if (item) {
      //this.word_menu.pos = item.isgroup ? this.mouse_wpos : item._pos;
      this.word_menu.pos = this.mouse_wpos;
      this.word_menu.item = item;
    }
    this.word_menu.shown = item != null;
  }

  log(s) {
    if (this.options.verbose) {
      console.log(s);
    }
  }

  setupMenu() {
    if (this.menu) document.body.removeChild(this.menu);
    this.menu = document.createElement("div");
    this.menu.classList.add("menu");
    this.el.appendChild(this.menu);
    var header = document.createElement("h3");
    header.appendChild(document.createTextNode("Options"));

    var exit_button = document.createElement("div");
    exit_button.appendChild(document.createTextNode("[X]"));
    exit_button.addEventListener("click", (t => e => t.closeMenu(e))(this));
    exit_button.style.cursor = "pointer";
    exit_button.style.position = "absolute";
    exit_button.style.left = 0;
    exit_button.style.top = 0;
    exit_button.style.margin = ".5rem";

    header.appendChild(exit_button);
    this.menu.appendChild(header);

    for (var o of Object.keys(this.options)) {
      var el = document.createElement("input");
      var txt = document.createTextNode(o.replace(/_/g, " "));
      var typ = typeof this.options[o];
      el.type =
        typ === "string"
          ? "text"
          : typ === "number"
          ? "number"
          : typ === "boolean"
          ? "checkbox"
          : typ;
      el.value = this.options[o];
      el.checked = this.options[o];
      el.title = this.option_explained[o] ? this.option_explained[o] : "";
      //txt.title = this.option_explained[o] ? this.option_explained[o] : '';
      el.addEventListener(
        "input",
        ((el, t, o, typ) => e => {
          t.options[o] =
            typ === "number"
              ? Number.parseFloat(el.value)
              : typ === "boolean"
              ? el.checked
              : el.value;
          t.optionsChanged();
        })(el, this, o, typ)
      );
      this.menu.appendChild(el);
      this.menu.appendChild(txt);
      this.menu.appendChild(document.createElement("br"));
    }
  }
  optionsChanged() {
    this.log(this.options);
    //this.tsneRepositionVariance();
    this.request("layout");
  }
  openMenu() {
    this.menu.style.visibility = "visible";
  }
  closeMenu(e) {
    this.menu.style.visibility = "hidden";
  }

  get mouse_wpos() {
    return add2(scale2(this.mouse, 1 / this.scale), this.pos); //something with scale
  }

  getAMWS(data, am, ws) {
    if (!this.am_by_ws[ws]) return -1;
    if (!this.am_by_ws[ws][am]) return -1;
    var m = this.am_by_ws[ws][am];
    if (!data.am_by_ws[ws] || !data.am_by_ws[ws][am]) return -1; //--> not existent in current context(am and ws)
    return (data.am_by_ws[ws][am] - m.min) / (m.max - m.min);
  }

  getSizeOf(data) {
    return this.getAMWS(data, this.am, this.ws);
  }
  getCompareSizeOf(data) {
    return this.getAMWS(data, this.compare_am, this.compare_ws);
  }

  worldToContainer(wpos) {
    if (!this.wWH) return wpos;
    return div2(sub2(wpos, this.min), this.wWH);
  }

  get worldPerScreen() {
    return 1 / this.scale;
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
    this.container.style.left = smin[0] * 100 + "%";
    this.container.style.right = (1 - smax[0]) * 100 + "%";
    this.container.style.top = smin[1] * 100 + "%";
    this.container.style.bottom = (1 - smax[1]) * 100 + "%";
    this.container.style.transition= this.transition?"all ease .5s":"none";

    //
    this._pos = p;
    this.minimap.reposition();
    return this._pos;
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

  onmousedown(e) {
    this.mouse_downpoint = this.mouse;
    this.mouse_down_wpos = this.mouse_wpos;
    this.window_downpos = this.pos;
    this.dragging = false;
    this.el.classList.remove("dragging");
    this.boxSelection = false;
    e.preventDefault();
  }

  clearSelection() {
    for (var s of this.selected_nodes) s.selected = false;
    //should already be empty at that point ( but to be sure)
    this.selected_nodes.clear();
  }

  onmouseup(e) {
    if (!this.dragging && !this.dragging_camera) {
      this.word_menu.shown = false;
      if (!e.shiftKey) {
        if (this.pressed_node && this.pressed_node.selected) {
          this.openWordMenuAt(this.pressed_node);
        } else {
          this.clearSelection();
        }
      }
      if (this.pressed_node) {
        this.pressed_node.selected = e.shiftKey
          ? !this.pressed_node.selected
          : true;
      }
    }
    if (this.dragging) {
      //if dragging node ends:
      this.request("layout");
    }
    if (this.boxSelection) {
      this.selectionBox.hide();
    }
    if (this.pressed_node && this.dragging) {
      if (this.hover_node) {
        this.pressed_node.dropAt(this.hover_node);
        /*        this.selected_nodes.add(this.hover_node);
        this.selected_nodes.add(this.pressed_node);
        this.groupSelected();
        this.clearSelection();
        //}
        this.pressed_node.pin.reset();*/
      }

      this.pressed_node.dragging = false;
    }
    this.pressed_node = null;
    this.hover_node = null;
    this.dragging = false;
    this.el.classList.remove("dragging");
    this.dragging_camera = false;
    this.window_downpos = null;
  }
  onmousemove(e) {
    this.boxSelection |= e.shiftKey;
   
    var R = this.el.getBoundingClientRect();
    //offset   = elemRect.top - bodyRect.top;
    this.mouse = [e.pageX - R.left, e.pageY - R.top];
//    this.mouse = [e.pageX - this.el.offsetLeft, e.pageY - this.el.offsetTop];
    if (this.pressed_node) {
      // dragging node
      this.dragging = true;
      this.el.classList.add("dragging");
      this.word_menu.shown = false;
      this.pressed_node._pos = this.pressed_node.pos = sub2(
        this.mouse_wpos,
        this.pressed_offset
      );
      this.pressed_node.user_defined_position = this.pressed_node.pos;
      this.pressed_node.dragging = true;
    } else if (this.window_downpos) {
      this.word_menu.shown = false;
      if (this.boxSelection) {
        this.selectionBox.show(this.mouse_down_wpos, this.mouse_wpos);
      } else {
        this.dragging_camera = true;
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
    this.word_menu.shown = false;
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

  groupSelected() {
    this.groupSet(this.selected_nodes);
  }

  groupSet(S, title) {
    var N = new Set();
    var G = new Set();
    for (var n of S) {
      if (n.isgroup) {
        G.add(n);
      } else N.add(n);
    }

    var item_names = [];
    if (G.size == 1) {
      if (!title) title = G.values().next().value.label;
      N = Array.from(N);
    } else {
      for (var g of G) {
        //treat every element in selected group as selected
        for (var n of g.items) N.add(n);
      }
      N = Array.from(N);
      if (!title)
        title = N.reduce(
          (sum, a) => (sum.normalized_size > a.normalized_size ? sum : a),
          { normalized_size: Number.NEGATIVE_INFINITY }
        ).label;
    }
    var item_names = N.map(a => a.label);
    this.formGroup(title, item_names);
    this.request("layout");
  }
  deleteSelection() {
    var G = new Set();
    var N = new Set();
    for (var i of this.selected_nodes) {
      if (i.isgroup) G.add(i);
      else N.add(i);
    }
    if (N.size == 0) {
      for (var g of G) {
        g.delete();
      }
    } else if (G.size == 0) {
      for (var n of N) {
        G = Array.from(n.groups, name => this.groups[name]);
        if(G.length==0){
          n.pin.reset();
        }
        for (var g of G) {
          g.removeItem(n);
        }
      }
    } else {
      for (var n of N) {
        for (var g of G) {
          g.removeItem(n); // this.removeItemFromGroups(n, G);
        }
      }
    }
    this.request("layout");
  }

  onkeydown(e) {
    //not every ctrlKey- combination reaches here in chrome ...:(
    if (e.ctrlKey && e.key == "i") {
      this.openFile();
      e.preventDefault();
    }
    if (e.ctrlKey && e.key == "y") {
      this.openMenu();
      e.preventDefault();
    }
    if (e.ctrlKey && e.key == "b") {
      this.changeAM();
      e.preventDefault();
    }
    if (e.ctrlKey && e.key == "g") {
      this.groupSelected();
      e.preventDefault();
    }
    if (e.keyCode == 46) {
      this.deleteSelection();
      e.preventDefault();
    }
  }

  centerCamera() {
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

  centerAtWord(word){
    this.transition = true;
    this.pos = sub2( word.pos, this.screenToWorld_vector(scale2(this.WH,.5)) );
    this.transition = false;
  }

  get WH() {
    return [this.el.offsetWidth, this.el.offsetHeight];
  }

  reposition_all() {
    for (var [_, W] of this.Map.entries()) {
      W.pos = W.pos;
    }
  }

  resize() {
    //centering window with fixed aspect ratio
    /*var scale = Math.min(innerHeight / 9, innerWidth / 16);
    this.el.style.width = 16 * scale + "px";
    this.el.style.height = 9 * scale + "px";
    this.el.style.left = (innerWidth - 16 * scale) / 2 + "px";
    this.el.style.top = (innerHeight - 9 * scale) / 2 + "px";
    */
    //recalculate screen positions
    this.scale = this.scale;
    this.pos = this.pos;
  }

  wordIdentifier(word) {
    return word.label;
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

  addWordGroup() {
    var W = new WordGroup("Hello");
    this.el.appendChild(W.el);
  }

  openFile() {
    var loader = document.createElement("input");
    loader.setAttribute("type", "file");
    document.body.appendChild(loader);
    loader.addEventListener(
      "change",
      (t => e => {
        readSingleFile(t, e);
      })(this),
      false
    );
    loader.click();
    document.body.removeChild(loader);

    function readSingleFile(t, e) {
      var file = e.target.files[0];
      if (!file) return;
      t.filename = file.name;
      var reader = new FileReader();
      reader.onload = e => {
        parseFileContent(t, e);
      };
      reader.readAsText(file);
    }

    function parseFileContent(t, e) {
      var contents = e.target.result;
      //TODO: fix nan output on server side
      //var wordcloud_object = JSON.parse(contents);
      var wordcloud_object = JSON.parse(
        contents.replace(/\bNaN\b/g, '"##NaN__Dummy##"'),
        (key, value) => {
          return value === "##NaN__Dummy##" ? NaN : value;
        }
      );
      t.setupContent(wordcloud_object);
    }
  }

  setupDummyContent(wordcloud_object) {
    var els = [
      {
        lemma: "hello"
      },
      {
        lemma: "world"
      },
      {
        lemma: "how"
      },
      {
        lemma: "is"
      },
      {
        lemma: "it"
      },
      {
        lemma: "!"
      },
      {
        lemma: "?"
      }
    ];
    for (var i = 0; i < 30; ++i) {
      for (var e of els) {
        var W = this.addWord({
          name: i + e.lemma,
          tsne_pos: [Math.random() * 16 - 8, Math.random() * 9 - 4.5],
          am_by_ws: {
            "5": {
              Dice: Math.random()
            }
          }
        });
        //W.size = 0.7 + W.data.normalized_size_category * 1.7;
        //W.pos = [0, 0];
      }
    }
    this.ws = "5";
    this.am = "Dice";
    this.am_by_ws = {
      "5": {
        Dice: {
          min: 0,
          max: 1
        }
      }
    };
    //this.addWordGroup();
    this.layoutTsnePositions();
    this.request("layout");
  }

  setupDummyContent2(wordcloud_object) {
    this.log("#################################### received Content");
    this.log(wordcloud_object);

    var discourses = {};
    var collocates = {};
    var am_by_ws = {};
    var discourse_ctr = 0;
    var current_discourse_bit = 0;

    discourses[wordcloud_object.topic_query] = {
      id: wordcloud_object.id,
      items: [wordcloud_object.topic_query],
      discourse_bit: (current_discourse_bit = discourse_ctr++)
    };

    for (var WsArr of wordcloud_object.collocates) {
      parseWsArr(WsArr);
    }
    parseCoords(wordcloud_object.coordinates);

    function parseWsArr(WsArr) {
      for (var ws in WsArr) {
        var Coll = WsArr[ws];
        for (var c in Coll) {
          var C = Coll[c];
          if (!collocates[c]) {
            collocates[c] = {};
            collocates[c].name = c;
            //collocates[c]["011"]= C["011"];
            //collocates[c]["f2"]= C["f2"];
            collocates[c].am_by_ws = {};
            collocates[c].discourse_mask = 0;
          }
          collocates[c].discourse_mask |= 1 << current_discourse_bit;
          collocates[c].am_by_ws[ws] = {};
          for (var key in C) {
            if (key.substr(0, 3) == "am.") {
              var key2 = key.replace("am.", "");
              collocates[c].am_by_ws[ws][key2] = C[key];
              if (!am_by_ws[ws]) {
                am_by_ws[ws] = {};
              }
              if (!am_by_ws[ws][key2]) {
                am_by_ws[ws][key2] = {
                  min: Number.POSITIVE_INFINITY,
                  max: Number.NEGATIVE_INFINITY
                };
              }
              am_by_ws[ws][key2].min = Math.min(C[key], am_by_ws[ws][key2].min);
              am_by_ws[ws][key2].max = Math.max(C[key], am_by_ws[ws][key2].max);
            } else {
              if (collocates[c][key] && collocates[c][key] != C[key]) {
                if (key != "O11")
                  console.error(
                    "'" + c + "'  property '" + key + "' is different "
                  );
              }
              collocates[c][key] = C[key];
            }
          }
        }
      }
    }

    function parseCoords(coords) {
      for (var c in coords) {
        if (!collocates[c]) {
          console.error("'" + c + "' has coordinates but is not defined");
          continue;
        }
        var C = coords[c];
        collocates[c].tsne_pos = [C.tsne_x, C.tsne_y];
        collocates[c].user_pos = [C.user_x, C.user_y];
      }
    }

    for (var d of wordcloud_object.discourse_collocates) {
      var D = (discourses[d.discourse_name] = {
        id: d["id:"], //TODO:: bug
        items: d.items,
        discourse_bit: (current_discourse_bit = discourse_ctr++)
      });
      parseWsArr(d.collocates);
      parseCoords(d.coordinates);
    }

    this.log("Parsed Content to:");
    this.log("discourse object:");
    this.log(discourses);
    this.log("and collocate object:");
    this.log(collocates);
    this.log(am_by_ws);

    this.discourses = discourses;
    this.collocates = collocates;
    this.am_by_ws = am_by_ws;

    this.ws = Object.keys(this.am_by_ws)[0];
    this.am = Object.keys(this.am_by_ws[this.ws])[0];

    this.log(this.am, this.ws);

    for (var c in this.collocates) {
      this.addWord(this.collocates[c]);
    }

    this.layoutTsnePositions();
    this.request("layout");
    this.changeAM(4, "MI", 5, "simple.ll");
    this.formGroup("AusZukunft", [
      "Ausstieg",
      "Zukunft",
      "Energieträger",
      "schädlich",
      "Gerücht",
      "Verzicht",
      "ankündigen"
    ]);
    this.formGroup("MyGroupName", [
      "Anteil",
      "Vorbild",
      "Teil",
      "leidenschaftlich",
      "Gerücht",
      "Verzicht"
    ]);
    this.formGroup("Ankü", ["ankündigen"]);
    this.formGroup("Bay", ["Bayer"]);
    /*
    var A = [];
    for (var c in this.collocates) {
      A.push(c);
    }
    function any() {
      return A[Math.min(A.length - 1, Math.floor(A.length * Math.random()))];
    }

    for (var i = 0; i < 10; ++i) {
      var arr = [any()];
      while (Math.random() > 0.4) {
        arr.push(any());
      }
      this.formGroup(arr[0], arr);
    }*/

    console.log(this.discourses);
    console.log(this.collocates);
  }

  formGroup(name, item_names) {
    if (!this.groups) this.groups = {};
    if (!this.groups[name]) this.groups[name] = new WordGroup(name, this);
    this.groups[name].addItems(item_names);

    // { name, items, color: random_color(true) };
    for (var i of item_names) {
      var a = this.Map.get(i);
      if (!a)
        return console.error("item '" + i + "' is grouped, but not present");
      a.groups.add(name);
    }
  }

  changeAM(ws, am, cws, cam) {
    this.compare_ws = cws ? cws : this.ws;
    this.compare_am = cam ? cam : this.am;
    var WS = Object.keys(this.am_by_ws);
    this.ws = ws ? ws : oneOf(WS);
    var AM = Object.keys(this.am_by_ws[this.ws]);
    this.am = am ? am : oneOf(AM);
    console.log("CHANGE TO " + this.ws + " " + this.am);

    for (var [_, a] of this.Map.entries()) {
      //a.shown = !a.hidden;
      a.size = 1 + a.normalized_size * 1;
      /*a.target_size = 1 + a.normalized_size * 1;
      if (a.hidden) a.size = 0.1;
      else a.size = a.size; //apply target size to shadow*/

      a.trend.evaluate();
    }

    this.request("layout");
    //this.timeout("changeAM", 3000);
  }

  setupContent2(collocates, coordinates, discoursemes){
    
    console.log(collocates);
    console.log(coordinates);
    console.log(discoursemes);

    for(var word of Object.keys(coordinates)){
      this.addWord( word );
    }

    this.layoutTsnePositions();
    this.request("layout");
  }


  setupContent(wordcloud_object) {
    this.setupDummyContent2(wordcloud_object);
  }

  // request the execution of the function in the next frame,
  // !BUT! only once (even if requested multiple times)
  request(fncName) {
    if (!this.requested) this.requested = new Set();
    if (this.requested.has(fncName)) return;
    this.requested.add(fncName);
    requestAnimationFrame(
      ((t, fncName) => () => {
        t.requested.delete(fncName);
        t[fncName]();
      })(this, fncName)
    );
  }

  // request the execution of the function after duration ms,
  // !BUT! when requested again in that period the older request is canceled
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

  debugClear() {
    if (this.debug) this.container.removeChild(this.debug);
    this.debug = document.createElement("div");
    this.container.appendChild(this.debug);
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

  layout(x) {

    
    //callWorker( this );

/*
    function myworker(){
      self.addEventListener('message', function(e) {
        setTimeout(()=>
        self.postMessage(e.data)
        ,1000);  
      }, false);
    }
    var wstring = myworker.toString(); 
    var body = wstring.slice(wstring.indexOf("{") + 1, wstring.lastIndexOf("}"));
    var blobURL = window.URL.createObjectURL(new Blob([body]));
    this.worker = new Worker(blobURL);
    //this.worker = new Worker("./layout_worker.js");

    this.worker.addEventListener("message", (msg) => console.log("MAIN: got msg: "+msg.data));
    this.worker.postMessage("Starteth thy work");
*/

    //this.layoutTsnePositions();
    if (!this.options.show_groups) layout.layoutWordcloudResolveOverlap(this);
    else layout.layoutWordcloudFormGroupsResolveOverlap(this);
    ///if (!this.options.show_groups) this.layoutWordcloudResolveOverlap();
    //else this.layoutWordcloudFormGroupsResolveOverlap();


    this.debugClear();
    this.drawContainmentEdges();
    this.drawGroups();

    this.pos = this.pos;
    this.scale = this.scale;
  }

  //  animation() {
  //    var total_delta = 0;
  //    for (var [_, a] of this.Map.entries()) {
  //      if (nan2(a.pos)) a.pos = [0, 0];
  //      if (nan2(a._pos)) a._pos = [0, 0];
  //
  //      var delta = scale2(sub2(a._pos, a.pos), 1); //0.2);
  //      //if (len2(delta) > 0.0001) {
  //      a.pos = add2(a.pos, delta);
  //
  //      total_delta += len2(delta);
  //
  //      /*if (a.target_size) {
  //        a.size = lerp(a.size, a.target_size, 0.2);
  //        total_delta += Math.abs(a.target_size - a.size) * 0.2;
  //      }*/
  //      //}
  //    }
  //    return;
  //    if (total_delta > 0.01) this.request("animation");
  //  }

  layoutTsnePositions() {
    //this.tsneRepositionVariance();
    //this.wWH = this.WH;
    var min = inf2();
    for (var [_, a] of this.Map.entries()) min = min2(min, a.computed_position);
    var max = negInf2();
    for (var [_, a] of this.Map.entries()) max = max2(max, a.computed_position);
    this.wWH = sub2(max, min); //this.WH;
    this.min = min;
    this.max = max;
    this.pos = min;
    this.centerCamera();
    this.screenBorder = [0, 0];

    for (var [_, a] of this.Map.entries()) {
      a._pos = a.computed_position;
      a.color = [0, 0, 0, 0.8]; //[Math.random(), Math.random(), Math.random()];
      this.screenBorder = max2(a.WH, this.screenBorder);
      //W.center = scale2(this.resolution, 0.5);
      //if (Math.random() < 0.5) W.el.classList.add("hidden");
    }

    //this.screenBorder = scale2(this.screenBorder, 1.2); //scale to match extended version
    this.centerCamera();
    //    this.request("animation");
  }

//  tsneRepositionVariance() {
//    var max_variance_factor = this.options.remap_standard_deviation_factor;
//    var center = null;
//    for (var [_, a] of this.Map.entries()) {
//      a.repositioned_tsne_position = null;
//      if (center === null) center = a.computed_position;
//      else center = add2(a.computed_position, center);
//    }
//    this.log(center);
//    this.log(this.Map.size);
//    center = scale2(center, 1 / this.Map.size);
//
//    var variance = null;
//    for (var [_, a] of this.Map.entries()) {
//      if (variance == null) variance = abs2(sub2(a.computed_position, center));
//      else variance = add2(variance, abs2(sub2(a.computed_position, center)));
//    }
//    variance = scale2(variance, 1 / this.Map.size);
//    this.log(center);
//    this.log(variance);
//
//    var max_variance = scale2(variance, max_variance_factor);
//    var min = sub2(center, max_variance);
//    var max = add2(center, max_variance);
//
//    for (var [_, a] of this.Map.entries()) {
//      var delta = sub2(a.computed_position, center);
//      if (this.options.remap_standard_deviation_clamp) {
//        delta = mul2(sign2(delta), min2(abs2(delta), max_variance));
//      }
//
//      if (this.options.remap_standard_deviation_log) {
//        delta = [
//          Math.sign(delta[0]) *
//            max_variance[0] *
//            Math.log(Math.abs(delta[0]) / max_variance[0] + 1),
//          Math.sign(delta[1]) *
//            max_variance[1] *
//            Math.log(Math.abs(delta[1]) / max_variance[1] + 1)
//        ];
//        /*
//        delta = [
//          Math.sign(delta[0]) *
//          max_variance[0] *
//          (1 -
//            1 /
//            Math.pow(
//              1 + Math.abs(delta[0]) / max_variance[0] / power,
//              power
//            )),
//          Math.sign(delta[1]) *
//          max_variance[1] *
//          (1 -
//            1 /
//            Math.pow(
//              1 + Math.abs(delta[1]) / max_variance[1] / power,
//              power
//            ))
//        ];*/
//      }
//
//      if (!this.options.remap_tsne_positions) {
//        a.repositioned_tsne_position = null;
//      } else {
//        a.repositioned_tsne_position = add2(center, delta);
//      }
//    }
//  }


  debugClear(){
    this.canvas.clearDebug();
  }
 
  debugRepositionLines(){
    var wordset = this;
    for (var [_, a] of wordset.Map.entries()) {
      a._pos = min2(max, a._pos);
      a._pos = max2(min, a._pos);
      if (wordset.options.reposition_shown_by_line) {
        wordset.canvas.debugLine(a._pos, a.layout_position, 2, [0, 0, 0, 0.1]);
      }
    }
  }
  
  debugRepositionColor(){
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
 
  
  drawContainmentEdges(){
  for (var [_, a] of this.Map.entries()) {
    if(!a.shown) continue;

    //TODO:: for every word, that is in multiple groups:
    if (this.options.show_lexical_items_of_group && a.groups.size > 1) {
      // draw a containment edge from the closest Group-Boundary-Point (lerp(Pi,Pi+1,0.5))
      // Pointing in normal direction
      // towards the center of the word, stopping at the word-boundary

      for (var gi of a.groups) {
        var G = this.groups[gi];
        //var closest = [0, 0];
        //var normal = [1, 0];
        var dist = Number.POSITIVE_INFINITY;
        var P = G.border_path;
        var ctr = [[0, 0], [0, 0], [0, 0], [0, 0]];
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

drawGroups(){
  for (var g of this.sorted_groups) {
    g.draw();
  }
}




}

///////////////////////////////////////
//
//    Inititalization
//
///////////////////////////////////////

export { WordcloudWindow };
