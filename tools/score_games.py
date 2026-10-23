"""Score Daily Drive answers by popularity and add games to games.js.

Usage (needs `pip install pytrends`):
  python tools/score_games.py tools/specs/<spec>.py pages      # find each answer's Wikipedia article (prints matches to review)
  python tools/score_games.py tools/specs/<spec>.py topics     # find each person's Google Trends topic
  python tools/score_games.py tools/specs/<spec>.py score DATE  # score one day -> tools/out/DATE.json
  python tools/score_games.py tools/specs/<spec>.py insert     # append scored days to games.js + research CSVs

Yards: rank answers by Google Trends interest and by Wikipedia views (last 12 months), average the ranks,
then spread them over 2, 5, 8, 11, 14, 17, 20 (most popular -> rarest). Spec files may also give HAND-tiered lists.
"""
import csv, importlib.util, json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "tools", "cache")
OUT = os.path.join(ROOT, "tools", "out")
UA = {"User-Agent": "DailyDriveTrivia/0.1 (https://playdailydrive.com; trivia research)"}
TIERS = [2, 5, 8, 11, 14, 17, 20]
FOOTBALL = ("football", "quarterback", "safety", "linebacker", "cornerback", "running back", "wide receiver", "defensive", "coach",
            "nfl", "tight end", "end", "tackle", "kicker")
MUSICAL = ("singer", "band", "rapper", "musician", "group", "artist", "songwriter", "producer", "duo")


def load_spec(path):
    s = importlib.util.spec_from_file_location("spec", path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    for name, default in [("PAGE", {}), ("PAGE_BY_DAY", {}), ("WIKI_ONLY", set()), ("SEARCH", {}), ("MUSIC", set()), ("NOT", {}), ("HAND", {}), ("MOVED", {})]:
        if not hasattr(m, name):
            setattr(m, name, default)
    return m


def cache(name):
    p = os.path.join(CACHE, name)
    return json.load(open(p)) if os.path.exists(p) else {}


def save_cache(name, data):
    os.makedirs(CACHE, exist_ok=True)
    json.dump(data, open(os.path.join(CACHE, name), "w"), indent=1, ensure_ascii=False)


def scored_prompts(spec, date=None):
    for d, prompts in spec.SPEC.items():
        if date and d != date:
            continue
        for q, p in enumerate(prompts, 1):
            if isinstance(p, tuple):
                yield d, q, p


def wiki_api(params):
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"})
    for a in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA)))
        except Exception:
            time.sleep(4 * (a + 1))


def resolve(name, trusted):
    q = wiki_api({"action": "query", "titles": name, "redirects": 1, "prop": "pageprops|description"})["query"]
    pg = list(q["pages"].values())[0]
    desc = pg.get("description", "")
    ok = "missing" not in pg and "disambiguation" not in pg.get("pageprops", {})
    if ok and (trusted or any(w in desc.lower() for w in ("football", "nfl", "team", "coach"))):
        return pg["title"], desc
    hits = wiki_api({"action": "query", "list": "search", "srsearch": f"{name} American football", "srlimit": 3})["query"]["search"]
    t = hits[0]["title"]
    pg = list(wiki_api({"action": "query", "titles": t, "prop": "description"})["query"]["pages"].values())[0]
    return t, pg.get("description", "") + "  [via search - check]"


def stage_pages(spec):
    pages = cache("pages.json")
    for d, q, (prompt, answers) in scored_prompts(spec):
        for name, _ in answers:
            key = spec.PAGE_BY_DAY.get(d, {}).get(name) or spec.PAGE.get(name)
            if name in pages and not key:
                continue
            title, desc = resolve(key or name, trusted=bool(key) or name in spec.MUSIC)
            pages[name] = title
            print(f"{name:28} -> {title}  ({desc})")
            time.sleep(0.4)
    save_cache("pages.json", pages)


def stage_topics(spec):
    from pytrends.request import TrendReq
    py = TrendReq(hl="en-US", tz=300)
    topics = cache("topics.json")
    for d, q, (prompt, answers) in scored_prompts(spec):
        for name, aliases in answers:
            if name in topics or name in spec.SEARCH or name in spec.WIKI_ONLY:
                continue
            if aliases and name.split()[-1] in aliases and len(name.split()) >= 2 and any(a[0].isupper() for a in aliases):
                topics[name] = None  # a team: plain search term is fine
                continue
            kinds = MUSICAL if name in spec.MUSIC else FOOTBALL
            queries = (name,) if name in spec.MUSIC else (name.replace("J. J.", "JJ"), name + " football")
            pick = None
            for qy in queries:
                for a in range(5):
                    try:
                        sug = py.suggestions(qy)
                        break
                    except Exception:
                        sug = []
                        time.sleep(20 * (a + 1))
                norm = lambda s: s.replace(".", "").replace(" ", "").lower()
                pick = next((s for s in sug if norm(s["title"]) == norm(name) and any(w in s["type"].lower() for w in kinds)), None)
                time.sleep(2)
                if pick:
                    break
            topics[name] = [pick["mid"], pick["type"]] if pick else "WIKI_ONLY"
            print(f"{name:28} {topics[name]}")
            save_cache("topics.json", topics)
    save_cache("topics.json", topics)


