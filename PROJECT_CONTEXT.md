# Project Context

**What This Project Is**
A dashboard workspace with 13 standalone dashboards plus one parent dashboard named `BC Dashboard Hub`.

**Current Goal**
Keep each dashboard independently editable in its own folder while the parent hub automatically reflects those child dashboards through embedding.

**Stack**
- Frontend: standalone HTML dashboards
- Data: dashboard-specific Excel files stored beside each dashboard in `data/`
- Local server: `scripts/serve.py`

**Architecture Summary**
- `dashboards/bc_dashboard_hub/html/dashboard.html` is the parent dashboard.
- `dashboards/bc_macroeconomy/html/dashboard.html`, `dashboards/look_west_strategy/html/dashboard.html`, `dashboards/projects/html/dashboard.html`, and `dashboards/sectors/*/html/dashboard.html` are standalone child dashboards.
- Each dashboard folder follows `html/`, `data/`, `docs/`.
- Legacy material is preserved under `archive/`.

**Key Constraints**
- The parent hub should embed child dashboards, not duplicate their implementation.
- Each child dashboard should keep its own workbook in its own `data/` folder.
- Two sector placeholders are currently reserved because only 8 sector names are explicit in the repo/user notes, while the target structure calls for 10 sectors total. (Uncertain)

**Conventions**
- Entry point for every dashboard is `html/dashboard.html`.
- Workbook files live in the same dashboard folder under `data/`.
- Shared visual assets live in `shared/assets/`.

**Important Files**
- `C:/Users/smehd/BCLS/dashboards/bc_dashboard_hub/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/bc_macroeconomy/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/html/dashboard.html`
- `C:/Users/smehd/BCLS/scripts/serve.py`
- `C:/Users/smehd/BCLS/README.md`

**Current Status**
- New dashboard-per-folder structure is in place.
- Parent hub embeds the standalone macroeconomy, strategy, projects, and sector dashboards.
- Life Sciences is the only sector with a copied live workbook/dashboard; the other child dashboards are placeholders.
- Old root `code/`, `docs/`, `output/`, and most of `data/` were moved into `archive/restructure_2026-04-02/root_working_state/`.

**Top Next Steps**
- Verify the hub and all child dashboard links render correctly in the browser.
- Decide the final names for the remaining two sector placeholders.
- Add real standalone dashboards and Excel workbooks for Look West, Projects, and the remaining sectors.
