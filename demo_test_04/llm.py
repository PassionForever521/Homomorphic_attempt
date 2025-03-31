import tenseal as ts 
from sentence_transformers import SentenceTransformer
import numpy as np
from scipy.spatial.distance import cosine
from typing import List, Dict
from graph import Entity

class LLMHelper:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the SentenceTransformer model and set up an empty embedding map.
        """
        self.model = SentenceTransformer(model_name)
        self.embed_map: Dict[str, np.ndarray] = {}
    
    def encode_embedding(self, entities: List[Entity]) -> Dict[str, np.ndarray]:
        """
        Compute embeddings for each entity using its label and store the results in a map,
        with the entity URI as the key.
        """
        embed_map: Dict[str, np.ndarray] = {}
        for e in entities:
            # Generate embedding using the entity's label.
            embedding = self.model.encode(e.get_label())
            embed_map[e.uri] = embedding
        self.embed_map = embed_map  # save the embedding map for later use
        return embed_map
    
    def _cosine_similarity_pltxt(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute the cosine similarity between two plaintext embeddings.
        """
        similarity = 1 - cosine(embedding1, embedding2)
        return similarity

    def _cosine_similarity_secure(self, ciphertext1, ciphertext2, random_mask: float) -> float:
        """
        Compute a "secure" cosine similarity between two encrypted embeddings.
        This is a placeholder; the exact implementation depends on your homomorphic encryption scheme.
        """
        dot_product = ciphertext1.dot(ciphertext2)
        similarity_secure = dot_product * random_mask
        return similarity_secure

    def plntxt_vertex_similarity_check(self, uri1: str, uri2: str, sigma: float) -> bool:
        """
        Check if the cosine similarity between the plaintext embeddings of the two vertices
        (identified by their URIs) is at least sigma.
        """
        # Ensure that embeddings for both URIs exist.
        assert uri1 in self.embed_map and uri2 in self.embed_map, "Embeddings not found for one or both URIs."
        embed1 = self.embed_map[uri1]
        embed2 = self.embed_map[uri2]
        return sigma <= self._cosine_similarity_pltxt(embed1, embed2)

    def secure_vertex_similarity_check(self, uri1: str, uri2: str, sigma: float) -> bool:
        from tenseal import context, SCHEME_TYPE, ckks_vector
        assert uri1 in self.embed_map and uri2 in self.embed_map
        emb1 = self.embed_map[uri1]
        emb2 = self.embed_map[uri2]
        # 创建 CKKS (TenSEAL?)加密上下文
        ctx = context(SCHEME_TYPE.CKKS, 8192, [60, 40, 40, 60])
        ctx.generate_galois_keys()
        ctx.global_scale = 2 ** 40
         # 加密两个 embedding
        enc1 = ckks_vector(ctx, emb1)
        enc2 = ckks_vector(ctx, emb2)
        # 计算加密 dot product，并解密（解密返回 list）
        dot_product = enc1.dot(enc2).decrypt()[0]
        # 还原 cosine
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        cosine_sim = dot_product / (norm1 * norm2)
        return cosine_sim >= sigma
