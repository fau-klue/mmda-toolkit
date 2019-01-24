
function dummycode(){
function mul2(a, b) {
  return [a[0] * b[0], a[1] * b[1]];
}

function sub2(a, b) {
  return [a[0] - b[0], a[1] - b[1]];
}

function add2(a, b) {
  return [a[0] + b[0], a[1] + b[1]];
}

function scale2(a, b) {
  return [a[0] * b, a[1] * b];
}

function div2(a, b) {
  return [a[0] / b[0], a[1] / b[1]];
}

function rand2() {
  return [Math.random(), Math.random()];
}

function lerp2(a, b, t) {
  return [t * b[0] + (1 - t) * a[0], t * b[1] + (1 - t) * a[1]];
}

function len2(a) {
  return Math.sqrt(dot2(a, a));
}
function normalize2(a) {
  return scale2(a, 1 / len2(a));
}
function dot2(a, b) {
  return a[0] * b[0] + a[1] * b[1];
}
function cross2(a, b) {
  return a[0] * b[1] - a[1] * b[0];
}

function lerp(a, b, t) {
  return (1 - t) * a + t * b;
}

function min2(a, b) {
  return [Math.min(a[0], b[0]), Math.min(a[1], b[1])];
}

function max2(a, b) {
  return [Math.max(a[0], b[0]), Math.max(a[1], b[1])];
}

function inf2() {
  return [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY];
}

function negInf2() {
  return [Number.NEGATIVE_INFINITY, Number.NEGATIVE_INFINITY];
}

function abs2(a) {
  return [Math.abs(a[0]), Math.abs(a[1])];
}

function sign2(a) {
  return [Math.sign(a[0]), Math.sign(a[1])];
}

function nan2(a) {
  return a[0] != a[0] || a[1] != a[1];
}

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


///////////////////////////////////////
//
//    Acceleration Structure
//
///////////////////////////////////////

function GridAccelerationStructure(num_elements, bounds) {
    // Initialize acceleration-Structure:
    // 2D array (ms x ms) of lists  <word collisions>
    this.size = Math.ceil(Math.sqrt(2 * num_elements));
    this.grid = new Array(this.size * this.size).fill(null).map(() => []);
    this.min = bounds.min;
    this.max = bounds.max;
    // console.log("mapfield: "+map_size+"x"+map_size+"   "+max_offset);
  
  this.worldToGrid =(v2)=> {
    return [
      this.coord(v2[0], this.min[0], this.max[0]),
      this.coord(v2[1], this.min[1], this.max[1])
    ];
  }
  this.coord=(val, min, max)=> {
    return Math.floor(
      Math.max(
        0,
        Math.min(this.size - 1, ((val - min) / (max - min)) * this.size)
      )
    );
  }
  this.forEachIn=(bounds, func)=> {
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


function iterativelyInsertObjectsTo(
    Objects,
    accGrid,
    noIntersection,
    shouldTest,
    failedInserting
  ) {
    var total_intersections = 0;
    for (var n of Objects) {
      n.outer_offset = null;
      var found_position = false;
      const MAX_INSERTION_TESTS = 1000;
      for (var i = 0; i < MAX_INSERTION_TESTS; ++i) {
        ++total_intersections;
        // Offsetting the Word to pseudo-random positions in increasing distances
        // around their desired position
        var world_footprint = sub2(n.max, n.min);
        var mf = Math.min(world_footprint[0], world_footprint[1]);
        n.offset = [
          Math.sin(1.8 * 2 * Math.sqrt(i) * mf) * i * mf * 0.0126,
          Math.cos(1.8 * 2 * Math.sqrt(i) * mf) * i * mf * 0.0126
        ];
        n._pos = add2(n.layout_position, n.offset);
        var intersection = false;
        if (shouldTest && !shouldTest(n)) {
          continue;
        }
        accGrid.forEachIn(n.bounds, F => {
          for (var m of F) {
            if (intersectObjects(m, n)) {
              //boundsIntersect(m.bounds, n.bounds)) {
              accGrid.abort = true;
              intersection = true;
              return;
            }
          }
        });
        if (!intersection) {
          if (noIntersection) {
            found_position = noIntersection(n);
          } else found_position = true;
          if (found_position) break;
        }
      }

      if (!found_position) {
        if (n.outer_offset !== null) {
          n.offset = n.outer_offset;
        } else {
          n.offset = [0, 0];
          if (failedInserting) failedInserting(n);
        }
        n._pos = add2(n.layout_position, n.offset);
      }
      accGrid.forEachIn(n.bounds, F => {
        F.push(n);
      });
    }
    return total_intersections;
  }


function  layoutWordcloudResolveOverlap( wordset ) {
    // Profiling
    //var starttime = Date.now();
    //var total_Tests = 0;
    //var total_intersections = 0;

    var sorted_nodes = [];
    for (var [_, n] of wordset.Map.entries()) {
      n.offset = [0, 0];
      n._pos = n.layout_position = n.computed_position;
      sorted_nodes.push(n);
    }

    sorted_nodes.sort((a, b) => {
      if (a.hidden && !b.hidden) return 1;
      if (!a.hidden && b.hidden) return -1;
      return b.normalized_size - a.normalized_size;
    });
    var min = inf2();
    for (var [_, a] of wordset.Map.entries()) min = min2(min, a.computed_position);
    var max = negInf2();
    for (var [_, a] of wordset.Map.entries()) max = max2(max, a.computed_position);
    wordset.max = max;
    wordset.min = min;
    wordset.wWH = sub2(max, min);

    if (wordset.options.resolve_overlap) {
      var accGrid = new GridAccelerationStructure(sorted_nodes.length, {
        min: min,
        max: max
      });

      total_intersections += iterativelyInsertObjectsTo(
        sorted_nodes,
        accGrid,
        n => {
          //Found Intersection and end
          if (
            n._pos[0] >= min[0] &&
            n._pos[0] <= max[0] &&
            n._pos[1] >= min[1] &&
            n._pos[1] <= max[1]
          ) {
            return true;
          } else if (n.outer_offset === null) {
            n.outer_offset = n.offset;
          }
          return false;
        },
        n => {
          //shouldTest
          return (
            n._pos[0] >= min[0] &&
            n._pos[0] <= max[0] &&
            n._pos[1] >= min[1] &&
            n._pos[1] <= max[1]
          );
        }
      );
    }

    // recalculate the margin around the drawing area
    wordset.screenBorder = [0, 0];
    for (var [_, a] of wordset.Map.entries()) {
      wordset.screenBorder = max2(a.WH, wordset.screenBorder);
    }
    //wordset.centerCamera();

    //    wordset.request("animation");
/*
    var n0 = sorted_nodes[0];
    wordset.log(n0);
    wordset.log(n0.bounds);
    wordset.log("Position 0 at " + n0._pos);
    wordset.log("          Words: " + sorted_nodes.length);
    wordset.log(
      "Insertion tests: " +
        total_intersections / sorted_nodes.length +
        " (/Word)"
    );
    wordset.log(
      "    Bound tests: " + total_Tests / total_intersections + " (/Insertion)"
    );
    wordset.log("           Took: " + (Date.now() - starttime) + " ms");
*/
    //      wordset.redrawLayout();
    // Send to Parent
    // wordset.$emit('event_text_ready', vm.list);
  }

function  layoutWordcloudFormGroupsResolveOverlap( wordset ) {
    // Profiling
    var starttime = Date.now();
    var total_Tests = 0;
    var total_intersections = 0;
    
    function insertion_order(a, b) {
      if (a.hidden && !b.hidden) return 1;
      if (!a.hidden && b.hidden) return -1;
      return b.normalized_size - a.normalized_size;
    }

    wordset.error.clear();

    wordset.group_map = {};

    wordset.min = inf2();
    wordset.max = negInf2();
    var all_nodes = [];
    for (var n of wordset.words) {
      n.offset = [0, 0];
      n._pos = n.layout_position = n.computed_position;
      all_nodes.push(n);
      wordset.min = min2(wordset.min, n.computed_position);
      wordset.max = max2(wordset.max, n.computed_position);

      n.shown = !n.hidden;
    }
    wordset.wWH = sub2(wordset.max, wordset.min);
    var vm = wordset;
    var failedInsertions = [];

    hierarchically_insert_groups(all_nodes, new Set());
    function hierarchically_insert_groups(all_nodes, set_of_parent_groups) {
      if (!all_nodes.length) return;
      var min = inf2();
      var max = negInf2();
      for (var n of all_nodes) {
        min = min2(min, n.computed_position);
        max = max2(max, n.computed_position);
      }

      var accGrid = new GridAccelerationStructure(all_nodes.length, {
        min,
        max
      });
      vm.total_acceleration_grid = accGrid;

      var free_nodes = [];
      for (var gi of Object.keys(vm.groups)) {
        var g = vm.groups[gi];
        g.uniqueItems = new Set(); //[];
      }

      for (var n of all_nodes) {
        if (n.groups.size == 1) {
          var g0;
          for (var v of n.groups) {
            g0 = v;
            break;
          }
          vm.groups[g0].uniqueItems.add(n);
          n.single_group = g0;
        } else if (
          n.groups.size == 0 ||
          vm.options.show_lexical_items_of_group
        ) {
          free_nodes.push(n);
        } else {
          n.shown = false;
        }
      }

      free_nodes.sort(insertion_order);

      var sorted_groups = [];
      for (var name of Object.keys(vm.groups)) {
        sorted_groups.push(vm.groups[name]);
      }

      for (var G of sorted_groups) {
        G.accumulated_size = 0;
        for (var i of G.uniqueItems) {
          G.accumulated_size += i.normalized_size > 0 ? i.normalized_size : 0;
        }
      }
      sorted_groups.sort((a, b) => {
        return b.accumulated_size - a.accumulated_size;
      });

      for (var G of sorted_groups) {
        var center = [0, 0];
        var gmin = inf2();
        var gmax = negInf2();
        var I = G.uniqueItems.size > 0 ? G.uniqueItems : G.items;
        for (var a of I) {
          center = add2(center, a.computed_position);
        }
        if (I.size > 0) {
          G.center = center = scale2(center, 1 / I.size);
        } else {
          G.center = center = G.computed_position
            ? G.computed_position
            : [0, 0];
        }
        var deltaTitle = vm.screenToWorld_vector(scale2(G.WH, 0.5));

        var PathPoints = [];
        G._min = sub2([0, 0], deltaTitle); //center,del);
        G._max = add2([0, 0], deltaTitle);
        PathPoints.push(
          [G._min[0], G._max[1]],
          G._min,
          [G._max[0], G._min[1]],
          G._max
        );
        if (!vm.options.show_lexical_items_of_group) {
          for (var a of G.uniqueItems) {
            a.shown = false;
          }
        } else if (G.uniqueItems.size) {
          for (var a of G.uniqueItems) {
            a.layout_position = scale2(
              sub2(a.computed_position, center),
              a.user_defined_position ? 1 : vm.options.relocation_by_group
            );
            gmin = min2(gmin, a.layout_position);
            gmax = max2(gmax, a.layout_position);
          }
          var itemsToInsert = Array.from(G.uniqueItems).sort(insertion_order);

          var groupGrid = new GridAccelerationStructure(G.uniqueItems.size, {
            min: gmin,
            max: gmax
          });
          total_intersections += iterativelyInsertObjectsTo(
            itemsToInsert,
            groupGrid,
            undefined,
            undefined,
            n => {
              failedInsertions.push(n.label);
              n.shown = false;
            }
          );

          gmin = G._min;
          gmax = G._max;
          var P = [];
          function margin(pos) {
            /*if(pos[1]<0){ 
              pos = [pos[0],pos[1] - 15*vm.worldPerScreen]; 
            }*/
            gmin = min2(gmin, pos);
            gmax = max2(gmax, pos);
            return pos;
          }
          for (var a of G.uniqueItems) {
            //collect all AABB edges
            PathPoints.push(
              margin(a.bounds.min),
              margin(a.bounds.max),
              margin([a.bounds.max[0], a.bounds.min[1]]),
              margin([a.bounds.min[0], a.bounds.max[1]])
            );
          }
          G._min = gmin;
          G._max = gmax;
        }
        G.border_path = convexHull(PathPoints);

        G.layout_position = G.computed_position;

        //border path should be ccw (when bottom-right == pos ydir, pos xdir)
        total_intersections += iterativelyInsertObjectsTo([G], accGrid);

        for (var a of G.uniqueItems) {
          // reposition items according to Group position
          a._pos = add2(a._pos, G._pos);
        }
      }

      for (var n of free_nodes) {
        if (n.groups.size > 0) {
          //var scale = vm.options.multigroup_attraction;
          var center = [0, 0];
          for (var gi of n.groups) {
            var G = vm.groups[gi];
            center = add2(center, G._pos);
          }
          n.layout_position = lerp2(
            n.layout_position,
            scale2(center, 1 / n.groups.size),
            1 - (n.user_defined_position ? 1 : vm.options.multigroup_attraction)
          );
        }
      }

      {
        total_intersections += iterativelyInsertObjectsTo(
          free_nodes,
          accGrid,
          n => {
            //Found Intersection and end
            if (
              n._pos[0] >= vm.min[0] &&
              n._pos[0] <= vm.max[0] &&
              n._pos[1] >= vm.min[1] &&
              n._pos[1] <= vm.max[1]
            ) {
              return true;
            } else if (n.outer_offset === null) {
              n.outer_offset = n.offset;
            }
            return false;
          },
          n => {
            //shouldTest
            return (
              n._pos[0] >= vm.min[0] &&
              n._pos[0] <= vm.max[0] &&
              n._pos[1] >= vm.min[1] &&
              n._pos[1] <= vm.max[1]
            );
          },
          n => {
            //failed Insertion
            if (n.normalized_size > 0 || n.normalized_size_compare > 0) {
              //if should be visible...
              failedInsertions.push(n.label);
            }
            n.shown = false;
          }
        );
      }

      if (failedInsertions.length) {
        vm.error.set(
          " " + failedInsertions.length,
          "Not enough space to show all the lexical items (zoom in to solve). The following lexical item(s) is/are missing:  " +
            failedInsertions.join(", ")
        );
      }
      
      wordset.sorted_groups = sorted_groups;
    }

    wordset.screenBorder = [0, 0];
    for (var [_, a] of wordset.Map.entries()) {
      wordset.screenBorder = max2(a.WH, wordset.screenBorder);
    }
    //wordset.centerCamera();

    //    wordset.request("animation");

    //    var n0 = free_nodes[0];
    //  wordset.log(n0);
    //wordset.log(n0.bounds);
    // wordset.log("Position 0 at " + n0._pos);
    /*wordset.log("          Words: " + all_nodes.length);
    wordset.log(
      "Insertion tests: " + total_intersections / all_nodes.length + " (/Word)"
    );
    wordset.log(
      "    Bound tests: " + total_Tests / total_intersections + " (/Insertion)"
    );
    wordset.log("           Took: " + (Date.now() - starttime) + " ms");
*/
    //      wordset.redrawLayout();
    // Send to Parent
    // wordset.$emit('event_text_ready', vm.list);
  }




}

export{dummycode};