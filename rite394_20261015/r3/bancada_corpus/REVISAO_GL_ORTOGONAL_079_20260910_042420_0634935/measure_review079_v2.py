"""Read-only source checks; exclusive writes only to this new review folder."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE_DIR = ROOT / "COMPLETAMENTO_GL_ORTOGONAL_079_20260910"
MANIFEST = SOURCE_DIR / "MANIFESTO_COMPARACAO_CONEXOES_079.json"
PROVENANCE = SOURCE_DIR / "PROVENIENCIA_WRITER_LIMPO_079.json"
NOTE = SOURCE_DIR / "CORRENTE_QUADRATICA_E_EQUIVALENCIA_DAS_CONEXOES.md"

def pin(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def emit(path, obj):
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    temporary = path.with_suffix(path.suffix + ".pending")
    if path.exists() or temporary.exists():
        raise FileExistsError(path)
    with temporary.open("xb") as output:
        output.write(data)
    if temporary.read_bytes() != data:
        raise RuntimeError("Byte mismatch")
    temporary.rename(path)

manifest = json.loads(MANIFEST.read_bytes())
provenance = json.loads(PROVENANCE.read_bytes())
files = [NOTE, MANIFEST, PROVENANCE,
         SOURCE_DIR / "write_connection_comparison_new.py",
         SOURCE_DIR / "write_connection_comparison_clean_new.py",
         SOURCE_DIR / "prepare_clean_connection_writer_new.py"]
files += [Path(item["path"]) for item in manifest["source_pins_before"]]
if sys.argv[1] == "begin":
    emit(HERE / "PINS_INICIAIS_REVISAO_079.json", [pin(p) for p in files])
    print("Measured", len(files), "sources")
elif sys.argv[1] == "close":
    initial = json.loads((HERE / "PINS_INICIAIS_REVISAO_079.json").read_bytes())
    final = [pin(p) for p in files]
    checks = []
    def check(name, value, detail=None):
        checks.append({"name": name, "pass": bool(value), "detail": detail})
        if not value:
            raise RuntimeError(name)
    check("twelve_sources_unchanged", initial == final)
    for position, expected in enumerate(manifest["source_pins_before"]):
        check("source_pin_" + str(position), pin(Path(expected["path"])) == expected)
    check("source_before_after_record", manifest["source_pins_before"] == manifest["source_pins_after"])
    for key in ["note", "creator"]:
        check("manifest_" + key, pin(Path(manifest[key]["path"])) == manifest[key])
    for key in ["source_before", "source_after", "target", "creator"]:
        check("provenance_" + key, pin(Path(provenance[key]["path"])) == provenance[key])
    old = Path(provenance["source_before"]["path"]).read_bytes()
    clean = Path(provenance["target"]["path"]).read_bytes()
    check("one_historical_null_byte", old.count(b"\0") == 1)
    check("clean_copy_exactly_removes_one_null", clean == old.replace(b"\0", b"") and b"\0" not in clean)
    try:
        ast.parse(old)
    except SyntaxError as error:
        parse_error = str(error)
    else:
        parse_error = ""
    check("historical_source_ast_failure", "null bytes" in parse_error, parse_error)
    tree = ast.parse(clean)
    check("clean_source_ast_valid", isinstance(tree, ast.Module))
    literal = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "NOTE" for t in node.targets):
            value = node.value
            if not (isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute)
                    and value.func.attr == 'replace' and not value.keywords and len(value.args) == 2):
                raise RuntimeError('Unexpected NOTE expression')
            source_literal = ast.literal_eval(value.func.value)
            arguments = [ast.literal_eval(item) for item in value.args]
            if not isinstance(source_literal, str) or arguments != [chr(0), '']:
                raise RuntimeError('Unexpected NOTE normalization')
            literal = source_literal.replace(chr(0), '')
    check("note_exactly_matches_literal", isinstance(literal, str) and literal.encode("utf-8") == NOTE.read_bytes())
    note_links = re.findall(r"\]\(<(C:/[^>]+)>\)", NOTE.read_text(encoding="utf-8"))
    for index, target in enumerate(note_links):
        check("source_note_link_" + str(index), Path(re.sub(r":\d+$", "", target)).is_file())
    pending = HERE / "PARECER_GL_ORTOGONAL_079.md.pending_v2"
    report = HERE / "PARECER_GL_ORTOGONAL_079.md"
    if report.exists():
        raise FileExistsError(report)
    report_bytes = pending.read_bytes()
    check("review_size", len(report_bytes) > 8000)
    for index, target in enumerate(re.findall(r"\]\(<(C:/[^>]+)>\)", report_bytes.decode("utf-8"))):
        check("review_link_" + str(index), Path(re.sub(r":\d+$", "", target)).is_file())
    pending.rename(report)
    receipt = {
        "status": "REAL documentary checks, DERIVED independent written mathematical review",
        "sources_before": initial,
        "sources_after": final,
        "checks": checks,
        "check_count": len(checks),
        "all_checks_pass": all(item["pass"] for item in checks),
        "report": pin(report),
        "measurement_script": pin(Path(__file__)),
        "execution_scope": "Only this standard-library metadata/AST script; source writers never executed/imported; no CAS/Lean/um.py",
        "historical_execution_claim": "Not independently reconstructible from file bytes; preserved as declared in provenance. Invalid AST and clean-copy byte relation were directly checked.",
        "primary_reference_read": {"title": "Chern and Simons, Characteristic Forms and Geometric Invariants (1974), section 3, proposition 3.2", "url": "https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf"},
    }
    emit(HERE / "RECIBO_REVISAO_GL_ORTOGONAL_079.json", receipt)
    print(json.dumps({"report": pin(report), "receipt": pin(HERE / "RECIBO_REVISAO_GL_ORTOGONAL_079.json"), "checks": len(checks), "sources": len(final)}, ensure_ascii=False))
else:
    raise RuntimeError("Unknown operation")
