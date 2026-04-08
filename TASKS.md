# Tasks

**Now**
- Validate Windows ZIP handoff package on a non-dev laptop.
- Keep `serve.py` runtime stable with auto-port behavior + StatsCan update flow.

**Next**
- Add lightweight versioning/release note file for each shipped ZIP.
- Continue UI polish for Hub cards and consistency pass for remaining dashboards.
- Optional: simplify `serve.py` proxy internals after stable validation.

**Blocked**
- `rg.exe` unavailable in this environment (`Access is denied`), slowing bulk search/refactor tasks.

**Recently Done**
- Life Sciences: removed `LIVE DASHBOARD`/`DATA:` top-box lines and cleaned subtitle `?` artifacts.
- Life Sciences: enforced single-source workbook (`Life_Sciences_light.xlsx`); removed unused legacy workbook/template.
- Hub sectors page: 4-card row layout, card footer changed to `Last updated`/`Coming Soon`, top counters removed.
- Runtime: `scripts/serve.py` now auto-selects free port to avoid WinError 10048.
- Distribution: created `BC_Dashboard_App.bat`, one-page install guide, zip packaging script, and `dist/BCLS_Dashboard_App.zip`.
- Cleanup: removed launcher-related files per user request.
