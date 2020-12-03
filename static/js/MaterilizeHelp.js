document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll(".tap-target");
  M.TapTarget.init(elems);
});

function next(n) {
  var inst;

  // Get each of the elements
  var elems = document.querySelectorAll(".tap-target");

  var current = n;
  var prev = --n;

  // If a previous target is open, close it.
  if(prev >= 0) {
    inst = M.TapTarget.getInstance(elems[prev]);
    inst.close();
    inst.destroy();
  }

  // Then, open the new target
  inst = M.TapTarget.getInstance(elems[current]);
  inst.open();
}