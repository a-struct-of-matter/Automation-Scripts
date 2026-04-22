from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

HOST = "127.0.0.1"
PORT = 8080

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        self.send_response(200)
        
        self.end_headers()

        response = f"Received params: {params}"
        self.wfile.write(response.encode())
    
    def do_POST(self):

        length = int(self.headers.get("Content-Length",0))
        data = self.rfile.read(length).decode()
        
        params = parse_qs(data)

        self.send_response(200)
        
        self.end_headers()

        response = f"Received params: {params}"
        self.wfile.write(response.encode())
        


server = HTTPServer((HOST,PORT), SimpleHandler)
print(f"Starting server at http://{HOST}:{PORT}")
server.serve_forever()

