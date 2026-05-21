# BC Economy Outlook Dataset

This folder stores the manually-maintained dataset used by the BC Economy Outlook dashboard page.

## Files

- `annual_forecast.csv`: annual forecast metrics (2023-2026) from report tables 2.6.1 to 2.6.3
- `quarterly_conditions_2025.csv`: in-year momentum indicators from table 2.1
- `outlook_metadata.json`: report metadata and summary bullets displayed in the dashboard
- `raw/2025-26-q2-report.pdf`: source report copy used for extraction reference
- `raw/2025-26-q2-report_extracted.txt`: extracted text reference used during dataset build

## Quarterly update process

1. Open the newest Ministry of Finance quarterly report.
2. Update `annual_forecast.csv` with values from the corresponding annual tables.
3. Update `quarterly_conditions_2025.csv` with values from table 2.1.
4. Update metadata fields in `outlook_metadata.json`.
5. Reload dashboard page.
