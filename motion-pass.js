/* Section handoff and interior film playback.
   Opacity only. Frames keep the transforms the act player already sets. */
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  function still() {
    return reduce.matches ||
      root.getAttribute("data-journey-motion") === "still" ||
      root.getAttribute("data-journey-tier") === "still";
  }

  var seams = [];

  function veil(parent, kind) {
    var el = document.createElement("div");
    el.className = "act-handoff act-handoff--" + kind;
    el.setAttribute("aria-hidden", "true");
    parent.appendChild(el);
    return el;
  }

  if (!still()) {
    document.querySelectorAll(".act:not(.act--hero) .act-stage").forEach(function (stage) {
      var act = stage.closest(".act");
      if (!act) return;
      seams.push({
        act: act,
        enter: veil(stage, "enter"),
        exit: veil(stage, "exit"),
        eo: 0,
        xo: 0
      });
    });
  }

  var films = Array.prototype.slice.call(document.querySelectorAll("video.job-film"));
  films.forEach(function (video) {
    var mark = function () {
      if (video.readyState >= 2) video.setAttribute("data-ready", "");
    };
    video.addEventListener("loadeddata", mark);
    video.addEventListener("playing", mark);
  });

  function syncFilms() {
    var vh = window.innerHeight || 1;
    films.forEach(function (video) {
      if (still()) {
        if (!video.paused) video.pause();
        return;
      }
      var r = video.getBoundingClientRect();
      var on = r.bottom > vh * 0.12 && r.top < vh * 0.88 && r.width > 0;
      if (!on) {
        if (!video.paused) video.pause();
        return;
      }
      if (video.preload === "none") video.preload = "auto";
      if (video.paused) {
        var pending = video.play();
        if (pending && pending.catch) pending.catch(function () {});
      }
    });
  }

  var running = false;
  function frame() {
    var vh = window.innerHeight || 1;
    var dirty = false;
    seams.forEach(function (n) {
      var r = n.act.getBoundingClientRect();
      var enterT = 0;
      var exitT = 0;
      if (r.bottom > 0 && r.top < vh) {
        var p = (r.top - vh * 0.06) / (vh * 0.58);
        enterT = p < 0 ? 0 : p > 1 ? 1 : p;
        var leave = (vh * 0.92 - r.bottom) / (vh * 0.38);
        exitT = leave < 0 ? 0 : leave > 1 ? 1 : leave;
      }
      n.eo += (enterT - n.eo) * 0.2;
      n.xo += (exitT - n.xo) * 0.2;
      if (Math.abs(enterT - n.eo) > 0.006 || Math.abs(exitT - n.xo) > 0.006) dirty = true;
      n.enter.style.opacity = n.eo < 0.012 ? "0" : n.eo.toFixed(3);
      n.exit.style.opacity = n.xo < 0.012 ? "0" : n.xo.toFixed(3);
      n.act.style.setProperty("--handoff", n.eo.toFixed(3));
    });
    if (dirty) requestAnimationFrame(frame);
    else running = false;
  }

  function kick() {
    syncFilms();
    if (still()) {
      seams.forEach(function (n) {
        n.eo = 0;
        n.xo = 0;
        n.enter.style.opacity = "0";
        n.exit.style.opacity = "0";
        n.act.style.setProperty("--handoff", "0");
      });
      return;
    }
    if (!seams.length) return;
    if (!running) {
      running = true;
      requestAnimationFrame(frame);
    }
  }

  kick();
  window.addEventListener("scroll", kick, { passive: true });
  window.addEventListener("resize", kick, { passive: true });
  reduce.addEventListener("change", kick);
  new MutationObserver(kick).observe(root, {
    attributes: true,
    attributeFilter: ["data-journey-tier", "data-journey-motion"]
  });
})();
