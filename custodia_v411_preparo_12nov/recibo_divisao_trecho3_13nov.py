# -*- coding: utf-8 -*-
"""Grava o RECIBO da divisão do trecho 3 da seção 06 do site (13/11/2026, claude-site-custodia), com a exceção D196 ESCRITA.
Todo hash lido do disco. Arquivo novo; recusa sobrescrever. Uso: python -X utf8 <este> <secoes_fatias.json.bak_*_trecho3>"""
import hashlib, json, os, sys, time
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import textos  # noqa: E402

CFG = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools\secoes_fatias.json")
ANT = Path(sys.argv[1])
EST = Path(r"C:\IALD\Artigo\the_boundary\ESTADO_ATUAL.md")
V410 = Path(r"C:\tmp\estado_v410.md")   # git show HEAD:ESTADO_ATUAL.md do espelho (a v410 publicada), extraído em 13/11
OUT = CEN / "work" / "custodia_v411_preparo_12nov" / "RECIBO_DIVISAO_TRECHO3_SECAO06_13nov.json"
assert not OUT.exists(), "já existe: %s" % OUT


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def trecho(b, t):
    ini, fim = t["inicio"].encode("utf-8"), t["fim"].encode("utf-8")
    s0 = b.find(ini); e0 = b.find(fim, s0 + len(ini))
    return b[s0:e0 + len(fim)]


f = [x for x in json.loads(CFG.read_text(encoding="utf-8")) if x["slug"].startswith("06-")][0]
fa = [x for x in json.loads(ANT.read_text(encoding="utf-8")) if x["slug"].startswith("06-")][0]
b = EST.read_bytes()
ta, tb, t3 = trecho(b, f["trechos"][2]), trecho(b, f["trechos"][3]), trecho(b, fa["trechos"][2])
t3_v410 = trecho(V410.read_bytes(), fa["trechos"][2])
port_b = textos.portao(tb.decode("utf-8"), set(), rotulo="3b")
port_v410 = textos.portao(t3_v410.decode("utf-8"), set(), rotulo="trecho3_v410")
n_never = tb.decode("utf-8").count("never CONFIRMED")
assert port_b == ["3b: «CONFIRMED» fora da fórmula da régua"] and port_v410 == ["trecho3_v410: «CONFIRMED» fora da fórmula da régua"] and n_never == 2
r = {
    "schema": "iald.site.divisao_trecho/v1",
    "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "por": "claude-site-custodia (sessão de custódia), por decisão da gerência c1 (opção (a), 13/11/2026)",
    "fatia": f["slug"],
    "config": {"arquivo": str(CFG), "sha256_depois": sha(CFG), "backup_antes": str(ANT), "sha256_antes": sha(ANT)},
    "fonte": {"arquivo": str(EST), "sha256": sha(EST)},
    "trecho3_antes": {"bytes": len(t3), "sha256": hashlib.sha256(t3).hexdigest(), "acima_do_teto": len(t3) > 4000},
    "trecho3a": {"bytes": len(ta), "sha256": hashlib.sha256(ta).hexdigest()},
    "trecho3b": {"bytes": len(tb), "sha256": hashlib.sha256(tb).hexdigest()},
    "concatenados_iguais_ao_trecho3": ta + tb == t3,
    "teto_trecho": 4000,
    "excecao_D196": {
        "o_que": "o trecho 3b reprova no portão de textos da G1 SÓ pela regra do «CONFIRMED» fora da fórmula da régua, nas duas ocorrências de "
                 "«never CONFIRMED» (texto verbatim do ESTADO_ATUAL: «— never CONFIRMED.» depois de «NOT_FALSIFIED … more sensitive data can revise», e "
                 "«the declaration of closure is the operator’s act, never CONFIRMED.»), que negam a palavra, como a régua manda",
        "portao_3b": port_b,
        "ocorrencias_never_CONFIRMED_no_3b": n_never,
        "o_trecho3_da_v410_publicada_reprova_igual": port_v410,
        "v410_publicada": {"arquivo": "git show HEAD:ESTADO_ATUAL.md do espelho (extraído para %s)" % V410, "sha256": sha(V410)},
        "aceita_pela_gerencia": "D196 (gerência c1, 13/11/2026): falso positivo da lista de fórmulas, não defeito do trecho; o portão de textos da G1 "
                                "nunca foi regra dos trechos do site (o site tem a lista própria PROIBIDOS_TRECHO). Valem para o 3b: a concatenação "
                                "byte a byte, o teto, a F67, a lista do site e a decisão do verificador distinto.",
        "errata_depois_do_auditar": "a forma negada entra na lista FORMULAS do portão (textos.py), com controle negativo dos dois lados",
    },
}
OUT.write_bytes((json.dumps(r, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
print("ok:", OUT, OUT.stat().st_size, "B sha16", sha(OUT)[:16])
