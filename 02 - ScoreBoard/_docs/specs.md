# Football Scoreboard — Frontend MVP

Build the frontend for a football/soccer scoreboard web application.

## 1. Technology

Use:

* **Node.js**
* **Next.js** with React
* TypeScript
* Tailwind CSS
* Modern component architecture
* Responsive design optimized for **tablet + desktop**
* Dark mode only

The application should be structured so that a real sports-data API can be connected later without rewriting the UI.

For now, use **mock data** that closely resembles the structure expected from a football sports-data provider.

Do not build the backend or database yet.

---

# 2. Product Goal

The product is a football scoreboard for fans.

Users should be able to:

* See today's football matches
* See live matches
* See upcoming matches
* See recently completed matches
* Browse leagues
* Browse/search teams
* Follow up to 10 teams
* View a team's fixtures and results
* View league standings from a team page
* Open a match center
* Follow live match events
* See lineups and basic statistics
* Receive UI representations of goal/match-start notifications

The application should feel like a polished production football-scoreboard product, not a prototype dashboard.

---

# 3. Navigation

Create a persistent navigation structure:

* Home
* Leagues
* Teams

Include Settings as a separate page accessible from the application header/navigation area.

---

# 4. Home Page

The home page is the primary screen.

Display matches in this priority:

1. Live matches
2. Upcoming matches
3. Completed matches from the previous 24 hours

If the user follows teams:

* Followed-team matches should be **highlighted**
* Followed-team matches should be **pinned toward the top**
* Other matches can appear underneath

Also display popular matches involving the biggest teams.

If the user follows no teams:

* Show today's matches

There should be **no filter controls** on the home feed.

Every match should display:

* Competition
* Home team
* Away team
* Team crests/placeholders
* Match date
* Match time
* Match status
* Score when available

Use the browser's local timezone for match times.

Always show both the **date and time**.

---

# 5. Match Cards

Create reusable match-card components.

Example states:

### Upcoming

```text
Premier League

Arsenal
vs
Chelsea

12 Sep 2026
20:00
```

### Live

```text
Premier League
LIVE

Arsenal       2
Chelsea       1

67'
```

### Completed

```text
Premier League
FULL TIME

Arsenal       2
Chelsea       1

12 Sep 2026
```

Followed-team matches should have a clear visual distinction.

---

# 6. Match Center

Clicking a match opens a dedicated match-center page.

The primary match-center view should show:

### Header

* Competition
* Date
* Kickoff time
* Match status
* Home team
* Away team
* Score

### Timeline

Show events chronologically.

Events supported in MVP:

* Goals
* Yellow cards
* Red cards
* Substitutions

Example:

```text
67'  🔴 Substitution
     Arsenal — Player A → Player B

54'  🟨 Yellow Card
     Chelsea — Player Name

32'  ⚽ Goal
     Arsenal — Player Name

12'  ⚽ Goal
     Chelsea — Player Name
```

### Lineups

Show:

* Starting XI
* Substitutes

Organize them clearly by team.

### Basic Statistics

Initially support:

* Possession
* Shots
* Shots on target
* Corners

Structure the frontend so advanced statistics such as xG, passes, tackles, etc. can be added later.

---

# 7. Real-Time Data Architecture

The frontend must be designed for real-time updates.

Create an abstraction such as:

```text
MatchDataProvider
```

The UI should not directly depend on mock data.

For example:

```ts
interface MatchDataProvider {
  getMatches(): Promise<Match[]>
  getMatch(id: string): Promise<Match>
  getTeam(id: string): Promise<Team>
  getLeague(id: string): Promise<League>
}
```

Create a mock implementation initially.

Later this can be replaced with a real sports-data API.

Design the state architecture so live match updates can eventually arrive through:

* WebSockets
* Server-Sent Events
* Provider webhook → backend → frontend

Do not hardcode the UI around polling.

---

# 8. API Failure State

If live/API data becomes unavailable, the UI should support:

```text
Last updated 2 minutes ago
STALE DATA
```

Continue displaying the last known data.

Create reusable states for:

* Loading
* Empty
* Error
* Stale data

---

# 9. Leagues Page

Create a leagues page.

Users can:

* Browse leagues
* Search leagues

Initial example competitions:

* Premier League
* La Liga
* UEFA Champions League
* Serie A
* Bundesliga
* Ligue 1

Unsupported leagues should appear as:

```text
Coming soon
```

Do not make unsupported leagues appear functional.

---

# 10. Teams Page

Users can:

* Search teams
* Browse teams by league

Each team should have:

* Name
* Crest
* Country
* League/competition
* Follow/unfollow control

Users can follow a maximum of **10 teams**.

When the limit is reached, clearly explain that another team must be unfollowed before adding a new one.

Users can unfollow a team at any time.

---

# 11. Team Page

The team page should contain:

### Team Header

* Crest
* Team name
* Country
* Follow/unfollow button

### Current Season

Display:

* Full season fixtures
* Full season results

The team can participate in multiple competitions.

Allow the user to switch between:

* Domestic competitions
* European competitions
* International matches

Only the **current season** is required.

Do not implement historical season selection.

### League Standings

Show the full league table associated with the competition.

Example:

```text
POS  TEAM             P   W   D   L   GD   PTS
1    Arsenal          10  8   1   1   +16  25
2    Chelsea           10  7   2   1   +11  23
...
```

There is no separate global standings page in this MVP.

---

# 12. User Preferences

Users can use the application without creating an account.

For anonymous users:

