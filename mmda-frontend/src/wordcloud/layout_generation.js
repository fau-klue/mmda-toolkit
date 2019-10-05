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

import {fwdEvent, hex_color_from_array} from "./util_misc.js";

var total_insertion_tests = 0;
var total_objects = 0;

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
    var avg = total_insertion_tests / Math.max(10, total_objects);
    var MAX_INSERTION_TESTS = Math.min(100, Math.max(1, 100 / Math.max(1, avg)));
    total_objects++;


    for (var i = 0; i < MAX_INSERTION_TESTS; ++i) {
      ++total_intersections;
      ++total_insertion_tests;
      // Offsetting the Word to pseudo-random positions in increasing distances
      // around their desired position
      var world_footprint = sub2(n.max, n.min);
      var mf = Math.min(world_footprint[0], world_footprint[1]);
      var tid = i / MAX_INSERTION_TESTS * 100;
      n.offset = [
        Math.sin(1.8 * 2 * Math.sqrt(tid) * mf) * tid * mf * 0.0126,
        Math.cos(1.8 * 2 * Math.sqrt(tid) * mf) * tid * mf * 0.0126
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
    n.failedInserting = false;
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

    total_insertion_tests = 0;
    total_objects = 0;

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
            if (!n.hidden) {
              failedInsertions.push(n);
            }
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
          if (!n.hidden) {
            //if should be visible...
            failedInsertions.push(n);
          }
        }
      );
    }

    if (failedInsertions.length) {
      for (var n of failedInsertions) {
        //wordset.debugPoint(n._pos);
        n.shown = false;
        n.failedInserting = true;
      }

      vm.error.set(
        " " + failedInsertions.length,
        "Not enough space to show all the lexical items (zoom in to solve). The following lexical item(s) is/are missing:  " +
        failedInsertions.map((n) => n.label).join(", ")
      );
    }

    wordset.sorted_groups = sorted_groups;
  }
  //console.log("tests: "+total_insertion_tests);
}







function checkOverlapObjectsIn(
  Objects,
  accGrid,
  failedInserting
) {
  for (var n of Objects) {
    var intersection = false;
    accGrid.forEachIn(n.bounds, F => {
      for (var m of F) {
        if (intersectObjects(m, n)) {
          accGrid.abort = true;
          intersection = true;
          return;
        }
      }
    });
    if (intersection) {
      if (failedInserting) failedInserting(n);
    } else {
      accGrid.forEachIn(n.bounds, F => {
        F.push(n);
      });
    }
  }
}

function insertion_order(a, b) {
  if (a.hidden && !b.hidden) return 1;
  if (!a.hidden && b.hidden) return -1;
  return b.normalized_size - a.normalized_size;
}


function layoutWordcloudFormGroupsHideOverlap(wordset) {

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
    n.failedInserting = false;
  }

  var failedInsertions = [];

  hierarchically_insert_groups(all_nodes, wordset);
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



  function hierarchically_insert_groups(all_nodes, vm) {
    if (!all_nodes.length) return;
    var min = inf2();
    var max = negInf2();
    for (var n of all_nodes) {
      min = min2(min, n.computed_position);
      max = max2(max, n.computed_position);
    }
    var accGrid = new GridAccelerationStructure(all_nodes.length, { min, max });
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

        var groupGrid = new GridAccelerationStructure(G.uniqueItems.size, { min: gmin, max: gmax });

        checkOverlapObjectsIn(
          itemsToInsert,
          groupGrid,
          n => {
            if (!n.hidden) {
              failedInsertions.push(n);
            }
          }
        );

        gmin = G._min;
        gmax = G._max;

        function margin(pos) {
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

      checkOverlapObjectsIn([G], accGrid);

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
      checkOverlapObjectsIn(
        free_nodes,
        accGrid,
        n => {
          //failed Insertion
          if (!n.hidden) {
            //if should be visible...
            failedInsertions.push(n);
          }
        }
      );
    }

    if (failedInsertions.length) {
      for (var n of failedInsertions) {
        //wordset.debugPoint(n._pos);
        n.shown = false;
        n.failedInserting = true;
      }

      vm.error.set(
        " " + failedInsertions.length,
        "Not enough space to show all the lexical items (zoom in to solve). The following lexical item(s) is/are missing:  " +
        failedInsertions.map((n) => n.label).join(", ")
      );
    }

    wordset.sorted_groups = sorted_groups;
  }
  //console.log("tests: "+total_insertion_tests);
}



class Multigroup {
  constructor(groups, id_string, vm){
    this.window = vm;
    this.nodes = [];
    this.groups = groups;
    this.id = id_string;
    this._min = [0,0];
    this._max = [0,0];
    this._pos = [0,0];
  }
  get pos(){return this._pos;}
  set pos(v){return this._pos = v;}
  get color(){ return [0,1,0];}
  get linewidth(){ return 0.2;}
  get _selected(){ return false; }
  get label(){ return "label"; }
  get min(){ return add2(this._pos,this._min); }
  get max(){ return add2(this._pos,this._max); }
  set min(m){ return this._min = sub2(m,this._pos); }
  set max(m){ return this._max = sub2(m,this._pos); }
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

