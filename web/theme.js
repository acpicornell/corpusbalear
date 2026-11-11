/* Light/dark theme for the portal, as on the sibling sites (cronicon,
   llinatges-actuals).

   Loaded synchronously in <head>: the stored choice is applied before the first
   paint, or the page would flash in the system theme before switching. The CSP
   is `script-src 'self'`, so this is a file and not an inline block.

   data-theme="light"|"dark" on <html>; absent means "follow the system"
   (prefers-color-scheme). The page has no other script, so the button that
   flips it is wired here too, once the document has been parsed. */
(function () {
  "use strict";
  var root = document.documentElement;
  var KEY = "corpusbalear-theme";
  try {
    var stored = localStorage.getItem(KEY);
    if (stored === "light" || stored === "dark") root.setAttribute("data-theme", stored);
  } catch (e) { /* storage blocked: follow the system */ }

  function wire() {
    var button = document.getElementById("theme");
    if (!button) return;
    button.addEventListener("click", function () {
      var showing = root.getAttribute("data-theme") ||
        (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches
          ? "dark" : "light");
      var next = showing === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* not remembered */ }
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
