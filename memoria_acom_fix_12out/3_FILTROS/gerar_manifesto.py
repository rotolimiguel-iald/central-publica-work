"""MANIFESTO.json da frente FILTROS: sha256, bytes e papel de TODO arquivo entregue sob 3_FILTROS
(exceto `tmp\\`, `guard_log\\` e `__pycache__`), mais os hashes dos originais de produção lidos no
início (ORIGINAIS.json) e a conferência de que a suíte testou exatamente os bytes de `copia\\`."""
from __future__ import annotations
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {"tmp", "guard_log", "__pycache__"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def role(rel):
    top = rel.parts[0]
    if top == "copia":
        return "entrega: arquivo modificado (árvore espelha a produção; C/... = C:\\...)"
    if top == "originais":
        return "referência: cópia de bytes do original instalado"
    if top == "suite":
        if rel.name.startswith("test_") and rel.parts[1] in ("sessions", "app", "queue", "blocos") and rel.name in (
                "test_filters.py", "test_guard.py", "test_app_filters.py", "test_filters_queue.py", "test_blocks.py"):
            return "teste novo desta frente"
        if rel.name.startswith("test_"):
            return "teste da origem (rodado sem alteração)"
        return "harness: cópia (código da frente ou apoio inalterado; ver SUITE_MANIFEST.json)"
    if top == "blocos":
        if rel.parts[1] == "copias":
            return "cópia intacta das superfícies D5 (para o ensaio e o teste)"
        if rel.parts[1] == "ensaio":
            return "resultado do ensaio do aplicar_blocos.py em cópia (com backups)"
        return "recibo do ensaio D5"
    if top == "guard_exec":
        return "guarda de execução da auditoria (cópia)"
    return {"MANIFESTO.json": "este manifesto", "DIFF.patch": "diff unificado originais -> copia", "TESTES.md": "resultado de cada teste",
            "SESSION_BRIDGE_v2.md": "texto novo do bloco (D5)", "aplicar_blocos.py": "script D5 (CAS + backup de bytes + substituição só do bloco)",
            "ORIGINAIS.json": "inventário dos originais lidos (sha256 por script)"}.get(rel.name, "script/recibo desta frente")


def main():
    files = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts) or rel.name == "MANIFESTO.json":
            continue
        files.append({"path": str(rel).replace(os.sep, "/"), "bytes": path.stat().st_size, "sha256": sha256(path), "role": role(rel)})
    origem = json.loads((ROOT / "ORIGINAIS.json").read_text(encoding="utf-8"))
    suite = json.loads((ROOT / "SUITE_MANIFEST.json").read_text(encoding="utf-8"))
    frente_ok = all(sha256(Path(i["source"])) == i["sha256"] == sha256(Path(i["target"])) for i in suite["files"] if i["role"] == "frente")
    by_path = {f["path"]: f for f in files}
    entrega = {k: v for k, v in by_path.items() if k.startswith("copia/")}
    manifest = {"frente": "FILTROS (D4 nomes/identidade/conteúdo fail-closed; D5 blocos; D6 escopo Escritório)",
                "at": datetime.now(timezone.utc).isoformat(), "root": str(ROOT),
                "originais_de_producao": origem["originais"], "superficies_d5": origem["superficies"], "ordem_do_operador": origem["ordem"],
                "entrega_copia": entrega, "suite_testou_os_bytes_de_copia": frente_ok, "files": files, "n_files": len(files)}
    (ROOT / "MANIFESTO.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"n_files": len(files), "entrega": len(entrega), "suite_testou_copia": frente_ok}))


if __name__ == "__main__":
    main()
