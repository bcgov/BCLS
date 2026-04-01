"""
Quick local server for the BCLS dashboard.
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

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"✓  Serving BCLS from:  {ROOT}")
    print(f"✓  Dashboard URL:      http://localhost:{PORT}/code/dashboard.html")
    print(f"   Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
