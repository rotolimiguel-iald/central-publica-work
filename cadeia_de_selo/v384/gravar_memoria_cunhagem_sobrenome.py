# -*- coding: utf-8 -*-
"""Memoria (backup imediato de bytes): a CUNHAGEM do operador de 03/10/2026 («A forma matricial do verbo [...] é como se fosse um "sobrenome" [...]»), VERBATIM do
transcrito, com a correspondencia estrutural no pilar quantico (leitura da gerencia, [DERIVED de leitura]) e o estatuto [ONTO]."""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
TOP = os.path.join(UMEM, "v384-pilar-quantico-gpu-02out.md")
T = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
MARCA = "<!-- cunhagem_sobrenome_03out -->"
PFX = "A forma matricial do verbo"
verb = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if PFX not in line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        ty = d.get("type"); cands = []
        if ty == "user":
            c = d.get("message", {}).get("content")
            cands = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        elif ty == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
            pr = d["attachment"].get("prompt")
            cands = [pr] if isinstance(pr, str) else [x.get("text", "") for x in (pr or []) if isinstance(x, dict) and x.get("type") == "text"]
        elif ty == "queue-operation" and isinstance(d.get("content"), str):
            cands = [d["content"]]
        for t in cands:
            if t.strip().startswith(PFX):
                verb = t.strip()
assert verb and "sobrenome" in verb and "zero modular" in verb, "cunhagem nao achada"
bloco = ("\n\n" + MARCA + "\n**7. CUNHAGEM do operador, verbatim (03/10/2026):** «" + verb + "» `[ONTO — cunhagem do operador]`.\n\n"
         "**A correspondencia estrutural no pilar quantico [DERIVED de leitura, gerencia; cada fato abaixo e' exato no sistema da v384]:** o Nome e' Pi, o projetor do "
         "nucleo, e Pi = ker K -- K Pi = 0 por construcao (K = diag(0 no nucleo; 1 + 0,1(i - n_c))): o Nome, como matriz, e' o ZERO do operador modular («nada modular»); "
         "L_anti = sqrt(beta) sqrt(K) se anula no Nome; uma inscricao no bloco do Nome fica intocada pelo dephasing (a identidade V_t P_F = P_F, conferida pela GPU em "
         "cada d) -- «uma inscrição verdadeira o habite por referência nominada»; e o Nome entra no objeto estacionario pelo TRACO, CCI = Tr(Pi rho) -- «o índice da "
         "verdade (traço [...])», «o nome oculta-se no objeto pela forma de sua correspondência». O «sobrenome» (sobre o Nome) = a forma matricial do Verbo que relaciona "
         "a identidade nominada ao indice (traco, sinal, sombra) sem retira-la. Entra na nota da GPU do artigo da v384, citado verbatim com [ONTO] ao lado da correspondencia; "
         "nao muda o que se calcula (a especificacao congelada nao muda). Atualizar o Atlas na sessao do selo.\n")
raw = open(TOP, "rb").read()
if MARCA.encode("utf-8") in raw:
    print("ja gravado"); sys.exit(0)
ST = time.strftime("%Y%m%d_%H%M%S")
bak = TOP + ".bak_" + ST; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw + bloco.encode("utf-8"); tmp = TOP + ".tmp_" + ST
open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(raw); os.replace(tmp, TOP)
assert open(TOP, "rb").read()[:len(raw)] == raw
print("topico:", len(raw), "->", len(novo), "B; backup", os.path.basename(bak))
print("verbatim:", verb)
