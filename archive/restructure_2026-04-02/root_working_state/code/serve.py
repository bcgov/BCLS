"""
Quick local server for the integrated BC Economic Monitor dashboard.
Run from the BCLS root folder:

    python code/serve.py

Then open:  http://localhost:8080/code/dashboard.html
"""
import http.server, socketserver, os, webbrowser, threading

PORT = 8080
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.chdir(ROOT)

def open_browser():
    import time; time.sleep(1.0)
    webbrowser.open(f"http://localhost:{PORT}/code/dashboard.html")

threading.Thread(target=open_browser, daemon=True).start()

class UTF8RequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
    }

Handler = UTF8RequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[OK] Serving integrated dashboard from: {ROOT}")
    print(f"[OK] Integrated URL: http://localhost:{PORT}/output/dashboard_integrated.html")
    print(f"[OK] Workbench URL:  http://localhost:{PORT}/code/dashboard.html")
    print(f"   Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

