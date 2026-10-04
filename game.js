const SECONDS = 40;
const GA_ID = "G-6QHLTKHKL5"; // Google Analytics Measurement ID (G-XXXXXXXXXX); analytics stay off while empty

// Storage helpers that never throw (some private-browsing modes block localStorage).
const load = (key, fallback) => { try { const v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); } catch { return fallback; } };
const save = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} };

// ?internal=1 marks this device as Jack's own so GA filters it out; ?internal=0 clears it. The param is then removed from the URL.
try {
  const url = new URL(location.href);
  const flag = url.searchParams.get("internal");
  if (flag === "1") localStorage.setItem("dd_internal", "1");
  if (flag === "0") localStorage.removeItem("dd_internal");
  if (flag !== null) {
    url.searchParams.delete("internal");
    history.replaceState(null, "", url.pathname + url.search + url.hash);
  }
} catch {}

// Anonymous device id, groundwork for a future optional sign-in. Stays on this device; never sent anywhere.
try { if (!localStorage.getItem("dd_player_id")) localStorage.setItem("dd_player_id", crypto.randomUUID()); } catch {}

// Analytics is best-effort: if it's blocked or fails, the game behaves exactly the same.
try {
  if (GA_ID) {
    const s = document.createElement("script");
    s.async = true;
    s.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.append(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    // No cookies for EU/EEA, UK, and Swiss visitors (they'd need a consent banner); cookieless pings only.
    gtag("consent", "default", {
      analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied",
      region: ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "IS", "LI", "NO", "GB", "CH"],
    });
    gtag("js", new Date());
    gtag("config", GA_ID, load("dd_internal", 0) === 1 ? { traffic_type: "internal" } : {});
  }
} catch {}
const track = (name, params) => {
  try { if (window.gtag) gtag("event", name, { game: dayNumber, ...params }); } catch {}
};

// Everyone plays the same game: the day rolls over at midnight US Eastern time.
const TZ = "America/New_York";
const today = new Date().toLocaleDateString("en-CA", { timeZone: TZ }); // YYYY-MM-DD in Eastern time
const dayNumber = Object.keys(GAMES).indexOf(today) + 1;
const game = GAMES[today];

const screen = document.getElementById("screen");
document.getElementById("meta").textContent = game
  ? `#${dayNumber} · ${new Date(today + "T12:00").toLocaleDateString("en-US", { month: "short", day: "numeric" })}`
  : "";
