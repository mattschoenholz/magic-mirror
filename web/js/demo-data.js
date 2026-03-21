/**
 * Demo payload — shape for HA (M-002, M-005, M-006, media player, video feed).
 */
window.MIRROR_DEMO = {
  nowPlaying: {
    title: "Satellite",
    artist: "Harry Styles",
    artworkUrl: "",
    isIdle: false,
    /** Queue: artist on first line, title below (no art). */
    nextUp: {
      artist: "Taylor Swift",
      title: "The Bolter",
    },
  },

  weather: {
    today: {
      condition: "Partly cloudy",
      feelsLikeF: 74,
      precipChance: 15,
      icon: "partly-cloudy",
    },
    hourlyToday: [
      { hourLabel: "Now", tempF: 72, icon: "partly-cloudy" },
      { hourLabel: "2 PM", tempF: 73, icon: "partly-cloudy" },
      { hourLabel: "4 PM", tempF: 71, icon: "cloudy" },
      { hourLabel: "6 PM", tempF: 69, icon: "cloudy" },
      { hourLabel: "8 PM", tempF: 66, icon: "rain" },
      { hourLabel: "10 PM", tempF: 64, icon: "rain" },
    ],
  },

  /**
   * Events: offset from **today** (0 = today). UI shows **today + next 4 days** (5 columns).
   */
  calendar: {
    events: [
      { offsetFromToday: 0, time: "3:00 PM", title: "Science fair setup" },
      { offsetFromToday: 1, time: "7:00 PM", title: "Band practice" },
      { offsetFromToday: 2, time: "All day", title: "Field trip" },
      { offsetFromToday: 3, time: "9:00 AM", title: "Dentist" },
      { offsetFromToday: 4, time: "2:00 PM", title: "Progress reports" },
    ],
  },

  /** 2×3 grid: six items read left→right, top→bottom. */
  todos: {
    items: [
      { text: "Finish math worksheet", done: false },
      { text: "Pack gym clothes", done: false },
      { text: "Reading 20 min", done: true },
      { text: "Charge iPad", done: false },
      { text: "Trash night", done: false },
      { text: "Water plants", done: false },
    ],
  },

  /** Up to 3 recent subscription uploads (~24h). Use `publishedAt` ISO from API or `hoursAgo` in demos. */
  videoRadar: {
    videos: [
      {
        title: "I tried living off-grid for a week",
        creator: "Outdoor Chris",
        hoursAgo: 2,
      },
      {
        title: "Home Assistant 2025.3 — what’s new",
        creator: "Everything Smart Home",
        hoursAgo: 5,
      },
      {
        title: "Sunday jazz mix · live set",
        creator: "NPR Music",
        hoursAgo: 18,
      },
    ],
  },
};
