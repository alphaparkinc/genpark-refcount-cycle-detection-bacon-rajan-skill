import sys
import json
from client import RefCountEngine

engine = RefCountEngine()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "detect_cyclic_garbage",
                        "description": "Build graph and detect reference counted cycles",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "nodes": {"type": "array", "items": {"type": "string"}},
                                "edges": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}}
                            },
                            "required": ["nodes", "edges"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "detect_cyclic_garbage":
            e = RefCountEngine()
            nmap = {n: RefCountEngine.Node(n) for n in args["nodes"]}
            e.nodes.update(nmap.values())
            for u, v in args["edges"]:
                if u in nmap and v in nmap:
                    e.add_reference(nmap[u], nmap[v])
            cycs = e.find_isolated_cycles()
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"cyclic_nodes": [c.name for c in cycs]})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
