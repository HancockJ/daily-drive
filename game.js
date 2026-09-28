const SECONDS = 40;
const today = new Date().toLocaleDateString("en-CA"); // YYYY-MM-DD
const dayNumber = Math.floor((new Date(today) - new Date("2026-09-28")) / 86400000) + 1;
const game = GAMES[(dayNumber - 1) % GAMES.length];

const screen = document.getElementById("screen");
let results = JSON.parse(localStorage.getItem(today) || "[]"); // one entry per round: { answer, yards }
let timer;

const clean = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, "");
const totalYards = () => results.reduce((sum, r) => sum + r.yards, 0);

function findAnswer(guess, answers) {
  const g = clean(guess);
  const lastName = (a) => clean(a.name.split(" ").pop());
  return answers.find((a) =>
    [a.name, ...(a.aliases || [])].some((n) => clean(n) === g) ||
    (lastName(a) === g && answers.filter((b) => lastName(b) === g).length === 1)
  );
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
  const share = `Fourth & Rare #${dayNumber}\n${yards === 100 ? "🏈 TOUCHDOWN! " : ""}${yards}/100 yards\n${results.map((r) => (r.yards === 20 ? "🏈" : r.yards)).join(" · ")}\n${location.origin + location.pathname}`;
  render(`
    <p class="prompt">${yards === 100 ? "Touchdown! Perfect drive." : `Drive over: ${yards} yards.`}</p>
    <ol>${results.map((r, i) => `<li>${r.answer || "(no answer)"} — ${r.yards} yds <span class="muted">(${game[i].prompt})</span></li>`).join("")}</ol>
    <button id="share">Copy result</button>
    <p class="muted">New game tomorrow.</p>`);
  document.getElementById("share").onclick = (e) => {
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

if (results.length === 5) showFinal();
else if (results.length > 0) showReveal();
else showStart();
