# Power BI Page Backgrounds

Generated PNG backgrounds are placed in this folder by running:

`powershell -ExecutionPolicy Bypass -File powerbi\assets\generate-page-backgrounds.ps1`

## Power BI Setup

Use a 16:9 page size.

For each Power BI page:

1. Open the page.
2. Go to the Format pane.
3. Open Canvas background.
4. Add the matching PNG as the image.
5. Set Image fit to `Fit`.
6. Set Transparency to `0%`.
7. Place visuals over the white containers.
8. Set visual backgrounds to transparent where you want the PNG boxes to show through.
9. Turn visual headers off unless the visual needs export/focus controls.

## Files

- `01_Hub_Background.png`
- `02_Life_Sciences_Background.png`
- `03_Look_West_Background.png`
- `04_Macroeconomy_Background.png`
- `05_Trade_Analysis_Background.png`
- `06_Evidence_Risks_Background.png`

## Notes

These assets are designed as visual shell backgrounds. They include static headers, navigation bars, page structure, section labels, KPI containers, chart containers, and table containers.

Use Power BI buttons/bookmarks on top of the navigation bar areas if you want the navigation to be clickable.

Use `layout-coordinate-map.md` for the exact Power BI visual positions.
