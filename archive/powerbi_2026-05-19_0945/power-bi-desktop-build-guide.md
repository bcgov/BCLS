# Power BI Desktop Build Guide

This guide describes how to assemble the first Power BI version of the BCLS dashboard.

Power BI Desktop install found:

`C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`

## Step 1: Create The Report

1. Open Power BI Desktop.
2. Create a blank report.
3. Save it as `BCLS_Dashboard.pbix`.
4. Import the theme file:
   `powerbi\theme\BCLS.PowerBI.Theme.json`

## Step 2: Load Source Files

Load these sources:

- `data\sectors\life_sciences\Life_Sciences_light.xlsx`
- `data\look_west_strategy\Look West media coverage - mock.xlsx`
- `data\look_west_strategy\LW related funding and investments - Mock.xlsx`
- `data\bc_macroeconomy\bc_econ_data_snapshot.json`
- `data\bc_trade_analysis\trade_composition_sample.json`

Use Power Query to shape them according to `power-query-plan.md`.

## Step 3: Create Final Model Tables

Create these final tables:

- `DimSubsector`
- `DimMetric`
- `DimPeriod`
- `DimPillar`
- `DimSourceQuality`
- `FactSectorKPI`
- `FactChartData`
- `FactStrategyGoal`
- `FactInitiative`
- `FactEvidence`
- `FactRisk`
- `BridgeGoalSubsector`
- `BridgeInitiativeSubsector`
- `FactLookWestMedia`
- `FactLookWestFunding`
- `FactMacroSeries`
- `FactTradeTotals`
- `FactTradeCategories`
- `FactTradePartners`
- `FactInterprovincialTrade`

## Step 4: Create Relationships

Core relationships:

- `FactSectorKPI[subsector_id]` to `DimSubsector[subsector_id]`
- `FactChartData[subsector_id]` to `DimSubsector[subsector_id]`
- `FactSectorKPI[metric_id]` to `DimMetric[metric_id]`
- `FactChartData[metric_id]` to `DimMetric[metric_id]`
- `FactStrategyGoal[pillar]` to `DimPillar[pillar]`
- `FactInitiative[pillar]` to `DimPillar[pillar]`
- `FactLookWestMedia[pillar]` to `DimPillar[pillar]`
- `FactLookWestFunding[pillar]` to `DimPillar[pillar]`
- `BridgeGoalSubsector[goal_id]` to `FactStrategyGoal[goal_id]`
- `BridgeGoalSubsector[subsector_id]` to `DimSubsector[subsector_id]`
- `BridgeInitiativeSubsector[initiative_id]` to `FactInitiative[initiative_id]`
- `BridgeInitiativeSubsector[subsector_id]` to `DimSubsector[subsector_id]`

Keep relationships single-direction by default. Use bidirectional filtering only where a bridge table requires it and after checking visual behavior.

## Step 5: Add Measures

Create measures from `dax-measure-catalog.md`.

Put measures in a dedicated table named `_Measures` so the model is easier to navigate.

## Step 6: Build Pages

Build pages in this order:

1. `Executive Hub`
2. `Life Sciences`
3. `Look West Strategy`
4. `BC Macroeconomy`
5. `BC Trade Analysis`
6. `Evidence and Risks`

Use `visual-parity-blueprint.md` for layout and visual selection.

## Step 7: Visual Parity Checks

Before calling the first version complete, check:

- Header color is BC navy and matches the HTML dashboard.
- Gold accent line appears on every primary page header.
- KPI cards are compact and aligned.
- Tables are dense, readable, and styled with subtle borders.
- RAG values use red, amber, and green consistently.
- Background is light grey, not plain white.
- Page navigation is visible without opening the Power BI page tabs.
- The Life Sciences page preserves the same information hierarchy as the HTML dashboard.

## Step 8: Publish Readiness

Before publishing:

- Replace mock workbook paths with final SharePoint or OneDrive paths.
- Confirm refresh credentials.
- Validate row counts against the source workbooks.
- Hide staging queries.
- Hide technical keys from report users.
- Confirm external audience can understand every table title, KPI label, and slicer.

