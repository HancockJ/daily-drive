# Answer popularity research

One CSV per game date, recording why each answer got its yards.

- `google_trends_relative`: average US Google Trends interest over the last 5 years, relative to the most-viewed answer in that prompt (1.0). Unofficial pytrends library.
- `wikipedia_views_12mo`: English Wikipedia pageviews for the answer's article, Sep 2025 – Aug 2026.
- `new_yards`: rank answers on each measure, average the two ranks, then spread them evenly across the tiers 2, 5, 8, 11, 14, 17, 20 (most popular → rarest).

From 2026-10-01: Google Trends uses each person's Trends *topic* (the football player, not everyone with that name). Answers with no football topic (e.g. Larry Brown, Jake Scott) leave Trends blank and count their Wikipedia rank twice.
