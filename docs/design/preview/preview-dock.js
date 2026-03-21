(function () {
  var panel = document.getElementById("exit-panel");
  var btn = document.getElementById("exit-help-btn");
  var galleryLink = document.getElementById("dock-gallery");
  if (galleryLink) {
    var onViewer = /viewer\.html/i.test(location.pathname);
    galleryLink.hidden = !onViewer;
    galleryLink.setAttribute("aria-hidden", onViewer ? "false" : "true");
  }
  if (btn && panel) {
    btn.addEventListener("click", function () {
      var open = panel.hasAttribute("hidden");
      if (open) {
        panel.removeAttribute("hidden");
        btn.setAttribute("aria-expanded", "true");
      } else {
        panel.setAttribute("hidden", "");
        btn.setAttribute("aria-expanded", "false");
      }
    });
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", "exit-panel");
  }
})();
