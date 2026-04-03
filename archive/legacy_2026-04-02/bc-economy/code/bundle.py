"""
bundle.py — BC Economic Monitor standalone builder
====================================================
Fetches live data from Statistics Canada WDS API (by vector ID),
then produces a fully self-contained HTML file with all data embedded
as JSON.  The output works from file:// with no internet needed.

Usage (run from your terminal — NOT from Cowork's sandbox):
    cd bc-economy/code
    python bundle.py

Output: bc-economy/output/dashboard_standalone.html

Vector IDs confirmed 2026-04 by inspecting Stats Can metadata:
  2057793    — BC Total employed (14-10-0355-01)
  1793288710 — BC Real GDP chained 2017$ (36-10-0711-01)
  41692462   — BC CPI All-items (18-10-0004-01)
  807928     — BC Manufacturing shipments SA (16-10-0048-01)
  1446860064 — BC Retail trade SA (20-10-0056-01)
  52673496   — Canada Commodity Price Index (10-10-0132-01)

NOTE: getDataFromVectorsAndLatestNPeriods is used instead of
getDataFromCubePidCoordAndLatestNPeriods because the coordinate-based
endpoint returns incorrect values for some BC provincial series.
"""

import base64
import json
import os
import sys
from datetime import datetime, timezone

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT        = os.path.dirname(SCRIPT_DIR)
TEMPLATE    = os.path.join(SCRIPT_DIR, 'dashboard.html')
OUTPUT_DIR  = os.path.join(ROOT, 'output')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'dashboard_standalone.html')
LOGO_PATH   = os.path.join(ROOT, 'docs', 'logo', 'BCID_H_RGB_rev.png')

SC_BASE = 'https://www150.statcan.gc.ca/t1/wds/rest'

# ── Chart definitions — keyed by vector ID ────────────────────────────────
# Each entry: chart id → (vector_id, n_periods)
# Data is stored as {"pts": [{ref, val}, ...]} matching renderChartFromData()
MACRO_CHARTS = [
    {'id': 'chart-labour',  'vec': 2057793,     'nPeriods': 24},
    {'id': 'chart-gdp',     'vec': 1793288710,  'nPeriods': 8},
    {'id': 'chart-cpi',     'vec': 41692462,    'nPeriods': 36},
    {'id': 'chart-trade',   'vec': 807928,      'nPeriods': 24},
    {'id': 'chart-retail',  'vec': 1446860064,  'nPeriods': 24},
    {'id': 'chart-permits', 'vec': 52673496,    'nPeriods': 36},
]


# ══════════════════════════════════════════════════════════════════════════
# Statistics Canada WDS API helpers  (all endpoints are HTTP POST)
# Docs: https://www.statcan.gc.ca/en/developers/wds/user-guide
# ══════════════════════════════════════════════════════════════════════════

def sc_post(endpoint, body):
    """POST to a Stats Can WDS endpoint; returns the full response array."""
    import urllib.request
    url  = f'{SC_BASE}/{endpoint}'
    data = json.dumps(body).encode('utf-8')
    req  = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'Accept':       'application/json',
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/122.0.0.0 Safari/537.36'
        ),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))


def fetch_vectors(vector_ids, n_periods):
    """
    Fetch latest N periods for a list of Stats Can vector IDs.
    Returns a list of [{ref, val}] lists (one per vector), in
    chronological order (oldest first), in the SAME ORDER as vector_ids.

    Uses getDataFromVectorsAndLatestNPeriods — the reliable endpoint.
    NOTE: the API does NOT preserve request order — it sorts results by
    vector ID ascending. We match each response item by its vectorId field.
    """
    body   = [{'vectorId': v, 'latestN': n_periods} for v in vector_ids]
    result = sc_post('getDataFromVectorsAndLatestNPeriods', body)

    # Build lookup: vectorId -> points
    by_id = {}
    for item in result:
        if item.get('status') != 'SUCCESS':
            raise RuntimeError(
                f"SC API error: {item.get('object', item.get('status'))}"
            )
        obj = item['object']
        vid = obj.get('vectorId')
        pts = []
        for p in reversed(obj.get('vectorDataPoint', [])):
            v = p.get('value')
            if v is not None and v != '':
                try:
                    pts.append({'ref': p['refPer'], 'val': float(v)})
                except (ValueError, TypeError):
                    pass
        by_id[vid] = pts

    # Return in the same order as vector_ids
    return [by_id.get(vid, []) for vid in vector_ids]


def fetch_chart(defn):
    """Fetch data for one chart definition. Returns stored-data dict."""
    series = fetch_vectors([defn['vec']], defn['nPeriods'])
    return {'pts': series[0]}


# ══════════════════════════════════════════════════════════════════════════
# HTML builders
# ══════════════════════════════════════════════════════════════════════════

def embed_logo(html):
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        html = html.replace(
            'src="../docs/logo/BCID_H_RGB_rev.png"',
            f'src="data:image/png;base64,{b64}"'
        )
        print('  ✓  BC Gov logo embedded')
    else:
        print(f'  ⚠  Logo not found: {LOGO_PATH}')
    return html


def inject_data(html, payload):
    """Inject window.BC_ECON_DATA before </head>."""
    blob  = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
    block = (
        '\n<!-- ── Inline data embedded by bundle.py ── -->\n'
        f'<script>window.BC_ECON_DATA={blob};</script>\n'
        '<!-- ─────────────────────────────────────── -->\n'
    )
    return html.replace('</head>', block + '</head>', 1)


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

def bundle():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(TEMPLATE):
        print(f'ERROR: Template not found at {TEMPLATE}')
        sys.exit(1)

    print('BC Economic Monitor — bundle.py')
    print('─' * 46)

    with open(TEMPLATE, encoding='utf-8') as f:
        html = f.read()

    html = embed_logo(html)

    # ── Fetch Stats Can data ───────────────────────────────────────────────
    charts = {}
    n_ok = n_fail = 0
    print()
    print('  Fetching Statistics Canada data…')

    for defn in MACRO_CHARTS:
        cid = defn['id']
        try:
            charts[cid] = fetch_chart(defn)
            pts_count = len(charts[cid].get('pts', []))
            print(f'  ✓  {cid}  ({pts_count} data points, vec={defn["vec"]})')
            n_ok += 1
        except Exception as e:
            print(f'  ✗  {cid}  — {e}')
            n_fail += 1

    print()
    if n_ok > 0:
        payload = {
            'updatedAt': datetime.now(timezone.utc).isoformat(),
            'source': 'Statistics Canada WDS API',
            'charts': charts,
        }
        html = inject_data(html, payload)
        print(f'  ✓  {n_ok} chart dataset(s) embedded')
        if n_fail:
            print(f'  ⚠  {n_fail} chart(s) failed — will show empty in dashboard')
    else:
        print('  ⚠  No data fetched — check your internet connection.')
        print('     Dashboard will open with empty charts.')
        print('     Use the "Update Data" button after running serve.py.')

    # ── Write output ───────────────────────────────────────────────────────
    print()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f'  ✓  output/dashboard_standalone.html  ({size_kb:.0f} KB)')
    print()
    print('  Open dashboard_standalone.html in any browser.')
    print('  Data is embedded — no internet connection required.')


if __name__ == '__main__':
    bundle()
