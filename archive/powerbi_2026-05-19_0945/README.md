# BCLS Power BI Migration Package

This folder contains the build package for recreating the current BCLS HTML dashboard in Power BI with a hybrid goal:

- preserve the current visual language as closely as Power BI allows
- move the data into a maintainable Power BI semantic model
- keep the report understandable for non-technical users and external audiences

Power BI Desktop is not available as a command-line tool in this workspace, so this package is designed to be opened and applied inside Power BI Desktop.

## Recommended Build Order

1. Apply the theme from `theme/BCLS.PowerBI.Theme.json`.
2. Load the source files described in `data-source-map.md`.
3. Build the model from `semantic-model.md`.
4. Create DAX measures from `dax-measure-catalog.md`.
5. Recreate pages using `visual-parity-blueprint.md`.
6. Use `power-query-plan.md` as the transformation checklist.

## Target Report Pages

1. Executive Hub
2. Life Sciences
3. Look West Strategy
4. BC Macroeconomy
5. BC Trade Analysis
6. Evidence and Risks

## Visual Parity Positioning

The Power BI version should feel like the same product: BC Government header styling, white analytical cards, compact KPI hierarchy, muted grey canvas, navy and gold accents, and table-first operational sections.

Power BI will not exactly reproduce the custom HTML/CSS behavior, iframe hub, or every responsive layout detail. The priority is to keep visual similarity high while making the report stable, refreshable, and maintainable.

