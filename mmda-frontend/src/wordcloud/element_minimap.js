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
  get WH() {
    return [this.el.offsetWidth, this.el.offsetHeight];
  }
  set shown(s) {
    this.el.style.backgroundColor = s ? "#000a" : "#a002";
  }
  reposition() {
    var wPos = this.word.window.worldToContainer(this.word.pos);
    this.el.style.left =
      "calc(" + wPos[0] * 100 + "% - " + this.WH[0] * 0.5 + "px)";
    this.el.style.top =
      "calc(" + wPos[1] * 100 + "% - " + this.WH[1] * 0.5 + "px)";
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

    this.el.style.width =
      this.window.wWH[0] / s2 * this.max_scale[0] +
      "rem";
    this.el.style.height =
      this.window.wWH[1] / s2 * this.max_scale[1] +
      "rem";
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

    this.frame.style.left =
      ((p[0] - this.window.min[0]) / this.window.wWH[0]) * 100 + "%";
    this.frame.style.top =
      ((p[1] - this.window.min[1]) / this.window.wWH[1]) * 100 + "%";

    this.frame.style.right =
      (1 -
        (p[0] + camDimToWorld[0] - this.window.min[0]) / this.window.wWH[0]) *
      100 +
      "%";
    this.frame.style.bottom =
      (1 -
        (p[1] + camDimToWorld[1] - this.window.min[1]) / this.window.wWH[1]) *
      100 +
      "%";
  }
}

export {
  Minimap,
  MinimapElement
};