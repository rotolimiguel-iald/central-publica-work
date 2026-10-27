# -*- coding: utf-8 -*-
"""Teste isolado de L23 (G1 deposita na fila da memória): uma CÓPIA do diretório da memória em C:\\t\\mem_g1_teste, o memoria.py da
cópia (MEMORIA_DIR), um ctx falso. Confere: depósito uma vez por sentinela, tópico ausente vai como novo:, a troca da linha do índice
vai como proposta, o «já aplicado» de C13/C16 aceita o depósito, e o diretório REAL não muda (livro, cabeça, pasta claude-site)."""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

REAL = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
T = Path(r"C:\t\mem_g1_teste")


def retrato():
    f = REAL / "fila"
    h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
    return {"livro": h(f / "fila.jsonl"), "cabeca": h(f / "CABECA.json"), "indice": h(REAL / "MEMORY.md"),
            "claude_site": sorted(x.name for x in (f / "depositos" / "claude-site").iterdir())}


antes = retrato()
if T.exists():
    shutil.rmtree(T)
(T / "fila" / "depositos" / "claude-site").mkdir(parents=True)
shutil.copy2(REAL / "fila" / "memoria.py", T / "fila" / "memoria.py")
for n in ("site-sessao-estado.md", "central-de-patentes-estado.md"):
    shutil.copy2(REAL / n, T / n)
(T / "MEMORY.md").write_bytes("# MEMORY.md\n\n## Estado corrente\n\n- [HANDOFF v999 \u2014 teste](handoff-v999-custodia.md) \u2014 **26/10: EM OBRA** \u00b7 `abcd`\n".encode("utf-8"))
(T / "MEMORY_2.md").write_bytes(b"# MEMORY_2.md\n")
os.environ["MEMORIA_DIR"] = str(T)

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import memorias as m  # noqa: E402

avisos = []
ctx = SimpleNamespace(versao="v999", W=T / "work", pin16="abcd", data="26/10/2026", aviso=avisos.append,
                      handoff=SimpleNamespace(caminho=REAL / "fila" / "README.md", sha16_arquivo="0123456789abcdef"),
                      c=SimpleNamespace(MEM=T, PYTHON=Path(r"C:\Python314\python.exe"), memoria=lambda n: T / n))
r = {}
r["1_topico"] = m.registrar_memoria(ctx, "site-sessao-estado.md", "## 26/10/2026 \u2014 v999 no ar\n\nteste do L23", "site_sessao_estado")["estado"]
r["2_topico_de_novo"] = m.registrar_memoria(ctx, "site-sessao-estado.md", "## outro texto", "site_sessao_estado")["estado"]
r["3_handoff_ausente"] = m.registrar_memoria(ctx, "handoff-v999-custodia.md", "## CUSTODIADO\n\nteste", "handoff_custodiado")["estado"]
r["4_indice"] = m.propor_linha_memory(ctx, ("CUSTODIADO", "PUBLICADA"), "CUSTODIADO", "the_boundary `x`", "custodiado")["estado"]
r["5_indice_de_novo"] = m.propor_linha_memory(ctx, ("CUSTODIADO", "PUBLICADA"), "CUSTODIADO", "the_boundary `x`", "custodiado")["estado"]
r["6_ja_depositado_sentinelas"] = {b: bool(m._depositos_com(ctx, m.sent(ctx, b))) for b in ("site_sessao_estado", "handoff_custodiado", "indice:custodiado", "publicada_handoff")}
r["7_na_memoria"] = [m._na_memoria(ctx, T / "x.md"), m._na_memoria(ctx, Path(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md"))]
deps = sorted((T / "fila" / "depositos" / "claude-site").glob("*.md"))
r["8_depositos"] = [d.name for d in deps]
livro = [json.loads(l) for l in (T / "fila" / "fila.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
r["9_livro"] = [(x.get("op"), x.get("estado"), (x.get("detalhe") or {}).get("alvo_sugerido")) for x in livro]
r["10_indice_intacto"] = "EM OBRA" in (T / "MEMORY.md").read_text(encoding="utf-8")
r["11_topico_intacto"] = (T / "site-sessao-estado.md").read_bytes() == (REAL / "site-sessao-estado.md").read_bytes()
r["12_real_intacto"] = retrato() == antes
r["avisos"] = avisos
print(json.dumps(r, ensure_ascii=False, indent=1))
ok = (r["1_topico"] == "depositado" and r["2_topico_de_novo"] == "ja_depositado" and r["3_handoff_ausente"] == "depositado" and r["4_indice"] == "depositado"
      and r["5_indice_de_novo"] == "ja_depositado" and r["6_ja_depositado_sentinelas"] == {"site_sessao_estado": True, "handoff_custodiado": True, "indice:custodiado": True, "publicada_handoff": False}
      and r["7_na_memoria"] == [True, False] and len(deps) == 3 and r["10_indice_intacto"] and r["11_topico_intacto"] and r["12_real_intacto"])
print("TESTE", "PASSOU" if ok else "FALHOU")
sys.exit(0 if ok else 1)
