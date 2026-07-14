# IPL Analytics — Power BI Dashboard Blueprint
### Senior BI Developer Design Document
**Source:** Gold Layer (S3 Data Lake → DuckDB → Power BI) — 5 tables: `player_statistics`, `bowler_statistics`, `team_statistics`, `venue_statistics`, `season_statistics`

---

## 0. Design Philosophy

This is built as a **6-page analytical product**, not a single crowded dashboard. Each page answers one stakeholder question:

| Page | Audience Question |
|---|---|
| 1. Executive Overview | "How healthy is the league overall, right now?" |
| 2. Batting Performance | "Who are the best batters, and why?" |
| 3. Bowling Performance | "Who controls the game with the ball?" |
| 4. Team Performance | "Which teams win, and how?" |
| 5. Venue Intelligence | "Where should you bat first? Where do chases succeed?" |
| 6. Season Trends | "How has the game evolved year over year?" |

A shared **theme, top nav bar, and global slicer panel** appear on every page for consistency — described once in Section 6, applied everywhere.

---

## 1. PAGE-BY-PAGE PLAN

### PAGE 1 — Executive Overview

**Purpose:** Single-screen league health check. First page recruiters/execs see.

**KPI Cards (6, top strip):**
1. Total Matches — `[Total Matches]`
2. Total Runs — `[Total Runs Scored]`
3. Total Wickets — `[Total Wickets Taken]`
4. Average Match Score — `[Avg Innings Score]`
5. Highest Team Score — `[Max Team Score]`
6. Highest Win % (Team) — `[Best Team Win %]`

**Visuals:**

| # | Visual Type | X-axis | Y-axis | Legend | Tooltip | Sort Order | Drillthrough | Filters | Cross-filter |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Line Chart | `year` (season_statistics) | `total_runs`, `total_wickets` (dual axis) | Measure name | Year, Runs, Wickets, Matches | X-axis ascending (year) | → Season Trends page | Year range slicer | Highlight (single direction) |
| 2 | Clustered Bar Chart | `win_percentage` | `batting_team` | none | Team, Wins, Losses, Win % | Y-axis desc by win % | → Team Performance page | Team slicer | Highlight |
| 3 | Donut Chart | — | `total_runs` by `batting_team` (share of total) | `batting_team` | Team, Runs, % of total | Value desc | none | Team slicer | Highlight |
| 4 | Card-style KPI strip (Top Performers) | — | Top 3 batters by `total_runs`, Top 3 bowlers by `wickets` | — | Player, stat value | Value desc | → Batting / Bowling pages | Min innings slicer | none |
| 5 | Map (if lat/long available) or Bar Chart | `venue` | `matches` | — | Venue, Matches, Avg 1st innings score | Matches desc | → Venue Intelligence page | none | Highlight |

**Insights answered:**
- Visual 1: Is scoring/wicket-taking trending up or down across seasons (bat-friendly vs bowler-friendly eras)?
- Visual 2: Which teams are structurally dominant across IPL history?
- Visual 3: Which teams have contributed most to total league run volume (proxy for longevity/participation)?
- Visual 4: Who are the standout individual performers league-wide?
- Visual 5: Which venues host the most matches — infrastructure/scheduling insight?

**Wireframe:**
```
--------------------------------------------------------------------
| LOGO / TITLE      IPL ANALYTICS      [Overview|Batting|Bowling|Team|Venue|Season] |
--------------------------------------------------------------------
| Matches | Total Runs | Total Wkts | Avg Score | Highest Score | Best Win % |
--------------------------------------------------------------------
|                 Runs & Wickets by Season (Line, dual axis)        |
--------------------------------------------------------------------
| Win % by Team (Bar)      |     Run Share by Team (Donut)          |
--------------------------------------------------------------------
| Top Batters / Bowlers (KPI strip) |  Matches by Venue (Bar/Map)   |
--------------------------------------------------------------------
```

---

### PAGE 2 — Batting Performance

**Purpose:** Deep dive into `player_statistics`.

