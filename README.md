# BCLS Dashboard Workspace

## Structure
- `dashboards/bc_dashboard_hub/`: parent dashboard that embeds the standalone dashboards.
- `dashboards/bc_macroeconomy/`: standalone BC macroeconomy dashboard.
- `dashboards/look_west_strategy/`: standalone Look West strategy dashboard.
- `dashboards/projects/`: standalone projects dashboard.
- `dashboards/sectors/<sector_name>/`: standalone sector dashboards, each with its own `html/`, `data/`, and `docs/` folders.
- `shared/assets/logo/`: shared image assets reused across dashboards.
- `scripts/serve.py`: local UTF-8 web server for the restructured workspace.
- `archive/`: legacy dashboards and pre-restructure working state.

## Conventions
- Each dashboard folder is self-contained: `html/` for the dashboard, `data/` for workbook inputs, `docs/` for notes.
- The parent dashboard should only embed child dashboards and should not duplicate their implementation logic.
- When a child dashboard is updated, the parent hub updates automatically because it points to the child `html/dashboard.html` file.
