# BCLS Dashboard SPFx Package

This project is an SPFx no-framework web part that hosts a self-contained duplicate of the BCLS dashboard.

## What gets deployed

- Web part: `BCLS Dashboard (SPFx)`
- Static dashboard assets: `SiteAssets/BCLS-Dashboard/...`
- Default hub URL: `SiteAssets/BCLS-Dashboard/dashboards/bc_dashboard_hub/html/dashboard.html`

## Build package

1. Install dependencies:

   `npm install`

2. Sync generated SPFx static assets from canonical source:

   `powershell -ExecutionPolicy Bypass -File ../../scripts/sync_runtime_targets.ps1 -SkipDist`

3. Build and package:

   `gulp bundle --ship`

   `gulp package-solution --ship`

4. Upload the generated package:

   `sharepoint/solution/bcls-dashboard-spfx.sppkg`

## Notes

- This solution uses feature assets, so keep `skipFeatureDeployment` set to `false`.
- The web part property pane lets you override the dashboard URL and iframe height.
