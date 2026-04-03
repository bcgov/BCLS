"""
Quick local server for the restructured BCLS dashboard workspace.
Run from the BCLS root folder:

    python scripts/serve.py

Then open:  http://localhost:8080/dashboards/bc_dashboard_hub/html/dashboard.html
"""
import http.server
import json
import os
import socketserver
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

PORT = 8080
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.chdir(ROOT)


def open_browser():
    import time
    time.sleep(1.0)
    webbrowser.open(f"http://localhost:{PORT}/dashboards/bc_dashboard_hub/html/dashboard.html")


threading.Thread(target=open_browser, daemon=True).start()


class UTF8RequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
    }

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        n = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(n) if n > 0 else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def _proxy_statcan_wds(self, body):
        path = str(body.get("path", "")).strip().lstrip("/")
        payload = body.get("payload", [])
        if not path:
            self._send_json(400, {"error": "Missing path"})
            return
        if not isinstance(payload, list):
            self._send_json(400, {"error": "payload must be an array"})
            return

        url = f"https://www150.statcan.gc.ca/t1/wds/rest/{path}"
        req = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "BCLS-local-proxy/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")
            self._send_json(502, {"error": f"WDS HTTP {e.code}", "details": msg[:400]})
        except Exception as e:
            self._send_json(502, {"error": "WDS proxy failed", "details": str(e)})

    def _proxy_statcan_csv(self, body):
        pid = str(body.get("pid", "")).strip()
        latest_n = int(body.get("latestN", 40) or 40)
        selected_members = body.get("selectedMembers", [])
        checked_levels = str(body.get("checkedLevels", "")).strip()
        start_date = str(body.get("startDate", "")).strip()
        end_date = str(body.get("endDate", "")).strip()
        if not pid:
            self._send_json(400, {"error": "Missing pid"})
            return
        if not isinstance(selected_members, list):
            self._send_json(400, {"error": "selectedMembers must be an array"})
            return

        q = urllib.parse.urlencode(
            {
                "pid": pid,
                "latestN": str(latest_n),
                "startDate": start_date,
                "endDate": end_date,
                "csvLocale": "en",
                "selectedMembers": json.dumps(selected_members),
                "checkedLevels": checked_levels,
            }
        )
        url = f"https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData-nonTraduit.action?{q}"
        req = urllib.request.Request(
            url=url,
            data=b"",
            method="POST",
            headers={
                "Accept": "text/csv,text/plain,*/*",
                "User-Agent": "BCLS-local-proxy/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")
            self._send_json(502, {"error": f"CSV HTTP {e.code}", "details": msg[:400]})
        except Exception as e:
            self._send_json(502, {"error": "CSV proxy failed", "details": str(e)})

    def do_POST(self):
        if self.path == "/api/statcan-wds":
            body = self._read_json_body()
            if body is None:
                self._send_json(400, {"error": "Invalid JSON"})
                return
            self._proxy_statcan_wds(body)
            return

        if self.path == "/api/statcan-csv":
            body = self._read_json_body()
            if body is None:
                self._send_json(400, {"error": "Invalid JSON"})
                return
            self._proxy_statcan_csv(body)
            return

        super().do_POST()


Handler = UTF8RequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[OK] Serving dashboard workspace from: {ROOT}")
    print(f"[OK] Hub URL:      http://localhost:{PORT}/dashboards/bc_dashboard_hub/html/dashboard.html")
    print(f"[OK] Macro URL:    http://localhost:{PORT}/dashboards/bc_macroeconomy/html/dashboard.html")
    print(f"   Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
