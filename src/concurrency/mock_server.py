from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

class MockHandler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        # 1. Имитация задержки(чтоб нагрузка была реалистичной)
        time.sleep(0.05)
        
        # 2. Подготовка ответа
        response = {"status": "ok", "path": self.path}
        body = json.dumps(response).encode("utf-8") #ютф8 чтоб байты отправлть
        
        # 3. Отправка заголовков
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers() #заголовки капут
        
        # 4. Отправка тела
        self.wfile.write(body)

def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = HTTPServer((host, port), MockHandler)
    print(f"Mock server running on http://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()