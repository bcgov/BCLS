# Look West Monitoring Dashboard & Data Workflow — Work Plan
*Draft v0.2 — 2026-06-11 · Owner: Mehdi Naji · For review & sign-off by: Jacqueline (Director) · Companion to the [Look West Monitor Two-Pager](./Look_West_Monitor_TwoPager.md)*

---

## 1. Purpose
This work plan explains how we will **gather, validate, organize, and report reliable data** to monitor progress under the **Look West Strategy**. It covers two things side by side: the **data workflow** (how trustworthy data reaches a single source of truth) and the **dashboard workflow** (how that data is turned into an executive-friendly monitoring tool and deployed to the people who need it).

The end product is a **Look West Monitor** dashboard, backed by a governed **Look West Data Hub**, that lets leadership see at a glance what the strategy committed to, what is moving, where it stands, and where the gaps are — without touching underlying spreadsheets.

## 2. Current context
The Look West Strategy sets out a hierarchy of **goals and targets** organized by **Stream → Pillar → Theme**. Monitoring progress requires a metric (or set of metrics) for each goal, reliable data behind each metric, and a way to report it clearly. Today that data is **fragmented** across public statistics, internal team spreadsheets, and government announcements, with no single validated source and no executive-facing view of progress. This work plan closes that gap by **end of summer**.

## 3. Where we are right now
- **Data Hub schema designed.** A 13-table model exists (`Targets`, `Target Tracker`, funding/policy/infrastructure/investment-promotion/major-project trackers, announcements/news, and reference dimensions for Stream/Pillar/Theme/Sector/Region/Timeframe). See `look_west_schema.csv`.
- **Dashboard prototype built.** An **HTML-based** Look West Monitor and five tracker subpages exist (`dashboard/look_west_tracker/`). HTML was chosen over Power BI for flexibility in design, navigation, interactivity, and UX.
- **Governance scaffolding started.** A `Workflow and Ownership Registry` and `Datasets Status` table define owners, cadence, and approval state.
- **Not yet done:** metrics are not finalized or leadership-approved; most targets lack validated data; the Hub is not yet populated as the source of truth; and the dashboard is **not yet deployed** to an internal environment.

## 4. Proposed approach
Run **two parallel tracks** that meet at a single connection point — the **Data Hub**:

- **Workstream 1 — Data gathering, validation, and Data Hub.** Define metrics, source and validate data, and land it in the Hub as the source of truth.
- **Workstream 2 — Dashboard development, reporting, and deployment.** Connect the dashboard to the Hub, report progress, and deploy it securely to executives and authorized users.

**Guiding rule — Hub-first.** Data flows in one direction: *sources → Data Hub → Dashboard*. Nothing is typed straight into the dashboard. Every figure shown traces back to a validated, owner-approved row in the Hub. This is why the **long pole of the project is sourcing and validating data — not building the page.**

```
   Public sources / Internal teams / Announcements
                      |
                      v
          [ Look West Data Hub ]  <-- source of truth (validated)
                      |
                      v
          [ Look West Monitor dashboard ]  --> Executives & authorized users
```

## 5. Workstream 1 — Data gathering, validation, and Data Hub

### 5.1 Data sources (in priority order)
1. **Reliable public data** — Statistics Canada, BC Stats, and other credible public sources. Preferred wherever it exists (transparent, repeatable, defensible).
2. **Internal government team data** — used when reliable public data is unavailable, or to validate/contextualize public figures.
3. **BC and federal government announcements** — used where relevant (e.g., funding commitments, major projects, investment wins).

### 5.2 From source to Hub — the validation chain
1. **Define the metric** for each goal (see §7).
2. **Source the data** from the best available source above.
3. **Clean & standardize** — align dates (monthly/quarterly), geography (BC / Canada / global), units, and definitions.
4. **Validate** with the relevant internal team / SME to confirm accuracy and credibility.
5. **Land in the Hub** — record in the appropriate table; update `Datasets Status` (owner, source, cadence, last updated, approved by).
6. **Flag gaps** — where data is missing or weak, mark the target *data-gap*, add a short qualitative narrative, and log the responsible owner. **Nothing is left blank.**

### 5.3 The Data Hub as source of truth
The Hub is the **canonical store**: governed, owned, and versioned. Each dataset has an **Owner + Backup Owner** and a **Workflow Stage** in the `Workflow and Ownership Registry`, and a **cadence** in `Datasets Status`. The dashboard never duplicates data — it reads from the Hub.

### 5.4 Maintaining the Hub
- One agreed format per table (flat tables, one row per record, controlled vocabularies for Stream/Pillar/Theme/Sector).
- Refresh on each dataset's stated cadence; manual snapshots are acceptable for the prototype, automation comes later.
- Periodic clean-up checkpoint to catch duplicates, stale rows, and broken links between targets and activity records.

## 6. Workstream 2 — Dashboard development, reporting, and deployment