def stage_score(spec, date):
    from pytrends.request import TrendReq
    py = TrendReq(hl="en-US", tz=300)
    pages, topics = cache("pages.json"), cache("topics.json")
    for n, t in spec.PAGE_BY_DAY.get(date, {}).items():
        pages[n] = t

    def term(n):
        if n in spec.SEARCH:
            return spec.SEARCH[n]
        t = topics.get(n)
        return t[0] if isinstance(t, list) else n

    def wiki(n):
        page = urllib.parse.quote(pages[n].replace(" ", "_"), safe="")
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{page}/monthly/2025090100/2026083100"
        for a in range(6):
            try:
                return sum(i["views"] for i in json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA)))["items"])
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return 0
                time.sleep(5 * (a + 1))
            except Exception:
                time.sleep(5 * (a + 1))
        raise SystemExit(f"wiki failed: {n}")

    def trends(names):
        names = [n for n in names if topics.get(n) != "WIKI_ONLY" and n not in spec.WIKI_ONLY]
        if len(names) < 2 or os.environ.get("NO_TRENDS"):  # NO_TRENDS=1 when Google is rate-limiting: rank by Wikipedia views alone
            return {}
        terms = [term(n) for n in names]
        rel = {terms[0]: 1.0}
        for i in range(1, len(terms), 4):
            batch = [terms[0]] + terms[i:i + 4]
            for a in range(6):
                try:
                    py.build_payload(batch, timeframe="today 5-y", geo="US")
                    m = py.interest_over_time()[batch].mean()
                    break
                except Exception as e:
                    err = e
                    time.sleep(30 * (a + 1))
            else:
                raise SystemExit(f"trends failed {batch}: {err}")
            for t in batch[1:]:
                rel[t] = round(float(m[t] / m[terms[0]]), 4) if m[terms[0]] else 0.0
            time.sleep(5)
        return {n: rel[term(n)] for n in names}

    rows = []
    for d, q, (prompt, answers) in scored_prompts(spec, date):
        w = {}
        for name, _ in answers:
            w[name] = wiki(name)
            time.sleep(1)
        names = sorted(w, key=lambda n: -w[n])  # most-viewed first, so the Trends anchor is never ~0
        t = trends(names)
        rank = lambda vals: {n: i for i, n in enumerate(sorted(vals, key=lambda n: -vals[n]))}
        rt, rw = rank(t), rank(w)
        for n in names:  # no usable Trends data: count the Wikipedia rank twice
            if n not in rt:
                rt[n] = rw[n]
                t[n] = None
        order = sorted(names, key=lambda n: (rt[n] + rw[n], rw[n]))
        for p, n in enumerate(order):
            rows.append([q, n, t[n], w[n], TIERS[round(p / (len(order) - 1) * 6)]])
        print(f"{date} Q{q} scored", file=sys.stderr)
    os.makedirs(OUT, exist_ok=True)
    json.dump(rows, open(os.path.join(OUT, f"{date}.json"), "w"), ensure_ascii=False)


def stage_insert(spec, moved_block_file=None, moved_rows_file=None):
    js = lambda s: json.dumps(s, ensure_ascii=False)
    games_path = os.path.join(ROOT, "games.js")
    s = open(games_path).read().rstrip()
    assert s.endswith("};")

    def block(prompt, rows, aliases, nots):
        out = f"    {{\n      prompt: {js(prompt)},\n      answers: [\n"
        for name, y in rows:
            extra = (f", aliases: {js(aliases[name])}" if aliases.get(name) else "") + (f", not: {js(nots[name])}" if nots.get(name) else "")
            out += f"        {{ name: {js(name)}, yards: {y}{extra} }},\n"
        return out + "      ],\n    },\n"

    added, out = [], ""
    for date, prompts in spec.SPEC.items():
        if f'"{date}"' in s:
            continue
        path = os.path.join(OUT, f"{date}.json")
        scored = json.load(open(path)) if os.path.exists(path) else None
        if scored is None and any(isinstance(p, tuple) for p in prompts):
            print("not scored yet:", date)
            continue
        out += f'  "{date}": [\n'
        csv_rows = []
        for q, p in enumerate(prompts, 1):
            if isinstance(p, tuple):
                prompt, answers = p
                rows = [(n, y) for qq, n, t, w, y in scored if qq == q]
                out += block(prompt, rows, dict(answers), spec.NOT)
                csv_rows += [[q, n, "" if t is None else t, w, y] for qq, n, t, w, y in scored if qq == q]
            elif p.startswith("HAND:"):
                prompt, items = spec.HAND[p[5:]]
                out += block(prompt, [(n, y) for n, y, a in items], {n: a for n, y, a in items}, {})
                csv_rows += [[q, n, "hand-tiered", "", y] for n, y, a in items]
            elif p == "MOVED":
                out += open(moved_block_file).read()
                csv_rows += [[q] + r[1:] for r in json.load(open(moved_rows_file))]
        out += "  ],\n"
        with open(os.path.join(ROOT, "research", f"{date}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["prompt", "answer", "google_trends_relative", "wikipedia_views_12mo", "yards"])
            w.writerows(csv_rows)
        added.append(date)
    open(games_path, "w").write(s[:-2] + out + "};\n")
    print("added", added)


if __name__ == "__main__":
    spec = load_spec(sys.argv[1])
    stage = sys.argv[2]
    if stage == "pages":
        stage_pages(spec)
    elif stage == "topics":
        stage_topics(spec)
    elif stage == "score":
        stage_score(spec, sys.argv[3])
    elif stage == "insert":
        stage_insert(spec, *sys.argv[3:5])