**KPI Cards (5):**
1. Total Runs (filtered) — `[Total Runs Scored]`
2. Highest Strike Rate — `[Best Strike Rate]`
3. Most Sixes — `[Max Sixes]`
4. Most Fours — `[Max Fours]`
5. Boundary % (League Avg) — `[Avg Boundary %]`

**Visuals:**

| # | Visual Type | X-axis | Y-axis | Legend | Tooltip | Sort Order | Drillthrough | Filters | Cross-filter |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Horizontal Bar Chart | `total_runs` | `batter` (Top 15) | none | Runs, Innings, Strike Rate, Avg | Runs desc | → Player Drillthrough page | Min innings slicer | Highlight |
| 2 | Scatter Chart | `strike_rate` | `total_runs` | `batter` (color by run bucket) | Batter, Runs, SR, Balls Faced | none (natural distribution) | → Player Drillthrough | Min innings, Min balls faced | Highlight |
| 3 | Clustered Column Chart | `batter` (Top 10 by sixes) | `fours`, `sixes` (dual series) | Boundary type | Batter, Fours, Sixes, Boundary % | Sixes desc | → Player Drillthrough | Min innings slicer | Highlight |
| 4 | Table / Matrix | Rows: `batter` | Columns: innings, balls_faced, total_runs, strike_rate, fours, sixes | — | (native cell values) | Runs desc (default) | → Player Drillthrough | All page slicers apply | Highlight |
| 5 | Gauge / KPI comparison | — | `strike_rate` vs league average | — | Player SR vs Avg SR | — | none | Single-player slicer (What-If) | none |

**Insights answered:**
- Visual 1: Who are the highest run-scorers (the "reliable" run-machines)?
- Visual 2: Who combines volume (runs) with tempo (strike rate) — separates anchors from finishers?
- Visual 3: Who scores through boundaries vs. rotating strike — power-hitters vs. accumulators?
- Visual 4: Full sortable reference table for analysts/recruiters to inspect raw stats.
- Visual 5: Is a selected player above or below league-average strike rate?

**Wireframe:**
```
--------------------------------------------------------------------
| Total Runs | Best SR | Most Sixes | Most Fours | Avg Boundary %   |
--------------------------------------------------------------------
| Top 15 Run Scorers (Bar)   |   Runs vs Strike Rate (Scatter)      |
--------------------------------------------------------------------
|      Fours vs Sixes — Top 10 Power Hitters (Column)               |
--------------------------------------------------------------------
|            Full Player Stats Table (Matrix, sortable)             |
--------------------------------------------------------------------
```

---

### PAGE 3 — Bowling Performance

**Purpose:** Deep dive into `bowler_statistics`.

**KPI Cards (5):**
1. Total Wickets — `[Total Wickets Taken]`
2. Best Economy — `[Best Economy Rate]`
3. Most Dot Balls — `[Max Dot Balls]`
4. Lowest Runs Conceded (qualified) — `[Min Runs Conceded]`
5. Dot Ball % (League Avg) — `[Avg Dot Ball %]`

**Visuals:**

| # | Visual Type | X-axis | Y-axis | Legend | Tooltip | Sort Order | Drillthrough | Filters | Cross-filter |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Horizontal Bar Chart | `wickets` | `bowler` (Top 15) | none | Wickets, Economy, Balls Bowled | Wickets desc | → Player Drillthrough | Min balls bowled slicer | Highlight |
| 2 | Scatter Chart | `economy` | `wickets` | `bowler` (color by dot ball %) | Bowler, Wickets, Economy, Dot % | none | → Player Drillthrough | Min balls bowled slicer | Highlight |
| 3 | Bar Chart | `bowler` (Top 10 by dot balls) | `dot_balls` | — | Bowler, Dot Balls, Dot Ball % | Dot balls desc | → Player Drillthrough | Min balls bowled | Highlight |
| 4 | Table / Matrix | Rows: `bowler` | Columns: wickets, balls_bowled, runs_conceded, economy, dot_balls | — | native | Wickets desc default | → Player Drillthrough | All page slicers | Highlight |
| 5 | KPI Comparison Card | — | `economy` vs league average | — | Bowler Economy vs Avg | — | none | Single-bowler slicer | none |

