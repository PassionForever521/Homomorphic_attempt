import socket, pickle, tenseal as ts, numpy as np
class Party:
    def __init__(self, ip_addr="127.0.0.1", port=9006):
        self.ip = ip_addr; self.port = port

    def send_vector_and_receive_norm(self, vec):
        with socket.socket() as s:
            s.connect((self.ip, self.port))
            s.sendall(pickle.dumps(vec.serialize()))
            s.shutdown(socket.SHUT_WR)  # Fix: notify B transmission is done
            result = b""
            while True:
                part = s.recv(4096)
                if not part: break
                result += part
            return pickle.loads(result)

    def receive_vector_compute_dot_and_send_norm(self, local, sigma, ctx):
        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            s.bind((self.ip, self.port)); s.listen(1)
            print(f"[B] Listening {self.ip}:{self.port}...")
            conn, _ = s.accept()
            with conn:
                print("[B] Connected.")
                data = b""
                while True:
                    part = conn.recv(4096)
                    if not part: break
                    data += part
                remote = ts.ckks_vector_from(ctx, pickle.loads(data))
                dot = remote.dot(local).decrypt()[0]
                norm = np.linalg.norm(local)
                conn.sendall(pickle.dumps((dot, norm)))
                print(f"[B] Done. Dot={dot:.4f}, Norm={norm:.4f}")
