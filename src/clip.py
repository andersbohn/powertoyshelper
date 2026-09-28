from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

content = "Paste or type text here..."

class ClipboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html = f"""<!DOCTYPE html>
        <html>
        <head><title>Shared Clipboard</title></head>
        <body style="font-family: sans-serif; padding: 20px;">
          <h2>Shared Web Clipboard</h2>
          <form method="POST">
            <textarea name="text" rows="12" style="width: 100%; font-family: monospace;">{content}</textarea><br><br>
            <button type="submit" style="padding: 10px 20px; font-size: 16px;">Save & Update</button>
          </form>
        </body>
        </html>"""
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        global content
        length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(length).decode("utf-8")
        parsed = urllib.parse.parse_qs(post_data)
        content = parsed.get("text", [""])[0]
        self.do_GET()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), ClipboardHandler)
    print("Shared clipboard running on port 8000...")
    server.serve_forever()