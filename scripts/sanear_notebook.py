import json, sys, uuid, nbformat

path = sys.argv[1] if len(sys.argv) > 1 else "notebooks/01_training.ipynb"
nb = json.load(open(path))
nb["nbformat"] = 4
nb["nbformat_minor"] = 5
nb.get("metadata", {}).pop("colab", None)
nb.get("metadata", {}).pop("widgets", None)
seen = set()
for c in nb["cells"]:
    md = c.setdefault("metadata", {})
    for k in ("id", "colab", "outputId", "executionInfo", "colab_type"):
        md.pop(k, None)
    md.pop("widgets", None)
    cid = c.get("id")
    if (not cid or len(str(cid)) > 64
            or not str(cid).replace("-", "").replace("_", "").isalnum()
            or cid in seen):
        c["id"] = uuid.uuid4().hex[:8]
    seen.add(c["id"])
    if c["cell_type"] == "code":
        c["outputs"] = [o for o in c.get("outputs", [])
                        if not (o.get("output_type") == "stream" and o.get("name") == "stderr")]
json.dump(nb, open(path, "w"), indent=1, ensure_ascii=False)
nbformat.validate(json.load(open(path)))
print("OK: válido, minor 5, gráficas conservadas")
