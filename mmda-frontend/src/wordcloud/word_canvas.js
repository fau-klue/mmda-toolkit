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
    fwdEvent
} from "./util_misc.js";


class WordCanvas {
    constructor(window) {
        this.window = window;
        this.window.container.setAttribute("id", "window_container");
        this.svg_worldspace = SVG("window_container");
        this.svg_worldspace.attr("style", "left:-1000%;top:-1000%;width:3000%;height:3000%;");
        this.clearDebug();
    }
    resize() {
        let m = this.window.min,
            M = this.window.max;
        let x = m[0],
            y = m[1],
            w = M[0] - m[0],
            h = M[1] - m[1];
        let X = x - 10 * w,
            Y = y - 10 * h,
            W = 30 * w,
            H = 30 * h;
        this.svg_worldspace.attr("viewBox", X + " " + Y + " " + W + " " + H);
    }
    remove(el) {
        var i = this.elements.findIndex(a => a == el);
        if (i != -1) {
            this.elements.splice(i, 1);
            el.remove();
        }
    }
    clearDebug() {
        if (this.elements)
            for (var p of this.elements) p.remove();
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
            .attr({
                fill: hex_color_from_array([...color, 0.1])
            });

        var text = this.svg_worldspace
            .text(function (add) {
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
        text.textPath().attr({
            startOffset: middlePercentage + "%"
        });

        var res = path;
        this.elements.push(res);
        this.elements.push(text);
        return {
            path,
            text
        };
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
            .attr({
                fill: "none"
            })
        );
    }
}

export {
    WordCanvas
};