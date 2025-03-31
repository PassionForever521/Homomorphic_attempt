import numpy as np
import tenseal as ts
import random
import config
from llm import LLMHelper
from graph import Vertex, Graph
from party import Party
import time

ctx = ts.context(ts.SCHEME_TYPE.CKKS, 4096, [60])
ctx.global_scale = 2**20
ctx.generate_galois_keys()
print("[Party A] CKKS context ready.")

llm = LLMHelper()
v1 = Vertex("v1", "A")
llm.encode_embedding([v1])
print(f"[A] Embed: {llm.embed_map[v1.uri]}")

r = round(random.uniform(0.8, 1.2), 4)
print(f"[A] Random mask r = {r}")
masked = np.array(llm.embed_map[v1.uri]) * r
enc = ts.ckks_vector(ctx, masked)
print("[A] Encrypted masked vector.")

start = time.time()
dot, norm2 = Party(port=config.PORT).send_vector_and_receive_norm(enc)
dot = float(dot) / r
norm1 = np.linalg.norm(llm.embed_map[v1.uri])
sim = dot / (norm1 * norm2)
end = time.time()

print(f"[A] Cosine similarity = {sim:.4f}, >= sigma? {sim >= config.sigma}")
print(f"[A] Done in {end - start:.2f}s")
