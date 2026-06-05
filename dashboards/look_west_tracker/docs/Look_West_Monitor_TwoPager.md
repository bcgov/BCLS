# BC Insights Dashboard — Look West Monitor
### Purpose, Audience, Phasing & Workflow · *Two-Pager*
*Draft v0.1 — 2026-06-04 · Owner: Mehdi Naji · For sign-off by: Kevin, Jacquelyn*

---

## 1. What it is
The **Look West Monitor** is the executive-facing layer of the **BC Insights Dashboard**. It sits on top of the **Look West Data Hub** — a single, comprehensive **source of truth** that consolidates the strategy's targets, announcements, funding, policy, infrastructure, investment-promotion, and major-project activity into one governed data model.

**The Data Hub holds the truth; the dashboard makes it legible.** The Monitor is a user-friendly interface that both *exposes the hub* and *illustrates progress* against the Look West strategy.

## 2. Who it's for
**Executives.** Leadership should see at a glance — *what the strategy committed to, what's moving, where it stands, and where the gaps are* — without touching the underlying spreadsheets. Depth lives in the hub; the page surfaces the high-level signal.

## 3. What it answers (per target)
For each Look West target: the **metric(s)** that show progress, **current status** (not started · initiated · in progress · complete), **investment** where relevant (amount, allocated?, recipient, how spent), **data availability**, and **who owns** the data/delivery. Where a metric has no quantified data yet, the Monitor shows a **qualitative narrative** plus an explicit **data-gap flag** — never a blank.

## 4. Scope & phasing
- **Phase 1 (now → 2026-06-11):** High-level Monitor page covering **only** the targets on strategy **pp. 5–9** and the **p. 53 "Look West: What's Next"** short-/medium-/long-term grid. Establish the target inventory, metric mapping, status, ownership, and gap flags.
- **Phase 2:** Extend to the **full target set** already in the `Targets` table; wire `Target Tracker` progress (current value, progress %).
- **Phase 3:** Layer in live **progress feeds** (announcements, funding, infrastructure, major projects, policy) linked to each target via Pillar / Theme / Sector.
- **Phase 4:** Automated refresh + a standing **data-gap outreach** workflow.

## 5. How it works (data model)
The Monitor reads the hub's **`Targets`** (definition, metric, baseline, target value, timeline) joined to **`Target Tracker`** (current value, progress %, update date), enriched by activity trackers (funding / infrastructure / major projects / etc.) and governed by the **`Workflow and Ownership Registry`** and **`Datasets Status`**. No data is duplicated into the page; the hub remains canonical.

## 6. Workflow & governance
- **Who's in charge:** every dataset has an **Owner + Backup Owner** and a **Workflow Stage** in the Ownership Registry; the lead (**Mehdi**) coordinates; **Daniel** supports data assembly/validation.
- **Metrics per target:** defined once in `Targets.Metric` with `Baseline` / `Target Value`; progress tracked in `Target Tracker`.
- **Cadence:** each dataset carries an **Update Frequency** in `Datasets Status`; refresh follows that cadence.
- **When data is missing:** (1) **flag** the target as *data-gap* on the page; (2) substitute a **qualitative narrative**; (3) **identify the responsible team/sector** via the Ownership Registry; (4) the lead **requests** the data from that owner. Nothing is silently left blank.

## 7. Roles
| Role | Person | Responsibility |
|---|---|---|
| Director | **Jacquelyn** | Oversight & sign-off |
| Supervisor | **Kevin** | Oversight & sign-off |
| Project lead | **Mehdi** | Design, delivery, coordination |
| Analyst | **Daniel** | Data gathering & validation (incl. sourcing metrics not yet held) |
| Dataset Owners | per Registry | Supply & approve data per cadence |

## 8. Timeline
- **Two-pager sign-off:** 2026-06-05
- **Phase 1 (Look West Monitor page) delivery target:** 2026-06-11
- **Daniel onboarded (runs dashboard) + feedback gathered:** 2026-06-11
