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
    const MAX_INSERTION_TESTS = 100;
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


function layoutWordcloudFormGroupsResolveOverlap(wordset) {
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

  var all_nodes = [];
  for (var [_, n] of wordset.Map.entries()) {
    n.offset = [0, 0];
    n._pos = n.computed_position;
    n._pos = max2(n._pos, wordset.min);
    n._pos = min2(n._pos, wordset.max);
    n.layout_position = n._pos;
    all_nodes.push(n);
    n.shown = !n.hidden;
  }

  var failedInsertions = [];

  hierarchically_insert_groups(all_nodes, new Set(), wordset);
  wordset.screenBorder = [0, 0];
  for (var [_, a] of wordset.Map.entries()) {
    wordset.screenBorder = max2(a.WH, wordset.screenBorder);
  }

  //finalize position
  for (var [_, a] of wordset.Map.entries()) {
    a.pos = a._pos;
  }

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




  function hierarchically_insert_groups(all_nodes, set_of_parent_groups, vm) {
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
    for (var G of vm.groups) {
      G.uniqueItems = new Set(); //[];
    }

    for (var n of all_nodes) {
      if (n.groups.size == 1) {
        var g0;
        for (var v of n.groups) {
          g0 = v;
          break;
        }
        g0.uniqueItems.add(n);
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

    var sorted_groups = Array.from(vm.groups);

    for (var G of sorted_groups) {
      G.accumulated_size = 0;
      for (var i of G.uniqueItems) {
        G.accumulated_size += i.normalized_size >= 0 ? i.normalized_size : 0;
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
        G.center = center = G.computed_position ?
          G.computed_position : [0, 0];
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
            failedInsertions.push(n);
          }
        );

        gmin = G._min;
        gmax = G._max;

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
      G.bounds.convex_hull = convexHull(PathPoints);

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
        for (var G of n.groups) {
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
          if (n.normalized_size >= 0 || n.normalized_size_compare >= 0) {
            //if should be visible...
            failedInsertions.push(n);
          }
        }
      );
    }

    if (failedInsertions.length) {
      for(var n of failedInsertions){
        //wordset.debugPoint(n._pos);
        n.shown = false;
      }
      
      vm.error.set(
        " " + failedInsertions.length,
        "Not enough space to show all the lexical items (zoom in to solve). The following lexical item(s) is/are missing:  " +
        failedInsertions.map((n)=>n.label).join(", ")
      );
    }

    wordset.sorted_groups = sorted_groups;
  }

}

export {
  iterativelyInsertObjectsTo,
  layoutWordcloudFormGroupsResolveOverlap,
}