// Search and sort the list of every service. Without script the full A–Z list still shows.
(function () {
  "use strict";
  var wn = document.querySelector('[data-role="wname"]');
  if (wn) document.querySelectorAll(".wall [data-name]").forEach(function (c) {
    // A tap or hover names the square; for a basic or Shadw the name line becomes the (44 px) link.
    function show() {
      if (wn.dataset.cur === c.dataset.name) return;
      wn.dataset.cur = c.dataset.name; wn.textContent = c.dataset.name + " ";
      if (c.dataset.open) { var a = document.createElement("a"); a.href = c.getAttribute("href"); a.textContent = c.dataset.open; wn.appendChild(a); }
    }
    c.addEventListener("pointerenter", function (ev) { if (ev.pointerType === "mouse") show(); });
    c.addEventListener("focus", function () { if (c.matches(":focus-visible")) show(); });
    c.addEventListener("click", function (ev) { if (wn.dataset.cur !== c.dataset.name) { ev.preventDefault(); show(); } });
  });
  var list = document.querySelector('[data-role="list"]');
  if (!list) return;
  var q = document.querySelector('[data-role="q"]'), count = document.querySelector('[data-role="count"]');
  var items = Array.prototype.slice.call(list.children), total = items.length;
  function filter() {
    var t = q.value.trim().toLowerCase(), n = 0;
    items.forEach(function (li) { var hit = !t || li.dataset.n.indexOf(t) >= 0; li.hidden = !hit; if (hit) n++; });
    var basics = items.filter(function (li) { return t && !li.hidden && li.hasAttribute("data-basic"); });
    (t ? basics.concat(items.filter(function (li) { return basics.indexOf(li) < 0; })) : items).forEach(function (li) { list.appendChild(li); });
    count.textContent = t ? n + " of " + total + " services match “" + q.value.trim() + "”" : total + " services";
  }
  q.addEventListener("input", filter);
  document.querySelectorAll("[data-sort]").forEach(function (b) {
    b.addEventListener("click", function () {
      var by = b.dataset.sort;
      document.querySelectorAll("[data-sort]").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      items.sort(function (a, c) { return by === "ops" ? (+c.dataset.ops - +a.dataset.ops) : (a.dataset.s < c.dataset.s ? -1 : 1); });
      items.forEach(function (li) { list.appendChild(li); });
    });
  });
})();
