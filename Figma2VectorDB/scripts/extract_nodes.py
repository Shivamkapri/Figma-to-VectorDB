# #!/usr/bin/env python3
# import json, sys
# from typing import List, Dict

# def extract_text_nodes(json_path: str) -> List[Dict]:
#     """Collect all SHAPE_WITH_TEXT nodes from Figma JSON."""
#     try:
#         with open(json_path, 'r', encoding='utf-8') as f:
#             root = json.load(f)
#     except Exception as e:
#         print(f"❌ Error reading {json_path}: {e}", file=sys.stderr)
#         sys.exit(1)

#     def traverse(node):
#         out = []
#         if node.get("type") == "SHAPE_WITH_TEXT":
#             txt = node.get("characters", "").strip()
#             if txt:
#                 out.append({
#                     "id": node["id"],
#                     "name": node.get("name",""),
#                     "text": txt
#                 })
#         for child in node.get("children", []):
#             out += traverse(child)
#         return out

#     return traverse(root.get("document", {}))

# if __name__ == "__main__":
#     nodes = extract_text_nodes("data/figma_data.json")
#     with open("data/text_nodes.json", "w", encoding='utf-8') as f:
#         json.dump(nodes, f, indent=2, ensure_ascii=False)
#     print(f"✅ Extracted {len(nodes)} text nodes → data/text_nodes.json")



#!/usr/bin/env python3
import json, sys, os
from typing import List, Dict

JSON_PATH = os.path.join("data", "figma_data.json")
OUT_PATH  = os.path.join("data", "text_nodes.json")

def extract_text_nodes(json_path: str) -> List[Dict]:
    """Recursively collect SHAPE_WITH_TEXT nodes from Figma JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        root = json.load(f)

    def traverse(node):
        out = []
        if node.get("type") == "SHAPE_WITH_TEXT":
            text = node.get("characters", "").strip()
            if text:
                out.append({
                    "id": node["id"],
                    "name": node.get("name",""),
                    "text": text
                })
        for child in node.get("children", []):
            out += traverse(child)
        return out

    return traverse(root.get("document", {}))

if __name__ == "__main__":
    # 1️⃣ Check input file
    if not os.path.isfile(JSON_PATH):
        print(f"❌ Could not find '{JSON_PATH}'. Are you in the project root?", file=sys.stderr)
        sys.exit(1)

    # 2️⃣ Extract nodes
    try:
        nodes = extract_text_nodes(JSON_PATH)
    except Exception as e:
        print(f"❌ Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # 3️⃣ Write output
    try:
        os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
        with open(OUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error writing '{OUT_PATH}': {e}", file=sys.stderr)
        sys.exit(1)

    # 4️⃣ Success message
    print(f"✅ Extracted {len(nodes)} text nodes → {OUT_PATH}")
