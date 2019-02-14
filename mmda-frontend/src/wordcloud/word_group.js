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
  random_color,
  fwdEvent
} from "./util_misc.js";

import {
  Pin
} from "./word_element.js";

///////////////////////////////////////
//
//    Word Group
//
///////////////////////////////////////

class WordGroup {
  constructor(title, window) {
    this.window = window;
    this.name = title;

    this.__pos = [0, 0];
    this.items = new Set(); //[];

    //this.el = document.createElement("div");
    //this.el.appendChild(document.createTextNode(title));
    //this.el.classList.add("wordcloud_group_title");

    this.pin = new Pin(this);
    //this.el.appendChild(this.pin.el);

    this.window.container.appendChild(this.pin.el);

    //this.window.container.appendChild(this.el);
    this.linewidth = 2;
    this.color = random_color(true);
  }
  addItemsByName(item_names) {
    for (var n of item_names) {
      var it = this.window.Map.get(n);
      if (!it) continue;
      this.addItem(it);
    }
  }
  delete() {
    this.window.groups.delete(this);
    if (this.selected) this.window.selected_nodes.delete(this);
    for (var i of this.items) {
      this.removeItem(i);
    }
    //this.window.container.appendChild(this.pin.el);
    // if (this.pin) 
    this.window.container.removeChild(this.pin.el);
    //if (this.el) this.window.container.removeChild(this.el);
    //this.el = undefined;
  }
  addItem(n) {
    this.items.add(n);
    n.groups.add(this);
  }
  removeItem(n) {
    this.items.delete(n);
    n.groups.delete(this);
  }

  get isgroup() {
    return true;
  }

  get label() {
    return this.name;
  }
  set color(c) {
    this._color = c;
    //this.el.style.color = hex_color_from_array([c[0], c[1], c[2], 0.1]);
    return this._color;
  }
  get color() {
    return this._color;
  }
  get WH() {
    return [40, 40]; //[this.el.offsetWidth, this.el.offsetHeight];
  }
  get computed_position() {
    return this.user_defined_position ?
      this.user_defined_position :
      this.center;
  }
  get user_defined_position() {
    return this._user_defined_position;
  }
  set user_defined_position(p) {
    this.pin.pinned = true;
    return (this._user_defined_position = p);
  }
  get pos() {
    return this._pos;
  }
  set pos(v) {
    return (this._pos = v);
  }

  get _pos() {
    return this.__pos;
  }
  set _pos(p) {
    this.__pos = p;
    var pixPos = div2(
      sub2(
        p, //sub2(p, scale2(this.WH, 0.5 * this.window.worldPerScreen)),
        this.window.min
      ),
      this.window.wWH
    );
    //this.el.style.left = pixPos[0] * 100 + "%";
    //this.el.style.top = pixPos[1] * 100 + "%";

    this.pin.el.style.left = pixPos[0] * 100 + "%";
    this.pin.el.style.bottom = (1 - pixPos[1]) * 100 + "%";
    this.redraw();
    return this.__pos;
  }
  get bounds() {
    var vm = this;
    return {
      min: this.min,
      max: this.max,
      get convex_hull() {
        return vm.border_path;
      },
      set convex_hull(c) {
        return vm.border_path = c;
      }
    };
  }
  get min() {
    return add2(this._pos, this._min);
  }
  get max() {
    return add2(this._pos, this._max);
  }
  set border_path(P) {
    this._border_path = P;
  }
  get border_path() {
    if (!this._border_path) return null;
    var res = [];
    for (var p of this._border_path) {
      res.push(add2(this._pos, p));
    }
    return res;
  }
  get selected() {
    return this._selected;
  }
  set selected(v) {
    this._selected = v;

    this.visual_representation.path.stroke({
      width: (this._selected ? 3 : 1) * this.window.worldPerScreen * this.linewidth
    });
    if (this._selected) {
      this.window.selected_nodes.add(this);
    } else {
      this.window.selected_nodes.delete(this);
    }
    return this._selected;
  }

  get dragging() {
    return this._dragging;
  }
  set dragging(v) {
    this._dragging = v;
    if (v) {
      //this.el.classList.add("dragged");
      this.visual_representation.path.node.classList.add("dragged");
      this.visual_representation.text.node.classList.add("dragged");
    } else {
      //this.el.classList.remove("dragged");
      this.visual_representation.path.node.classList.remove("dragged");
      this.visual_representation.text.node.classList.remove("dragged");
    }
  }

  dropAt(el) {
    if (el.isgroup) {
      this.selected = true;
      el.selected = true;
      this.window.groupSet(this.window.selected_nodes, el.label);
      this.window.clearSelection();
    }
    //do nothing ...
  }

  redraw() {
    if (!this.visual_representation) return;
    this.window.canvas.remove(this.visual_representation.path);
    this.window.canvas.remove(this.visual_representation.text);
    this.draw();
  }
  draw() {
    this.visual_representation = this.window.canvas.debugConvex(
      this.border_path,
      this.linewidth * (this._selected ? 3 : 1),
      this.color,
      this.label
    );


    var el = this.visual_representation.path.node;
    fwdEvent(this, el, "mouseover");
    fwdEvent(this, el, "mouseout");
    fwdEvent(this, el, "mousedown");
    el.classList.add("wordcloud_group");
    el = this.visual_representation.text.node;
    fwdEvent(this, el, "mouseover");
    fwdEvent(this, el, "mouseout");
    fwdEvent(this, el, "mousedown");
    el.classList.add("wordcloud_group");
    this.onmouseout();
  }
  onmousedown(e) {
    this.window.last_selected_node = this;
    this.window.pressed_node = this;
    this.window.pressed_offset = sub2(this.window.mouse_wpos, this.pos);
    e.preventDefault();
  }
  onmouseover(e) {
    this.visual_representation.path.attr({
      fill: hex_color_from_array([...this.color, 0.2])
    });
    this.window.hover_node = this;
  }
  onmouseout(e) {
    this.visual_representation.path.attr({
      fill: hex_color_from_array([...this.color, 0.02])
    });
    if (!this.dragging) {
      this.window.hover_node = null;
    }
  }
}

export {
  WordGroup
};