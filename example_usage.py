from client import RefCountEngine

engine = RefCountEngine()
a = RefCountEngine.Node("A")
b = RefCountEngine.Node("B")
engine.nodes.update([a, b])

engine.add_reference(a, b)
engine.add_reference(b, a)

cycles = engine.find_isolated_cycles()
print(f"Detected {len(cycles)} nodes participating in cycles: {[c.name for c in cycles]}")
