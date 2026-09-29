const SECONDS = 40;
const today = new Date().toLocaleDateString("en-CA"); // YYYY-MM-DD
const dayNumber = Object.keys(GAMES).indexOf(today) + 1;
const game = GAMES[today];

const screen = document.getElementById("screen");
let results = JSON.parse(localStorage.getItem(today) || "[]"); // one entry per round: { answer, yards }
let timer;

const totalYards = () => results.reduce((sum, r) => sum + r.yards, 0);

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
  const fuzzy = answers.filter((a) => names(a).some((n) => close(g, n)));
  return fuzzy.length === 1 ? fuzzy[0] : undefined; // ambiguous typos don't count
}

function render(html) {
  screen.innerHTML = html;
  const yards = totalYards();
  document.getElementById("yardage").textContent = `${yards} yards`;
  document.getElementById("ball").style.left = `calc(${yards}% - ${yards * 0.3}px)`;
}

function startRound() {
  const round = game[results.length];
  let left = SECONDS;
  render(`
    <p class="muted">Play ${results.length + 1} of 5</p>
    <p class="timer" id="clock">0:${left}</p>
    <p class="prompt">${round.prompt}</p>
    <form id="form">
      <input id="guess" autocomplete="off" spellcheck="false" placeholder="Your answer" autofocus>
      <button>Snap it</button>
    </form>
    <p id="msg" class="muted"></p>`);
  document.getElementById("guess").focus();
  timer = setInterval(() => {
    left--;
    document.getElementById("clock").textContent = `0:${String(left).padStart(2, "0")}`;
    if (left <= 0) finishRound("");
  }, 1000);
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

function finishRound(guess) {
  clearInterval(timer);
  const match = findAnswer(guess, game[results.length].answers);
  results.push({ answer: match ? match.name : guess, yards: match ? match.yards : 0 });
  localStorage.setItem(today, JSON.stringify(results));
  showReveal();
}

function answerList(round) {
  return `<ul>${round.answers.map((a) => `<li>${a.name} — ${a.yards} yds</li>`).join("")}</ul>`;
}

function showReveal() {
  const i = results.length - 1;
  const r = results[i];
  const verdict = r.answer ? `${r.answer}: +${r.yards} yards` : "Delay of game! No gain.";
  render(`
    <p class="prompt">${verdict}</p>
    <details><summary>All accepted answers</summary>${answerList(game[i])}</details>
    <button id="next">${results.length < 5 ? "Next play" : "See final drive"}</button>`);
  document.getElementById("next").onclick = results.length < 5 ? startRound : showFinal;
}

function showFinal() {
  const yards = totalYards();
  const emoji = (y) => (y === 20 ? "🏈" : y >= 14 ? "🥇" : y >= 8 ? "🥈" : y > 0 ? "🥉" : "❌");
  const share = `Fourth & Rare #${dayNumber}\n${yards === 100 ? "🏈 TOUCHDOWN! " : ""}${yards}/100 yards\n${results.map((r) => emoji(r.yards)).join("")}\n${location.origin + location.pathname}`;
  render(`
    <p class="prompt">${yards === 100 ? "Touchdown! Perfect drive." : `Drive over: ${yards} yards.`}</p>
    <ol>${results.map((r, i) => `<li>${r.answer || "(no answer)"} — ${r.yards} yds <span class="muted">(${game[i].prompt})</span></li>`).join("")}</ol>
    <button id="share">Share Score</button>
    <p class="muted">New game tomorrow.</p>`);
  document.getElementById("share").onclick = (e) => {
    if (navigator.share) return navigator.share({ text: share }).catch(() => {});
    navigator.clipboard.writeText(share);
    e.target.textContent = "Copied!";
  };
}

function showStart() {
  render(`
    <p class="muted">Game #${dayNumber}</p>
    <p class="prompt">5 NFL prompts. 40-second play clock each. The less obvious your answer, the more yards you gain. Go 100 yards for a touchdown.</p>
    <button id="start">Kick off</button>`);
  document.getElementById("start").onclick = startRound;
}

// Leaving mid-play counts as a delay of game, so reloading can't reset the clock.
window.onbeforeunload = () => { if (timer && screen.querySelector("#form")) finishRound(""); };

if (!game) render(`<p class="prompt">No game today. Check back tomorrow!</p>`);
else if (results.length === 5) showFinal();
else if (results.length > 0) showReveal();
else showStart();
