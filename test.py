import json
from pathlib import Path
from typing import Any

def shape_only(x: Any):
    """Return a structure preserving keys; values collapsed to {} / [] / 'type'."""
    if isinstance(x, dict):
        return {k: shape_only(v) for k, v in x.items()}
    if isinstance(x, list):
        # Merge shapes of all list items to capture union of keys
        if not x:
            return []  # empty list
        merged = None
        for item in x:
            s = shape_only(item)
            if isinstance(s, dict):
                if merged is None:
                    merged = {}
                if isinstance(merged, dict):
                    for k, v in s.items():
                        if k in merged:
                            merged[k] = merge_shapes(merged[k], v)
                        else:
                            merged[k] = v
                else:
                    merged = s  # fallback
            elif isinstance(s, list):
                merged = []  # list of lists; represent simply as []
            else:
                # scalars inside list; represent as 'type'
                merged = type_tag(item)
        return merged if merged is not None else []
    # scalar
    return type_tag(x)

def merge_shapes(a, b):
    """Merge two shapes for arrays of objects with varying keys."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k, v in b.items():
            if k in out:
                out[k] = merge_shapes(out[k], v)
            else:
                out[k] = v
        return out
    if isinstance(a, list) or isinstance(b, list):
        return []  # keep simple for nested lists
    # Prefer a if same scalar/type; else fallback to a
    return a

def type_tag(x):
    if x is None: return "null"
    if isinstance(x, bool): return "boolean"
    if isinstance(x, (int, float)): return "number"
    if isinstance(x, str): return "string"
    return "unknown"

def print_tree(shape, indent=0, name=None):
    prefix = "  " * indent
    if name is not None:
        print(f"{prefix}{name}: ", end="")
        prefix = "  " * (indent + 1)

    if isinstance(shape, dict):
        print("{}")
        for k, v in shape.items():
            print_tree(v, indent + 1, k)
    elif isinstance(shape, list):
        print("[]")
        # Optionally show internal dict keys for list of objects
        if shape and isinstance(shape, dict):
            for k, v in shape.items():
                print_tree(v, indent + 1, k)
    else:
        print(shape)

if __name__ == "__main__":
    in_path = Path("provenance.json")   # <-- your file
    out_path = Path("provenance_keys.json")

    data = json.loads(in_path.read_text(encoding="utf-8"))
    shape = shape_only(data)

    # 1) Print a tree view to console
    print("Structure of keys:\n")
    if isinstance(shape, dict):
        for k, v in shape.items():
            print_tree(v, 0, k)
    else:
        # top-level list or scalar
        print_tree(shape)

    # 2) Save schema-like JSON preserving key structure
    out_path.write_text(json.dumps(shape, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved key structure to: {out_path.resolve()}")