# Tasks

**Now**
- Stabilize Life Sciences sector dashboard after major layout/interaction changes.
- QA Dashboard Hub embed behavior (single-scroll target for macro iframe + tab navigation integrity).
- Clean remaining visible encoding artifacts in active dashboards.

**Next**
- Finalize and apply the canonical `Life_Sciences_light.xlsx` migration (when workbook is not locked).
- Remove dead/unused subsector-tab code paths from `life_sciences/html/dashboard.html` to reduce maintenance risk.
- Align Look West/Projects dashboards with the same polish and navigation behavior.

**Blocked**
- In-place workbook updates are blocked while `Life_Sciences_light.xlsx` is open/locked.
- `rg.exe` unavailable in this environment (`Access is denied`), slowing bulk search/refactor tasks.

**Recently Done**
- Life Sciences: removed subsector section, moved KPIs into Sector Trends, added subsector tags on KPI cards.
- Life Sciences: sector-level chart model and local cached display toggles (`Select KPIs/Charts/Goals`).
- Life Sciences: integrated subsector definitions into top definition box; removed footer.
- Dashboard Hub: removed footer, simplified top-nav labels/icons, removed duplicate sectors dropdown headers.
- Dashboard Hub: added iframe auto-height fitting + `scrolling="no"` to reduce nested scrollbars.