**Insights answered:**
- Visual 1: Who takes the most wickets — the strike bowlers?
- Visual 2: Who combines wicket-taking with control (low economy) — the genuine match-winners vs. wicket-only bowlers?
- Visual 3: Who builds pressure through dot balls (containment bowlers, often death/middle-overs specialists)?
- Visual 4: Full sortable reference table.
- Visual 5: Is a selected bowler tighter or looser than league average?

**Wireframe:** *(mirrors Batting page layout for visual consistency)*
```
--------------------------------------------------------------------
| Total Wkts | Best Economy | Most Dots | Min Runs Conc | Avg Dot % |
--------------------------------------------------------------------
| Top 15 Wicket Takers (Bar) |  Economy vs Wickets (Scatter)        |
--------------------------------------------------------------------
|         Top 10 Dot Ball Bowlers (Bar)                              |
--------------------------------------------------------------------
|            Full Bowler Stats Table (Matrix, sortable)             |
--------------------------------------------------------------------
```

---

### PAGE 4 — Team Performance

**Purpose:** Deep dive into `team_statistics`.

**KPI Cards (5):**
1. Total Matches — `[Total Matches]`
2. Highest Win % — `[Best Team Win %]`
3. Highest Team Score — `[Max Team Score]`
4. Average Team Score — `[Avg Team Score]`
5. Most Wins — `[Max Wins]`

**Visuals:**

| # | Visual Type | X-axis | Y-axis | Legend | Tooltip | Sort Order | Drillthrough | Filters | Cross-filter |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Bar Chart | `win_percentage` | `batting_team` | Win/Loss color coding via conditional formatting | Team, Wins, Losses, Matches, Win % | Win % desc | → Team Drillthrough page | Season slicer (if joinable) | Highlight |
| 2 | Stacked Bar Chart | `batting_team` | `wins`, `losses` (stacked) | Result | Team, Wins, Losses, Total Matches | Wins desc | → Team Drillthrough | none | Highlight |
| 3 | Clustered Column Chart | `batting_team` | `average_score`, `highest_score` (dual series) | Metric | Team, Avg Score, Highest Score | Avg score desc | → Team Drillthrough | none | Highlight |
| 4 | Table / Matrix | Rows: `batting_team` | Columns: matches, wins, losses, win_percentage, total_runs, average_score, highest_score | — | native | Win % desc default | → Team Drillthrough | All page slicers | Highlight |
| 5 | Ribbon Chart or Radar Chart | `batting_team` | `average_score` vs `win_percentage` (normalized) | Team | Team, metric values | — | none | Team multi-select slicer | Highlight |

**Insights answered:**
- Visual 1: Which team has the best overall win conversion rate?
- Visual 2: How do wins/losses split per team — consistency vs. volatility?
- Visual 3: Do high-scoring teams actually win more, or is scoring not correlated with winning?
- Visual 4: Full comparative reference table across all franchises.
- Visual 5: Which teams combine strong batting output with strong results (top-right quadrant performers)?

**Wireframe:**
```
--------------------------------------------------------------------
| Matches | Best Win % | Highest Score | Avg Score | Most Wins      |
--------------------------------------------------------------------
|     Win % by Team (Bar, conditional color)                        |
--------------------------------------------------------------------
| Wins/Losses Split (Stacked Bar) | Avg vs Highest Score (Column)   |
--------------------------------------------------------------------
|            Full Team Stats Table (Matrix, sortable)               |
--------------------------------------------------------------------
```

---

### PAGE 5 — Venue Intelligence

**Purpose:** Deep dive into `venue_statistics` — toss/strategy decision support.

**KPI Cards (5):**
1. Total Venues — `[Total Venues]`
2. Highest Venue Score — `[Max Venue Score]`
3. Lowest Venue Score — `[Min Venue Score]`
4. Avg Batting-First Win % — `[Avg Bat First Win %]`
5. Avg Chasing Win % — `[Avg Chase Win %]`

**Visuals:**

