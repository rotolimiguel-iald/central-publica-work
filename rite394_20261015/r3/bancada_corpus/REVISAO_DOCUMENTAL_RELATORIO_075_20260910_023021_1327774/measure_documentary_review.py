from pathlib import Path
import datetime, hashlib, json, re, sys
ROOT = Path(__file__).resolve().parent
WORK = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
assert ROOT.is_relative_to(WORK)
def measure(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
def atomic_new(name, obj):
    dest = ROOT / name
    temp = ROOT / (name + ".pending")
    assert dest.parent == ROOT and not dest.exists() and not temp.exists()
    b = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with temp.open("xb") as f: f.write(b)
    assert temp.read_bytes() == b and len(b) > 0
    temp.rename(dest)
    assert dest.read_bytes() == b
    return measure(dest)
snap = json.loads((ROOT / "PINS_INICIAIS.json").read_text(encoding="utf-8"))
pins = []
for old in snap["pins"]:
    now = measure(old["path"])
    now["unchanged"] = all(now[k] == old[k] for k in ("path", "bytes", "sha256"))
    pins.append(now)
assert all(x["unchanged"] for x in pins), "SOURCE_CHANGED"
if sys.argv[1] == "check":
    links, externals = [], []
    rx = re.compile(r"\[[^\]\n]*\]\((?:<([^>\n]+)>|([^)\n]+))\)")
    for item in pins:
        p = Path(item["path"])
        if p.suffix.lower() != ".md": continue
        content = p.read_text(encoding="utf-8")
        for m in rx.finditer(content):
            raw = (m.group(1) or m.group(2)).strip()
            if re.match(r"^https?://", raw):
                externals.append({"source": p.as_posix(), "url": raw})
                continue
            if raw.startswith("#"): continue
            without_fragment = raw.split("#", 1)[0]
            line = None
            lm = re.search(r":([1-9][0-9]*)(?::[1-9][0-9]*)?$", without_fragment)
            if lm:
                line = int(lm.group(1))
                without_fragment = without_fragment[:lm.start()]
            target = Path(without_fragment)
            if not target.is_absolute(): target = p.parent / target
            exists = target.is_file()
            line_ok = None
            if line is not None and exists:
                line_ok = line <= len(target.read_bytes().decode("utf-8").splitlines())
            links.append({"source": p.as_posix(), "source_line": content.count("\n", 0, m.start()) + 1,
                          "link": raw, "target": target.as_posix(), "exists": exists,
                          "target_line": line, "target_line_valid": line_ok,
                          "ok": exists and line_ok is not False})
    cap75p = next(Path(x["path"]) for x in pins if x["path"].endswith("ESTADO_CANONICO_075.json"))
    cap74p = next(Path(x["path"]) for x in pins if x["path"].endswith("ESTADO_CANONICO_074.json"))
    cap75, cap74 = [json.loads(p.read_text(encoding="utf-8")) for p in (cap75p, cap74p)]
    oldmap = {x["path"]: x for x in cap74["pins"]}
    canonical = []
    for row in cap75["comparison_with_delivery074"]:
        p = row["path"]
        expected = next(x for x in cap75["pins"] if x["path"] == p)
        actual = measure(p)
        actual["matches_capture075"] = all(actual[k] == expected[k] for k in ("bytes", "sha256"))
        actual["capture075_matches074"] = all(expected[k] == oldmap[p][k] for k in ("bytes", "sha256"))
        canonical.append(actual)
    result = {
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "DOCUMENTARY_ONLY; no um execution/import, no AST repeat, no Lean/CAS",
        "sources_after": pins, "links": links, "external_links": externals,
        "summary": {"sources": len(pins), "unchanged_sources": sum(x["unchanged"] for x in pins),
                    "local_links": len(links), "local_links_ok": sum(x["ok"] for x in links),
                    "links_with_line": sum(x["target_line"] is not None for x in links)},
        "canonical_read_only_measurements": canonical,
        "capture_counts_checked_in_json": {
            "modules": len(cap75["modules"]), "present": sum(x["present"] for x in cap75["modules"]),
            "absent": sum(not x["present"] for x in cap75["modules"]),
            "embedded_files": cap75["embedded_files"]},
        "all_ok": all(x["ok"] for x in links) and all(x["matches_capture075"] and x["capture075_matches074"] for x in canonical)
    }
    pin = atomic_new("VERIFICACAO_DOCUMENTAL.json", result)
    print(json.dumps({"summary": result["summary"], "canonical_pins_match": all(x["matches_capture075"] and x["capture075_matches074"] for x in canonical), "all_ok": result["all_ok"], "output": pin}, ensure_ascii=False))
elif sys.argv[1] == "final":
    verify = json.loads((ROOT / "VERIFICACAO_DOCUMENTAL.json").read_text(encoding="utf-8"))
    manifest = {"created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "author": "/root/finish_gibbs_realization",
        "status": "REVIEW_NO_MATERIAL_DOCUMENTARY_DISCREPANCY_IN_DECLARED_SCOPE",
        "source_pins_final": pins,
        "artifacts": [measure(ROOT / n) for n in ("PARECER_RELATORIO_075.md", "PINS_INICIAIS.json", "VERIFICACAO_DOCUMENTAL.json", "measure_documentary_review.py")],
        "summary": verify["summary"], "all_documentary_checks_ok": verify["all_ok"],
        "primary_checked": [{"url": "https://arxiv.org/pdf/1803.10235v3", "scope": "Theorem 7, equations 154-157; off-shell versus background distinction; not a new proof of causal existence."}],
        "limitations": ["No new analytic proof", "No Lean/CAS/diagrams", "No um.py execution/import", "No source edited", "No result from delivery076", "No total primitive, QME, interacting charge or UV closure"],
        "originals_written": False, "existing_files_changed": False}
    print(json.dumps(atomic_new("MANIFESTO_REVISAO_DOCUMENTAL_075.json", manifest), ensure_ascii=False))
else:
    raise ValueError("Use check or final")

