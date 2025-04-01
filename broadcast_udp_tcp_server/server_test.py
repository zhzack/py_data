import socket
import threading
import time

UDP_PORT = 4210   # UDP 发现端口
TCP_PORT = 8080   # TCP 服务器端口
BUFFER_SIZE = 1024

# 获取本机 IP
server_ip = socket.gethostbyname(socket.gethostname())

def udp_server():
    """UDP 服务器：监听发现请求并返回本机 IP"""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.bind(("", UDP_PORT))
    print(f"UDP Server listening on port {UDP_PORT}...")

    while True:
        data, client_addr = udp_socket.recvfrom(BUFFER_SIZE)
        message = data.decode("utf-8")
        print(f"Received UDP message '{message}' from {client_addr}")

        if message == "DISCOVER_SERVER":
            response = f"SERVER_IP:{server_ip}"
            udp_socket.sendto(response.encode(), client_addr)
            print(f"Sent UDP response '{response}' to {client_addr}")

def tcp_server():
    """TCP 服务器：等待客户端连接并发送心跳包"""
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((server_ip, TCP_PORT))
    tcp_socket.listen(5)
    print(f"TCP Server listening on port {TCP_PORT}...")

    while True:
        client_socket, client_addr = tcp_socket.accept()
        print(f"New TCP connection from {client_addr}")

        while True:
            try:
                client_socket.sendall(b"HEARTBEAT\n")
                time.sleep(1)
            except:
                print(f"Client {client_addr} disconnected.")
                client_socket.close()
                break

# 启动 UDP 和 TCP 服务器线程
threading.Thread(target=udp_server, daemon=True).start()
threading.Thread(target=tcp_server, daemon=True).start()

# 保持主线程运行
while True:
    time.sleep(1)