  redraw() {
    if (!this.visual_representation) return;
    this.window.canvas.remove(this.visual_representation.path);
    this.window.canvas.remove(this.visual_representation.text);
    this.draw();
  }
  draw() {
    this.visual_representation = this.window.canvas.debugConvex(
      this.bounds.convex_hull,
      this.linewidth * (this._selected ? 3 : 1),
      this.linewidth,
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


function layoutWordcloudFormGroups2ResolveOverlap(vm) {
  // Profiling
  var starttime = Date.now();
  var total_Tests = 0;
  var total_intersections = 0;

  vm.error.clear();
  vm.group_map = {};
  if(!vm.multigroups) vm.multigroups = new Map();

  var all_nodes = [];
  for (var [_, n] of vm.Map.entries()) {
    n.offset = [0, 0];
    n._pos = n.computed_position;
    n._pos = max2(n._pos, vm.min);
    n._pos = min2(n._pos, vm.max);
    n.layout_position = n._pos;
    all_nodes.push(n);
    n.shown = !n.hidden;
    n.failedInserting = false;
  }

  var failedInsertions = [];
  function nodeInsertionFailed(n) {
    if (!n.hidden) {
      failedInsertions.push(n);
    }
  }

  if (!all_nodes.length) return;
  var min = inf2();
  var max = negInf2();
  for (var n of all_nodes) {
    min = min2(min, n.computed_position);
    max = max2(max, n.computed_position);
  }

  total_insertion_tests = 0;
  total_objects = 0;

  var accGrid = new GridAccelerationStructure(all_nodes.length, {
    min,
    max
  });
  vm.total_acceleration_grid = accGrid;

  var nodes_by_groups = new Map();
  for (var n of all_nodes) {
    var Gs = Array.from(n.groups);
    var GIDs = Gs.map((g) => g.id);
    var groupID = "#" + GIDs.sort().join("-");
    if (!nodes_by_groups.has(groupID)){
      if( vm.multigroups.has(groupID) ){
        var mg = vm.multigroups.get(groupID);
        mg.nodes = []; //reset
        nodes_by_groups.set(groupID, mg);
      }else{
        nodes_by_groups.set(groupID, new Multigroup(Gs,groupID,vm) );
      }
    }
    nodes_by_groups.get(groupID).nodes.push(n);
  }

  var free_nodes = nodes_by_groups.get("#").nodes;
  nodes_by_groups.delete("#");
  free_nodes.sort(insertion_order);
  vm.multigroups = nodes_by_groups;

  var mixgroups = Array.from(nodes_by_groups.values());
  for (var g of mixgroups) {
    g.nodes.sort(insertion_order);
    g.accumulated_size = 0;
    for (var n of g.nodes) g.accumulated_size += Math.max(0, n.normalized_size);
  }
  mixgroups.sort((a, b) => b.accumulated_size - a.accumulated_size);


  for (var g of mixgroups) {
    var center = [0, 0];
    for (var n of g.nodes) center = add2(center, n.computed_position);
    g.center = center = scale2(center, 1 / g.nodes.length);

    var gmin = inf2();
    var gmax = negInf2();

    if (!vm.options.show_lexical_items_of_group) {
      for (var n of g.nodes) n.shown = false;
      g.min = sub2(center,scale2(g.nodes[0].WH,0.5));
      g.max = add2(center,scale2(g.nodes[0].WH,0.5)); ///TODO:: some sensible bounds
    } else {
      for (var n of g.nodes) {
        n.layout_position = scale2(
          sub2(n.computed_position, center),
          n.user_defined_position ? 1 : vm.options.relocation_by_group
        );
        gmin = min2(gmin, n.layout_position);
        gmax = max2(gmax, n.layout_position);
      }

      iterativelyInsertObjectsTo(
        g.nodes,
        new GridAccelerationStructure(g.nodes.length, { min: gmin, max: gmax }),
        undefined,
        undefined,
        nodeInsertionFailed
      );

      gmin = [0, 0];
      gmax = [0, 0];
      function margin(pos) {
        gmin = min2(gmin, pos);
        gmax = max2(gmax, pos);
        return pos;
      }
      var PathPoints = [];
      for (var n of g.nodes) {
        //collect all AABB edges
        PathPoints.push(
          margin(n.bounds.min),
          margin(n.bounds.max),
          margin([n.bounds.max[0], n.bounds.min[1]]),
          margin([n.bounds.min[0], n.bounds.max[1]])
        );
      }
      g.min = gmin;
      g.max = gmax;
      g.border_path = convexHull(PathPoints);
    }
    g._pos = g.pos = g.layout_position = g.computed_position = g.center;


    //border path should be ccw (when bottom-right == pos ydir, pos xdir)
    iterativelyInsertObjectsTo([g], accGrid);

    for (var n of g.nodes) {
      // reposition items according to Group position
      n._pos = add2(n._pos, g._pos);
    }
  }

  iterativelyInsertObjectsTo(
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
    nodeInsertionFailed
  );

  if (failedInsertions.length) {
    for (var n of failedInsertions) {
      n.shown = false;
      n.failedInserting = true;
    }
    vm.error.set(
      " " + failedInsertions.length,
      "Not enough space to show all the lexical items (zoom in to solve). The following lexical item(s) is/are missing:  " +
      failedInsertions.map((n) => n.label).join(", ")
    );
  }

  vm.screenBorder = [0, 0];
  for (var n of all_nodes) vm.screenBorder = max2(n.WH, vm.screenBorder);
  //finalize position
  for (var n of all_nodes) n.pos = n._pos;

  for(var g of mixgroups){
    g.draw();
  }

}













export {
  iterativelyInsertObjectsTo,
  layoutWordcloudFormGroupsResolveOverlap,
  layoutWordcloudFormGroups2ResolveOverlap,
  layoutWordcloudFormGroupsHideOverlap
}