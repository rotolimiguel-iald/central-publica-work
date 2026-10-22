"""Preserve the failed review helper and draft; create explicit new copies."""
from pathlib import Path
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent

def pin(p):
    b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def emit(p, b):
    t = p.with_name(p.name + ".tmp_new")
    if p.exists() or t.exists():
        raise FileExistsError(p)
    with t.open("xb") as out:
        out.write(b)
    if t.read_bytes() != b:
        raise RuntimeError("Byte mismatch")
    t.rename(p)

old_helper = HERE / "measure_review079.py"
old_note = HERE / "PARECER_GL_ORTOGONAL_079.md.pending"
before = [pin(old_helper), pin(old_note)]
helper = old_helper.read_text(encoding="utf-8")
old = "            literal = ast.literal_eval(node.value)"
new = """            value = node.value
            if not (isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute)
                    and value.func.attr == 'replace' and not value.keywords and len(value.args) == 2):
                raise RuntimeError('Unexpected NOTE expression')
            source_literal = ast.literal_eval(value.func.value)
            arguments = [ast.literal_eval(item) for item in value.args]
            if not isinstance(source_literal, str) or arguments != [chr(0), '']:
                raise RuntimeError('Unexpected NOTE normalization')
            literal = source_literal.replace(chr(0), '')"""
if helper.count(old) != 1:
    raise RuntimeError("Unexpected helper source")
helper = helper.replace(old, new)
helper = helper.replace('pending = HERE / "PARECER_GL_ORTOGONAL_079.md.pending"',
                        'pending = HERE / "PARECER_GL_ORTOGONAL_079.md.pending_v2"')
ast.parse(helper)
emit(HERE / "measure_review079_v2.py", helper.encode("utf-8"))

note = old_note.read_text(encoding="utf-8")
old_text = "A constante NOTE é extraída por ast.literal_eval da atribuição literal do writer limpo. Sua codificação UTF-8 coincide byte a byte com a nota examinada."
new_text = "A expressão NOTE do writer limpo contém um literal de texto seguido da normalização explícita .replace('\\\\x00',''). O helper desta revisão aceita somente essa forma AST, extrai o literal e os dois argumentos por ast.literal_eval, exige os argumentos byte NUL e string vazia e realiza essa única substituição na string local. Não avalia código arbitrário. O resultado codificado em UTF-8 coincide byte a byte com a nota examinada."
if note.count(old_text) != 1:
    raise RuntimeError("Unexpected note wording")
note = note.replace(old_text, new_text)
marker = "As doze fontes sob revisão são medidas novamente ao fechar o recibo."
insert = "Nesta própria revisão, o primeiro helper documental tentou ast.literal_eval diretamente sobre a expressão NOTE completa e parou com ValueError por ela ser uma chamada .replace. A falha ocorreu antes de emitir o parecer final ou o recibo. O helper inicial e o rascunho foram preservados; uma cópia nova estritamente limitada ao padrão AST acima e um novo rascunho corrigem o procedimento. A proveniência dessa correção é registrada separadamente. Não se registra a primeira tentativa como sucesso.\n\n"
if note.count(marker) != 1:
    raise RuntimeError("Unexpected insertion marker")
note = note.replace(marker, insert + marker)
emit(HERE / "PARECER_GL_ORTOGONAL_079.md.pending_v2", note.encode("utf-8"))
after = [pin(old_helper), pin(old_note)]
if before != after:
    raise RuntimeError("Historical files changed")
record = {
    "sources_before": before, "sources_after": after,
    "old_files_preserved": True,
    "failure": "First review helper ast.literal_eval encountered a Call .replace rather than a literal; ValueError before final report/receipt emission.",
    "changes": ["New helper accepts only an AST literal string with replace(NUL, empty) normalization", "New draft states the exact extraction and preserves the review failure"],
    "new_helper": pin(HERE / "measure_review079_v2.py"),
    "new_draft": pin(HERE / "PARECER_GL_ORTOGONAL_079.md.pending_v2"),
    "source_writers_executed_or_imported": False,
}
emit(HERE / "PROVENIENCIA_CORRECAO_HELPER_REVISAO_079.json", json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
print("New review helper/draft prepared; both historical files preserved")
