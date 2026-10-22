import hashlib, json, os, sys, datetime
paths = sys.argv[2:]
out = {}
for p in paths:
    try:
        b = open(p, "rb").read()
        st = os.stat(p)
        out[p] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
                  "mtime": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")}
    except Exception as e:
        out[p] = {"error": repr(e)}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for p, v in out.items():
    print(v.get("sha256", "ERR")[:16], v.get("bytes"), p)
