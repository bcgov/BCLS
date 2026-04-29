# Data Source Map

This document describes the datasets used by the current dashboard and how they should be loaded into Power BI.

## Source Control Workbook

File: `C:\Users\smehd\BCLS\DATA_FILE_MAP.xlsx`

Sheet: `FILE_MAP`

Columns:

- `key`: logical dataset name used by the dashboard
- `path`: local or synced workbook path
- `required`: whether the source is required
- `description`: business description
- `notes`: data steward or loading note
- `sheet`: optional sheet filter

Power BI use:

This file can be kept as a governance reference, but the Power BI model should connect directly to the curated source files or to SharePoint/OneDrive locations once final paths are confirmed.

## Life Sciences

File: `C:\Users\smehd\BCLS\data\sectors\life_sciences\Life_Sciences_light.xlsx`

Power BI role:

Primary structured sector workbook. This should become the core sector semantic model.

Sheets:

- `CONFIG`: report-level settings
- `SECTOR_STRUCTURE`: sector and subsector dimension
- `KEY_KPIS`: KPI fact table
- `CHART_DATA`: flexible chart fact table
- `STRATEGY_GOALS`: goals and target table
- `INITIATIVE_TRACKER`: initiatives and milestone table
- `EVIDENCE_LIBRARY`: evidence/source table
- `RISKS_GAPS`: risks and gaps table

## Look West Strategy

Media file: `C:\Users\smehd\BCLS\data\look_west_strategy\Look West media coverage - mock.xlsx`

Funding file: `C:\Users\smehd\BCLS\data\look_west_strategy\LW related funding and investments - Mock.xlsx`

Power BI role:

Operational monitoring tables for media coverage, funding/investments, policy/regulation tracking, and major project announcements.

Media sheets:

- `"Look West" news`
- `BC Gov News`
- `Federal Announcements`
- `Other related news`
- `Keywords - used by BC Gov`

Funding sheets:

- `Funding and Investments`
- `Major Projects`
- `Policy & Regulations` (currently empty in the mock workbook)

## BC Macroeconomy

Snapshot file: `C:\Users\smehd\BCLS\data\bc_macroeconomy\bc_econ_data_snapshot.json`

Power BI role:

Macroeconomic time-series snapshot. The current file contains pre-shaped chart series. For production Power BI, this should eventually be replaced by direct Statistics Canada extraction or a curated refresh table.

Current chart series:

- `chart-labour`
- `chart-gdp`
- `chart-cpi`
- `chart-trade`
- `chart-retail`
- `chart-permits`

Each point uses:

- `ref`: reference period
- `val`: numeric value

## BC Trade Analysis

File: `C:\Users\smehd\BCLS\data\bc_trade_analysis\trade_composition_sample.json`

Power BI role:

Trade composition and partner analysis dataset.

Top-level entities:

- `meta`
- `years`
- `flows`
- `interprovincial`

Recommended Power BI tables:

- `FactTradeTotals`
- `FactTradeCategories`
- `FactTradePartners`
- `FactInterprovincialTrade`
- `DimTradeFlow`
- `DimYear`
- `DimPartnerRegion`

