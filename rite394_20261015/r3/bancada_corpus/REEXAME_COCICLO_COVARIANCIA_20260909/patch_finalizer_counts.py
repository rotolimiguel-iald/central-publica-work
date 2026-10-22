"""Update our own unexecuted reporter atomically, after an immediate byte backup."""
from pathlib import Path
from datetime import datetime
import os

folder = Path(__file__).resolve().parent
path = folder / "finalize_reexamination.py"
assert folder.parent == Path(r"C:\IALD\Central de Patentes\Chatgpt")
before = path.read_bytes()
backup = path.with_name(path.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as stream:
    stream.write(before)
    stream.flush()
    os.fsync(stream.fileno())
assert backup.read_bytes() == before
text = before.decode("utf-8")
changes = [
    ("import hashlib\n", "import ast\nimport hashlib\n"),
    ('== set(integration["theorem_names"])', '== set(integration["all_declaration_names"])'),
    ('    quantum = BASE / "DUHAMEL_UNITARIO_20260909_153247_640286"',
     '''    def embedded_counts(path):
        tree = ast.parse(path.read_bytes().decode("utf-8"))
        tables = [node.value for node in tree.body if isinstance(node, ast.Assign) and
                  any(isinstance(target, ast.Name) and target.id == "_EMBEDDED_KERNEL_FILES"
                      for target in node.targets)]
        assert len(tables) == 1
        embedded = ast.literal_eval(tables[0])
        return len(embedded), sum(key.endswith(".lean") for key in embedded)
    old_files, old_lean = embedded_counts(copy_folder / "um_ORIGINAL_SNAPSHOT.py")
    new_files, new_lean = embedded_counts(copy_folder / "um.py")
    assert old_files == integration["old_embedded_file_count"]
    assert new_files == integration["new_total_embedded_file_count"]
    assert new_lean - old_lean == total["modules"]

    quantum = BASE / "DUHAMEL_UNITARIO_20260909_153247_640286"'''),
    ("as fontes Lean passaram de 602 para {602 + total['modules']}",
     "as fontes Lean passaram de {old_lean} para {new_lean}"),
]
for old, new in changes:
    assert text.count(old) == 1, old
    text = text.replace(old, new)
after = text.encode("utf-8")
assert len(after) > len(before)
compile(text, str(path), "exec")
temp = path.with_name(path.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
with temp.open("xb") as stream:
    stream.write(after)
    stream.flush()
    os.fsync(stream.fileno())
assert temp.read_bytes() == after
assert path.read_bytes() == before
os.replace(temp, path)
assert path.read_bytes() == after
print("Reporter updated with byte backup; no report generated and no um.py loaded.")
