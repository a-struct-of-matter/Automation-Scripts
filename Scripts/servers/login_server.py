from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

HOST = "127.0.0.1"
PORT = 8080

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
            print("Received GET request")
            parsed = urlparse(self.path)
            print("Path:", parsed.path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            html = """
            <html>
            <body>
                <h1>Login Form</h1>
                <form method="POST" action="/">
                    <input type="text" name="username" placeholder="Username" required/>
                    <br><br>
                    <input type="password" name="password" placeholder="Password" required/>
                    <br><br>
                    <input type="submit" value="Login"/>
                </form>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length",0))
        data = self.rfile.read(length).decode()
        

        params = parse_qs(data)

        username = params.get("username", [""])[0]
        password = params.get("password", [""])[0]

        if username == "admin" and password == "Gravity@5237":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            parse = urlparse(self.path)
            self.end_headers()
            print("Path:",parse.path)
            self.wfile.write(b"<h1>Login Successful</h1>")


        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Unauthorized Access</h1>")

        
try:
     
    server = HTTPServer((HOST,PORT), SimpleHandler)
    print(f"The server is running on: http://{HOST}:{PORT}")
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer is stopping...")
    server.server_close()
    print("Server stopped.")