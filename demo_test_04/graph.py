class Entity:
    def __init__(self, uri, label):
        self.uri = uri
        self.label = label

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label
