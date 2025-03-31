class Vertex:
 def __init__(self, uri, label): self.uri = uri; self.label = label
class Graph:
 def __init__(self): self.vertices=[]
 def add_vertex(self, v): self.vertices.append(v)