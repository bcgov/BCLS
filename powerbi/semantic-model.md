# Semantic Model

This is the recommended Power BI semantic model for the hybrid rebuild.

## Model Style

Use an import model with a star-schema shape. Keep raw Excel sheet names out of report visuals where possible. Rename tables to business-friendly names and create reusable measures rather than repeating calculations in visuals.

## Dimensions

### DimSubsector

Source: `SECTOR_STRUCTURE`

Grain: one row per subsector.

Key: `subsector_id`

Columns:

- `subsector_id`
- `sector_id`
- `subsector_name`
- `naics_4digit`
- `naics_5digit`
- `naics_description`
- `tab_order`
- `show_as_tab`
- `dashboard_color`
- `has_reliable_data`
- `data_availability_note`

Special row:

`ALL` represents the whole-sector view.

### DimMetric

Source: derive from `KEY_KPIS[metric_id]` and `CHART_DATA[metric_id]`.

Grain: one row per metric.

Columns:

- `metric_id`
- `metric_name`
- `unit`
- `metric_group`
- `display_order`

### DimPeriod

Source: derive from all date/year fields.

Grain: one row per period. For annual sector metrics, use year. For monthly macro data, use a date at the start of the period.

Columns:

- `period_key`
- `date`
- `year`
- `quarter`
- `month`
- `period_label`

### DimPillar

Source: `STRATEGY_GOALS`, `INITIATIVE_TRACKER`, Look West media/funding tables.

Columns:

- `pillar`
- `pillar_short_name`
- `display_order`

### DimSourceQuality

Source: `source_tier`, `confidence_tag`.

Columns:

- `source_tier`
- `confidence_tag`
- `quality_group`
- `display_label`

## Fact Tables

### FactSectorKPI

Source: `KEY_KPIS`

Grain: one metric, subsector, province, and period.

Columns:

- `metric_id`
- `subsector_id`
- `province`
- `period`
- `value`
- `baseline_period`
- `baseline_value`
- `unit`
- `source_tier`
- `confidence_tag`

Relationships:

- `FactSectorKPI[subsector_id]` to `DimSubsector[subsector_id]`
- `FactSectorKPI[metric_id]` to `DimMetric[metric_id]`
- `FactSectorKPI[period]` to `DimPeriod[period_key]`

### FactChartData

Source: `CHART_DATA`

Grain: one chart group, metric, subsector, geography/comparator, and period.

Columns:

- `chart_group`
- `metric_id`
- `subsector_id`
- `province`
- `region_name`
- `comparator`
- `period`
- `value`
- `value_2`
- `unit`
- `source_tier`
- `notes`

Relationships:

- `FactChartData[subsector_id]` to `DimSubsector[subsector_id]`
- `FactChartData[metric_id]` to `DimMetric[metric_id]`
- `FactChartData[period]` to `DimPeriod[period_key]`

### FactStrategyGoal

Source: `STRATEGY_GOALS`

Grain: one row per strategic goal.

Columns:

- `goal_id`
- `goal_name`
- `pillar`
- `rag_status`
- `progress_pct`
- `target_value`
- `target_unit`
- `target_year`
- `baseline_year`
- `baseline_value`
- `related_subsectors`

Note:

`related_subsectors` is a pipe-separated multi-value field. For best modeling, split it into a bridge table.

### BridgeGoalSubsector

Source: split `STRATEGY_GOALS[related_subsectors]`.

Columns:

- `goal_id`
- `subsector_id`

### FactInitiative

Source: `INITIATIVE_TRACKER`

Grain: one row per initiative.

Columns:

- `initiative_id`
- `initiative_name`
- `pillar`
- `rag_status`
- `status`
- `progress_pct`
- `owner_ministry`
- `next_milestone`
- `next_milestone_date`
- `last_review_date`
- `related_subsectors`
- `description`

### BridgeInitiativeSubsector

Source: split `INITIATIVE_TRACKER[related_subsectors]`.

Columns:

- `initiative_id`
- `subsector_id`

### FactEvidence

Source: `EVIDENCE_LIBRARY`

Grain: one evidence item.

Columns:

- `type`
- `title`
- `summary`
- `author`
- `publication_date`
- `confidence_tag`
- `source_tier`
- `related_goal_id`
- `related_initiative_id`
- `link`

Relationships:

- `related_goal_id` to `FactStrategyGoal[goal_id]`
- `related_initiative_id` to `FactInitiative[initiative_id]`

### FactRisk

Source: `RISKS_GAPS`

Grain: one risk or data gap.

Columns:

- `risk_name`
- `category`
- `description`
- `severity`
- `likelihood`
- `rag_status`
- `owner`
- `mitigation`
- `last_reviewed`

### FactLookWestMedia

Source: normalized media sheets.

Grain: one media item or announcement.

Columns:

- `date`
- `source_type`
- `source`
- `sector`
- `headline`
- `headline_url`
- `message`
- `temp_check`
- `theme`
- `status`
- `pillar`

### FactLookWestFunding

Source: `Funding and Investments`

Grain: one funding/investment announcement.

Columns:

- `date`
- `source`
- `project`
- `pillar`
- `lw_sector`
- `theme`
- `status`
- `partner`
- `details`
- `provincial_amount_m`
- `attracted_amount_m`
- `federal_amount_m`
- `other_amount_m`
- `total_amount_m`
- `jobs_created`
- `jobs_protected`
- `region`
- `data_source`

### FactMacroSeries

Source: `bc_econ_data_snapshot.json`

Grain: one chart series and period.

Columns:

- `series_id`
- `period`
- `value`
- `source`
- `updated_at`

### FactTradeTotals

Source: `trade_composition_sample.json`

Grain: one trade flow and year.

Columns:

- `flow`
- `year`
- `value`

### FactTradeCategories

Source: `trade_composition_sample.json`

Grain: one trade flow, year, and commodity/category.

Columns:

- `flow`
- `year`
- `category`
- `value`

### FactTradePartners

Source: `trade_composition_sample.json`

Grain: one trade flow, year, partner, and partner region.

Columns:

- `flow`
- `year`
- `partner_name`
- `partner_region`
- `value`

### FactInterprovincialTrade

Source: `trade_composition_sample.json`

Grain: one partner province and year.

Columns:

- `year`
- `province`
- `exports`
- `imports`