| # | Visual Type | X-axis | Y-axis | Legend | Tooltip | Sort Order | Drillthrough | Filters | Cross-filter |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Diverging Bar Chart | `batting_first_win_percentage` − `chasing_win_percentage` | `venue` | Positive (bat first) / Negative (chase) color | Venue, Bat First %, Chase % | Difference desc | → Venue Drillthrough page | Min matches slicer | Highlight |
| 2 | Clustered Bar Chart | `venue` | `average_1st_innings`, `average_2nd_innings` | Innings | Venue, Avg 1st, Avg 2nd | Avg 1st innings desc | → Venue Drillthrough | Min matches slicer | Highlight |
| 3 | Column Chart | `venue` (Top 10 highest scoring) | `highest_score` | — | Venue, Highest Score, Lowest Score | Highest score desc | → Venue Drillthrough | Min matches slicer | Highlight |
| 4 | Table / Matrix | Rows: `venue` | Columns: matches, innings, highest_score, lowest_score, avg_1st, avg_2nd, bat_first_win%, chase_win% | — | native | Matches desc default | → Venue Drillthrough | All page slicers | Highlight |
| 5 | Donut Chart | — | Count of venues by "Bat First Favored" vs "Chase Favored" | Category | Category, count of venues | — | none | none | Highlight |

**Insights answered:**
- Visual 1: At which venues should captains bat first vs. chase — direct toss-decision intelligence.
- Visual 2: Does par score drop significantly in the 2nd innings (dew/pressure effect) by venue?
- Visual 3: Which grounds are the highest-scoring (batting paradises) vs. lowest (bowling tracks)?
- Visual 4: Full venue reference table for strategists.
- Visual 5: Across the league, is toss strategy generally in favor of batting first or chasing?

**Wireframe:**
```
--------------------------------------------------------------------
| Venues | Highest Score | Lowest Score | Avg Bat-1st Win% | Avg Chase Win% |
--------------------------------------------------------------------
|   Bat First vs Chase Win % Advantage by Venue (Diverging Bar)     |
--------------------------------------------------------------------
| Avg 1st vs 2nd Innings Score (Bar) | Highest Scores (Column)      |
--------------------------------------------------------------------
|            Full Venue Stats Table (Matrix, sortable)              |
--------------------------------------------------------------------
```

---

### PAGE 6 — Season Trends

**Purpose:** Deep dive into `season_statistics` — league evolution over time.

**KPI Cards (5):**
1. Total Seasons — `[Total Seasons]`
2. Latest Season Runs — `[Current Season Runs]`
3. Latest Season Avg Score — `[Current Season Avg Score]`
4. Highest Team Score (All-Time) — `[Max Team Score]`
5. YoY Run Growth % — `[YoY Run Growth %]`

**Visuals:**

| # | Visual Type | X-axis | Y-axis | Legend | Tooltip | Sort Order | Drillthrough | Filters | Cross-filter |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Line & Column Combo | `year` | `total_runs` (column), `average_score` (line) | Metric | Year, Runs, Avg Score, Matches | Year asc | none | Year range slicer | Highlight |
| 2 | Area Chart | `year` | `total_wickets` | — | Year, Wickets, Matches | Year asc | none | Year range slicer | Highlight |
| 3 | Column Chart | `year` | `highest_team_score` | — | Year, Highest Score | Year asc | none | Year range slicer | Highlight |
| 4 | Table / Matrix | Rows: `year` | Columns: matches, total_runs, total_wickets, average_score, highest_team_score | — | native | Year desc default | none | Year slicer | Highlight |
| 5 | KPI Trend Sparkline strip | — | YoY % change in avg score, runs, wickets | — | Year, % change | — | none | none | none |

**Insights answered:**
- Visual 1: Is the league becoming more run-heavy over time (rule changes, bigger bats, shorter boundaries)?
- Visual 2: Are bowlers taking more or fewer wickets per season — bat vs. ball dominance shift.
- Visual 3: Has the ceiling for a single team's score risen historically (evolution of aggressive batting)?
- Visual 4: Full season-by-season reference table.
- Visual 5: Quick YoY momentum check — is the current season trending up or down vs. history?

