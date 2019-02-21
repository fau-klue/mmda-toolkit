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
  fwdEvent
} from "./util_misc.js";

import {
  Minimap,
  MinimapElement
} from "./element_minimap.js";

class Pin {
  constructor(parent) {
    this.parent = parent;
    this.el = document.createElement("div");
    this.el.classList.add("wordcloud_pin");
    this.el.classList.add("hidden");

    //var ic = document.createTextNode("📌");
    var ic = document.createElement("i");
    ic.classList.add("v-icon");
    ic.classList.add("material-icons");
    ic.classList.add("place_icon");
    ic.appendChild(document.createTextNode("place"));

    this.el.title = "unpin item/group";
    this.el.appendChild(ic);

    this.el.addEventListener("click", ((t) => (e) => t.reset(e))(this));
  }
  get pinned() {
    return this._pinned;
  }
  set pinned(p) {
    if (p) this.el.classList.remove("hidden");
    else this.el.classList.add("hidden");
    return (this._pinned = p);
  }
  reset(e) {
    this.pinned = false;
    this.parent.selected = false;
    this.parent._user_defined_position = null;
    this.parent.pos = this.parent.computed_position;
    this.parent.window.request("layout");
    //this.parent.window.word_menu.shown = false;
    //
  }
}

///////////////////////////////////////
//
//    Word Trend
//
///////////////////////////////////////

class WordTrend {
  constructor(word) {
    this.word = word;
    this.el = document.createElement("div");
    this.el.classList.add("wordcloud_trend");
    this.word.txt.appendChild(this.el);
    this.hide();
  }
  set(v, size) {
    if (v == "hidden") {
      this.hide();
      return;
    }
    this.el.classList.remove("hidden");
    this.el.classList.remove(this.state);
    this.el.classList.add((this.state = v));
    if (size) this.el.style.fontSize = size + "rem";
    else this.el.style.fontSize = "auto";
    var map = {
      strong_up_alt: "⬆",
      strong_down_alt: "⬇",
      new: "⭑",
      deleted: "x",
      up: "⯅",
      down: "⯆"
    };
    this.el.innerText = map[v];
  }
  hide() {
    this.el.classList.add("hidden");
  }
  evaluate() {
    this.word.el.classList.remove("disappeared");
    if (!this.word.window.options.word_trend_show) return this.hide();
    var eps = 0.1;
    var eps2 = 0.4;
    var nu = this.word.normalized_size;
    var old = this.word.normalized_size_compare;
    if (old < 0 && nu < 0) {
      //is still invisible
      this.hide();
    } else if (old < 0) {
      //just appeared
      this.set("new", 1.5);
    } else if (nu < 0) {
      // just disappeared
      this.word.el.classList.add("disappeared");
      this.hide();
    } else if (old + eps < nu) {
      // increasing
      this.set("up", (nu - old) * 2);
    } else if (old - eps > nu) {
      // decreasing
      this.set("down", (old - nu) * 2);
    } else {
      // staying
      this.hide();
    }
  }
}

///////////////////////////////////////
//
//    Word Element
//
///////////////////////////////////////

class WordElement {
  constructor(w) {
    this.data = w;
    this.el = document.createElement("div");
    this.el.classList.add("wordcloud_element");
    this.el.appendChild(document.createTextNode(this.label));

    this.txt = document.createElement("div");
    this.txt.classList.add("text");
    this.txt.appendChild(document.createTextNode(this.label));
    this.el.appendChild(this.txt);

    this.groups = new Set();

    this.pin = new Pin(this);
    this.txt.appendChild(this.pin.el);

    this.trend = new WordTrend(this);
    this.mini = new MinimapElement(this);
    for (var v of ["mouseover", "mouseout", "mousedown"])
      fwdEvent(this, this.el, v);
  }
  link(window) {
    //window.container.appendChild(this.shadow);
    //    window.container.appendChild(this.shadow_el);
    window.container.appendChild(this.el);
    this.window = window;
    this.pos = [0, 0];
    this.size = 1 + Math.max(0,Math.min(1,this.normalized_size));
    this.mini.link();
  }

  delete(){
    this.window.container.removeChild(this.el);
    this.mini.delete();
  }

  get WH() {
    return [this.el.offsetWidth, this.el.offsetHeight];
  }
  get wWH() {
    return scale2(this.WH, this.window.worldPerScreen);
  }
  get normalized_size() {
    var val = this.window.getSizeOf(this.data);
    return val;
  }
  get normalized_size_compare() {
    return this.window.getCompareSizeOf(this.data);
  }
  get original_position() {
    return [this.data.tsne_x, this.data.tsne_y];
  }

