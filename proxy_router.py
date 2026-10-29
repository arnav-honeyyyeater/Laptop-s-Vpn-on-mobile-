import socket
import select
import threading
import sys

def handle_client(client_socket):
    try:
        request = b""
        client_socket.settimeout(5.0)
        while b"\r\n\r\n" not in request:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            request += chunk
            if len(request) > 65536:
                break

        if not request:
            client_socket.close()
            return

        first_line = request.split(b"\r\n")[0].decode('latin1', errors='ignore')
        words = first_line.split()
        if len(words) < 2:
            client_socket.close()
            return

        method = words[0].upper()
        target = words[1]

        if method == "CONNECT":
            # HTTPS Tunneling
            if ":" in target:
                host, port_s = target.split(":", 1)
                port = int(port_s)
            else:
                host = target
                port = 443

            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.settimeout(10.0)
            target_socket.connect((host, port))
            client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\nProxy-Agent: HotspotVPNRouter/1.0\r\n\r\n")

            sockets = [client_socket, target_socket]
            client_socket.setblocking(False)
            target_socket.setblocking(False)

            while True:
                readable, _, exceptional = select.select(sockets, [], sockets, 60)
                if exceptional or not readable:
                    break
                for s in readable:
                    other = target_socket if s is client_socket else client_socket
                    try:
                        data = s.recv(16384)
                        if not data:
                            return
                        other.sendall(data)
                    except Exception:
                        return
        else:
            # Regular HTTP Proxying
            url = target
            if url.startswith("http://"):
                url = url[7:]
            host_port = url.split("/")[0]
            if ":" in host_port:
                host, port_s = host_port.split(":", 1)
                port = int(port_s)
            else:
                host = host_port
                port = 80

            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.settimeout(10.0)
            target_socket.connect((host, port))
            target_socket.sendall(request)

            sockets = [client_socket, target_socket]
            client_socket.setblocking(False)
            target_socket.setblocking(False)

            while True:
                readable, _, exceptional = select.select(sockets, [], sockets, 60)
                if exceptional or not readable:
                    break
                for s in readable:
                    other = target_socket if s is client_socket else client_socket
                    try:
                        data = s.recv(16384)
                        if not data:
                            return
                        other.sendall(data)
                    except Exception:
                        return
    except Exception:
        pass
    finally:
        try:
            client_socket.close()
        except:
            pass

def main():
    host = "0.0.0.0"
    port = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(128)
    print(f"[+] Hotspot VPN Proxy Server listening on {host}:{port}...", flush=True)
    while True:
        try:
            client_sock, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(client_sock,), daemon=True)
            t.start()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[!] Server error: {e}", flush=True)

if __name__ == "__main__":
    main()
