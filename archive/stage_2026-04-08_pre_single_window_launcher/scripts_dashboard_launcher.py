"""
BCLS Dashboard Launcher (desktop GUI)

Double-click run (via run_dashboard_launcher.bat) to:
1) start a local HTTP server (required by the dashboards), and
2) open dashboards with one click (no terminal needed).
"""

from __future__ import annotations

import http.server
import json
import os
import socket
import socketserver
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import ssl
import subprocess
from pathlib import Path
from typing import Iterable

import tkinter as tk
from tkinter import ttk


ROOT = Path(__file__).resolve().parents[1]
PREFERRED_PORTS = [8080, 8081, 8090, 0]


DASHBOARDS = [
    ("BC Dashboard Hub", "dashboards/bc_dashboard_hub/html/dashboard.html"),
    ("B.C. Economy Snapshot", "dashboards/bc_macroeconomy/html/dashboard.html"),
    ("Look West Strategy", "dashboards/look_west_strategy/html/dashboard.html"),
    ("Projects", "dashboards/projects/html/dashboard.html"),
    ("Life Sciences Sector", "dashboards/sectors/life_sciences/html/dashboard.html"),
    ("Trade & Logistics Sector", "dashboards/sectors/trade_logistics/html/dashboard.html"),
    ("Maritime Sector", "dashboards/sectors/maritime/html/dashboard.html"),
    ("AI & Quantum Sector", "dashboards/sectors/ai_quantum_computing/html/dashboard.html"),
    ("Aerospace Sector", "dashboards/sectors/aerospace/html/dashboard.html"),
    ("Construction Innovation Sector", "dashboards/sectors/construction_innovation/html/dashboard.html"),
    ("Agriculture Sector", "dashboards/sectors/agriculture/html/dashboard.html"),
    ("Tourism Sector", "dashboards/sectors/tourism/html/dashboard.html"),
]


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class DashboardRequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
    }

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def _read_json_body(self):
        n = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(n) if n > 0 else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def _urlopen_no_proxy(self, req: urllib.request.Request, timeout: int):
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        )
        try:
            return opener.open(req, timeout=timeout)
        except Exception:
            opener_insecure = urllib.request.build_opener(
                urllib.request.ProxyHandler({}),
                urllib.request.HTTPSHandler(context=ssl._create_unverified_context()),
            )
            return opener_insecure.open(req, timeout=timeout)

    def _curl_post_no_proxy(self, url: str, headers: dict, data: bytes, timeout_sec: int) -> bytes:
        cmd = ["curl.exe", "-sS", "-L", "--max-time", str(int(timeout_sec)), "-X", "POST", url]
        for k, v in (headers or {}).items():
            cmd.extend(["-H", f"{k}: {v}"])
        cmd.extend(["--data-binary", "@-"])
        env = os.environ.copy()
        for k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy", "NO_PROXY", "no_proxy"):
            env[k] = ""
        proc = subprocess.run(cmd, input=(data or b""), capture_output=True, env=env)
        if proc.returncode != 0:
            err = (proc.stderr or b"").decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"curl failed ({proc.returncode}): {err[:300]}")
        return proc.stdout

    # Browser-like headers that StatsCan accepts
    _BROWSER_UA = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    _STC_ORIGIN   = "https://www150.statcan.gc.ca"
    _STC_REFERER  = "https://www150.statcan.gc.ca/n1/en/type/data"

    def _proxy_statcan_wds(self, body: dict) -> None:
        path = str(body.get("path", "")).strip().lstrip("/")
        payload = body.get("payload", [])
        if not path:
            self._send_json(400, {"error": "Missing path"})
            return
        if not isinstance(payload, list):
            self._send_json(400, {"error": "payload must be an array"})
            return

        url = f"https://www150.statcan.gc.ca/t1/wds/rest/{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url=url,
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": self._BROWSER_UA,
                "Origin": self._STC_ORIGIN,
                "Referer": self._STC_REFERER,
                "Accept-Language": "en-CA,en;q=0.9",
            },
        )
        try:
            with self._urlopen_no_proxy(req, timeout=45) as resp:
                raw = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")
            import sys; print(f"[WDS proxy] HTTP {e.code} from StatsCan: {msg[:300]}", file=sys.stderr)
            self._send_json(502, {"error": f"WDS HTTP {e.code}", "details": msg[:400]})
        except Exception as e:
            try:
                raw = self._curl_post_no_proxy(
                    url,
                    {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": self._BROWSER_UA,
                        "Origin": self._STC_ORIGIN,
                        "Referer": self._STC_REFERER,
                        "Accept-Language": "en-CA,en;q=0.9",
                    },
                    data,
                    45,
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
                return
            except Exception as e2:
                detail = f"{type(e).__name__}: {repr(e)} | curl fallback: {type(e2).__name__}: {repr(e2)}"
                import sys; print(f"[WDS proxy] error: {detail}", file=sys.stderr)
                self._send_json(502, {"error": "WDS proxy failed", "details": detail})

    def _proxy_statcan_csv(self, body: dict) -> None:
        pid = str(body.get("pid", "")).strip()
        try:
            latest_n = int(float(body.get("latestN", 40) or 40))
        except Exception:
            latest_n = 40
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

        # Build the download URL (all params in query string, POST body is empty).
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
        url = (
            "https://www150.statcan.gc.ca/t1/tbl1/en/"
            f"dtl!downloadDbLoadingData-nonTraduit.action?{q}"
        )

        # StatsCan's CSV download endpoint requires browser-like headers and
        # a non-empty POST body (a space byte satisfies servers that check Content-Length).
        req = urllib.request.Request(
            url=url,
            data=b" ",
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "text/csv,text/plain,*/*",
                "User-Agent": self._BROWSER_UA,
                "Origin": self._STC_ORIGIN,
                "Referer": f"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid={pid}",
                "Accept-Language": "en-CA,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        try:
            with self._urlopen_no_proxy(req, timeout=90) as resp:
                raw = resp.read()
            # Decompress if server sent gzip despite us asking for it
            content = raw
            ct = resp.headers.get("Content-Type", "")
            if resp.headers.get("Content-Encoding") == "gzip" or (content[:2] == b"\x1f\x8b"):
                import gzip
                try:
                    content = gzip.decompress(raw)
                except Exception:
                    pass
            decoded = content.decode("utf-8-sig", errors="replace")
            if "REF_DATE" not in decoded:
                import sys
                print(f"[CSV proxy] StatsCan returned non-CSV for pid={pid}: {decoded[:300]}", file=sys.stderr)
                self._send_json(502, {
                    "error": "StatsCan did not return CSV data",
                    "details": decoded[:400],
                })
                return
            out = decoded.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")
            import sys; print(f"[CSV proxy] HTTP {e.code} from StatsCan: {msg[:300]}", file=sys.stderr)
            self._send_json(502, {"error": f"CSV HTTP {e.code}", "details": msg[:400]})
        except Exception as e:
            try:
                raw = self._curl_post_no_proxy(
                    url,
                    {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "text/csv,text/plain,*/*",
                        "User-Agent": self._BROWSER_UA,
                        "Origin": self._STC_ORIGIN,
                        "Referer": f"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid={pid}",
                        "Accept-Language": "en-CA,en;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    b" ",
                    90,
                )
                decoded = raw.decode("utf-8-sig", errors="replace")
                if "REF_DATE" not in decoded:
                    self._send_json(502, {
                        "error": "StatsCan did not return CSV data",
                        "details": decoded[:400],
                    })
                    return
                out = decoded.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)
                return
            except Exception as e2:
                detail = f"{type(e).__name__}: {repr(e)} | curl fallback: {type(e2).__name__}: {repr(e2)}"
                import sys; print(f"[CSV proxy] error: {detail}", file=sys.stderr)
                self._send_json(502, {"error": "CSV proxy failed", "details": detail})

    def do_POST(self):
        try:
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
        except Exception as e:
            self._send_json(500, {"error": "Local proxy handler failure", "details": str(e)})

    def log_message(self, format: str, *args) -> None:
        # Suppress routine GET/POST access logs but let errors through.
        msg = format % args if args else format
        if '502' in msg or '500' in msg or '400' in msg or 'error' in msg.lower():
            import sys
            print(f"[Server] {msg}", file=sys.stderr)


def pick_port(candidates: Iterable[int]) -> int:
    for port in candidates:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("", port))
                return s.getsockname()[1]
            except OSError:
                continue
    raise RuntimeError("No available port found.")


class LauncherApp:
    def __init__(self) -> None:
        os.chdir(ROOT)
        self.port = pick_port(PREFERRED_PORTS)
        self.server = ThreadingTCPServer(("", self.port), DashboardRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

        self.root = tk.Tk()
        self.root.title("BC Dashboard Suite — Server Manager")
        self.root.geometry("540x300")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.launcher_url = self.url_for("launcher.html")
        self._build_ui()

        # Open the beautiful HTML launcher in the browser automatically
        self.root.after(400, lambda: webbrowser.open(self.launcher_url))

    def url_for(self, rel_path: str) -> str:
        return f"http://localhost:{self.port}/{rel_path}"

    def open_url(self, rel_path: str) -> None:
        webbrowser.open(self.url_for(rel_path))

    def _build_ui(self) -> None:
        # ── Outer frame with BC navy background ──────────────────────────────
        outer = tk.Frame(self.root, bg="#003366", bd=0)
        outer.pack(fill=tk.BOTH, expand=True)

        # Gold accent bar at top
        gold_bar = tk.Frame(outer, bg="#FCBA19", height=4)
        gold_bar.pack(fill=tk.X, side=tk.TOP)

        # ── Header row ────────────────────────────────────────────────────────
        hdr = tk.Frame(outer, bg="#003366")
        hdr.pack(fill=tk.X, padx=24, pady=(18, 4))
        tk.Label(
            hdr, text="BC",
            bg="#FCBA19", fg="#003366",
            font=("Segoe UI", 10, "bold"),
            padx=8, pady=2,
        ).pack(side=tk.LEFT)
        tk.Label(
            hdr, text="  British Columbia Dashboard Suite",
            bg="#003366", fg="#FFFFFF",
            font=("Segoe UI", 13, "bold"),
        ).pack(side=tk.LEFT)

        # ── Status card ───────────────────────────────────────────────────────
        card = tk.Frame(outer, bg="#0A3A6B", bd=0)
        card.pack(fill=tk.X, padx=24, pady=(14, 0))

        # Status row
        status_row = tk.Frame(card, bg="#0A3A6B")
        status_row.pack(fill=tk.X, padx=18, pady=(16, 4))

        dot_canvas = tk.Canvas(status_row, width=10, height=10, bg="#0A3A6B", highlightthickness=0)
        dot_canvas.pack(side=tk.LEFT, padx=(0, 7))
        dot_canvas.create_oval(1, 1, 9, 9, fill="#4CAF50", outline="")

        tk.Label(
            status_row,
            text="Server running",
            bg="#0A3A6B", fg="#4CAF50",
            font=("Segoe UI", 10, "bold"),
        ).pack(side=tk.LEFT)

        tk.Label(
            card,
            text=f"  http://localhost:{self.port}",
            bg="#0A3A6B", fg="#79B8FF",
            font=("Segoe UI Mono", 10) if "Segoe UI Mono" else ("Courier", 10),
            anchor="w",
        ).pack(fill=tk.X, padx=18, pady=(2, 14))

        # ── Buttons ────────────────────────────────────────────────────────────
        btn_row = tk.Frame(outer, bg="#003366")
        btn_row.pack(fill=tk.X, padx=24, pady=(18, 0))

        open_btn = tk.Button(
            btn_row,
            text="⬡  Open Dashboard Launcher",
            bg="#FCBA19", fg="#003366",
            font=("Segoe UI", 11, "bold"),
            relief="flat", bd=0, cursor="hand2",
            padx=20, pady=9,
            activebackground="#FFD040", activeforeground="#003366",
            command=lambda: webbrowser.open(self.launcher_url),
        )
        open_btn.pack(side=tk.LEFT)

        hub_btn = tk.Button(
            btn_row,
            text="  Dashboard Hub  →",
            bg="#1A4F8A", fg="#FFFFFF",
            font=("Segoe UI", 10),
            relief="flat", bd=0, cursor="hand2",
            padx=16, pady=9,
            activebackground="#2563EB", activeforeground="#FFFFFF",
            command=lambda: self.open_url("dashboards/bc_dashboard_hub/html/dashboard.html"),
        )
        hub_btn.pack(side=tk.LEFT, padx=(10, 0))

        # ── Tip ───────────────────────────────────────────────────────────────
        gold_bar2 = tk.Frame(outer, bg="#FCBA19", height=1)
        gold_bar2.pack(fill=tk.X, pady=(20, 0))

        tk.Label(
            outer,
            text="💡  Keep this window open while using dashboards. Close to stop the server.",
            bg="#002244", fg="#8AA8C8",
            font=("Segoe UI", 9),
            pady=10,
        ).pack(fill=tk.X, padx=0)

    def on_close(self) -> None:
        try:
            self.server.shutdown()
            self.server.server_close()
        except Exception:
            pass
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = LauncherApp()
    app.run()


if __name__ == "__main__":
    main()
