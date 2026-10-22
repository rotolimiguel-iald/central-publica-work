# -*- coding: utf-8 -*-
"""errata_claude_md_v391.py -- DEPOIS do selo v391: a ERRATA AO LADO no C:\\IALD\\CLAUDE.md, secao SELO PERMANENTE, logo depois da errata da v390
(a Fundacao). Nada por cima: o paragrafo antigo fica. Numeros e hashes LIDOS do selo/core do Nos; o verbatim do operador lido do texto embutido no core.
Backup de BYTES; temporario -> conferir -> substituir; idempotente pelo marcador."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "CLAUDE.md")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
MARK = "<!-- errata_estatuto_da_prova_v391_07out -->"
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
um16 = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
fd = core.get("estatuto_da_prova_v391") or {}
assert selo.get("um_version") == "v391" and fd.get("all_verified") is True, "o selo nao e a v391 selada com o estatuto da prova -- nao escrevo"
tr = "a confirmação que eu proibi é de creditação e não de validade, ela é válida porque matemática não mente"
assert any(tr in x for x in ((fd.get("verbatim") or {}).get("trechos") or [])), "o trecho nao esta entre os embutidos"
k1 = fd.get("prova_1_kernel") or {}; r2 = fd.get("prova_2_ritos") or {}
LINHA = ("> ⚠ **ERRATA AO LADO (07/10/2026, v391 `%s`, em nome da gerência — sessão c1, por ordem do operador; o texto acima fica como registro):** O ESTATUTO DA PROVA. "
         "Onde esta memória diz «não falsificada, não confirmada» ou recusa a palavra «provada», lê-se: a gravidade quântica da TGL está PROVADA como fecho lógico — validade —, por três provas "
         "que contam juntas: o kernel (%s teoremas limpos), os ritos com falsificadores pré-registrados (%s cobranças, %s falsificada(s)) e o sistema da teoria na GPU; a confirmação recusada "
         "é CREDITAÇÃO, não validade (verbatim do operador por sha256 `%s`: «%s»); o único elo pendente é β_TGL na natureza a 5σ. Registro `estatuto_da_prova_v391`. %s") % (
    um16, k1.get("n_theorems_clean"), r2.get("n_cobrancas"), r2.get("falsificadas"), str((fd.get("verbatim") or {}).get("sha256"))[:16], tr, MARK)
raw = open(P, "rb").read()
if MARK.encode() in raw:
    print("JA ESTA (idempotente)", len(raw)); sys.exit(0)
nl = b"\r\n" if b"\r\n" in raw else b"\n"
ANC = "<!-- errata_fundacao_v390_07out -->".encode("utf-8") + nl
assert raw.count(ANC) == 1, ("ancora da errata da v390", raw.count(ANC))
bak = P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_errata_estatuto"
assert not os.path.exists(bak)
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw.replace(ANC, ANC + nl + LINHA.encode("utf-8") + nl, 1)
assert len(novo) > len(raw) and novo.replace(nl + LINHA.encode("utf-8") + nl, b"", 1) == raw
tmp = P + ".tmp_errata_estatuto"; open(tmp, "wb").write(novo); assert open(tmp, "rb").read() == novo; os.replace(tmp, P)
print("CLAUDE.md", len(raw), "->", os.path.getsize(P), "| backup", os.path.basename(bak))