* Store followed teams locally in the browser.

Use something like:

```text
localStorage
```

The architecture should make it easy to replace this with server-side persistence later.

Users can optionally create an account.

Authentication UI should support:

* Email
* Password

Do not implement:

* Social login
* Password reset
* Password recovery

Account synchronization can be represented with frontend placeholders for now.

---

# 13. Settings Page

Create a dedicated Settings page.

Include:

* Account status
* Followed teams
* Notification preferences
* Basic application information

Notification options:

* Match starts
* Goals

The UI should make it clear that notifications require browser permission where applicable.

---

# 14. Notifications

The frontend should have a notification architecture ready for:

### Match start

```text
Arsenal vs Chelsea
Match starting now
```

### Goal

```text
GOAL
Arsenal 2–1 Chelsea
67' Player Name
```

For the frontend MVP, notification behavior can be mocked.

Do not build a notification backend yet.

---

# 15. First Visit

When a user first opens the application:

**Do not force onboarding.**

Immediately show today's matches.

The user can optionally browse Teams and follow teams later.

---

# 16. Visual Design

The product should look like a premium modern sports application.

Requirements:

* Dark mode only
* Clean typography
* Strong visual hierarchy
* Compact match cards
* Clear live indicators
* Strong score emphasis
* Subtle borders and surfaces
* Smooth hover states
* Good spacing
* Desktop-first but tablet responsive

Avoid:

* Excessive gradients
* Excessive animations
* Huge hero sections
* Generic SaaS dashboard styling

The experience should feel like a **professional football scoreboard**.

---

# 17. Responsive Layout

Primary targets:

### Desktop

Use a multi-column layout where appropriate.

Example:

```text
┌──────────────────────────────────────────────────────┐
│ Header                                               │
├──────────────┬───────────────────────────────────────┤
│ Navigation   │ Main content                          │
│              │                                       │
│ Home         │ Live matches                          │
│ Leagues      │ Upcoming matches                      │
│ Teams        │ Completed matches                     │
│              │                                       │
└──────────────┴───────────────────────────────────────┘
```

### Tablet

Collapse the layout appropriately while keeping navigation and match information easily accessible.

Do not optimize primarily for phones.

---

# 18. Component Architecture

Create reusable components rather than putting everything into page files.

Suggested structure:

```text
components/
  layout/
  navigation/
  matches/
    MatchCard
    MatchList
    MatchStatus
    ScoreDisplay
  match-center/
    MatchHeader
    MatchTimeline
    MatchEvent
    Lineups
    Statistics
  teams/
    TeamCard
    TeamHeader
    FollowButton
    TeamFixtures
    TeamResults
  leagues/
    LeagueCard
    LeagueSearch
  standings/
    StandingsTable
  notifications/
  ui/

lib/
  api/
  mock/
  auth/
  preferences/
  notifications/

types/
  match.ts
  team.ts
  league.ts
  player.ts
```

Adjust the structure if you have a better architecture, but maintain clear separation of concerns.

---

# 19. Data Types

Create strongly typed models.

At minimum:

```ts
type MatchStatus =
  | "scheduled"
  | "live"
  | "halftime"
  | "finished"
  | "postponed"
  | "cancelled";

type MatchEventType =
  | "goal"
  | "yellow_card"
  | "red_card"
  | "substitution";
```

Create models for:

* Match
* Team
* League
* Player
* MatchEvent
* Lineup
* MatchStatistics
* Standing

Do not use `any` for core domain models.

---

# 20. Mock Data

Create realistic mock data for:

* Multiple leagues
* Multiple teams
* Live matches
* Upcoming matches
* Completed matches
* Match events
* Lineups
* Substitutes
* Basic statistics
* League standings

Include enough data to demonstrate the complete product without requiring an API.

---

# 21. Important Product Rules

Implement these rules:

* Maximum 10 followed teams
* Users can unfollow anytime
* Followed-team matches are pinned/highlighted
* No match search
* No match sharing
* No home-feed filters
* No separate standings page
* Current season only
* Full season fixtures
* Full season results
* Full league table on team pages
* All competitions supported by the data provider
* Unsupported leagues show "Coming soon"
* Browser/local timezone
* Always show date + time
* Dark mode only
* Tablet + desktop
* Optional account
* Email/password authentication UI
* No password reset
* No terms/privacy acceptance gate
* First visit immediately shows today's matches

---

# 22. Backend Boundary

Do **not** build a backend yet.

However, structure the frontend so that the following can later be connected:

```text
Frontend
   ↓
Application API
   ↓
Sports Data Provider
```

The frontend should never need to know the provider's raw API format.

Use an internal normalized data model.

---

# 23. Definition of Done

The frontend MVP is complete when a user can:

1. Open the app and immediately see today's matches.
2. Browse live/upcoming/recent matches.
3. Open a match center.
4. View its score and event timeline.
5. View lineups and basic statistics.
6. Browse leagues.
7. Search leagues.
8. Browse teams by league.
9. Search teams.
10. Follow up to 10 teams.
11. Unfollow teams.
12. See followed matches prioritized on Home.
13. Open a team page.
14. View its full current-season fixtures.
15. View its full current-season results.
16. View the relevant full league table.
17. Switch between the team's competitions.
18. Use the app without creating an account.
19. See account/settings UI.
20. Experience realistic loading, empty, error, and stale-data states.

Build the application as if the real sports API will be connected immediately after the frontend is approved.

Do not add features outside this specification without explicitly identifying them as optional.
