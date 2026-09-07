# Household Chore Tracker — MVP Scope

## Problem
Chores get forgotten or left undone, and disagreements happen over who was supposed to do what on a given day.

## Goal
Give the household a shared, always-visible view of this week's chores and who's responsible for each one, without automation that could feel punitive or unfair.

## Core Flow
1. **Weekly planning session** — the group opens the app together and defines the week's chore list, assigning each chore to a person.
2. **Daily use** — anyone can open the app, log in with their PIN, and check off chores as they complete them.
3. **Missed chores** — if a chore isn't checked off, it simply stays visibly undone. No punishment, no auto-reassignment.
4. **History review** — anyone can look back at past weeks to see who completed or missed which chores.

## In Scope (MVP)
- **Platform**: single shared web app, works on any device (phone, tablet, laptop)
- **People**: household members set up once, each with a name and a PIN
- **Login**: simple PIN entry to identify who's taking an action (no passwords, no accounts/email)
- **Weekly chore list**: created fresh each week — add chore name + assign to a person
- **Completion tracking**: checkbox per chore; records who checked it and when
- **Current week view**: shows all chores, assignee, and status at a glance
- **History view**: past weeks' chores with completed/missed status per person
- **Data**: shared across all household members' devices (everyone sees the same board)

## Explicitly Out of Scope (for MVP)
- Auto-assignment or workload-balancing logic
- Reminders/notifications/nagging
- Auto-reassigning missed chores
- Photo proof or peer verification of completion
- Recurring/templated chore lists (each week is defined manually)
- Multiple households / multi-tenant support
- Real accounts, passwords, or email-based login

## Success Looks Like
- Every household member can see, at any time, what's due this week and who owns it.
- "I didn't know that was my job" and "I did do that" disputes go away because the board is the shared source of truth.
- Missed chores are visible in history — enough for an honest conversation, without the app playing enforcer.

## Open Questions for Later (Post-MVP)
- Should the weekly list carry over defaults from last week to save setup time?
- Should there be a lightweight "swap" mechanic between two people?
- Any interest in a simple completion streak or fairness stat, once trust in the tool is established?
