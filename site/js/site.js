// Search and sort the list of every service. Without script the full A–Z list still shows.
(function () {
  "use strict";
  var list = document.querySelector('[data-role="list"]');
  if (!list) return;
  var q = document.querySelector('[data-role="q"]'), count = document.querySelector('[data-role="count"]');
  var items = Array.prototype.slice.call(list.children), total = items.length;
  function filter() {
    var t = q.value.trim().toLowerCase(), n = 0;
    items.forEach(function (li) { var hit = !t || li.dataset.n.indexOf(t) >= 0; li.hidden = !hit; if (hit) n++; });
    count.textContent = t ? n + " of " + total + " services match “" + q.value.trim() + "”" : total + " services";
  }
  q.addEventListener("input", filter);
  document.querySelectorAll("[data-sort]").forEach(function (b) {
    b.addEventListener("click", function () {
      var by = b.dataset.sort;
      document.querySelectorAll("[data-sort]").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      items.sort(function (a, c) { return by === "ops" ? (+c.dataset.ops - +a.dataset.ops) : (a.dataset.n.split(" ").pop() < c.dataset.n.split(" ").pop() ? -1 : 1); });
      items.forEach(function (li) { list.appendChild(li); });
    });
  });
})();
