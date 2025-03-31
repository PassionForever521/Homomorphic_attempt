import socket
import pickle
import tenseal as ts

class Party:
    def __init__(self, ip_addr="127.0.0.1", port=9000):
        self.ip_addr = ip_addr
        self.port = port
 # A 端函数：将加密向量发送到 B 端
    def send_encrypted_vector(self, encrypted_vec):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip_addr, self.port))
            data = pickle.dumps(encrypted_vec.serialize())
            s.sendall(data)
            result = s.recv(1024).decode()
            #A 发r
            return result
# B 端函数：监听接收密文向量，计算加密相似度并返回 True/False
    def receive_and_compute_similarity(self, local_vec, sigma, ctx):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip_addr, self.port))
            s.listen(1)
            print(f"[Party B] Listening on {self.ip_addr}:{self.port} ...")
            #B接受r
            conn, addr = s.accept()
            with conn:
                print(f"[Party B] Connected by {addr}")
                received = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    received += chunk
                # 恢复为向量by反序
                remote_cipher = ts.ckks_vector_from(ctx, pickle.loads(received))
                dot = remote_cipher.dot(local_vec)
                # 找解密结果
                sim = dot.decrypt()[0]
                result = "True" if sim >= sigma else "False"
                print(f"[Party B] Decrypted similarity = {sim:.4f}, >= sigma? {result}")
                conn.sendall(result.encode())