### 6.1 What the dashboard reports
The Look West Monitor connects to the Hub and will:
- Show **progress against targets, goals, and metrics** (status, current vs. target, progress %).
- Provide an **executive summary** of overall progress.
- **Flag missing or weak data coverage** explicitly.
- **Flag areas below expectations** (off-track / at-risk).
- Show which **goals, targets, sectors, or regions need attention**.
- Include a **snapshot of the broader BC economic context**.
- Help users quickly understand **progress, gaps, risks, and next steps**.

### 6.2 Page structure (executive-scannable)
- **Monitor (executive summary):** per-target status, key metric, investment where relevant, owner, data-availability/gap flag.
- **Targets Tracker:** current value, progress % vs. target.
- **Funding & Investment / Policy & Regulation / Infrastructure / Investment Promotion trackers.**
- **BC economic context** snapshot (key public indicators — employment, GDP, exports, investment).

### 6.3 Technology choice
The dashboard is **HTML-based** (not Power BI) for flexibility in design, navigation, interactivity, and UX. It reads validated data exported/served from the Hub.

### 6.4 Deployment (the key bottleneck)
The HTML dashboard must be deployed somewhere **secure and accessible** to executives and authorized internal users. This requires early coordination with the **government IT team** on hosting options, authentication/access control, and the data-refresh path. **Deployment is started early and in parallel — not left to the end** — because IT approvals and provisioning typically drive the critical path.

## 7. Proposed metrics development process
For every Look West **goal/target**, we propose one or more **practical, reliable metrics**. Each proposed metric is documented against the following template, then consulted with internal teams and approved by leadership before it is "locked" in the Hub.

**Per-metric template:**

| Field | What it captures |
|---|---|
| Goal / target | The Look West goal this metric serves (Stream → Pillar → Theme → Target) |
| Metric | What the metric measures |
| Relevance | Why it is meaningful for this specific goal |
| Data exists? | Whether reliable data already exists |
| Public source? | Whether it can come from a public source (StatsCan/BC Stats) |
| Internal input? | Whether internal teams must provide or validate it |
| Update frequency | How often it should be refreshed |
| Limitations / gaps / risks | Known data limitations, gaps, or risks |
| Baseline / target | Starting point and target value, where available |

**Process:**
1. **Draft metrics** for each goal (Mehdi + Daniel) using the template.
2. **Consult internal teams / SMEs** to confirm each metric is meaningful, reliable, and feasible.
3. **Revise** based on feedback.
4. **Leadership review & approval** (Jacqueline) — the formal checkpoint that locks the metric set.
5. **Populate the Hub** with approved metrics, baselines, targets, and cadence.

## 8. Governance, checkpoints, and approvals
| Checkpoint | What is approved | Who | When |
|---|---|---|---|
| **CP1 — Metrics consultation** | Internal teams confirm metrics are meaningful/feasible | SMEs / data owners | Short-term |
| **CP2 — Leadership metric sign-off** | Approved metric set locked into the Hub | Jacqueline | Short-term (gate to scale Hub) |
| **CP3 — Data validation** | Each dataset validated & marked approved in `Datasets Status` | Owners / Daniel / Mehdi | Ongoing, per cadence |
| **CP4 — Deployment go/no-go** | Hosting, access, and refresh path approved | Government IT + Jacqueline | Medium-term |
| **CP5 — Executive review** | Dashboard meets exec needs; continue/scale | Jacqueline + leadership | End of summer |

Governance is anchored by the `Workflow and Ownership Registry` (ownership) and `Datasets Status` (cadence, approval state). No metric is reported, and no dataset is shown, until it has cleared its checkpoint.

## 9. Engagement pathway with Jacqueline, Daniel, Nathan, and relevant teams
| Person / group | Role in this work | When their input is needed |
|---|---|---|
| **Jacqueline** *(Director / leadership)* | Oversight & **approval** | CP2 metric sign-off; CP4 deployment go/no-go; CP5 executive review |
| **Daniel** *(Analyst)* | **Data input** — sourcing, cleaning, validation into the Hub | Throughout Workstream 1; metric drafting; ongoing refresh |
| **Nathan** *(Technical / IT advice)* | **Technical advice** — hosting, security, deployment path *(confirm role)* | Early scoping of deployment; CP4; refresh automation |
| **Internal teams / SMEs** | Provide & **validate** data; confirm metrics | CP1 consultation; data validation (CP3) |
| **Dataset owners** *(per Registry)* | Supply & approve data per cadence | Ongoing per `Datasets Status` |
| **Mehdi** *(Project lead)* | Design, coordination, delivery, narrative | Throughout both workstreams |

**Engagement cadence:** weekly internal sync (Mehdi + Daniel); biweekly check-ins with dataset owners; early and recurring touchpoints with Nathan / government IT on deployment; scheduled leadership checkpoints at CP2, CP4, CP5.

## 10. Workflow diagram
Two parallel tracks that meet at the Data Hub, with approval, consultation, validation, deployment, and iteration points marked.

