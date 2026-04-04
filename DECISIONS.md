# Decisions

- Parent dashboard name is `BC Dashboard Hub`.
  Rationale: clearer than "mother dashboard".
  Consequence: docs/server links use hub paths.

- Folder standard is per-dashboard `html/`, `data/`, `docs/`.
  Rationale: independent maintainability and clear structure.
  Consequence: new dashboards should follow this layout.

- Hub integration uses iframes that embed child `html/dashboard.html` files.
  Rationale: keeps child dashboards independent.
  Consequence: child changes flow into hub without duplication.

- Legacy assets are archived, not deleted.
  Rationale: preserve rollback/history.
  Consequence: `archive/` is non-active unless restoring.

- Macro industry movers table uses fixed, hardcoded BC vectors from StatsCan table `14-10-0355-01` (no runtime metadata discovery).
  Rationale: deterministic behavior in this environment.
  Consequence: vector/map updates are manual if StatsCan changes.

- Macro dataset source tags (`.ds-tag`) are clickable links to StatCan table pages (`tv.action?pid=...`) and open in new tabs.
  Rationale: direct source traceability from each chart.
  Consequence: dataset code formatting must stay consistent for link generation.

- Trade chart axes are fixed:
  - Interprovincial: left `10–40`, right `-20–20` ($B)
  - International: left `50–100`, right `-40–20` ($B)
  Rationale: consistent visual framing/comparison.
  Consequence: revisit bounds if values move outside these ranges.

- Macro KPI order is fixed as: GDP, Inflation, Employment, Unemployment, Labour Force.
  Rationale: top-line macro first, labour detail second.
  Consequence: future KPI additions should preserve this order unless explicitly changed.
