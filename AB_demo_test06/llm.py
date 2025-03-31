class LLMHelper:
 def __init__(self): self.embed_map={}
 def encode_embedding(self, vs):
  for v in vs: self.embed_map[v.uri] = [0.2, 0.4]