**Wireframe:**
```
--------------------------------------------------------------------
| Seasons | Latest Runs | Latest Avg Score | Max Score | YoY Growth% |
--------------------------------------------------------------------
|        Total Runs (Column) & Avg Score (Line) by Year             |
--------------------------------------------------------------------
| Total Wickets by Year (Area) | Highest Team Score by Year (Col)   |
--------------------------------------------------------------------
|            Full Season Stats Table (Matrix, sortable)             |
--------------------------------------------------------------------
```

---

### Drillthrough Pages (hidden, accessed via right-click / navigation)

- **Player Drillthrough** — takes `batter` or `bowler` as filter context; shows a large player card, radar chart of strengths (runs/SR/boundary% or wickets/economy/dot%), and a season-wise trend if season-level player data exists.
- **Team Drillthrough** — takes `batting_team` as filter context; shows season-by-season performance trend, top players from that team, and venue performance.
- **Venue Drillthrough** — takes `venue` as filter context; shows historical scores at that venue and bat-first vs chase breakdown over time.

---

## 2. GLOBAL SLICERS (appear on every page, docked left or top)

| Slicer | Field | Type | Applies To |
|---|---|---|---|
| Season / Year | `season_statistics[year]` | Dropdown / Timeline slicer | All pages (if a season key exists on fact tables; otherwise scoped to Season Trends page) |
| Team | `batting_team` | Dropdown (searchable) | Team, Venue (via relationship), Overview |
| Venue | `venue` | Dropdown (searchable) | Venue, Overview |
| Player | `batter` / `bowler` | Searchable dropdown | Batting, Bowling pages |
| Minimum Innings | `innings` | Slider (numeric range) | Batting page — removes small-sample outliers |
| Minimum Balls Bowled | `balls_bowled` | Slider (numeric range) | Bowling page — same purpose |
| Minimum Matches (Venue) | `matches` | Slider | Venue page |

**Design rule:** Minimum-innings/balls-bowled slicers are essential — without them, a player with 1 innings and 1 six can appear as "highest strike rate," which misleads any recruiter reviewing the dashboard. This is the single detail that most separates an amateur build from a professional one.

---

## 3. FULL KPI CARD INVENTORY (across all pages)

| KPI | DAX Measure Name | Page(s) |
|---|---|---|
| Total Matches | `Total Matches` | Overview, Team |
| Total Runs Scored | `Total Runs Scored` | Overview, Season |
| Total Wickets Taken | `Total Wickets Taken` | Overview, Season |
| Avg Innings Score | `Avg Innings Score` | Overview |
| Max Team Score | `Max Team Score` | Overview, Team, Season |
| Best Team Win % | `Best Team Win %` | Overview, Team |
| Best Strike Rate | `Best Strike Rate` | Batting |
| Max Sixes | `Max Sixes` | Batting |
| Max Fours | `Max Fours` | Batting |
| Avg Boundary % | `Avg Boundary %` | Batting |
| Best Economy Rate | `Best Economy Rate` | Bowling |
| Max Dot Balls | `Max Dot Balls` | Bowling |
| Min Runs Conceded | `Min Runs Conceded (Qualified)` | Bowling |
| Avg Dot Ball % | `Avg Dot Ball %` | Bowling |
| Avg Team Score | `Avg Team Score` | Team |
| Max Wins | `Max Wins` | Team |
| Total Venues | `Total Venues` | Venue |
| Max Venue Score | `Max Venue Score` | Venue |
| Min Venue Score | `Min Venue Score` | Venue |
| Avg Bat First Win % | `Avg Bat First Win %` | Venue |
| Avg Chase Win % | `Avg Chase Win %` | Venue |
| Total Seasons | `Total Seasons` | Season |
| YoY Run Growth % | `YoY Run Growth %` | Season |

---

## 4. DAX MEASURES (organized by table)

