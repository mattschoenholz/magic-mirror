/**
 * Maps HA-style condition keys → SVG symbol id (see index.html <defs>).
 * Icons use CSS variables (--wx-*) for multi-color symbols.
 */
window.WEATHER_ICON_MAP = {
  clear: "wx-clear",
  sunny: "wx-clear",
  "partly-cloudy": "wx-partly-cloudy",
  cloudy: "wx-cloudy",
  overcast: "wx-cloudy",
  rain: "wx-rain",
  drizzle: "wx-rain",
  snow: "wx-snow",
  thunderstorm: "wx-thunderstorm",
  fog: "wx-fog",
  mist: "wx-fog",
  wind: "wx-wind",
};

window.weatherSymbolId = function weatherSymbolId(key) {
  var k = key && String(key).toLowerCase().replace(/\s+/g, "-");
  var id = window.WEATHER_ICON_MAP[key] || window.WEATHER_ICON_MAP[k];
  return id || "wx-default";
};

/** SVG <use> with classes for colored wx sprites */
window.svgUseIcon = function svgUseIcon(symbolId, title) {
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 64 64");
  svg.setAttribute("class", "wx-svg wx-svg--" + symbolId);
  svg.setAttribute("role", title ? "img" : "presentation");
  if (title) {
    var t = document.createElementNS("http://www.w3.org/2000/svg", "title");
    t.textContent = title;
    svg.appendChild(t);
  }
  var use = document.createElementNS("http://www.w3.org/2000/svg", "use");
  use.setAttribute("href", "#" + symbolId);
  svg.appendChild(use);
  return svg;
};
