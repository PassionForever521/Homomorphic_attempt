import os
import sys
import tenseal as ts
import numpy as np
import config
from config import parse_config
from llm import LLMHelper
from graph import Entity
from party import Party

cfg_path = os.path.join(os.path.dirname(__file__), "config.xml")
parse_config(cfg_path)

def init_ctx():
    ctx = ts.context(ts.SCHEME_TYPE.CKKS, 8192, [60, 40, 40, 60])
    ctx.global_scale = 2**40
    ctx.generate_galois_keys()
    return ctx

if __name__ == "__main__":
    llm = LLMHelper()
    e1 = Entity("uri1", "cat")
    e2 = Entity("uri2", "dog")
    llm.encode_embedding([e1, e2])

    plain_sim = llm.plntxt_vertex_similarity_check("uri1", "uri2", sigma=config.sigma)
    print(f"明文相似度是否 >= {config.sigma}: {plain_sim}")

    secure_sim = llm.secure_vertex_similarity_check("uri1", "uri2", sigma=config.sigma)
    print(f"加密相似度是否 >= {config.sigma}: {secure_sim}")

    if len(sys.argv) == 2:
        ctx = init_ctx()
        if sys.argv[1] == "A":
            emb = ts.ckks_vector(ctx, llm.embed_map["uri1"])
            print("[Party A] 发送加密 embedding...")
            res = Party().send_encrypted_vector(emb)
            print("[Party A] 接收到判断结果:", res)
        elif sys.argv[1] == "B":
            emb = ts.ckks_vector(ctx, llm.embed_map["uri2"])
            print("[Party B] 等待接收加密 embedding...")
            Party().receive_and_compute_similarity(emb, config.sigma, ctx)