### `player_statistics` measures
```dax
Total Runs Scored = SUM(player_statistics[total_runs])

Total Innings (Batting) = SUM(player_statistics[innings])

Total Balls Faced = SUM(player_statistics[balls_faced])

Overall Strike Rate = 
DIVIDE(SUM(player_statistics[total_runs]) * 100, SUM(player_statistics[balls_faced]), 0)

Best Strike Rate = 
CALCULATE(
    MAX(player_statistics[strike_rate]),
    player_statistics[innings] >= 5   -- qualification threshold, tie to Min Innings slicer
)

Max Sixes = MAX(player_statistics[sixes])

Max Fours = MAX(player_statistics[fours])

Total Boundary Runs = 
SUM(player_statistics[fours]) * 4 + SUM(player_statistics[sixes]) * 6

Boundary % = 
DIVIDE(
    [Total Boundary Runs],
    SUM(player_statistics[total_runs]),
    0
)

Avg Boundary % = 
AVERAGEX(
    player_statistics,
    DIVIDE(
        player_statistics[fours] * 4 + player_statistics[sixes] * 6,
        player_statistics[total_runs],
        0
    )
)

Runs Per Innings = 
DIVIDE(SUM(player_statistics[total_runs]), SUM(player_statistics[innings]), 0)

Qualified Batters Flag = 
IF(SELECTEDVALUE(player_statistics[innings]) >= [Min Innings Slicer Value], 1, 0)
```

### `bowler_statistics` measures
```dax
Total Wickets Taken = SUM(bowler_statistics[wickets])

Total Balls Bowled = SUM(bowler_statistics[balls_bowled])

Total Runs Conceded = SUM(bowler_statistics[runs_conceded])

Overall Economy Rate = 
DIVIDE(SUM(bowler_statistics[runs_conceded]) * 6, SUM(bowler_statistics[balls_bowled]), 0)

Best Economy Rate = 
CALCULATE(
    MIN(bowler_statistics[economy]),
    bowler_statistics[balls_bowled] >= 60   -- min 10 overs qualification
)

Min Runs Conceded (Qualified) = 
CALCULATE(
    MIN(bowler_statistics[runs_conceded]),
    bowler_statistics[wickets] >= 5
)

Max Dot Balls = MAX(bowler_statistics[dot_balls])

Dot Ball % = 
DIVIDE(SUM(bowler_statistics[dot_balls]), SUM(bowler_statistics[balls_bowled]), 0)

Avg Dot Ball % = 
AVERAGEX(
    bowler_statistics,
    DIVIDE(bowler_statistics[dot_balls], bowler_statistics[balls_bowled], 0)
)

Wickets Per Match (Proxy) = 
DIVIDE(SUM(bowler_statistics[wickets]), DISTINCTCOUNT(bowler_statistics[bowler]), 0)
```

### `team_statistics` measures
```dax
Total Matches = SUM(team_statistics[matches])

Total Wins = SUM(team_statistics[wins])

Total Losses = SUM(team_statistics[losses])

Overall Win % = 
DIVIDE(SUM(team_statistics[wins]), SUM(team_statistics[matches]), 0) * 100

Best Team Win % = MAX(team_statistics[win_percentage])

Max Team Score = MAX(team_statistics[highest_score])

Avg Team Score = AVERAGE(team_statistics[average_score])

Max Wins = MAX(team_statistics[wins])

Win Loss Ratio = 
DIVIDE(SUM(team_statistics[wins]), SUM(team_statistics[losses]), BLANK())
```

### `venue_statistics` measures
```dax
Total Venues = DISTINCTCOUNT(venue_statistics[venue])

Max Venue Score = MAX(venue_statistics[highest_score])

Min Venue Score = MIN(venue_statistics[lowest_score])

Avg Bat First Win % = AVERAGE(venue_statistics[batting_first_win_percentage])

Avg Chase Win % = AVERAGE(venue_statistics[chasing_win_percentage])

Avg First Innings Score = AVERAGE(venue_statistics[average_1st_innings])

Avg Second Innings Score = AVERAGE(venue_statistics[average_2nd_innings])

Innings Score Drop % = 
DIVIDE(
    AVERAGE(venue_statistics[average_1st_innings]) - AVERAGE(venue_statistics[average_2nd_innings]),
    AVERAGE(venue_statistics[average_1st_innings]),
    0
)

Venue Bias = 
IF(
    [Avg Bat First Win %] > [Avg Chase Win %],
    "Bat First Favored",
    "Chase Favored"
)
```

