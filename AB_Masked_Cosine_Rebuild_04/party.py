import tenseal as ts
import numpy as np
import socket
import pickle

PORT = 9007
EMBED_A = [0.2, 0.4]
EMBED_B = [0.2, 0.4]
SIGMA = 0.6

class PartyA:
    def __init__(self):
        self.context = ts.context(ts.SCHEME_TYPE.CKKS, 8192, [60, 40, 40, 60])
        self.context.generate_galois_keys()
        self.context.global_scale = 2 ** 40

    def run(self):
        print("[A] CKKS context ready.")
        embed = np.array(EMBED_A)
        print("[A] Embed:", embed)
        r = np.random.uniform(0.5, 1.5)
        print("[A] Random mask r =", round(r, 4))
        masked = embed * r
        print("[A] Masked vector:", masked)
        encrypted = ts.ckks_vector(self.context, masked)
        print("[A] Encrypted masked vector.")

        payload = {
            "enc": encrypted.serialize(),
            "r": r
        }

        with socket.create_connection(("127.0.0.1", PORT)) as sock:
            data = pickle.dumps(payload)
            sock.sendall(data)
            print("[A] Sent encrypted data + mask to B.")

class PartyB:
    def __init__(self):
        self.context = ts.context(ts.SCHEME_TYPE.CKKS, 8192, [60, 40, 40, 60])
        self.context.generate_galois_keys()
        self.context.global_scale = 2 ** 40
        self.embed = np.array(EMBED_B)

    def listen(self):
        print("[B] CKKS ready.")
        print("[B] Embed:", self.embed)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", PORT))
            s.listen(1)
            print(f"[B] Listening 127.0.0.1:{PORT}...")
            conn, _ = s.accept()
            with conn:
                print("[B] Connected.")
                data = b""
                while True:
                    part = conn.recv(4096)
                    if not part:
                        break
                    data += part
                payload = pickle.loads(data)
                enc_vec = ts.ckks_vector_from(self.context, payload["enc"])
                r = payload["r"]
                print("[B] Received encrypted vector and r =", round(r, 4))

                dot = enc_vec.dot(self.embed).decrypt()[0]
                norm = np.linalg.norm(self.embed)
                cosine_sim = dot / (norm * r)
                result = cosine_sim >= SIGMA
                print(f"[B] Cosine similarity = {cosine_sim:.4f}, >= sigma? {result}")