# Decisions

- Parent dashboard name is `BC Dashboard Hub`.
  Rationale: clear umbrella naming for embedded child dashboards.
  Consequence: docs/server links use hub paths.

- Folder standard is per-dashboard `html/`, `data/`, `docs/`.
  Rationale: independent maintainability and clear ownership.
  Consequence: new dashboards should follow this layout.

- Hub integration uses iframes to embed child `html/dashboard.html` files.
  Rationale: keep child dashboards independently editable.
  Consequence: parent should avoid duplicating child chart logic.

- Life Sciences charts are treated as sector-level (not subsector-level).
  Rationale: simplify UX and avoid per-subsector chart visibility complexity.
  Consequence: chart config rows should use `subsector_id = ALL` in `CHART_CATALOG`.

- Life Sciences display controls (`Select KPIs`, `Select Charts`, `Select Goals`) are local-cache only.
  Rationale: user-specific temporary layout control without mutating workbook data.
  Consequence: settings persist in browser localStorage, not in Excel.

- Life Sciences subsector content is summarized inline inside top sector definition.
  Rationale: reduce page complexity after removing subsector section.
  Consequence: no standalone subsector definition panel in current layout.

- Dashboard Hub footer removed.
  Rationale: cleaner shell chrome around embedded dashboards.
  Consequence: status/provenance text must live elsewhere if needed.

- Life Sciences dashboard data source is strict single workbook: `Life_Sciences_light.xlsx`.
  Rationale: prevent split-source drift and simplify maintenance.
  Consequence: legacy `Life_Sciences.xlsx` fallback removed.

- Windows handoff format is ZIP + Python prerequisite (no installer).
  Rationale: fastest user distribution path without deployment work.
  Consequence: package includes `BC_Dashboard_App.bat` and one-page setup doc.

- Startup flow standardized to `scripts/serve.py` / `BC_Dashboard_App.bat`; launcher stack removed.
  Rationale: reduce runtime complexity and user confusion from multiple windows/entrypoints.
  Consequence: `run_dashboard_launcher.bat` and related launcher code/files were deleted.

- `scripts/serve.py` must tolerate occupied ports.
  Rationale: avoid WinError 10048 on machines with existing local servers.
  Consequence: server now selects from preferred ports and falls back to any free port.
