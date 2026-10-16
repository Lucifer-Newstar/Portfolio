/* Sets the theme before first paint (no flash). Stored choice wins, else the OS preference. */
(function () {
  var d = document.documentElement, t = null;
  try { t = localStorage.getItem("theme"); } catch (e) {}
  if (t !== "light" && t !== "dark") t = (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) ? "light" : "dark";
  d.setAttribute("data-theme", t);
  var m = document.querySelector('meta[name="theme-color"]'); if (m) m.setAttribute("content", t === "light" ? "#f3f5f8" : "#06080c");
})();
