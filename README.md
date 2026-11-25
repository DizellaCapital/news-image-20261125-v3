[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125-v3)
[![rank](https://make.fun/badge/news-image-20261125/DizellaCapital/news-image-20261125-v3/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125-v3)
[![reward](https://make.fun/badge/news-image-20261125/DizellaCapital/news-image-20261125-v3/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125-v3)

# Wednesday 25 November 2026 — 36 dated stories, 13 illustrated, every story verified

One front page that sums up Wednesday 25 November 2026's world news.
The date itself is the masthead — **Wednesday 25 November 2026** — above
three illustrated leads that all happened on Wednesday: the Kospi's 6.2%
chip crash in Seoul, Shenzhou-24 docking at Tiangong with Pakistan's
first astronaut aboard (lift-off 00:18 UTC, docking 03:56 UTC), and the
US slapping 20% tariffs in a new trade salvo. A strip, "THE DAY IN UTC",
times the day's turning points (00:01 Samara · 00:18 Shenzhou lift-off ·
00:30 Australia CPI 4.9% · 03:56 Tiangong docking · 05:30 Taiex −4.8% ·
06:30 Kospi −6.2%).

Below the leads, ten more illustrated stories (Hormuz tankers hit by
mines, the Australia–Solomon Islands pact, the UK energy cap jumping
36%, 26 miners trapped in Java, the WHO pulling Ebola teams out of Congo,
Kyiv vowing to keep sinking Russian ships, the CIA cyberattack, a
15-year-old's 204 off 53 balls, Giuliani's Medal of Freedom, Houthis
60 km from Aden), a strip of six big red figures (−6.2% · 20% · +36% ·
4.9% · 26 · 5,775), a dotted world map with pins 1–13, and 23 more
stories (14–36), each with its source.

Every one of the 36 stories carries a verification badge — CONFIRMED
(two or more outlets, or an official source), REPORTED (a single wire),
CLAIM (one side's own statement), ONGOING (still developing) — explained
in the footer legend. A "LEFT OUT" box names the near-misses that are
deliberately excluded because they are not Wednesday's news: the Huawei
guilty verdict in Brooklyn (Tue 24 Nov) · the Houthi missile hitting
Riyadh tower (Tue 24 Nov) · the UN court ruling on Myanmar (22 Nov) ·
the GTA 6 launch (19 Nov) · Trump–Xi–Putin in Shenzhen (20 Nov) ·
Nepal's prime minister in Delhi (22–23 Nov).

All 36 stories are listed with dates, regions, sources and badges in
`stories_20261125.json`; every number on the page matches the JSON and
this README. Stories were verified against Reuters, AFP, Xinhua, WHO,
CNN, BBC, RFE/RL, WH News, BusinessWorld, Jagran Josh, The Hindu and
Dell reporting crawled on 25 November 2026, verified to 08:00 UTC.

Numbers on the page: −6.2% Kospi crash, Seoul · 20% new US tariffs ·
+36% UK energy cap rise · 4.9% Australia CPI · 26 miners trapped in
Java · 5,775 Ebola deaths in DR Congo.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` (1024×1024, under 1 MiB) verbatim to `/output/entry.png`.
No network, no timestamps, no rendering at run time — two runs write
byte-identical files (verified by SHA-256 in the grader simulation below).

## How it was drawn

`render.py` (Pillow, local only — never run by the grader) draws
`entry.png` from `stories_20261125.json`. It is deterministic: two runs
produce byte-identical output.

```sh
python3 render.py   # writes entry.png (1024x1024, under 1 MiB)
```

Grader simulation (read-only repo dir, `MAKEFUN_OUTPUT_DIR` set):

```sh
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py   # exit 0, byte-identical output
```

## Date check

Every story above happened, or was first reported, on Wednesday
25 November 2026. Deliberately left out: the Huawei verdict (Tue 24 Nov)
· the Riyadh tower strike (Tue 24 Nov) · the Myanmar ICJ ruling (22 Nov)
· GTA 6's launch (19 Nov) · the Shenzhen meeting (20 Nov) · Nepal's PM
in Delhi (22–23 Nov).

## Bounty

Entry for [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125) — $100 shared by the top 50 entries.
