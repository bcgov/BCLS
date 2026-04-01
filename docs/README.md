# B.C. Life Sciences Sector Dashboard — Look West Strategy
## Internal MVP · Data & Technical Documentation

---

## Quick Start

1. Open a terminal and navigate to the `BCLS` folder.
2. Run:
   ```bash
   python code/serve.py
   ```
3. The dashboard opens at: [http://localhost:8080/code/dashboard.html](http://localhost:8080/code/dashboard.html)

> **Why a server?** Browsers block local file reads for security reasons. The Python script
> spins up a one-line HTTP server and auto-opens the dashboard. No installation required — Python is included with macOS and most Linux/Windows systems.

---

## Project Structure

```
BCLS/
├── code/
│   ├── dashboard.html       ← Single-file HTML+JS+CSS dashboard (main deliverable)
│   └── serve.py             ← One-command local server launcher
├── data/
│   ├── 00_reference/        ← Sector definition and NAICS lookup tables
│   ├── 10_official_sector/  ← Curated BC official metrics (employment, GDP, etc.)
│   ├── 20_public_metrics/   ← Public proxy data (Stats Can, CIHR, etc.)
│   ├── 30_strategy/         ← Look West goals, initiatives, risks
│   └── 40_manual/           ← Manual data layer: evidence, overrides, companies
├── docs/
│   └── README.md            ← This file
└── output/                  ← Folder for exported CSVs and reports
```

---

## CSV File Reference

All files use UTF-8 CSV format. Replace values in any file and refresh the dashboard — no code changes needed.

---

### `data/00_reference/`

#### `sector_definition_notes.csv` ← **Required**
| Column | Type | Description |
|---|---|---|
| `id` | string | Unique row ID (e.g. `DEF-001`) |
| `category` | string | `definition`, `scope`, or `caveat` |
| `heading` | string | Short display heading |
| `body_text` | string | Full text shown in dashboard |
| `caveat` | string | Optional caveat or limitation note |
| `last_updated` | date | YYYY-MM-DD |
| `source_tier` | string | See Source Tiers below |
| `confidence_tag` | string | See Confidence Tags below |

> The row with `id = DEF-001` is used as the main sector definition card in the dashboard header.

#### `subsector_naics_lookup.csv` ← **Required**
| Column | Type | Description |
|---|---|---|
| `subsector_id` | string | Short code (e.g. `PHARMA`) — used as key throughout all CSVs |
| `subsector_name` | string | Display name |
| `naics_codes` | string | Comma-separated NAICS codes |
| `naics_description` | string | Plain-language NAICS description |
| `is_core` | boolean | `TRUE` = core quantitative subsector; `FALSE` = excluded from totals |
| `digital_health_included` | boolean | `TRUE` only for commercialization-linked digital health |
| `dashboard_color` | hex | Chart color for this subsector |
| `sort_order` | integer | Display order in charts and filters |
| `note` | string | Internal note |

---

### `data/10_official_sector/`

#### `official_sector_metrics.csv` ← **Required**
Primary source for all KPI cards and the employment trend chart.

| Column | Description |
|---|---|
| `metric_id` | Stable ID used across all references (e.g. `EMP-TOTAL-BC`) |
| `metric_name` | Human-readable metric name |
| `sector` | Always `life_sciences` (or your sector ID for other sectors) |
| `subsector_id` | `ALL` for sector-wide totals; subsector code for breakdowns |
| `year` | Integer year |
| `value` | Numeric value (leave blank if not available) |
| `unit` | `FTE`, `millions CAD`, `businesses`, `%`, etc. |
| `baseline_year` | Year of the strategy baseline |
| `baseline_value` | Value at baseline year |
| `province` | `BC`, `ON`, `QC`, `AB`, or `Canada` |
| `geography_scope` | `provincial`, `national`, etc. |
| `source` | Source description |
| `source_tier` | See Source Tiers |
| `confidence_tag` | See Confidence Tags |
| `last_updated` | YYYY-MM-DD |
| `note` | Internal note |

> **Supported metric IDs used by dashboard KPI cards:**
> `EMP-TOTAL-BC`, `GDP-TOTAL-BC`, `REV-TOTAL-BC`, `BIZ-COUNT-BC`, `EXP-GOODS-BC`, `EXP-SERV-BC`, `FUND-PUBLIC-BC`
>
> Leaving `value` blank for `EXP-SERV-BC` will show "Not currently available" in the KPI card.

#### `official_sector_region_shares.csv` ← Required for regional chart
| Column | Description |
|---|---|
| `year` | Integer year |
| `region_id` | Region code (e.g. `METROVANCOUVER`) |
| `region_name` | Display name |
| `metric_id` | Links to `official_sector_metrics.metric_id` |
| `metric_name` | Display name |
| `share_pct` | Share of provincial total (%) |
| `value` | Absolute value |
| `unit` | Unit |
| `source_tier`, `confidence_tag`, `last_updated`, `note` | Standard columns |

#### `official_sector_province_compare.csv` ← Required for provincial comparison chart
Same structure as `official_sector_metrics.csv` but covers `BC`, `ON`, `QC`, `AB`, `Canada`.

---

### `data/20_public_metrics/`

#### `public_business_counts.csv`
| Column | Description |
|---|---|
| `year` | Integer |
| `subsector_id` | Subsector code or `ALL` |
| `subsector_name` | Display name |
| `province` | Province abbreviation |
| `size_band` | `1-4 employees`, `5-19 employees`, `20-99 employees`, `100-499 employees`, `500+ employees`, or `ALL` |
| `count` | Business count |
| `source`, `source_tier`, `confidence_tag`, `last_updated`, `note` | Standard |

#### `public_gdp_metrics.csv`
| Column | Description |
|---|---|
| `year` | Integer |
| `subsector_id` | Subsector code |
| `subsector_name` | Display name |
| `province` | Province abbreviation |
| `gdp_type` | e.g. `GDP at basic prices` |
| `value_millions_cad` | Numeric |
| Standard columns | — |

#### `io_multipliers.csv`
| Column | Description |
|---|---|
| `subsector_id` | Subsector code |
| `multiplier_type` | `employment_multiplier`, `gdp_multiplier`, `revenue_multiplier` |
| `value` | Numeric multiplier |
| `year`, `scope`, `source`, standard columns | — |

#### `public_goods_exports.csv`
| Column | Description |
|---|---|
| `year` | Integer |
| `subsector_id` | Subsector code or `ALL` |
| `product_category` | Product type string |
| `destination_country` | Country or `ALL` for totals |
| `destination_region` | Region string |
| `value_millions_cad` | Numeric |
| `yoy_change_pct` | Year-over-year change % |
| `province` | Province abbreviation |
| Standard columns | — |

> For the trend chart, the dashboard uses rows where `destination_country = 'ALL'` and `province = 'BC'`.

#### `public_clinical_trials.csv`
| Column | Description |
|---|---|
| `year` | Integer |
| `phase` | `Phase I`, `Phase II`, `Phase III`, or `ALL` |
| `therapeutic_area` | e.g. `Oncology`, or `ALL` |
| `trial_count` | Integer |
| `sponsor_type` | `Industry`, `Academic`, `Industry + Academic` |
| `location_region` | Region string |
| `status` | `Active`, `Completed`, etc. |
| Standard columns | — |

> For the trend chart, the dashboard uses rows where `phase = 'ALL'`, `province = 'BC'`, and `therapeutic_area = 'ALL'`.

#### `public_funding_projects.csv`
| Column | Description |
|---|---|
| `year` | Integer |
| `program_name` | Grant / program name |
| `funder_type` | `Federal`, `Provincial`, `Mixed` |
| `funder_name` | Organization name |
| `recipient_subsector` | Subsector code or `ALL` |
| `amount_millions_cad` | Numeric |
| `project_count` | Integer (optional) |
| `stage` | e.g. `Scale-up`, `Research`, `Startup` |
| `province` | Province abbreviation |
| Standard columns | — |

> For the funding chart, the dashboard uses rows where `year = '2024'` and `recipient_subsector = 'ALL'`.

#### `region_context.csv`
Reference table for regional descriptions. Used to enrich regional data.
| Column | Description |
|---|---|
| `region_id` | Matches `region_id` in region_shares |
| `region_name`, `province`, `hub_city`, `area_type` | Descriptive |
| `population_2021` | Integer |
| `key_institutions` | Semicolon-separated list |
| `life_sciences_cluster`, `cluster_maturity`, `note` | Descriptive |

#### `postsecondary_pipeline.csv`
| Column | Description |
|---|---|
| `year` | Integer |
| `institution` | Institution name or `ALL` |
| `credential_type` | `PhD`, `MSc`, `BSc`, `Diploma`, `Certificate`, or `ALL` |
| `program_area` | Program name or `ALL` |
| `graduates_count` | Integer |
| `province` | Province |
| Standard columns | — |

> For the PSI trend chart, the dashboard uses rows where `institution = 'ALL'`, `credential_type = 'ALL'`.

---

### `data/30_strategy/`

#### `lookwest_goals.csv` ← **Required**
Drives the Look West Progress Snapshot section.

| Column | Description |
|---|---|
| `goal_id` | Stable ID (e.g. `LW-G01`) |
| `pillar` | Strategy pillar name |
| `goal_name` | Short display name |
| `description` | Full description |
| `target_value` | Target number |
| `target_unit` | Unit string |
| `baseline_value` | Value at baseline year |
| `baseline_year` | Integer year |
| `target_year` | Integer year (e.g. `2030`) |
| `current_value` | Latest known value |
| `current_year` | Year of current_value |
| `progress_pct` | Calculated progress % toward target |
| `rag_status` | `RED`, `AMBER`, or `GREEN` |
| Standard columns | — |

> `LW-G01` (employment target) is used for the headline employment KPI in the Look West Snapshot.
> `LW-G07` (clinical trials) and `LW-G08` (PSI graduates) drive target lines in charts.

#### `lookwest_initiatives.csv` ← **Required**
Drives the Initiative Tracker table.

| Column | Description |
|---|---|
| `initiative_id` | Stable ID (e.g. `LW-I01`) |
| `initiative_name` | Display name |
| `pillar` | Strategy pillar |
| `owner_ministry` | Owning ministry or team |
| `lead_contact` | Contact role (optional) |
| `status` | `Active`, `Planning`, `Stalled`, `Complete`, `On Hold` |
| `rag_status` | `RED`, `AMBER`, or `GREEN` |
| `progress_pct` | Integer 0–100 |
| `start_date` | YYYY-MM-DD |
| `target_completion` | YYYY-MM-DD |
| `next_milestone` | Text description of next milestone |
| `next_milestone_date` | YYYY-MM-DD |
| `last_review_date` | YYYY-MM-DD |
| `evidence_count` | Integer (used as badge count) |
| `description` | Full description |
| `note` | Internal note |

#### `risks_and_gaps.csv`
| Column | Description |
|---|---|
| `risk_id` | Stable ID (e.g. `RSK-001`) |
| `category` | `Data Gap`, `Policy Risk`, `Funding Risk`, `Talent Risk`, etc. |
| `risk_name` | Short display name |
| `description` | Full description |
| `severity` | `Critical`, `High`, `Medium`, `Low` |
| `likelihood` | `Certain`, `High`, `Medium`, `Low` |
| `rag_status` | `RED`, `AMBER`, or `GREEN` |
| `owner` | Owning ministry / team |
| `mitigation` | Mitigation actions |
| `related_goal_id` | Links to `lookwest_goals.goal_id` (optional) |
| `related_initiative_id` | Links to `lookwest_initiatives.initiative_id` (optional) |
| `last_reviewed` | YYYY-MM-DD |
| Standard columns | — |

---

### `data/40_manual/`

#### `evidence_library.csv`
| Column | Description |
|---|---|
| `evidence_id` | Stable ID (e.g. `EV-001`) |
| `type` | `Strategy Document`, `Research Report`, `Government Report`, `News Article` |
| `title` | Full title |
| `summary` | 1–2 sentence summary |
| `link` | URL (leave blank if not publicly available) |
| `publication_date` | YYYY-MM-DD |
| `author` | Author or organization |
| `source_tier`, `confidence_tag` | Standard |
| `related_goal_id` | Links to `lookwest_goals.goal_id` |
| `related_initiative_id` | Links to `lookwest_initiatives.initiative_id` |
| `related_metric_id` | Links to `official_sector_metrics.metric_id` |
| `last_reviewed` | YYYY-MM-DD |
| `note` | Internal note |

#### `manual_metric_overrides.csv`
Allows ministry staff to override KPI card values with internally computed estimates.

| Column | Description |
|---|---|
| `override_id` | Stable ID (e.g. `OVR-001`) |
| `metric_id` | Links to `official_sector_metrics.metric_id` |
| `metric_name` | Display name |
| `value` | Override value (leave blank to show "Not currently available") |
| `unit` | Unit string |
| `year` | Year the override applies to |
| `commentary` | Context note shown in tooltip |
| `owner` | Who provided the override |
| `source_tier`, `confidence_tag`, `last_updated`, `note` | Standard |

> **Priority:** If a `manual_metric_overrides.csv` row exists for a `metric_id`, it takes priority over `official_sector_metrics.csv` for KPI card display.

#### `anchor_companies_optional.csv` ← Optional
Reference list of notable companies. Not currently displayed in MVP — reserved for future company spotlight section.

| Key columns | `company_id`, `company_name`, `subsector`, `hq_region`, `employee_count_bc`, `stage`, `is_anchor` |

#### `whats_new_optional.csv` ← Optional
If this file is present and contains rows, a collapsible "What's New" panel appears at the top of the dashboard.

| Column | Description |
|---|---|
| `item_id` | Stable ID |
| `date` | YYYY-MM-DD (sorted descending) |
| `category` | e.g. `Strategy Update`, `Data Update`, `Investment`, `Risk Escalation` |
| `headline` | Short headline |
| `body` | 1–3 sentence description |
| `link` | Optional URL |
| `priority` | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` — controls badge color |
| `source_tier`, `note` | Standard |

---

## Source Tiers

| Tier | Meaning |
|---|---|
| `official-curated` | BC Stats or Ministry curated dataset |
| `public-direct` | Downloaded directly from Statistics Canada, CIHR, etc. |
| `public-prepared` | Derived/calculated from public data |
| `manual-ministry` | Entered by ministry staff |
| `report-based` | Extracted from a published report |
| `scenario-model` | Scenario or model estimate |
| `mock-sample` | **Placeholder data — replace before using for decisions** |

---

## Confidence Tags

| Tag | Meaning |
|---|---|
| `official public statistical series` | Reliable official statistics |
| `proxy estimate` | Best available proxy; not a direct measure |
| `manual ministry input` | Ministry-provided; subject to revision |
| `anecdotal / report-based` | From a sector report; varies in methodology |
| `stale baseline` | Data exists but is outdated |
| `mock sample data` | **Placeholder only** |

---

## Replacing Mock Data with Real Data

1. Open the relevant CSV file in Excel, Google Sheets, or a text editor.
2. Replace the mock rows with real values. Keep all column headers **exactly as they are**.
3. Change `source_tier` from `mock-sample` to the appropriate tier.
4. Change `confidence_tag` from `mock sample data` to the appropriate tag.
5. Update `last_updated` to today's date.
6. Save the file and refresh the dashboard — the charts and KPIs will update automatically.

> **Important:** Do not rename columns. Column names are the data contract.
> Adding new columns is fine. Removing or renaming existing columns will break the dashboard.

---

## Manual Edit Layer (In-Browser)

The Initiative Tracker table has an **Edit** button on each row. Changes made through the modal are:
- Stored in the browser's **localStorage** (no server needed)
- Applied on top of the CSV data (the CSV is never modified)
- Marked with a small ✎ indicator in the table
- Exportable via the **Export** button above the table

To share edits with a colleague:
1. Click **↓ Export** above the Initiative Tracker table.
2. Send the exported CSV to your colleague.
3. They replace the contents of `data/30_strategy/lookwest_initiatives.csv` with the exported file.

---

## Reusing This Dashboard for Another Sector

1. **Duplicate** the entire `BCLS/` folder and rename it (e.g. `CleanTech/`).
2. In `code/dashboard.html`, update the `CONFIG` object at the top of the `<script>` section:
   ```javascript
   const CONFIG = {
     sector_id:        'clean_tech',         // ← change
     sector_name:      'Clean Technology',    // ← change
     strategy_name:    'CleanBC Strategy',    // ← change
     strategy_year:    2035,                  // ← change
     province:         'British Columbia',
     province_abbr:    'BC',
     dashboard_title:  'B.C. Clean Technology Sector Dashboard',  // ← change
     dashboard_subtitle: 'CleanBC Strategy · 2035 Target Monitoring', // ← change
     last_updated:     '2025-01-01',          // ← change
   };
   ```
3. Update the `THEME.subsectors` object for the new sector's subsectors and colors.
4. Replace all CSV contents with sector-appropriate data.
5. The dashboard structure, charts, and logic will all work without changes.

---

## File Status Summary

| File | Required | Contains Mock Data |
|---|---|---|
| `sector_definition_notes.csv` | ✓ Required | ⚠ Yes |
| `subsector_naics_lookup.csv` | ✓ Required | ⚠ Partially (some real NAICS codes) |
| `official_sector_metrics.csv` | ✓ Required | ⚠ Yes |
| `official_sector_region_shares.csv` | ✓ For regional chart | ⚠ Yes |
| `official_sector_province_compare.csv` | ✓ For province chart | ⚠ Yes |
| `public_business_counts.csv` | Optional | ⚠ Yes |
| `public_gdp_metrics.csv` | ✓ For GDP chart | ⚠ Yes |
| `io_multipliers.csv` | Optional | ⚠ Yes |
| `public_goods_exports.csv` | ✓ For exports chart | ⚠ Yes |
| `public_clinical_trials.csv` | ✓ For trials chart | ⚠ Yes |
| `public_funding_projects.csv` | ✓ For funding chart | ⚠ Yes |
| `region_context.csv` | Optional | — (descriptive) |
| `postsecondary_pipeline.csv` | ✓ For PSI chart | ⚠ Yes |
| `lookwest_goals.csv` | ✓ Required | ⚠ Yes |
| `lookwest_initiatives.csv` | ✓ Required | ⚠ Yes |
| `risks_and_gaps.csv` | ✓ For risks panel | ⚠ Yes |
| `evidence_library.csv` | ✓ For evidence panel | ⚠ Yes |
| `manual_metric_overrides.csv` | Optional | ⚠ Yes |
| `anchor_companies_optional.csv` | Optional | ⚠ Yes |
| `whats_new_optional.csv` | Optional | ⚠ Yes |

---

*Generated as part of the B.C. Life Sciences Sector Dashboard MVP. Internal use only.*
