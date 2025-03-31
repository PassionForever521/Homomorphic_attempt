import tenseal as ts
import numpy as np
import config
from llm import LLMHelper
from graph import Vertex, Graph
from party import Party

ctx = ts.context(ts.SCHEME_TYPE.CKKS, 4096, [60])
ctx.global_scale = 2**20
ctx.generate_galois_keys()
print("[B] CKKS ready.")

llm = LLMHelper()
v2 = Vertex("v2", "B")
llm.encode_embedding([v2])
print(f"[B] Embed: {llm.embed_map[v2.uri]}")

Party(port=config.PORT).receive_vector_compute_dot_and_send_norm(llm.embed_map[v2.uri], config.sigma, ctx)