  get computed_position() {
    if (this.user_defined_position) return this.user_defined_position;
    if (this.repositioned_tsne_position) return this.repositioned_tsne_position;
    return this.original_position;
  }
  resetPosition() {
    this.user_defined_position = null; //this.original_position;
  }

  get identifier() {
    return this.data.name;
  }
  get label() {
    return this.data.name;
  }

  get pos() {
    return this._pos;
  }
  set pos(p) {
    this._pos = p;
    this.applyPosition();
  }
  applyPosition() {
    if (!this.window.wWH) return;
    var p = this.window.worldToContainer(this._pos); //div2(sub2(this._pos, this.window.min), this.window.wWH);
    this.el.style.left = p[0] * 100 + "%";
    this.el.style.top = p[1] * 100 + "%";

    // shadow position
    /*    var s = this.window.worldToContainer(
          sub2(
            lerp2(this._pos, this.original_position, 0.05),
            scale2(this.WH, 0.5 * this.window.worldPerScreen)
          )
        );

        var del = sub2(s, p);
        if (
          !this.window.options.reposition_shown_by_shadow ||
          len2(del) * 10 < 0.02
        )
          this.el.style.textShadow = "";
        else
          this.el.style.textShadow =
          del[0] * 100 +
          "rem " +
          del[1] * 100 +
          "rem " +
          len2(del) * 10 +
          "rem #0002";*/
    this.mini.reposition();
  }

  get dragging() {
    return this._dragging;
  }
  set dragging(v) {
    this._dragging = v;
    if (v) this.el.classList.add("dragged");
    else this.el.classList.remove("dragged");
  }
  //bounds in worldcoordinates, but depending on camera zoom --> layout recalculation after zoom
  get min() {
    return sub2(this.pos, scale2(this.WH, 0.5 * this.window.worldPerScreen));
  }
  get max() {
    return add2(this.pos, scale2(this.WH, 0.5 * this.window.worldPerScreen));
  }
  get bounds() {
    return {
      min: this.min,
      max: this.max
    };
  }

  set shown(s) {
    if (s) this.el.classList.remove("hidden");
    else this.el.classList.add("hidden");
    this.mini.shown = s;
    return this._shown = s;
  }
  get shown() {
    return this._shown;
  }
  get hidden() {
    return this.normalized_size < 0 && this.normalized_size_compare < 0;
  }



  get size() {
    return this._size;
  }
  set size(s) {
    this._size = s;
    this.el.style.fontSize = s + "rem";
    if (this.groups.size > 0 && s <= 0) {
      //TODO:: add permanent on group setup
      this.el.classList.add("permanent");
    } else {
      this.el.classList.remove("permanent");
    }
    return (this._size = s);
  }

  get color() {
    return this._color;
  }
  set color(c) {
    this._color = c;
    this.el.style.color = hex_color_from_array(this._color);
    return c;
  }
  get selected() {
    return this._selected;
  }
  set selected(v) {
    this._selected = v;
    if (this._selected) {
      this.window.selected_nodes.add(this);
      this.el.classList.add("selected");
    } else {
      this.window.selected_nodes.delete(this);
      this.el.classList.remove("selected");
    }
  }

  get user_defined_position() {
    return this._user_defined_position;
  }
  set user_defined_position(p) {
    this.pin.pinned = true;

    if (this.groups.size == 1) {
      //group-local user position:
      var G = this.groups.values().next().value;
      p = sub2(p, sub2(G.computed_position, G.center));
    }

    return (this._user_defined_position = p);
  }

  dropAt(el) {
    if (el.isgroup) {
      if (this.groups.has(el)) return;
      this.selected = true;
      el.selected = true;
      this.window.groupSet(this.window.selected_nodes, el.label);
    } else {
      this.selected = true;
      el.selected = true;
      this.window.groupSet(this.window.selected_nodes);
    }
    this.window.clearSelection();
    this.pin.reset();
  }

  onmouseover(e) {
    this.size *= 1.2;
    //only temporarily change color
    this.el.style.color = hex_color_from_array([0.2, 0.5, 0.2]);
    this.window.hover_node = this;
  }
  onmouseout(e) {
    this.size /= 1.2;
    //reset color
    this.color = this.color;
    this.window.hover_node = null;
  }
  onmousedown(e) {
    this.window.last_selected_node = this;
    this.window.pressed_node = this;
    this.window.pressed_offset = sub2(this.window.mouse_wpos, this.pos);
    //this.window.centerAtWord(this);
    e.preventDefault();
  }
}

export {
  Pin,
  WordElement,
  WordTrend
};