// "Move my streak" link (#restore=20261004-20.14.0.5.2_...): copies finished days from another device.
// Only fills in days this device hasn't played. Lives in the URL hash, so it never reaches the server.
try {
  const m = location.hash.match(/^#restore=([\d._-]+)$/);
  if (m) {
    for (const part of m[1].split("_")) {
      const [d, y = ""] = part.split("-");
      const date = `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`;
      const yards = y.split(".").map(Number);
      const valid = yards.length === 5 && yards.every((n) => Number.isInteger(n) && n >= 0 && n <= 20);
      if (GAMES[date] && valid && !load(date, []).length) save(date, yards.map((n) => ({ answer: "", yards: n, restored: true })));
    }
    history.replaceState(null, "", location.pathname + location.search);
  }
} catch {}

let results = load(today, []); // one entry per round: { answer, yards }
let timer;

const totalYards = () => results.reduce((sum, r) => sum + r.yards, 0);

// Streak = consecutive Eastern-time days with a finished game on this device. Today's unfinished game doesn't break it.
const finished = (date) => load(date, []).length === 5;
const dayBefore = (date) => {
  const d = new Date(date + "T12:00:00Z");
  d.setUTCDate(d.getUTCDate() - 1);
  return d.toISOString().slice(0, 10);
};
function streaks() {
  let current = 0;
  for (let d = finished(today) ? today : dayBefore(today); finished(d); d = dayBefore(d)) current++;
  let best = 0, run = 0;
  for (const date of Object.keys(GAMES)) best = Math.max(best, (run = finished(date) ? run + 1 : 0)); // game dates are consecutive days
  return { current, best: Math.max(best, current) };
}
const streakLink = () =>
  `${location.origin}/#restore=` +
  Object.keys(GAMES).filter(finished).map((d) => d.replaceAll("-", "") + "-" + load(d, []).map((r) => r.yards).join(".")).join("_");

// Split into lowercase words, ignoring punctuation and suffixes like Jr. or III.
const SUFFIXES = ["jr", "sr", "ii", "iii", "iv"];
const words = (s) => s.toLowerCase().replace(/[.'’-]/g, "").split(/[^a-z0-9]+/).filter((w) => w && !SUFFIXES.includes(w));

// Number of letter edits (add, remove, change, or swap two neighbors) to turn a into b.
function typos(a, b) {
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
  for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++)
    for (let j = 1; j <= b.length; j++) {
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      if (a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
    }
  return d[a.length][b.length];
}

// Each word may be up to ~40% misspelled, so "Toa Tavagoloa" finds "Tua Tagovailoa"
// but "Calvin Johnson" never becomes "Chris Johnson".
const close = (g, n) => g.length === n.length && g.every((w, i) => typos(w, n[i]) <= Math.round((n[i].length - 1) * 0.4));

function findAnswer(guess, answers) {
  const g = words(guess);
  const last = (a) => words(a.name).slice(-1);
  const lastIsUnique = (a) => answers.filter((b) => last(b)[0] === last(a)[0]).length === 1;
  const names = (a) => [...[a.name, ...(a.aliases || [])].map(words), ...(lastIsUnique(a) ? [last(a)] : [])];
  const exact = answers.find((a) => names(a).some((n) => n.join("") === g.join("")));
  if (exact) return exact;
  // known look-alikes (e.g. "North Carolina" for South Carolina) never count as typos
  if (answers.some((a) => (a.not || []).some((n) => words(n).join("") === g.join("")))) return undefined;
  const fuzzy = answers.filter((a) => names(a).some((n) => close(g, n)));
  return fuzzy.length === 1 ? fuzzy[0] : undefined; // ambiguous typos don't count
}

const emoji = (y) => (y === 20 ? "🏈" : y >= 14 ? "🥇" : y >= 8 ? "🥈" : y > 0 ? "🥉" : "❌");
const gainLabel = (y) => (y === 20 ? "Deep cut" : y >= 14 ? "Big gain" : y >= 8 ? "Solid gain" : y > 0 ? "Short gain" : "Delay of game");

function render(html) {
  screen.innerHTML = html;
  const yards = totalYards();
  document.getElementById("yardage").innerHTML = `${yards}<small>YDS</small>`;
  document.getElementById("ball").style.left = `${yards}%`;
  document.getElementById("gain").style.width = `${yards}%`;
  document.getElementById("pips").innerHTML = [0, 1, 2, 3, 4]
    .map((i) => `<span class="${results[i] ? (results[i].yards ? "gain" : "miss") : i === results.length && screen.querySelector("#form") ? "now" : ""}"></span>`)
    .join("");
  tick();
}

// The play clock runs off a saved deadline, so leaving the app or reloading never pauses it.
const deadlineKey = `${today}-deadline`;
const savedDeadline = () => JSON.parse(localStorage.getItem(deadlineKey) || "null");

function startRound() {
  const round = game[results.length];
  const saved = savedDeadline();
  const deadline = saved && saved.play === results.length ? saved.at : Date.now() + SECONDS * 1000;
  localStorage.setItem(deadlineKey, JSON.stringify({ play: results.length, at: deadline }));
  const secondsLeft = () => Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
  let left = secondsLeft();
  render(`
    <div class="card">
      <div class="clockrow">
        <p class="label">Play ${results.length + 1} of 5</p>
        <span class="timer" id="clock">0:${String(left).padStart(2, "0")}</span>
      </div>
      <div class="bar"><div id="bar"></div></div>
      <p class="prompt">${round.prompt}</p>
      <form id="form">
        <input id="guess" autocomplete="off" autocapitalize="words" spellcheck="false" placeholder="Your answer" autofocus>
        <button>Snap it</button>
        <button type="button" id="punt" class="secondary">Punt</button>
      </form>
      <p id="msg" class="muted">Wrong guesses are free. Stuck? Punt to skip ahead.</p>
    </div>`);
  document.getElementById("guess").focus();
  const bar = document.getElementById("bar");
  bar.style.transition = "none";
  bar.style.width = `${(left / SECONDS) * 100}%`;
  setTimeout(() => {
    bar.style.transition = `width ${left}s linear`;
    bar.style.width = "0%";
  }, 50);
  timer = setInterval(() => {
    left = secondsLeft();
    const clock = document.getElementById("clock");
    clock.textContent = `0:${String(left).padStart(2, "0")}`;
    clock.className = `timer ${left <= 5 ? "danger" : left <= 10 ? "warn" : ""}`;
    if (left <= 0) finishRound("");
  }, 1000);
  if (left <= 0) return finishRound(""); // time ran out while away
  document.getElementById("punt").onclick = () => finishRound("", true);
  document.getElementById("form").onsubmit = (e) => {
    e.preventDefault();
    const input = document.getElementById("guess");
    const guess = input.value.trim();
    if (!guess) return;
    if (findAnswer(guess, round.answers)) return finishRound(guess);
    document.getElementById("msg").textContent = `"${guess}" isn't on the board. Keep trying!`;
    input.value = "";
  };
}

function finishRound(guess, punted = false) {
  clearInterval(timer);
  localStorage.removeItem(deadlineKey);
  const match = findAnswer(guess, game[results.length].answers);
  results.push({ answer: match ? match.name : guess, yards: match ? match.yards : 0, ...(punted && { punt: true }) });
  localStorage.setItem(today, JSON.stringify(results));
  track("play_result", { play: results.length, yards: results.at(-1).yards, result: match ? "correct" : punted ? "punt" : "timeout" });
  if (results.length === 5) track("game_complete", { total_yards: totalYards(), streak: streaks().current });
  showReveal();
}

function answerList(round, yours) {
  return `<details><summary>All ${round.answers.length} accepted answers</summary><ul class="answers">${[...round.answers]
    .sort((a, b) => b.yards - a.yards)
    .map((a) => `<li class="${a.name === yours ? "you" : ""}"><span>${a.name}</span><b>${a.yards}</b></li>`)
    .join("")}</ul></details>`;
}

function showReveal() {
  const i = results.length - 1;
  const r = results[i];
  render(`
    <div class="card">
      <p class="label">Play ${i + 1} of 5 · ${r.punt ? "Punt" : gainLabel(r.yards)}</p>
      <div class="result">
        <span class="name">${r.answer || (r.punt ? "Punted" : "Clock ran out")}</span>
        <span class="yds ${r.yards ? "" : "zero"}">${r.yards ? `+${r.yards} YDS` : "NO GAIN"}</span>
      </div>
      ${answerList(game[i], r.answer)}
      <button id="next">${results.length < 5 ? "Next play" : "See final drive"}</button>
    </div>`);
  document.getElementById("next").onclick = results.length < 5 ? startRound : showFinal;
}

function showFinal() {
  const yards = totalYards();
  const streak = streaks();
  const share = `Daily Drive #${dayNumber}\n${yards === 100 ? "🏈 TOUCHDOWN! " : ""}${yards}/100 yards${streak.current >= 3 ? ` · 🔥 ${streak.current}` : ""}\n${results.map((r) => emoji(r.yards)).join("")}\n${(location.host + location.pathname).replace(/\/$/, "")}`;
  const card = (r, i) => `
    <div class="card mini">
      <div class="row"><span class="label">Play ${i + 1}</span><span class="yds">${emoji(r.yards)} +${r.yards}</span></div>
      <p class="prompt">${game[i].prompt}</p>
      <div>${r.answer || `<span class="muted">${r.restored ? "Played on another device" : r.punt ? "Punted" : "Clock ran out"}</span>`}</div>
      ${answerList(game[i], r.answer)}
    </div>`;
  render(`
    <div class="card">
      <p class="label">${yards === 100 ? "Touchdown! Perfect drive" : "Drive complete"}</p>
      <p class="big">${yards}<small> / 100 YDS</small></p>
      <p class="emojis">${results.map((r) => emoji(r.yards)).join("")}</p>
      <p class="streak">🔥 ${streak.current}-day streak${streak.best > streak.current ? ` <span class="muted">· Best: ${streak.best}</span>` : ""}</p>
      <button id="share">Share score</button>
      <p class="muted" style="text-align:center;margin:12px 0 0;font-size:14px">Next drive in <span id="countdown"></span> · midnight ET</p>
    </div>
    ${results.map(card).join("")}
    <p class="movelink"><a href="#" id="move">Playing on another device? Copy your streak link</a></p>`);
  document.getElementById("move").onclick = (e) => {
    e.preventDefault();
    const link = streakLink();
    Promise.resolve().then(() => navigator.clipboard.writeText(link)).then(
      () => (e.target.textContent = "Copied! Open it on your other device."),
      () => e.target.replaceWith(Object.assign(document.createElement("input"), { value: link, readOnly: true })) // no clipboard: show it to copy by hand
    );
    track("streak_link_copy");
  };
  document.getElementById("share").onclick = (e) => {
    track("share_click", { total_yards: yards });
    if (navigator.share) return navigator.share({ text: share }).catch(() => {});
    navigator.clipboard.writeText(share);
    e.target.textContent = "Copied!";
  };
}

// Which game numbers this device has started, to tell brand-new players (1) from returning ones (2+).
// Games finished before this list existed are counted from their saved results.
function markStarted() {
  const dates = Object.keys(GAMES);
  const started = new Set(load("dd_started", []));
  dates.forEach((date, i) => { if (load(date, []).length) started.add(i + 1); });
  const isNew = !started.has(dayNumber);
  started.add(dayNumber);
  save("dd_started", [...started].sort((a, b) => a - b));
  return { isNew, days: started.size };
}

function showStart() {
  render(`
    <div class="card">
      <p class="label">How to play</p>
      <p class="prompt">Start at your own goal line. Go 100 yards for a touchdown.</p>
      <p class="muted" style="font-size:14px;margin:0">A new game drops every day at midnight Eastern (ET).</p>
      <ol class="steps">
        <li><b>5 NFL prompts</b>, each with a 40-second play clock.</li>
        <li><b>Guess as often as you like.</b> Wrong answers are free. Stuck? Punt to move on.</li>
        <li><b>Rarer answers gain more yards.</b> Up to 20 per play: the obvious pick gets a few, a true deep cut gets all 20.</li>
      </ol>
      <button id="start">Kick off</button>
    </div>`);
  document.getElementById("start").onclick = () => {
    const { isNew, days } = markStarted();
    if (isNew) track("game_start", { days_played: days }); // once per game per device, even after refreshes
    startRound();
  };
}

// Countdown to midnight Eastern, when the next game unlocks.
function tick() {
  const el = document.getElementById("countdown");
  if (!el) return;
  const [h, m, sec] = new Date().toLocaleTimeString("en-GB", { timeZone: TZ, hour12: false }).split(":").map(Number);
  const secs = Math.max(0, 86400 - ((h % 24) * 3600 + m * 60 + sec));
  if (secs <= 1) setTimeout(() => location.reload(), 2000); // new game is out
  el.textContent = [secs / 3600, (secs / 60) % 60, secs % 60].map((n) => String(Math.floor(n)).padStart(2, "0")).join(":");
}
setInterval(tick, 1000);

if (!game) render(`<div class="card"><p class="prompt">No game today.</p><p class="muted">Next drive in <span id="countdown"></span> · midnight ET</p></div>`);
else if (results.length === 5) showFinal();
else if (savedDeadline()?.play === results.length) startRound(); // back mid-play: resume the same clock (times out if expired)
else if (results.length > 0) showReveal();
else showStart();