### `season_statistics` measures
```dax
Total Seasons = DISTINCTCOUNT(season_statistics[year])

Total Runs (Season) = SUM(season_statistics[total_runs])

Total Wickets (Season) = SUM(season_statistics[total_wickets])

Avg Score (Season) = AVERAGE(season_statistics[average_score])

Max Team Score (Season) = MAX(season_statistics[highest_team_score])

Current Season Runs = 
CALCULATE(
    SUM(season_statistics[total_runs]),
    season_statistics[year] = MAX(season_statistics[year])
)

Previous Season Runs = 
CALCULATE(
    SUM(season_statistics[total_runs]),
    season_statistics[year] = MAX(season_statistics[year]) - 1
)

YoY Run Growth % = 
DIVIDE([Current Season Runs] - [Previous Season Runs], [Previous Season Runs], 0)

Current Season Avg Score = 
CALCULATE(
    AVERAGE(season_statistics[average_score]),
    season_statistics[year] = MAX(season_statistics[year])
)
```

> **Note:** Threshold values (e.g. `innings >= 5`, `balls_bowled >= 60`) should ideally be dynamic via a **What-If parameter** (`Min Innings Slicer Value` / `Min Balls Bowled Slicer Value`) rather than hardcoded, so slicers on the report canvas drive qualification thresholds live.

---

## 5. THEME — "Fabric Slate" Design System

**Color Palette (dark-neutral base, single accent — avoids the "rainbow default theme" look):**

| Role | Color | Hex |
|---|---|---|
| Primary Accent | IPL Orange-Red | `#F04E23` |
| Secondary Accent | Deep Teal | `#0E7C7B` |
| Background | Off-white / Charcoal (light/dark mode) | `#F7F7F9` / `#14161A` |
| Card Background | White / Slate | `#FFFFFF` / `#1E2126` |
| Text Primary | Near-black / Off-white | `#1B1D21` / `#EDEDED` |
| Text Secondary (labels) | Grey | `#6B7280` |
| Positive/Win | Green | `#2E9E5B` |
| Negative/Loss | Muted Red | `#D64545` |
| Gridlines | Very light grey | `#E4E4E7` |

**Fonts:**
- Headers / KPI numbers: **Segoe UI Semibold** (or **Lato Bold** if custom fonts enabled) — 24–32pt for KPI values
- Body / axis labels: **Segoe UI**, 9–10pt
- Titles: **Segoe UI Semibold**, 14pt, left-aligned, sentence case (not ALL CAPS — reads as more modern/product-grade)

**Icons:** Minimal line-style icon set (matches, bat, ball, trophy, stadium, calendar) — one small icon per KPI card, top-left corner, colored in the secondary accent, never more than 1 icon per card.

**Card Style:**
- White/slate background, `1px` border in `#E4E4E7` (light mode) or none (dark mode, use elevation instead)
- Border radius: **8px**
- Shadow: subtle, `0 1px 3px rgba(0,0,0,0.08)` — visible on hover only, not static (keeps it clean, not "gamified")
- Padding: 16px internal on all cards and visual containers

**Layout / Grid:**
- 12-column responsive grid; page canvas 1280×720 (16:9, matches standard Power BI service view)
- KPI row: fixed height ~110px
- Consistent 8px gutter between all visual containers
- Every page: Top Nav (48px) → KPI Row (110px) → Primary Visual Row (~260px) → Secondary Visual Row (~260px) → optional Table Row (~200px, scrollable)

**Page Background:** Flat, no gradients, no background images — `#F7F7F9` light mode. Gradients/images read as "template," not "product."

---

## 6. NAVIGATION STRATEGY

