# -*- coding: utf-8 -*-
"""Recopia para o preparo do NÚCLEO arquivos rastreados que mudaram depois que o construtor passou por eles (22/10/2026: as erratas
ao lado do titular em memory/TGL_CORE_MEMORY.md e memory/TGL_ATLAS.md), pela MESMA esteira do construir_nucleo_publico.py — guarda
pública (credencial, carga embutida), máscara visível de dado pessoal, filtro das notas operacionais nos .md — e atualiza a linha de cada
um no INDICE_PUBLICO.json (bytes e sha256). Só arquivos de texto já presentes no índice; recusa o resto.
Uso: recopiar_no_preparo.py <pasta_do_preparo> <caminho_rastreado> [...]"""
import hashlib, json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mascara_pii import mascarar  # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402
import guarda_publica as GP  # noqa: E402

SRC = Path(r"C:\IALD\Central de Patentes")
D = Path(sys.argv[1])
IP = D / "INDICE_PUBLICO.json"
idx = json.loads(IP.read_text(encoding="utf-8"))
pos = {a["caminho"]: i for i, a in enumerate(idx["arquivos"])}
for t in sys.argv[2:]:
    assert t in pos, ("não está no índice do preparo — PARAR", t)
    assert t.endswith((".md", ".txt", ".json", ".py")), t
    txt = (SRC / t).read_bytes().decode("utf-8", "replace")
    n_cred, pii = GP.avaliar_texto(txt)
    assert not n_cred and not pii, ("a guarda recusa", t, n_cred, pii)
    txt, c = mascarar(txt)
    if t.endswith(".md"):
        txt, n = filtrar_markdown(txt)
        c["notas_operacionais_omitidas"] = n
    b = txt.encode("utf-8")
    dst = D / t
    tmp = dst.with_name(dst.name + ".tmp_recopia")
    tmp.write_bytes(b)
    os.replace(tmp, dst)
    antes = dict(idx["arquivos"][pos[t]])
    idx["arquivos"][pos[t]] = {"caminho": t, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    print("recopiado:", t, antes["bytes"], "->", len(b), "| máscaras", c)
tmp = IP.with_name(IP.name + ".tmp_recopia")
tmp.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
os.replace(tmp, IP)
print("índice atualizado:", idx["n_arquivos"], "arquivos")
