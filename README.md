# BCLS Dashboard Workspace

## Runtime Model (Hub-First)
- Single entrypoint: `dashboard/hub/html/dashboard.html`
- Child dashboards are now **embed-only** pages (loaded by the hub in tabs/iframes).
- If a child dashboard is opened directly, it auto-redirects back to the hub tab.
- Optional debug escape hatch for direct child testing: append `?standalone=1`.

## Canonical Source
- Edit only canonical source folders:
  - `dashboard/`
  - `data/`
  - `shared/`
- Treat `dist/BCLS_Dashboard_App/` and `spfx/bcls-dashboard-spfx/sharepoint/assets/BCLS-Dashboard/` as generated runtime targets.
- Those generated folders are intentionally **not tracked in git** to keep the repo lightweight.

## Sync Generated Targets
- Run after source changes:
  - `powershell -ExecutionPolicy Bypass -File scripts/sync_runtime_targets.ps1`
- Dist-only:
  - `powershell -ExecutionPolicy Bypass -File scripts/sync_runtime_targets.ps1 -SkipSpfx`
- SPFx-only:
  - `powershell -ExecutionPolicy Bypass -File scripts/sync_runtime_targets.ps1 -SkipDist`

## Local Run
- Start local server:
  - `python scripts/serve.py`
- Open:
  - `http://localhost:8080/dashboard/hub/html/dashboard.html`
