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

///////////////////////////////////////
//
//    Wordcloud Element-Menu
//
///////////////////////////////////////

class WordMenu {
  constructor(window) {
    this.window = window;
    this.item = null;
    this.options = [];

    this.el = document.createElement("div");
    this.el.classList.add("word_menu");
    this.window.container.appendChild(this.el);

    var interresting_icons = ["👁📈📌📊⊕📂⚇💾📄⮋⊞➕"];

    var options = [
      {
        icon: "📌",
        icon_overlay: "╳",
        title: "un-pin selected",
        executable: (t => e => {
          for (var n of t.window.selected_nodes) {
            if (n.pin.pinned) return true;
          }
        })(this),
        fnc: (t => e => {
          for (var n of t.window.selected_nodes) {
            if (n.pin.pinned) n.pin.reset();
          }
          t.window.request("layout");
        })(this)
      },
      {
        icon: "➕",
        title: "create new group (with all selected words)",
        fnc: (t => () => {
          t.window.groupSelected();
        })(this)
      },
      {
        icon: "🗑",
        title: "ungroup selection",
        fnc: () => {
          this.window.deleteSelection();
        }
      },
      { icon: "⮋", title: "enter group" },
      { icon: "📈", title: "show distribution over time" },
      { icon: "📊", title: "show evaluation" }
    ];

    for (var oi in options) {
      var o = options[oi];
      var firstlen = Math.ceil(options.length * 0.5);
      var secondlen = options.length - firstlen;
      o.angle =
        oi < firstlen
          ? 180 + (firstlen > 1 ? 45 + (oi * 90) / (firstlen - 1) : 90)
          : secondlen > 1
          ? 180 - 45 - ((oi - firstlen) * 90) / (secondlen - 1)
          : 90;
      this.makeItem(o);
    }

    this.shown = false;
  }
  get WH() {
    return [this.el.offsetWidth, this.el.offsetHeight];
  }
  get pos() {
    return this._pos;
  }
  set pos(p) {
    this._pos = p;
    if (!this.window.wWH) return;
    var pixPos = div2(
      sub2(
        sub2(this._pos, scale2(this.WH, 0.5 * this.window.worldPerScreen)),
        this.window.min
      ),
      this.window.wWH
    );
    this.el.style.left = pixPos[0] * 100 + "%";
    this.el.style.top = pixPos[1] * 100 + "%";
  }
  get shown() {
    return this._shown;
  }
  set shown(s) {
    if (!s) this.el.style.visibility = "hidden";
    else {
      this.el.style.visibility = "visible";
      for (var o of this.options) {
        if (o.executable) {
          if (o.executable()) {
            o.el.classList.remove("hidden");
          } else o.el.classList.add("hidden");
        }
      }
    }
    this._shown = s;
  }

  makeItem(obj) {
    this.options.push(obj);
    var el = (obj.el = document.createElement("div"));
    el.classList.add("item");
    this.el.appendChild(el);
    el.addEventListener(
      "mouseup",
      (obj => e => {
        if (!obj.executable || obj.executable()) {
          obj.fnc();
        }
      })(obj)
    );
    el.appendChild(document.createTextNode(obj.icon));
    if (obj.icon_overlay) {
      var el_ol = document.createElement("div");
      el_ol.style.position = "absolute";
      el_ol.style.top = 0;
      el_ol.style.left = 0;
      el_ol.appendChild(document.createTextNode(obj.icon_overlay));
      el.appendChild(el_ol);
    }
    if (obj.title) el.title = obj.title;
    el.style.top =
      50 +
      (Math.sin((obj.angle / 180) * Math.PI) -
        el.offsetHeight / this.el.offsetHeight) *
        100 +
      "%";
    el.style.left =
      50 +
      (Math.cos((obj.angle / 180) * Math.PI) -
        el.offsetWidth / this.el.offsetWidth) *
        100 +
      "%";
  }
}

export { WordMenu };
