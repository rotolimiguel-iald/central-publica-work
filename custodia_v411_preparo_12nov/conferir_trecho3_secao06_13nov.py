# -*- coding: utf-8 -*-
"""Conferência mecânica da divisão do trecho 3 da seção 06 (13/11/2026, claude-site-custodia; condições da gerência c1). Só leitura.
Uso: python -X utf8 conferir_trecho3_secao06_13nov.py <secoes_fatias.json.bak_*_trecho3 (o de antes)>"""
import json, re, sys
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import h0dn, motor, textos  # noqa: E402

CFG = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools\secoes_fatias.json")
ANT = Path(sys.argv[1])
ESP = Path(r"C:\IALD\Artigo\the_boundary")
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, detalhe=""):
    if cond:
        RES["ok"] += 1
        print("  ok  ", nome)
    else:
        RES["falhas"].append(nome)
        print("  FALHA", nome, detalhe)


def trecho(t):
    b = (ESP / t["arquivo"]).read_bytes()
    ini, fim = t["inicio"].encode("utf-8"), t["fim"].encode("utf-8")
    assert b.count(ini) == 1, "início achado %d vezes" % b.count(ini)
    s0 = b.find(ini); e0 = b.find(fim, s0 + len(ini))
    assert e0 >= 0
    return b[s0:e0 + len(fim)]


novo, ant = json.loads(CFG.read_text(encoding="utf-8")), json.loads(ANT.read_text(encoding="utf-8"))
fn = [x for x in novo if x["slug"].startswith("06-")][0]
fa = [x for x in ant if x["slug"].startswith("06-")][0]
caso("as outras sete fatias iguais", [x for x in novo if not x["slug"].startswith("06-")] == [x for x in ant if not x["slug"].startswith("06-")])
caso("os trechos 1, 2 e o último da 06 iguais", fn["trechos"][:2] == fa["trechos"][:2] and fn["trechos"][4:] == fa["trechos"][3:] and len(fn["trechos"]) == 5)
caso("sínteses, títulos e problemas da 06 iguais", all(fn[k] == fa[k] for k in ("titulo_en", "titulo_pt", "sintese_en", "sintese_pt", "problemas")))
t3 = trecho(fa["trechos"][2])
ta, tb = trecho(fn["trechos"][2]), trecho(fn["trechos"][3])
caso("3a + 3b = o trecho 3 de antes, byte a byte (%d = %d + %d)" % (len(t3), len(ta), len(tb)), ta + tb == t3)
caso("cada trecho <= 4000 B", len(ta) <= 4000 and len(tb) <= 4000, (len(ta), len(tb)))
caso("bytes_medidos conferem", fn["trechos"][2]["bytes_medidos"] == len(ta) and fn["trechos"][3]["bytes_medidos"] == len(tb))
pars = t3.split(b"\r\n\r\n")
p2 = pars[1]
caso("o parágrafo do P2 (o resultado com as obrigações) está INTEIRO no 3a e nada dele no 3b", p2 in ta and p2[:80] not in tb and p2[-80:] not in tb)
caso("o parágrafo do P2 traz o resultado", bool(re.search(rb"6\.11|6,11", p2)))
ctx = motor.Ctx(versao="v411", sessao="site", ensaio=True, trabalho=str(CEN / "work" / "custodia_v411_13nov"))
conh = textos.conhecidos_da_rodada(ctx)
for rot, t in (("3a", ta), ("3b", tb)):
    s = t.decode("utf-8")
    caso("F67 do trecho %s" % rot, h0dn.f67(s) == [], h0dn.f67(s))
    v = textos.portao(s, conh, rotulo="trecho " + rot)
    caso("portão do trecho %s" % rot, v == [], v[:3])
caso("a fatia está com aprovado = false (pendente do verificador)", fn.get("aprovado") is False)
print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)
