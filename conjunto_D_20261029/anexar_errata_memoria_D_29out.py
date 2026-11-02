# -*- coding: utf-8 -*-
"""Errata AO LADO no tópico de memória conjunto-d-autorizado-29out.md (backup de bytes; temporário → conferir prefixo → substituir)."""
import os, time
from pathlib import Path
p = Path("C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/conjunto-d-autorizado-29out.md")
raw = p.read_bytes(); eol = "\r\n" if b"\r\n" in raw else "\n"
tx = eol.join(["", "## ERRATA AO LADO (29/10/2026, mais tarde; gerência c1 em nome próprio) — o número corrigiu a frase",
 "- Onde acima diz «se D se comportar como a calibração A … FALSIFIED_AT_5SIGMA do par (z_excl ≈ 7 com 10 eventos)», leia-se: isso supunha informação média do A31. Os 10 de D têm SNR de rede 12,1–16,8; com o ajuste σ(SNR) calibrado no A31 (6 %), o **poder de planejamento é 3,7–3,9σ (D10) e 4,4–4,6σ (D14)** [DERIVED]; pela regra 2 congelada (regra 3 antes da 5) o veredito seria **NOT_FALSIFIED_UNDERPOWERED qualquer que seja δ̂**. Falta 1,78× de informação para 5σ em D10. O conjunto B do V1 (GW150914, GW200129, …; SNR 20–26) dá 6,4σ: a diferença é o SNR.",
 "- Custo [DERIVED/DECLARADO]: 170 CPU-h por PE (central; 51–517); D10 só 55–63 h de parede; cadeia F4.1 + D10 + C2: 121–140 h (5–6 dias; pessimista 15–17). As duas PE reais da casa (GW250114) nunca convergiram (Δlogz 425 e 177 em maxcall).",
 "- Falta código antes de qualquer PE: guarda novo pinado ao V1 (a cadeia 013-bis/015 está vencida desde 03/10 e sem recibo de auditoria), semente de cegueira, injeções C2 em off-source de D, estimador do ramo B + estágio cego + abertura + veredito (`gw_stack.veredito` é do eco e devolve DETECTED, que o V1 não permite); o prior d_L [100, 2000] Mpc truncaria 5 dos 10 (D_L até 4,9 Gpc).",
 "- **A decisão voltou ao operador** (quadro F4.1/F4.2 AGUARDA_OPERADOR; Mapa: ERRATA do seq 1545; ACOM rev 15): (c) PE cega até o estágio cego e decidir a abertura com as σ_i reais; (b) não rodar, parede medida, D fica cego para E com combinação pré-registrada; (a) cadeia completa. Plano: `work\\conjunto_D_20261029\\PLANO_EXECUCAO_D_29out.md`.",
 "<!-- conjunto_d:errata_poder_29out -->", ""])
novo = raw + (b"" if raw.endswith(eol.encode()) else eol.encode()) + tx.encode("utf-8")
ts = time.strftime("%Y%m%d_%H%M%S"); bak = p.with_name(p.name + ".bak_" + ts); bak.write_bytes(raw); assert bak.read_bytes() == raw
tmp = p.with_name(p.name + ".tmp_" + ts); tmp.write_bytes(novo); assert tmp.read_bytes().startswith(raw) and len(novo) > len(raw)
os.replace(tmp, p); print("errata anexada", len(raw), "->", len(p.read_bytes()), "backup", bak.name)
