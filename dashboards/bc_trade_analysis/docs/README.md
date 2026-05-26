# BC Trade Analysis

Standalone one-page dashboard for international trade composition.

## Entry Point
- `html/dashboard.html`

## Data
- Optional external JSON: `C:/Users/mehdi/BCLS/data/trade_composition_sample.json`
- Built-in fallback: `dashboards/bc_trade_analysis/html/trade_composition_embedded.js`

Current dataset is a development sample aligned to:
- Statistics Canada table `36-10-0709-01`
- Statistics Canada table `12-10-0175-01`

## Scope (v1)
- Trade composition only (no map view, no global share, no product space, no growth opportunity module)
- Treemap by broad product categories
- Partner ranking (countries or regions)
- Trend lines and trade balance cards
- Value + share + YoY

## Hub Integration
Designed to be embedded later in `BC Dashboard Hub` via iframe.
