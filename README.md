# World News, 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/thomasmoa97/news-image-20261123-entry/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard)
[![reward](https://make.fun/badge/news-image-20261123/thomasmoa97/news-image-20261123-entry/reward.svg)](https://make.fun/bounty/news-image-20261123/leaderboard)

One image that sums up the world's news of **Monday, 23 November 2026** — drawn
as a one-page newspaper front page with Pillow (Python 3.13, no network, fully
deterministic).

**The day's lead story:** Tanker war in the Strait of Hormuz — at least 25
tankers struck in and around the strait in seven days as Iran's navy reports
ships hitting mines and UK maritime authorities report projectile strikes, with
Gulf oil flow dropping sharply. Also inside: the COP31 climate talks collapse
without a deal, Ukrainian sea drones hit a Russian warship at a Libyan naval
base, Poland confirms fallen objects were Russian cruise missiles as NATO
prepares to meet, the BepiColombo probe enters orbit around Mercury, and world
markets plunge on AI-bubble fears.

## How it works

`main.py` draws the 1024×1024 infographic with Pillow and the bundled DejaVu
fonts — masthead, hero panel with a stylised Strait of Hormuz map, a 2×3 grid
of story cards, and a news ticker — then writes `entry.png` to
`MAKEFUN_OUTPUT_DIR` (default `/output`).

```sh
MAKEFUN_OUTPUT_DIR=. python3 main.py
```

Two runs produce byte-identical output: no clock, no randomness, no network.

## Entry

- Competition: [news-image-20261123](https://make.fun/bounty/news-image-20261123)
- Program: `main.py` (Python 3.13 + Pillow)
- Output: `entry.png` (1024×1024 PNG)
