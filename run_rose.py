import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # 静默控制台请求日志，保持清爽
        pass

def find_available_port(start_port=8080):
    import socket
    port = start_port
    while port < start_port + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
        port += 1
    return start_port

def main():
    os.chdir(DIRECTORY)
    port = find_available_port(PORT)
    url = f"http://localhost:{port}/particle_rose_diffusion.html"

    print("=" * 60)
    print("🌹 3D 梦幻粒子玫瑰 · 浪漫解离与聚合已就绪")
    print(f"🔗 本地服务地址: {url}")
    print("=" * 60)

    # 启动后台服务
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", port), Handler)

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # 自动在浏览器中打开页面
    time.sleep(0.5)
    print("🚀 正在自动为您打开默认浏览器...")
    webbrowser.open(url)

    print("\n按 Ctrl+C 可停止本地服务。享受浪漫视觉盛宴！\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 本地服务已安全退出。")
        server.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
