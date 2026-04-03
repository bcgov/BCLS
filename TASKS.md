# Tasks

**Now**
- Validate the hub embeds each child dashboard correctly (especially Life Sciences + Macro).
- Verify the macro Employment/Labour Force/Unemployed chart renders correctly after `Update Data`.
- Verify the industry movers table populates (default month is most recent) and month selector works.

**Next**
- Build the standalone Look West dashboard in `dashboards/look_west_strategy/html/dashboard.html`.
- Build the standalone Projects dashboard in `dashboards/projects/html/dashboard.html`.
- Replace sector placeholders with real dashboards and workbook-driven content as Excel files arrive.
- Decide final names for sector 9 and sector 10 and rename placeholders accordingly.

**Blocked**
- Final naming for the remaining two sector dashboards is missing.
- Root `data/00_reference` could not be archived because it was locked by another process.

**Recently Done**
- Reorganized the repo into dashboard-specific folders.
- Added the `BC Dashboard Hub` parent dashboard.
- Copied the legacy macroeconomy and Life Sciences dashboards into the new structure.
- Archived the previous mixed root layout.
- Removed/hid legacy headers and “mock/sample” ribbons in macro and Life Sciences to better support embedding.
- Implemented macro employment KPI cards (Employment, Unemployment Rate, Labour Force) with MoM + YoY deltas.
- Converted the macro employment chart to a combined view (Employment + Labour Force lines + Unemployed bars with fixed right-axis range).
- Added an industry movers table (top 5 gainers / bottom 5 losers by MoM change) to the macroeconomy dashboard.
