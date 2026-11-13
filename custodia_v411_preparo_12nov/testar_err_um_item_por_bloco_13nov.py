# -*- coding: utf-8 -*-
"""Teste da errata «um item por bloco» (13/11/2026, claude-site-custodia; decisão da gerência c1, opção (A)) sobre a errata REAL:
textos.construir(ctx) da v411 em modo ensaio (nada é gravado), com a G1 de G1_TESTE_TOOLS (padrão a real).
Confere: nenhuma violação do portão em toda a perna 1; a F67 da errata passa; cada item da errata é o texto do handoff (KERNEL_LEITURA_EN e
ABERTOS_EN byte a byte); os itens estão em blocos separados; o controle negativo (um item que sozinho traz gatilho e ligação sem as
obrigações) REPROVA; e, com ESPERA_FALHA=1, reproduz a parada da G1 anterior (a F67 na errata).
Uso: [G1_TESTE_TOOLS=<pasta que contém custodia_g1>] [ESPERA_FALHA=1] python -X utf8 testar_err_um_item_por_bloco_13nov.py"""
import os, re, sys
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
TOOLS = Path(os.environ.get("G1_TESTE_TOOLS") or (CEN / "tools"))
sys.path.insert(0, str(TOOLS))
from custodia_g1 import h0dn, motor, textos  # noqa: E402

RES = {"ok": 0, "falhas": []}


def caso(nome, cond, detalhe=""):
    if cond:
        RES["ok"] += 1
        print("  ok  ", nome)
    else:
        RES["falhas"].append(nome)
        print("  FALHA", nome, detalhe)


print("G1 testada:", textos.__file__)
ctx = motor.Ctx(versao="v411", sessao="site", ator="claude-site-custodia", ensaio=True, trabalho=str(CEN / "work" / "custodia_v411_13nov"))
H = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v411_CUSTODIA.md").read_text(encoding="utf-8")
M = {m.group(1): m.group(2) for m in re.finditer(r"<!-- INICIO_([A-Za-z0-9_]+?)_v411 -->\n?(.*?)\n?<!-- FIM_\1_v411 -->", H, re.S)}
T = textos.construir(ctx)
err = T.err_en.texto
if os.environ.get("ESPERA_FALHA") == "1":
    caso("a G1 anterior reproduz a parada: F67 na errata", any("F67" in str(x) and "Errata beside" in str(x) for x in T.violacoes), T.violacoes[:2])
    caso("e é a única violação da perna 1", len(T.violacoes) == 1, len(T.violacoes))
else:
    caso("nenhuma violação do portão em toda a perna 1 (TXT, ERR, NOTA, ARCO_EN, ARCO_PT, LEDGER, commit)", T.violacoes == [], T.violacoes[:3])
    caso("a F67 da errata passa", h0dn.f67(err) == [], h0dn.f67(err))
    linhas = err.split("\n")
    itens = [l for l in linhas if re.match(r"> \d+\. ", l)]
    caso("a errata tem os itens numerados (%d)" % len(itens), len(itens) >= 3, itens[:1])
    caso("cada item é um bloco (linha em branco entre itens consecutivos)", all(("\n\n" + it) in err for it in itens[1:]))
    caso("o item «What the kernel proves» é o KERNEL_LEITURA_EN do handoff, byte a byte",
         any(i.endswith("*What the kernel proves and what is reading*: " + M["KERNEL_LEITURA_EN"]) for i in itens))
    caso("o item «What stays open» é o ABERTOS_EN do handoff, byte a byte", any(i.endswith("*What stays open*: " + M["ABERTOS_EN"]) for i in itens))
    caso("unidos por um \\n só, os mesmos itens reprovam (a causa é a colagem)", h0dn.f67(err.replace("\n\n> ", "\n> ")) != [])
    neg = err + "\n\n> 9. *Control*: the primary H0DN Z against the null is 6.11."
    caso("controle negativo: item que sozinho traz gatilho e ligação sem as obrigações -> REPROVA", h0dn.f67(neg) != [], h0dn.f67(neg))
    led = T.bloco_ledger.texto
    caso("o bloco do LEDGER traz a errata inteira", err in led)
    caso("a F67 do bloco do LEDGER passa", h0dn.f67(led) == [], h0dn.f67(led)[:2])
    print("\n--- a errata montada (%d bytes)\n%s\n---" % (len(err.encode("utf-8")), err))
print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)
