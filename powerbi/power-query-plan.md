# Power Query Plan

This is the transformation plan for Power BI Desktop.

## General Rules

- Load all source tables as staging queries first.
- Disable load for raw staging queries where they are only used to create final model tables.
- Rename final tables using business names such as `FactSectorKPI`, `DimSubsector`, and `FactLookWestFunding`.
- Apply explicit data types to every final table.
- Keep source columns until relationships and measures are validated, then hide technical columns in the report view.

## Life Sciences Workbook

Source: `Life_Sciences_light.xlsx`

Create the following final queries:

- `DimSubsector` from `SECTOR_STRUCTURE`, filtered where `record_type = "subsector"`
- `DimSectorDefinition` from `SECTOR_STRUCTURE`, filtered where `record_type = "definition"`
- `FactSectorKPI` from `KEY_KPIS`
- `FactChartData` from `CHART_DATA`
- `FactStrategyGoal` from `STRATEGY_GOALS`
- `FactInitiative` from `INITIATIVE_TRACKER`
- `FactEvidence` from `EVIDENCE_LIBRARY`
- `FactRisk` from `RISKS_GAPS`
- `BridgeGoalSubsector` by splitting `FactStrategyGoal[related_subsectors]`
- `BridgeInitiativeSubsector` by splitting `FactInitiative[related_subsectors]`

Recommended data types:

- IDs and labels: text
- values/progress: decimal number
- years: whole number
- date fields: date
- RAG/status fields: text

## Look West Media

Source: `Look West media coverage - mock.xlsx`

Combine the four operational media sheets into one `FactLookWestMedia` query.

Add a calculated source sheet column before combining:

- `"Look West" news`
- `BC Gov News`
- `Federal Announcements`
- `Other related news`

Normalize source columns:

- date from `Date`
- source from `Source` or `Ministry`
- sector from `Sector / Stakeholder`, `Primary Sector`, or `Sector`
- headline from `Headline` or `Announcement`
- message from `Theme / Key message`, `Theme / Key Message`, or `Theme / Key  Message`
- temp check from `"Temp Check"` or `LW Mention`

Add derived columns:

- `pillar`
- `theme`
- `status`

For first version, these can follow the same rule logic as the HTML dashboard:

- skills/workforce/training text maps to `Strengthening Our Workforce`
- permit/major project/infrastructure text maps to `Delivering Major Projects Faster`
- export/market/trade/diversification text maps to `Diversifying Markets`
- otherwise map to `Growing Targeted Sectors`

## Look West Funding

Source: `LW related funding and investments - Mock.xlsx`

Create `FactLookWestFunding` from `Funding and Investments`.

Rename columns:

- `Date Announced` to `date`
- `Funding Source` to `source`
- `Project/Program Name` to `project`
- `LW Pillar` to `pillar`
- `LW Sector` to `lw_sector`
- `Partner Org.` to `partner`
- `Project Details` to `details`
- `Provincial Commitment ($M)` to `provincial_amount_m`
- `Investment attracted to BC($M)` to `attracted_amount_m`
- `Federal ($M)` to `federal_amount_m`
- `Other Sources ($M)` to `other_amount_m`
- `Total Investment Value ($M)` to `total_amount_m`
- `Jobs Created` to `jobs_created`
- `Jobs Protected` to `jobs_protected`
- `Econ. Devt. Region` to `region`
- `Data Source` to `data_source`

If `total_amount_m` is blank, calculate it as provincial + attracted + federal + other.

## Macroeconomy JSON

Source: `bc_econ_data_snapshot.json`

Transform into `FactMacroSeries`:

- Expand `charts` into rows by chart id
- Expand each chart `pts` array into period/value rows
- Rename `ref` to `period`
- Rename `val` to `value`
- Add `source`
- Add `updated_at`

## Trade JSON

Source: `trade_composition_sample.json`

Create:

- `FactTradeTotals` from `flows.exports.totals` and `flows.imports.totals`
- `FactTradeCategories` from `flows.*.categories`
- `FactTradePartners` from `flows.*.partners.regions` and `flows.*.partners.countries`
- `FactInterprovincialTrade` from `interprovincial.partners`
- `DimYear` from the `years` array

Keep the `flow` column as text values `exports` and `imports`.

