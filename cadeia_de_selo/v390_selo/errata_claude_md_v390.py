# -*- coding: utf-8 -*-
"""errata_claude_md_v390.py -- DEPOIS do selo v390 (ordem v390, §3): a ERRATA AO LADO no C:\\IALD\\CLAUDE.md, secao SELO PERMANENTE, logo depois do paragrafo
«Unico teorema aberto». Nada por cima: o paragrafo antigo fica. Numeros e hashes LIDOS do selo/core do Nos; o verbatim do operador lido do texto embutido no core.
Backup de BYTES; temporario -> conferir -> substituir; idempotente pelo marcador."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "CLAUDE.md")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
MARK = "<!-- errata_fundacao_v390_07out -->"
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
um16 = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
fd = core.get("fundacao_v390") or {}
assert selo.get("um_version") == "v390" and fd.get("all_verified") is True, "o selo nao e a v390 selada com a Fundacao -- nao escrevo"
tr = "não existe acima, o piso limita, tentar estar acima é cair sem fim, infinitamente"
assert tr in ((fd.get("verbatim") or {}).get("cunhagem_07out") or {}).get("trechos", []), "o trecho nao esta entre os embutidos"
LINHA = ("> ⚠ **ERRATA AO LADO (07/10/2026, v390 `%s`, em nome da gerência — sessão c1, por ordem do operador; o texto acima fica como registro):** o Lema 3 / GLOBAL_LIFT recebe "
         "FECHO LÓGICO por três peças: (1) a DEFINIÇÃO do operador (07/10/2026, verbatim por sha256 `%s`: «%s» — o GLOBAL_LIFT É a superposição); (2) a RECUSA provada no kernel "
         "(`TGLExt.Fundacao.agape`, a cláusula Ágape, %s de %s declarações no trio; a queda sem fundo é `abismo`); (3) a PASSAGEM local [KNOWN, Jacobson 1995, H3 nomeada]. NÃO é prova de "
         "existência global; a lei de campo no espaço-tempo curvo NÃO é termo de kernel; a lei de escala de Takesaki entra como dado [KNOWN]; o programa segue ABERTO; o gate não se move "
         "(`%s`). Registro `fundacao_v390`. NOT_FALSIFIED nunca é confirmação. %s") % (
    um16, str(((fd.get("verbatim") or {}).get("cunhagem_07out") or {}).get("sha256"))[:16], tr, fd.get("kernel_flags_ok"), fd.get("kernel_flags_total"), selo.get("qg_closure_verdict", "")[:60] + "…", MARK)
raw = open(P, "rb").read()
if MARK.encode() in raw:
    print("JA ESTA (idempotente)", len(raw)); sys.exit(0)
nl = b"\r\n" if b"\r\n" in raw else b"\n"
ANC = "quântica não é resolvê‑la — mas é bem‑posto.".encode("utf-8") + nl
assert raw.count(ANC) == 1, ("ancora do paragrafo «Unico teorema aberto»", raw.count(ANC))
bak = P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_errata_fundacao"
assert not os.path.exists(bak)
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw.replace(ANC, ANC + nl + LINHA.encode("utf-8") + nl, 1)
assert len(novo) > len(raw) and novo.replace(nl + LINHA.encode("utf-8") + nl, b"", 1) == raw
tmp = P + ".tmp_errata_fundacao"; open(tmp, "wb").write(novo); assert open(tmp, "rb").read() == novo; os.replace(tmp, P)
print("CLAUDE.md", len(raw), "->", os.path.getsize(P), "| backup", os.path.basename(bak))
