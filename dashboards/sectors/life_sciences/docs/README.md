# Life Sciences

- HTML entry point: `html/dashboard.html`
- Canonical workbook (lightweight schema): `data/Life_Sciences_light.xlsx`
- Legacy workbook (backward-compatible): `data/Life_Sciences.xlsx`
- Source copied from the archived legacy Life Sciences standalone dashboard.

Chart configuration model (Excel-first):
- Use `CHART_CATALOG` to control chart visibility/order/title/subtitle/caveat for whole-sector charts.
- Keep `subsector_id` as `ALL` in `CHART_CATALOG` (subsector-specific chart toggles are no longer used).
- Set `data_sheet` for each chart row to point to the sheet that feeds that chart.
- Prefer one sheet per chart data domain, for example: `DATA_GDP_TREND`, `DATA_BIZ_COUNT`, `DATA_EXPORTS`.
- If `CHART_CATALOG` is missing, dashboard falls back to built-in defaults.
- Legacy `CHART_DATA` is still supported as a fallback for backward compatibility.
