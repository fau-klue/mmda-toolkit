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
} from "./util_bounds_and_intersection.js";

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
        this.bounds = {
            min: [0, 0],
            max: [0, 0]
        };
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
        this.window.total_acceleration_grid.forEachIn({
                min: wmin,
                max: wmax
            },
            (t => els => {
                for (var el of els) {
                    if (intersectObjects(el, {
                            bounds: {
                                min: wmin,
                                max: wmax
                            }
                        })) {
                        if (el.shown) t.newSelection.add(el);
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


export {
    SelectionBox
};