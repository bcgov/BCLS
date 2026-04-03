# Decisions

- Parent dashboard name: `BC Dashboard Hub`.
  Rationale: clearer than "mother dashboard" and describes its role as the entry point that connects standalone child dashboards.
  Consequence: docs and local server now point to the hub path.

- Folder standard: each dashboard lives in its own folder with `html/`, `data/`, and `docs/`.
  Rationale: makes dashboards independently maintainable and easy to locate.
  Consequence: the root folder is cleaner and new dashboards should follow the same pattern.

- Integration method: the parent hub embeds child dashboards with iframes.
  Rationale: preserves dashboard independence and lets child dashboards evolve separately.
  Consequence: changes to child `html/dashboard.html` files automatically appear in the hub.

- Legacy assets are archived instead of deleted.
  Rationale: preserves working history and reduces risk while restructuring.
  Consequence: `archive/` is part of the workspace and should not be treated as active implementation.

- Sector count is structured as 10, but only 8 named sectors are currently explicit in repo/user notes. (Uncertain)
  Consequence: `future_sector_01` and `future_sector_02` are temporary placeholders until final names are confirmed.

- Macro employment KPIs and the combined Employment/Labour Force/Unemployed chart use Statistics Canada LFS (Table `14-10-0287-01`) vectors for BC SA 15+:
  - Employment `v2064701` (vec `2064701`)
  - Labour force `v2064700` (vec `2064700`)
  - Unemployment rate `v2064705` (vec `2064705`)
  Rationale: supports consistent monthly MoM/YoY deltas across employment + labour force + unemployment rate.
  Consequence: the “Unemployed” bars are derived as (Labour force − Employment) from the same LFS series; the right axis is fixed to 0–500k (thousands).

- Child dashboards hide standalone headers/banners when they interfere with embedding (CSS hide vs. removing DOM/JS).
  Rationale: minimal-risk change that preserves dashboard internals while avoiding duplicate chrome inside iframes.
  Consequence: if a dashboard needs a true standalone header later, this rule may need to be conditional (standalone vs embedded).

- Macro “industry movers” table uses hardcoded BC industry employment vectors from StatsCan table `14-10-0355-01` instead of WDS cube metadata discovery at runtime.
  Rationale: runtime metadata calls were unreliable in this environment; hardcoding keeps the dashboard deterministic.
  Consequence: if StatsCan changes vectors/labels, the mapping must be updated manually.