| Mechanism | Use For | Reasoning |
|---|---|---|
| **Page Navigator (buttons, top bar)** | Primary page-to-page navigation (Overview ↔ Batting ↔ Bowling ↔ Team ↔ Venue ↔ Season) | Explicit, discoverable, recruiter-friendly — mirrors real product nav bars. Build as a rectangle button group with active-page highlight state (selected page = filled accent, others = outline). |
| **Drillthrough** | Player Drillthrough, Team Drillthrough, Venue Drillthrough | Correct native Power BI pattern for "give me everything about this one entity" — keeps main pages clean while offering depth on demand. |
| **Bookmarks** | Optional "Story mode" toggle on Overview page (e.g. switch KPI row between "All-Time" and "Current Season" view) | Bookmarks are for *state changes*, not page changes — using them for navigation (instead of the Page Navigator) is a common beginner mistake to avoid. |
| **Tooltips (Report Page Tooltips)** | Hover-detail on bar/scatter visuals (e.g. hovering a bar in Top Run Scorers shows a mini stat card) | Adds depth without adding clutter — professional dashboards use custom tooltip pages, not just default tooltips. |
| **Buttons (icon-based)** | Reset filters button (top-right of every page), Back button on drillthrough pages | Every professional dashboard has an explicit reset — don't make users guess how to clear slicers. |

**Do NOT use:** Bookmark-based fake "page navigation" (an anti-pattern), or nested tab visuals mimicking browser tabs — these break Power BI's native selection/export behavior.

---

## 7. UX / PROFESSIONAL PRACTICES

1. **Alignment:** Every visual snaps to the 12-column grid — no freeform placement. Use "Align" + "Distribute" in Power BI's format pane religiously.
2. **Spacing:** Minimum 8px gutter between all containers; never let visuals touch page edges (16px page margin minimum).
3. **KPI placement:** Always top row, left-to-right in order of business importance (volume metrics first, rate/quality metrics after).
4. **Chart placement:** Trend/time visuals go left or top (read first, left-to-right, top-to-bottom — F-pattern eye tracking); ranking/comparison visuals go below or right.
5. **Consistency:** Same chart type answering the same "shape" of question (e.g. Top-N ranking) uses the same visual type across every page — a user shouldn't have to relearn the chart language per page.
6. **Color discipline:** Accent color reserved for the *single most important* series per visual; everything else in neutral greys. Never use more than 3 colors in one visual unless it's a categorical breakdown that requires it.
7. **Titles as insights, not labels:** Instead of "Runs by Team," title it "Which teams score the most runs?" — this is a subtle but real signal of product thinking, and should be used sparingly (2–3 pages, not every single visual, to avoid feeling gimmicky).
8. **Number formatting:** Runs/wickets as whole numbers with thousands separators; percentages to 1 decimal; strike rate/economy to 2 decimals — consistent across every card and axis.
9. **Empty/loading states:** Every page should behave gracefully if a slicer selection returns no data (use a measure-driven message card, not a blank visual).
10. **Accessibility:** Maintain 4.5:1 text contrast minimum; never rely on color alone (e.g. win/loss should use color **and** a +/- icon or label).

---

## 8. FINAL DASHBOARD SUMMARY

**Structure:** 6 primary pages + 3 hidden drillthrough pages = 9 total pages
**Global elements:** Persistent top nav bar, global reset button, consistent slicer panel per page context
**Total KPI cards:** 22 across all pages (~5–6 per page, never more, to avoid dashboard fatigue)
**Total DAX measures:** 35+ core measures, organized by fact table, with What-If parameters for dynamic qualification thresholds
**Visual language:** One accent color (IPL orange-red) + one secondary (teal) + neutral greys; flat cards, 8px radius, hover-only shadow; Segoe UI/Lato typography
**Navigation:** Page Navigator buttons (primary) + Drillthrough (entity depth) + Report Page Tooltips (micro-detail) + Bookmarks (state toggles only)

This structure mirrors what a **Fortune 500 sports/media analytics team** (e.g., a broadcaster's internal BI team or a fantasy-sports product) would ship: clean executive rollup → domain-specific deep dives → entity-level drillthrough, all under one consistent design system rather than six independently styled pages.

---

*End of blueprint. No .pbix file generated per request — this document is the complete design specification to build the report in Power BI Desktop.*
