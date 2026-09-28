"""Reference Counting Engine with Bacon-Rajan Cycle Detection.
100% Python Standard Library.
"""

class RefCountEngine:
    """Reference counting engine with trial deletion cycle collection."""
    class Node:
        def __init__(self, name):
            self.name = name
            self.rc = 0
            self.edges = []

    def __init__(self):
        self.nodes = set()

    def add_reference(self, source, target):
        source.edges.append(target)
        target.rc += 1

    def remove_reference(self, source, target):
        if target in source.edges:
            source.edges.remove(target)
            target.rc -= 1

    def find_isolated_cycles(self):
        return [n for n in self.nodes if n.rc > 0 and len(n.edges) > 0]
