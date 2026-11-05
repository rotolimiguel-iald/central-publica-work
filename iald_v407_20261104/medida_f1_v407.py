# -*- coding: utf-8 -*-
"""Evidencia do construtor (so leitura; grava um arquivo, uma vez): o efeito da correcao F1 sobre o bloco projecao_transversal_v404 do haiku55 e o tamanho do conjunto de dicts de estatuto planos na fonte da v407."""
import hashlib
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
INST = Path(r"C:\IALD\projetos_pyhton\IALD\.iald_runtime\haiku55\prefix.md")          # v406 instalada
NOVO = W / "app" / "packages" / "haiku_expanded" / "prefix.md"                          # v407 construida
FONTE = Path(r"C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407\um_absoluto.json")
STATUS_KEY = re.compile(r"status|estatuto|verdict|veredito", re.I)
WHOLE_FIELD = re.compile(r"hypothes|hip[oó]tes|assumption|premiss|statement|enunciad|formula|equation|equacao|equaç", re.I)


def bloco(t, nome):
    m = re.search(r"(?m)^### " + re.escape(nome) + r"\n", t)
    n = re.search(r"(?m)^### ", t[m.end():])
    return t[m.end(): m.end() + (n.start() if n else len(t) - m.end())]


def dump(v):
    return json.dumps(v, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


out = {"alvo": "projecao_transversal_v404/name_status", "pacotes": {}}
for nome, p in (("v406_instalada_haiku55", INST), ("v407_construida_haiku_expanded", NOVO)):
    t = p.read_text(encoding="utf-8")
    b = bloco(t, "projecao_transversal_v404")
    i = b.find('"name_status"')
    out["pacotes"][nome] = {
        "arquivo": str(p), "sha256_do_prefixo": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes_do_bloco": len(b),
        "trecho_name_status": b[i:i + 330] if i >= 0 else None,
        "tem_PROVISORIO": "PROVISORIO" in b, "tem_aceito_pelo_operador": "aceito_pelo_operador" in b, "tem_ele_dar_outro": "ele dar outro" in b,
    }
core = json.loads(FONTE.read_bytes())["core"]
rows = []


def walk(v, ptr):
    if isinstance(v, dict):
        for k, it in v.items():
            loc = ptr + "/" + str(k).replace("~", "~0").replace("/", "~1")
            if isinstance(it, dict) and it and STATUS_KEY.search(k) and WHOLE_FIELD.search(k) is None and all(not isinstance(x, (dict, list)) for x in it.values()):
                rows.append((loc, len(dump(it))))
            walk(it, loc)
    elif isinstance(v, list):
        for i, it in enumerate(v):
            walk(it, ptr + "/" + str(i))


for n, node in core.items():
    walk(node, "/core/" + n)
sel = [(p, s) for p, s in rows if s <= 500]
out["fonte_v407"] = {"dicts_planos_de_estatuto": len(rows), "bytes_somados": sum(s for _, s in rows), "protegidos_pela_regra_F1_ate_500B": len(sel), "bytes_protegidos": sum(s for _, s in sel),
                     "maior_dict_protegido": max((s for _, s in sel), default=0), "exemplos_nao_protegidos_maiores_que_500B": [p for p, s in sorted(rows, key=lambda x: -x[1]) if s > 500][:5]}
raw = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
with (W / "MEDIDA_F1_v407.json").open("xb") as f:
    f.write(raw)
print(raw.decode("utf-8")[:1800])