```
 WORKSTREAM 1: DATA                              WORKSTREAM 2: DASHBOARD
 ---------------------------------               ----------------------------------
 Public data (StatsCan, BC Stats)                HTML Monitor prototype (built)
 Internal team data                              Define exec views & flags
 Gov't announcements                                      |
        |                                                 |
        v                                                 |
 Draft metrics per goal -----------------+                |
        |                                |                 |
        v                                |  (early, parallel)
 [CONSULT internal teams / SMEs] <-------+                v
        |                                        [ENGAGE Gov't IT / Nathan]
        v                                         hosting * access * refresh
 [LEADERSHIP APPROVAL - metrics]  (Jacqueline)            |
        |                                                 |
        v                                                 |
 Source + clean + standardize data                        |
        |                                                 |
        v                                                 |
 [VALIDATE data with SMEs]                                |
        |                                                 |
        v                                                 |
 ===========>  [ LOOK WEST DATA HUB ]  <==================+   <- TRACKS CONNECT
               source of truth (validated)               |
                       |                                  |
                       +--------------------------------> Connect dashboard to Hub
                                                          |
                                                          v
                                              Report progress / flag gaps & risks
                                                          |
                                                          v
                                              [DEPLOYMENT GO/NO-GO]  (IT + Jacqueline)
                                                          |
                                                          v
                                              Deploy to executives / authorized users
                                                          |
                                                          v
                                          <===== ITERATE & REFINE (feedback loop) =====>
```

**Reading the diagram:** metrics are consulted and **approved by leadership before** data is mass-sourced; validated data lands in the **Hub (the single connection point)**; the dashboard reads from the Hub; **IT engagement runs in parallel from the start** so deployment isn't a late surprise; everything loops back through **iteration and refinement**.

## 11. Timeline and milestones
Target: **process streamlined and dashboard deployed by end of summer.** Dates are indicative and anchor to checkpoints rather than fixed calendar days.

| Horizon | Focus | Key outputs | Gates / dependencies |
|---|---|---|---|
| **Immediate (Weeks 1–2)** | Lock scope; draft metrics; open IT conversation | Metric drafts per goal (template); confirmed dataset owners; initial IT/deployment scoping with Nathan | — |
| **Short-term (Weeks 3–5)** | Consult teams; get metrics approved; begin sourcing | CP1 consultation done; **CP2 leadership metric sign-off**; first validated datasets in Hub | CP2 gates Hub scale-up |
| **Medium-term (Weeks 6–9)** | Populate Hub; build dashboard against real data; lock deployment path | Hub populated across domains; dashboard wired to Hub; **CP4 deployment go/no-go** | CP4 depends on IT provisioning |
| **End of summer (Weeks 10–12)** | Deploy; validate with users; iterate | Dashboard deployed to internal environment; **CP5 executive review**; refined v1 | Deployment requires CP4 cleared |
| **Ongoing** | Maintain & refresh | Cadence-based refresh; standing data-gap outreach; move toward automation | — |

**Key checkpoints on the timeline:** CP1 (consultation) → CP2 (metric approval) → CP3 (rolling data validation) → CP4 (deployment go/no-go) → CP5 (executive review).

## 12. Data blockers, limitations, and risks
| Bottleneck / risk | Impact | Mitigation |
|---|---|---|
| **Finding reliable data** for every metric | Some goals may lack a clean metric | Prefer public sources; allow internal/proxy metrics; flag gaps openly with narrative |
| **Validating accuracy & credibility** | Reporting wrong numbers erodes trust | SME validation step before any figure enters the Hub |
| **Timely input from internal teams** | Slows sourcing & validation | Owner packets + biweekly check-ins; escalate via leadership if blocked |
| **Leadership approval of metrics** | Hub scale-up is gated on CP2 | Early consultation so approval is a confirmation, not a debate |
| **Maintaining a clean Hub** | Drift, duplicates, stale data | Controlled vocabularies, ownership, periodic clean-up checkpoint |
| **Connecting Hub to dashboard** | Manual refresh is brittle | Define a simple, repeatable export/serve path; automate in a later phase |
| **Deploying the HTML dashboard** *(key bottleneck)* | Executives can't access it | Engage government IT early (parallel track); resolve hosting/auth at CP4 |
| **Keeping the dashboard updated** | Decisions made on stale data | Cadence in `Datasets Status`; move from manual snapshots to scheduled refresh |

## 13. Immediate next steps
1. **Confirm dataset owners** from the `Workflow and Ownership Registry`.
2. **Draft metrics** for each Look West goal using the §7 template (Mehdi + Daniel).
3. **Open the deployment conversation** with Nathan / government IT (hosting, access, refresh) — start in parallel now.
4. **Schedule the metrics consultation (CP1)** with internal teams/SMEs.
5. **Book the leadership metric sign-off (CP2)** with Jacqueline.
6. **Stand up the cadence:** weekly internal sync + biweekly owner check-ins.
