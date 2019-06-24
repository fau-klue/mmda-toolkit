
import { domSet } from '@/wordcloud/util_misc.js';


///////////////////////////////////////
//
//    Minimap Element
//
///////////////////////////////////////

class MinimapElement {
  constructor(word) {
    this.word = word;
    this.el = document.createElement("div");
    this.el.classList.add("minimap_element");
    this.initialWidth = this.el.offsetWidth;
  }
  link() {
    this.word.window.minimap.el.appendChild(this.el);
  }
  delete(){
    this.word.window.minimap.el.removeChild(this.el);
  }
  get WH() {
    return [this.el.offsetWidth, this.el.offsetHeight];
  }
  set shown(s) {
    //this.el.style.backgroundColor = s ? "#000a" : "#a002";
    domSet(this.el,'backgroundColor',s?'#000a':'#a002');
  }
  reposition() {
    var wPos = this.word.window.worldToContainer(this.word.pos);
    domSet(this.el,'left',"calc(" + wPos[0] * 100 + "% - " + this.WH[0] * 0.5 + "px)");
    domSet(this.el,'top',"calc(" + wPos[1] * 100 + "% - " + this.WH[1] * 0.5 + "px)");
  }
}

////////////////////////////////
//
//    Minimap
//
///////////////////////////////////////

class Minimap {
  constructor(window) {
    this.window = window;
    // minmap content div
    this.el = document.createElement("div");
    this.el.classList.add("minimap");
    this.window.el.appendChild(this.el);

    // minimap frame (highlighting the area visible by the camera)
    this.frame = document.createElement("div");
    this.frame.classList.add("frame");
    this.el.appendChild(this.frame);

    //minimap in minimap (inside frame)
    this.frame.appendChild(document.createElement("div"));
    this.max_scale = [20, 20];
  }

  rescale() {
    var s2 = Math.max(this.window.wWH[0], this.window.wWH[1]);

    domSet(this.el,'width', this.window.wWH[0] / s2 * this.max_scale[0] + "rem");
    domSet(this.el,'height',this.window.wWH[1] / s2 * this.max_scale[1] + "rem");
  }

  set shown(s) {
    if (s) this.el.classList.remove("hidden");
    else this.el.classList.add("hidden");
  }
  get shown() {
    return !this.el.classList.contains("hidden");
  }

  reposition() {
    var p = this.window.pos;
    var camDimToWorld = this.window.screenToWorld_vector(this.window.WH);

    domSet(this.frame,'left', ((p[0] - this.window.min[0]) / this.window.wWH[0]) * 100 + "%");
    domSet(this.frame,'top',  ((p[1] - this.window.min[1]) / this.window.wWH[1]) * 100 + "%");
    domSet(this.frame,'right', (1 - (p[0] + camDimToWorld[0] - this.window.min[0]) / this.window.wWH[0]) *  100 + "%");
    domSet(this.frame,'bottom', (1 - (p[1] + camDimToWorld[1] - this.window.min[1]) / this.window.wWH[1]) * 100 + "%");
  }
}

export {
  Minimap,
  MinimapElement
};