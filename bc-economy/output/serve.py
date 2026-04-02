"""
BC Economic Monitor — Local HTTP Server
========================================
Run this script from the output/ folder to serve the dashboard
over localhost so the live Statistics Canada API calls work.

Usage:
    python serve.py

Then open:
    http://localhost:8080/dashboard_standalone.html
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8080
FILE = "dashboard_standalone.html"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress request logs for cleanliness

url = f"http://localhost:{PORT}/{FILE}"
print(f"\n  BC Economic Monitor — Local Server")
print(f"  ─────────────────────────────────────")
print(f"  Serving:  {os.getcwd()}")
print(f"  Open:     {url}")
print(f"  Stop:     Ctrl + C\n")

webbrowser.open(url)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
