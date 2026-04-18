(function () {
  var SNAPSHOT_POLL_MS = 60000;
  var NOW_PLAYING_POLL_MS = 5000;
  var API_BASE = "";

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function startOfDay(d) {
    var x = new Date(d);
    x.setHours(0, 0, 0, 0);
    return x;
  }

  function addDays(d, n) {
    var x = new Date(d);
    x.setDate(x.getDate() + n);
    return x;
  }

  function sameDay(a, b) {
    return (
      a.getFullYear() === b.getFullYear() &&
      a.getMonth() === b.getMonth() &&
      a.getDate() === b.getDate()
    );
  }

  function formatVideoAgo(video) {
    if (!video) return "—";
    if (video.hoursAgo != null && !isNaN(Number(video.hoursAgo))) {
      var h = Math.floor(Number(video.hoursAgo));
      if (h <= 0) return "Just now";
      if (h === 1) return "1 hour ago";
      return h + " hours ago";
    }
    if (video.publishedAt) {
      var t = new Date(video.publishedAt).getTime();
      if (isNaN(t)) return "—";
      var hrs = (Date.now() - t) / 3600000;
      if (hrs < 1) return "Just now";
      var hh = Math.floor(hrs);
      if (hh === 1) return "1 hour ago";
      if (hh < 24) return hh + " hours ago";
      var d = Math.floor(hh / 24);
      if (d === 1) return "1 day ago";
      return d + " days ago";
    }
    return "—";
  }

  function tickClock() {
    var now = new Date();
    var h24 = now.getHours();
    var m = now.getMinutes();
    var h12 = h24 % 12;
    if (h12 === 0) h12 = 12;
    var ampm = h24 < 12 ? "AM" : "PM";
    var el = document.getElementById("clock-time");
    if (el) {
      el.innerHTML =
        '<span class="h">' +
        h12 +
        '</span><span class="sep">:</span><span class="m">' +
        pad(m) +
        '</span><span class="ampm">' +
        ampm +
        "</span>";
    }
    var dateEl = document.getElementById("clock-date");
    if (dateEl) {
      dateEl.textContent = now.toLocaleDateString(undefined, {
        weekday: "long",
        month: "short",
        day: "numeric",
      });
    }
  }

  function renderHourly(container, slots) {
    if (!container || !window.svgUseIcon || !window.weatherSymbolId) return;
    container.innerHTML = "";
    if (!Array.isArray(slots) || slots.length === 0) {
      var empty = document.createElement("p");
      empty.className = "weather-hourly__empty";
      empty.setAttribute("role", "status");
      empty.textContent =
        "Nothing hourly to show for the rest of today yet. Ask a grown-up to sync the mirror app if this doesn’t fill in after a little while.";
      container.appendChild(empty);
      return;
    }
    slots.forEach(function (s) {
      var sym = window.weatherSymbolId(s.icon);
      var col = document.createElement("div");
      col.className = "weather-hourly__slot";
      col.setAttribute("role", "listitem");
      col.innerHTML =
        '<span class="weather-hourly__label"></span><div class="weather-hourly__icon"></div><span class="weather-hourly__temp"></span>';
      col.querySelector(".weather-hourly__label").textContent = s.hourLabel;
      col.querySelector(".weather-hourly__temp").textContent =
        s.tempF != null && s.tempF !== "" ? s.tempF + "°" : "—";
      col.querySelector(".weather-hourly__icon").appendChild(
        window.svgUseIcon(sym, s.condition || s.icon || s.hourLabel)
      );
      container.appendChild(col);
    });
  }

  function eventDateForOffset(todayStart, offset) {
    return startOfDay(addDays(todayStart, offset));
  }

  function renderCalendarWeek(container, cal) {
    if (!container || !cal || !cal.events) return;
    var now = new Date();
    var today0 = startOfDay(now);
    container.innerHTML = "";

    var byDay = {};
    cal.events.forEach(function (ev) {
      var off = ev.offsetFromToday != null ? ev.offsetFromToday : 0;
      var d = eventDateForOffset(today0, off);
      var key = d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
      if (!byDay[key]) byDay[key] = [];
      byDay[key].push(ev);
    });

    for (var i = 0; i < 5; i++) {
      var colDate = addDays(today0, i);
      var key =
        colDate.getFullYear() + "-" + pad(colDate.getMonth() + 1) + "-" + pad(colDate.getDate());
      var isToday = sameDay(colDate, now);
      var dayEvents = byDay[key] || [];

      var col = document.createElement("div");
      col.className = "calendar-weekday" + (isToday ? " calendar-weekday--today" : "");
      col.setAttribute("role", "listitem");

      var head = document.createElement("div");
      head.className = "calendar-weekday__head";
      head.innerHTML =
        '<span class="calendar-weekday__dow"></span><span class="calendar-weekday__date"></span>';
      head.querySelector(".calendar-weekday__dow").textContent = colDate.toLocaleDateString(
        undefined,
        { weekday: "short" }
      );
      head.querySelector(".calendar-weekday__date").textContent = String(colDate.getDate());

      var ul = document.createElement("ul");
      ul.className = "calendar-weekday__events";
      if (dayEvents.length === 0) {
        var empty = document.createElement("li");
        empty.className = "calendar-weekday__event";
        empty.style.color = "var(--mm-text-muted)";
        empty.style.fontSize = "18px";
        empty.textContent = "—";
        ul.appendChild(empty);
      } else {
        dayEvents.forEach(function (ev) {
          var li = document.createElement("li");
          li.className = "calendar-weekday__event";
          li.innerHTML =
            '<span class="calendar-weekday__event-time"></span><span class="calendar-weekday__event-title"></span>';
          li.querySelector(".calendar-weekday__event-time").textContent = ev.time || "";
          li.querySelector(".calendar-weekday__event-title").textContent = ev.title || "";
          ul.appendChild(li);
        });
      }

      col.appendChild(head);
      col.appendChild(ul);
      container.appendChild(col);
    }
  }

  function renderTodos(container, todo) {
    if (!container || !todo || !Array.isArray(todo.items)) return;
    container.innerHTML = "";
    if (todo.items.length === 0) {
      var li = document.createElement("li");
      li.className = "todo-item todo-item--empty";
      li.setAttribute("role", "status");
      li.textContent =
        "Nothing on the list right now — you’re all set. New tasks can be added in Home Assistant whenever you need them.";
      container.appendChild(li);
      return;
    }
    todo.items.forEach(function (item) {
      var row = document.createElement("li");
      row.className = "todo-item" + (item.done ? " todo-item--done" : "");
      row.innerHTML =
        '<span class="todo-item__mark" aria-hidden="true"></span><span class="todo-item__body"></span>';
      row.querySelector(".todo-item__body").textContent = item.text;
      container.appendChild(row);
    });
  }

  function setVideoRadarVisible(show) {
    var el = document.getElementById("module-video-radar");
    if (!el) return;
    el.hidden = !show;
    el.style.display = show ? "" : "none";
  }

  function renderVideoRadar(container, data) {
    if (!container) return;
    container.innerHTML = "";
    var list = data && data.videos ? data.videos : [];
    if (list.length === 0) {
      setVideoRadarVisible(false);
      return;
    }
    setVideoRadarVisible(true);
    list.slice(0, 3).forEach(function (v) {
      var card = document.createElement("article");
      card.className = "video-radar__card";
      card.setAttribute("role", "listitem");
      card.innerHTML =
        '<p class="video-radar__title"></p>' +
        '<p class="video-radar__creator"></p>' +
        '<p class="video-radar__ago"></p>';
      card.querySelector(".video-radar__title").textContent = v.title || "—";
      card.querySelector(".video-radar__creator").textContent = v.creator || "—";
      card.querySelector(".video-radar__ago").textContent = formatVideoAgo(v);
      container.appendChild(card);
    });
  }

  function setNowPlayingArt(url, titleForAlt) {
    var imgEl = document.getElementById("now-playing-art");
    var phEl = document.getElementById("now-playing-art-placeholder");
    if (!imgEl || !phEl) return;
    imgEl.onload = null;
    imgEl.onerror = null;
    var u = url && String(url).trim();
    if (u) {
      imgEl.hidden = true;
      phEl.hidden = false;
      imgEl.alt = titleForAlt ? String(titleForAlt).slice(0, 120) : "Album art";
      imgEl.onerror = function () {
        imgEl.onload = null;
        imgEl.onerror = null;
        imgEl.removeAttribute("src");
        imgEl.alt = "";
        imgEl.hidden = true;
        phEl.hidden = false;
      };
      imgEl.onload = function () {
        imgEl.onload = null;
        imgEl.onerror = null;
        imgEl.hidden = false;
        phEl.hidden = true;
      };
      imgEl.src = u;
    } else {
      imgEl.removeAttribute("src");
      imgEl.alt = "";
      imgEl.hidden = true;
      phEl.hidden = false;
    }
  }

  function hydrateNextUp(next) {
    var aEl = document.getElementById("now-playing-next-artist");
    var tEl = document.getElementById("now-playing-next-title");
    if (!aEl || !tEl) return;
    if (!next || (!next.title && !next.artist)) {
      aEl.textContent = "—";
      tEl.textContent = "";
      return;
    }
    aEl.textContent = next.artist || "—";
    tEl.textContent = next.title || "";
  }

  function hydrateNowPlaying(np) {
    var titleEl = document.getElementById("now-playing-title");
    var artistEl = document.getElementById("now-playing-artist");
    if (!titleEl) return;
    if (!np || np.isIdle || (!np.title && !np.artist)) {
      hydrateNextUp(null);
      titleEl.textContent = "Nothing playing";
      if (artistEl) artistEl.textContent = "";
      setNowPlayingArt("", "");
      return;
    }
    hydrateNextUp(np.nextUp || null);
    titleEl.textContent = np.title || "—";
    if (artistEl) artistEl.textContent = np.artist || "";
    setNowPlayingArt(np.artworkUrl, np.title);
  }

  function applyPayload(demo) {
    if (!demo) return;

    hydrateNowPlaying(demo.nowPlaying);

    if (demo.weather) {
      var t = demo.weather.today;
      if (t) {
        var ce = document.getElementById("weather-condition");
        var me = document.getElementById("weather-metrics");
        var iconHost = document.getElementById("weather-today-icon");
        if (ce) ce.textContent = t.condition || "—";
        var tempEl = document.getElementById("weather-temp");
        if (tempEl) tempEl.textContent = t.tempF != null ? t.tempF + "°" : "—";
        if (me) {
          var parts = [];
          if (t.feelsLikeF != null && t.feelsLikeF !== t.tempF) parts.push("Feels like " + t.feelsLikeF + "°");
          if (t.precipChance != null) parts.push(t.precipChance + "% precip");
          me.textContent = parts.join(" · ");
        }
        if (iconHost && window.svgUseIcon && window.weatherSymbolId) {
          iconHost.innerHTML = "";
          iconHost.appendChild(
            window.svgUseIcon(window.weatherSymbolId(t.icon), t.condition)
          );
        }
      }
      renderHourly(document.getElementById("weather-hourly"), demo.weather.hourlyToday);
    }

    renderCalendarWeek(document.getElementById("calendar-week"), demo.calendar);
    renderTodos(document.getElementById("todo-list"), demo.todos);
    renderVideoRadar(document.getElementById("video-radar"), demo.videoRadar);
  }

  function fetchSnapshot() {
    var url = API_BASE + "/api/snapshot";
    return fetch(url, { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.json();
    });
  }

  function hydrateFromDemo() {
    if (window.MIRROR_DEMO) applyPayload(window.MIRROR_DEMO);
  }

  function start() {
    if (window.MIRROR_DEMO) applyPayload(window.MIRROR_DEMO);
    tickClock();
    setInterval(tickClock, 1000);

    fetchSnapshot()
      .then(function (data) {
        applyPayload(data);
        setInterval(function () {
          fetchSnapshot().then(applyPayload).catch(function () {});
        }, SNAPSHOT_POLL_MS);
        setInterval(function () {
          fetch(API_BASE + "/api/now-playing", { credentials: "same-origin" })
            .then(function (r) { return r.ok ? r.json() : null; })
            .then(function (np) { if (np) hydrateNowPlaying(np); })
            .catch(function () {});
        }, NOW_PLAYING_POLL_MS);
      })
      .catch(function () {
        hydrateFromDemo();
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
