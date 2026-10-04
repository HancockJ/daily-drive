# Real player stats (Krillion-style) — plan, not built yet

Goal: show stats from real players, e.g. "12% of players said Brady", "You beat 74% of drives today",
yards that reflect what people actually answer, and (later) history/streaks that follow you across devices.

## Key point
Crowd stats need a **server + database**, not a login. The anonymous `dd_player_id` already on each device
is enough to count players and dedupe. Login is only for cross-device history, streaks, and friends.

## Phase 1 — live crowd stats (no login)
- **Backend:** a Cloudflare Worker added to the existing project (same domain, same deploys) + **Cloudflare D1** (SQLite).
  Free tier covers this easily (Workers ~100k requests/day, D1 5 GB / millions of reads per day).
- **Config:** `wrangler.jsonc` gets `"main": "worker.js"`, a D1 binding, and assets set to run the Worker only for `/api/*`.
- **Database tables:**
  - `plays(game, play, player_id, answer, yards, result, created_at)` — one row per play, unique on (game, play, player_id)
  - `games(game, player_id, total_yards, finished_at)` — one row per finished game
- **API:**
  - `POST /api/play` — sent after each play (same moment as the GA `play_result` event)
  - `POST /api/finish` — sent with the final score
  - `GET /api/stats?game=N` — per-answer percentages, score distribution, average yards (cached ~60s)
- **Game UI:** reveal card shows "X% of players said this"; final screen shows "You beat N% of drives" and a small
  score histogram; accepted-answer list shows each answer's real pick rate.
- **Safety:** submissions are fire-and-forget (game never waits on them); server checks the answer against that day's
  answer list, ignores duplicates, rate-limits per IP, and skips `dd_internal` devices. Show crowd numbers only after
  ~25 players so early stats aren't misleading.
- **Privacy page:** update to say answers + scores are stored with an anonymous ID.

## Phase 2 — real rarity
- Use stored answers to set yards from actual pick rates (Krillion's "familiarity" calibration).
- Start with **future** games: after a game runs, compare real pick rates to our Trends/Wikipedia yards and re-tier
  similar questions. Optional later: live re-scoring once a game has enough players (needs care so scores stay fair).
- Bonus: logged wrong guesses show which answers people *think* are right → finds missing answers / bad prompts.

## Phase 3 — optional sign-in (guest play stays the default)
- **Sign in with Google** (Google Identity Services button; Worker verifies Google's ID token) — optionally Apple
  later since most players are on iPhone.
- `users(google_sub, email, created_at)` + link table to `dd_player_id`, so signing in **claims this device's history**.
- Unlocks: history + streaks on any device, "your stats over time" page, friends/leaderboards.
- Needs: session cookie (first-party, essential — no consent banner), privacy policy update, account deletion option.

## What it needs from Jack
- Phase 1: nothing new to buy; create the D1 database in Cloudflare (or let Wrangler do it) — ~5 minutes.
- Phase 3: a Google Cloud project with an OAuth client ID (free, ~15 minutes), decide on Apple sign-in later.

## Rough effort
- Phase 1: ~1 focused session to build + test on a preview branch.
- Phase 2: small once data exists (a script + periodic review).
- Phase 3: ~1–2 sessions, mostly testing sign-in flows on iPhone.
