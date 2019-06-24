function hex_color_from_array(c) {
  function hex2Digits(v) {
    return "00"
      .concat(Math.floor(Math.min(255, Math.max(0, v * 255))).toString(16))
      .slice(-2);
  }
  return (
    "#" +
    hex2Digits(c[0]) +
    hex2Digits(c[1]) +
    hex2Digits(c[2]) +
    hex2Digits(c[3] ? c[3] : 1)
  );
}

function oneOf(A) {
  return A[Math.floor(Math.min(A.length - 1, A.length * Math.random()))];
}

var pseudorandomIndex = 0;
function pseudorandom(i) {
  var index = i ? i : (pseudorandomIndex++);
  var base = 3;
  var res = 0;
  var f = 1;
  while (index > 0) {
    f = f / base;
    res = res + f * (index % base);
    index = Math.floor(index / base);
  }
  return res;
}


var requestedDomOps = false;
var domOps = [];
var domOpsEL = [];
function domApplyAll(){
  requestedDomOps = false;
  for(var x of domOps){
    x.el.style[x.key] = x.value;
  }
  for(var x of domOpsEL){
    x.el[x.key] = x.value;
  }
  domOps = [];
  domOpsEL = [];
}
function domSet(el,key,value){
  domOps.push({el,key,value});
  if(!requestedDomOps){
    requestAnimationFrame( domApplyAll);
    requestedDomOps=true;
  }
}
function domSetEL(el,key,value){
  domOpsEL.push({el,key,value});
  if(!requestedDomOps){
    requestAnimationFrame( domApplyAll);
    requestedDomOps=true;
  }
}


function random_color(pseudo) {
  if (typeof pseudo === 'boolean') return hsv_to_rgb(360 * pseudorandom(), 0.8, 0.5);
  if (typeof pseudo === 'number') return hsv_to_rgb(360 * pseudorandom(pseudo), 0.8, 0.5);
  return hsv_to_rgb(
    220 * Math.random(),
    0.8 + 0.1 * Math.random(),
    0.5 + 0.1 * Math.random()
  );
}

function hsv_to_rgb(h, s, v) {
  if (s === 0) {
    return [v, v, v]; // grey
  }
  var i = Math.floor(h / 60);
  var f = h / 60 - i;
  var p = v * (1 - s);
  var q = v * (1 - s * f);
  var t = v * (1 - s * (1 - f));
  switch (i % 6) {
    case 0:
      return [v, t, p];
    case 1:
      return [q, v, p];
    case 2:
      return [p, v, t];
    case 3:
      return [p, q, v];
    case 4:
      return [t, p, v];
    case 5:
      return [v, p, q];
  }
  return [v, v, v];
}

function fwdEvent(target, element, action) {
  element.addEventListener(
    action,
    ((target, action) => event => {
      target["on" + action](event);
    })(target, action)
  );
}

export {
  hex_color_from_array,
  oneOf,
  pseudorandom,
  random_color,
  hsv_to_rgb,
  fwdEvent,
  domSet,
  domSetEL,
};
