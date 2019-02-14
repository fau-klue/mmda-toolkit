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

export {
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
};