# Household Chore Tracker — Backlog

Derived from `plan.md`. Ordered roughly by dependency; each milestone should leave the app in a working, demoable state.

## Milestone 1 — Data Model
- [x] `Person` model: name, PIN (hashed), active flag
- [x] `Week` model: start date, end date (or just start date + auto-computed range)
- [x] `Chore` model: week (FK), name, assigned person (FK), completed flag, completed_by (FK, nullable), completed_at (nullable)
- [x] Register all models in `admin.py` for quick data inspection/debugging
- [x] Initial migration + smoke test in Django admin

## Milestone 2 — PIN Login (no accounts/passwords)
- [x] Login view: pick a person, enter PIN
- [x] Store "acting as `<person>`" in the session on success
- [x] Logout / switch-person view
- [x] Simple decorator/middleware to require a logged-in person for write actions (checking off chores, weekly planning)
- [x] Read-only views (current week, history) stay visible even when no one is "logged in"

## Milestone 3 — Weekly Planning
- [x] "Start new week" action: creates a `Week` with today's date
- [x] Add-chore form: name + assignee, attached to the current week
- [x] Edit/delete a chore within the current (unfinished) week
- [x] Guard against creating a second open week while one is already active (or explicitly allow and just show most recent as "current")

## Milestone 4 — Daily Use / Current Week View
- [x] Current week view: list all chores with assignee and status
- [x] Checkbox to mark a chore complete/incomplete, recording who (session person) and when
- [x] Anyone can view; only the logged-in person can toggle completion (per plan: no punishment/auto-reassignment, so keep this permissive rather than restrictive — maybe any logged-in person can check off any chore, since it's a shared trust-based board)

## Milestone 5 — History View
- [x] List past weeks (most recent first)
- [x] Per-week detail: chores with assignee + completed/missed status, no editing allowed
- [x] Simple visual distinction between "done" and "missed" (no shaming language, just clear status)

## Milestone 6 — Polish
- [x] Minimal responsive templates (works on phone/tablet/laptop per plan's platform requirement)
- [x] Base template with nav: Current Week / History / Login-Switch
- [x] Basic styling pass (can stay plain/functional — no design system needed for MVP)
- [x] Seed/fixture data for local dev (a handful of people + a sample week)

## Milestone 7 — Tests & Hardening
- [x] Model tests: chore completion records correct person/timestamp
- [x] View tests: PIN login success/failure, chore toggle requires login, history is read-only
- [x] Basic PIN brute-force friction (e.g. rate-limit or lockout after repeated failures) — lightweight, since there's no email/password recovery flow to fall back on

## Explicitly Not in This Backlog (per plan's out-of-scope list)
Auto-assignment, reminders/notifications, auto-reassignment of missed chores, photo/peer verification, recurring/templated weeks, multi-household support, real accounts/passwords/email login.
