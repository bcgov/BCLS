# DAX Measure Catalog

This catalog gives the first set of measures to create in Power BI. Names are written in a report-friendly style.

## Core KPI Measures

```DAX
KPI Value =
SUM ( FactSectorKPI[value] )
```

```DAX
KPI Baseline Value =
MAX ( FactSectorKPI[baseline_value] )
```

```DAX
KPI Change =
[KPI Value] - [KPI Baseline Value]
```

```DAX
KPI Change % =
DIVIDE ( [KPI Change], [KPI Baseline Value] )
```

```DAX
Latest KPI Period =
MAX ( FactSectorKPI[period] )
```

```DAX
Latest KPI Value =
VAR LatestPeriod = [Latest KPI Period]
RETURN
CALCULATE (
    [KPI Value],
    FactSectorKPI[period] = LatestPeriod
)
```

## Strategy Measures

```DAX
Goal Count =
COUNTROWS ( FactStrategyGoal )
```

```DAX
Average Goal Progress =
AVERAGE ( FactStrategyGoal[progress_pct] )
```

```DAX
Green Goals =
CALCULATE (
    [Goal Count],
    FactStrategyGoal[rag_status] = "GREEN"
)
```

```DAX
Amber Goals =
CALCULATE (
    [Goal Count],
    FactStrategyGoal[rag_status] = "AMBER"
)
```

```DAX
Red Goals =
CALCULATE (
    [Goal Count],
    FactStrategyGoal[rag_status] = "RED"
)
```

```DAX
Initiative Count =
COUNTROWS ( FactInitiative )
```

```DAX
Average Initiative Progress =
AVERAGE ( FactInitiative[progress_pct] )
```

## Look West Measures

```DAX
Media Items =
COUNTROWS ( FactLookWestMedia )
```

```DAX
Funding Announcements =
COUNTROWS ( FactLookWestFunding )
```

```DAX
Provincial Commitment $M =
SUM ( FactLookWestFunding[provincial_amount_m] )
```

```DAX
Investment Attracted $M =
SUM ( FactLookWestFunding[attracted_amount_m] )
```

```DAX
Federal Funding $M =
SUM ( FactLookWestFunding[federal_amount_m] )
```

```DAX
Other Funding $M =
SUM ( FactLookWestFunding[other_amount_m] )
```

```DAX
Total Investment $M =
SUM ( FactLookWestFunding[total_amount_m] )
```

```DAX
Jobs Created =
SUM ( FactLookWestFunding[jobs_created] )
```

```DAX
Jobs Protected =
SUM ( FactLookWestFunding[jobs_protected] )
```

```DAX
Pillars Covered =
DISTINCTCOUNT ( DimPillar[pillar] )
```

## Macro Measures

```DAX
Macro Value =
SUM ( FactMacroSeries[value] )
```

```DAX
Latest Macro Period =
MAX ( FactMacroSeries[period] )
```

```DAX
Latest Macro Value =
VAR LatestPeriod = [Latest Macro Period]
RETURN
CALCULATE (
    [Macro Value],
    FactMacroSeries[period] = LatestPeriod
)
```

## Trade Measures

```DAX
Trade Value =
SUM ( FactTradeTotals[value] )
```

```DAX
Export Value =
CALCULATE (
    [Trade Value],
    FactTradeTotals[flow] = "exports"
)
```

```DAX
Import Value =
CALCULATE (
    [Trade Value],
    FactTradeTotals[flow] = "imports"
)
```

```DAX
Trade Balance =
[Export Value] - [Import Value]
```

```DAX
Trade Balance % of Exports =
DIVIDE ( [Trade Balance], [Export Value] )
```

```DAX
Category Trade Value =
SUM ( FactTradeCategories[value] )
```

```DAX
Partner Trade Value =
SUM ( FactTradePartners[value] )
```

```DAX
Interprovincial Exports =
SUM ( FactInterprovincialTrade[exports] )
```

```DAX
Interprovincial Imports =
SUM ( FactInterprovincialTrade[imports] )
```

## Formatting Guidance

Use these formats:

- percentages: `0.0%`
- currency millions: `$#,0.0M`
- counts: `#,0`
- period labels: use dimension columns rather than formatting inside measures

