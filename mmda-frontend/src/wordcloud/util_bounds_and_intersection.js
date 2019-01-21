import { sub2, cross2, normalize2 } from "./util_math.js";

function intersectAABBs(a, b) {
  return !(
    a.max[0] < b.min[0] ||
    a.min[0] > b.max[0] ||
    a.max[1] < b.min[1] ||
    a.min[1] > b.max[1]
  );
}
function intersectConvexAABB(p, r) {
  //a path is an array of vertices of a convex shape.
  var min = r.min;
  var max = r.max;
  var minmax = [r.min[0], r.max[1]];
  var maxmin = [r.max[0], r.min[1]];
  for (var i = 0; i < p.length; ++i) {
    var d = sub2(p[(i + 1) % p.length], p[i]);
    if (cross2(d, sub2(min, p[i])) > 0) continue;
    if (cross2(d, sub2(max, p[i])) > 0) continue;
    if (cross2(d, sub2(maxmin, p[i])) > 0) continue;
    if (cross2(d, sub2(minmax, p[i])) > 0) continue;
    //If the current axis is separating, we are not overlapping
    return false;
  }
  return true;
}
function intersectConvexs(p, q) {
  //TODO:: optimize     (e.g. with binary search)
  //a path is an array of vertices of a convex shape.
  for (var i = 0; i < p.length; ++i) {
    var d = sub2(p[(i + 1) % p.length], p[i]);
    var separating = true;
    for (var j = 0; j < q.length; ++j) {
      if (cross2(d, sub2(q[j], p[i])) > 0) {
        separating = false;
        break;
      }
    }
    if (!separating) continue;
    //If the current axis is separating, we are not overlapping
    return false;
  }
  return true;
}
function intersectObjects(a, b) {
  if (!intersectAABBs(a.bounds, b.bounds)) return false;
  else {
    if (!a.border_path) {
      if (!b.border_path) return true;
      else return intersectConvexAABB(b.border_path, a.bounds);
    } else {
      if (!b.border_path) return intersectConvexAABB(a.border_path, b.bounds);
      else return intersectConvexs(a.border_path, b.border_path);
    }
  }
}

export {
  intersectAABBs,
  intersectConvexAABB,
  intersectConvexs,
  intersectObjects
};

function convexHull(P) {
  var conv = [P[0], P[1], P[2]];

  var bottom_left = 0;
  var pmin = [Number.POSITIVE_INFINITY, -Number.POSITIVE_INFINITY]; //negInf2();
  for (var i = 0; i < P.length; ++i) {
    if (pmin[1] < P[i][1] || (pmin[1] == P[i][1] && pmin[0] > P[i][0])) {
      pmin = P[i];
      bottom_left = i;
    }
  }

  var angle_sorted = [];
  for (var i in P) {
    if (i == bottom_left) continue;
    var angle = -normalize2(sub2(P[i], pmin))[0];
    angle_sorted.push({ angle, p: P[i], i });
  }

  angle_sorted.sort((a, b) => {
    return b.angle - a.angle;
  });

  conv = [pmin];
  for (var a of angle_sorted) {
    for (; conv.length >= 2; ) {
      var A = sub2(a.p, conv[conv.length - 1]);
      var B = sub2(conv[conv.length - 1], conv[conv.length - 2]);
      if (cross2(A, B) < 0) break; //last tri is turning in the right direction
      conv.pop();
    }
    conv.push(a.p);
  }
  //console.log(conv);
  return conv;
}

export { convexHull };

///////////////////////////////////////
//
//    Acceleration Structure
//
///////////////////////////////////////

class GridAccelerationStructure {
  constructor(num_elements, bounds) {
    // Initialize acceleration-Structure:
    // 2D array (ms x ms) of lists  <word collisions>
    this.size = Math.ceil(Math.sqrt(2 * num_elements));
    this.grid = new Array(this.size * this.size).fill(null).map(() => []);
    this.min = bounds.min;
    this.max = bounds.max;
    // console.log("mapfield: "+map_size+"x"+map_size+"   "+max_offset);
  }
  worldToGrid(v2) {
    return [
      this.coord(v2[0], this.min[0], this.max[0]),
      this.coord(v2[1], this.min[1], this.max[1])
    ];
  }
  coord(val, min, max) {
    return Math.floor(
      Math.max(
        0,
        Math.min(this.size - 1, ((val - min) / (max - min)) * this.size)
      )
    );
  }
  forEachIn(bounds, func) {
    this.abort = false;
    var min = this.worldToGrid(bounds.min);
    var max = this.worldToGrid(bounds.max);
    for (var x = min[0]; x <= max[0]; ++x) {
      for (var y = min[1]; y <= max[1]; ++y) {
        func(this.grid[x * this.size + y], this);
        if (this.abort) return;
      }
    }
  }
}

export { GridAccelerationStructure };
