# Visual Parity Blueprint

This blueprint translates the current HTML dashboard into Power BI pages with visual parity as the main design priority.

## Global Visual System

Canvas:

- Background: `#F2F5F9`
- Main card background: `#FFFFFF`
- Border: `#D6DCE4`
- Primary text: `#1A202C`
- Muted text: `#4A5568`
- Subtle text: `#718096`

Header:

- Height: compact, approximately 60 px
- Background: BC navy `#003366`
- Accent rule: BC gold `#FCBA19`
- Title: white, semibold
- Subtitle/meta: muted white

Cards:

- White background
- Thin grey border
- 8 px corner radius or less
- No heavy shadows
- KPI cards should have a colored top rule or left rule

Charts:

- Use restrained colors
- Primary series: `#003366`
- Secondary series: `#1A5276`
- Gold target/accent line: `#FCBA19`
- Green/amber/red status colors:
  - Green: `#276749`
  - Amber: `#C05621`
  - Red: `#C53030`

Tables:

- Compact row height
- Header background: `#F8FAFC`
- Alternating or hover-like row contrast should be subtle
- Use conditional formatting for RAG/status fields

## Page 1: Executive Hub

Purpose:

Replacement for the HTML hub page. This page should guide users to the main analytical domains.

Layout:

- Top navy header with report title and last refresh date
- Wide row of navigation buttons or bookmarks:
  - Life Sciences
  - Look West Strategy
  - Macroeconomy
  - Trade Analysis
  - Evidence and Risks
- KPI strip:
  - Total investment
  - Jobs created
  - Jobs protected
  - Active goals
  - Open risks
- Sector cards or table:
  - sector name
  - data status
  - last updated
  - page navigation action

Power BI visuals:

- Card/new card visuals for KPIs
- Button navigator for pages
- Matrix or table for sector cards if visual consistency matters more than decorative cards

## Page 2: Life Sciences

Purpose:

Closest reproduction of the current Life Sciences dashboard.

Layout:

- Header band with title, subtitle, and data status
- Sector definition text block
- Subsector slicer styled as horizontal buttons:
  - Whole Sector Overview
  - Biotechnology
  - Medical Devices
  - Pharmaceuticals
  - CRO
  - Other
- KPI strip:
  - Employment
  - GDP Contribution
  - Sector Revenue
  - Business Count
  - Goods Exports
  - Public Funding
- Chart grid:
  - Employment trend
  - GDP contribution
  - Business count
  - Goods exports
  - Regional share
  - Province comparison
  - Research activity
  - Funding
  - Talent pipeline
- Bottom operational sections:
  - strategy goals
  - initiative tracker

Power BI visuals:

- Slicer with tile style for subsector selection
- Cards for KPI values
- Line charts for trends
- Clustered/stacked bar charts for comparisons
- Table/matrix for initiatives
- Conditional formatting for `rag_status`

Visual parity notes:

- Keep cards dense and compact.
- Use the subsector color as a conditional accent where practical.
- Keep chart titles short and aligned to the HTML titles.

## Page 3: Look West Strategy

Purpose:

Rebuild the Look West tracker and funding view.

Layout:

- Header band with title and refresh/data mode
- KPI strip:
  - Media coverage items
  - BC Gov mentions
  - Funding announcements
  - Policy/regulation items
  - Total investment value
  - Jobs created
  - Jobs protected
  - Pillars covered
- Funding chart row:
  - Investment by pillar
  - Funding mix
  - Top regions by investment
  - Employment impact by pillar
- Media table section
- Funding/investments table section
- Policy/regulations table section

Power BI visuals:

- Cards
- Stacked column chart for funding by pillar
- Donut or stacked bar for funding mix
- Horizontal bar chart for top regions
- Clustered column for jobs created/protected
- Tables with slicers above them

Visual parity notes:

- Use the same operational tracker feeling as the HTML version.
- Tables should remain central; this page should not become only chart-based.

## Page 4: BC Macroeconomy

Purpose:

Power BI equivalent of the macroeconomic dashboard.

Layout:

- Header band with latest data period
- KPI cards:
  - labour
  - GDP
  - CPI
  - trade
  - retail
  - permits
- Chart grid:
  - labour trend
  - GDP trend
  - CPI trend
  - trade trend
  - retail trend
  - building permits trend

Power BI visuals:

- Card visuals
- Line charts
- Small multiples if appropriate for the macro series

Visual parity notes:

- Use clean chart panels with minimal decoration.
- Maintain the dashboard's "briefing note" feeling.

## Page 5: BC Trade Analysis

Purpose:

Recreate trade composition and partner analysis.

Layout:

- Header band
- Slicers:
  - year
  - flow
  - partner mode
- KPI cards:
  - exports
  - imports
  - trade balance
  - top category
  - top partner
- Composition chart
- Partner ranking chart
- Trend chart
- Interprovincial trade section

Power BI visuals:

- Decomposition tree or treemap for composition
- Bar chart for partners
- Line chart for exports/imports/balance
- Table for composition detail

Visual parity notes:

- If Power BI native treemap is too visually different, use a ranked bar chart for a cleaner executive version.

## Page 6: Evidence and Risks

Purpose:

Dedicated governance page for evidence, confidence, risks, and gaps.

Layout:

- KPI strip:
  - evidence items
  - risks/gaps
  - red risks
  - amber risks
  - latest review date
- Evidence library table
- Risks and gaps table
- Filters:
  - subsector
  - evidence type
  - risk category
  - RAG status

Power BI visuals:

- Tables with conditional formatting
- Cards
- Slicers

Visual parity notes:

- This page should feel like a control room, not a presentation page.
- Keep rows compact and make links visible.

