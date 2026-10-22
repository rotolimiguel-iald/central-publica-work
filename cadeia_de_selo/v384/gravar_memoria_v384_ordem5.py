# -*- coding: utf-8 -*-
"""Memoria + mapa (regra do backup imediato): a ORDEM 5 do operador (03/10, manha) -- ratificacao («Concordo com tudo»: as cinco matrizes,
o L_diss como vazamento nucleo -> periferia, os coeficientes dos validadores), o NIVEL B (rito robusto), a FERRAMENTA de reaproveitamento
(versoes intermediarias nao rodam as duas horas; a versao final roda completa sempre) e a primeira rodada completa. Verbatim do transcrito."""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
TOP = os.path.join(UMEM, "v384-pilar-quantico-gpu-02out.md")
T = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
MARCA = "<!-- ordem5_ratificacao_ferramenta_v384 -->"
verb = None
with open(T, encoding="utf-8") as f:
    for line in f:
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") != "user":
            continue
        c = d.get("message", {}).get("content")
        txts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        for t in txts:
            t2 = t.strip()
            if t2.startswith("Concordo com tudo, vamos de rito robusto"):
                verb = t2
assert verb and "rodar ela completa uma primeira vez" in verb, "verbatim nao achado"
bloco = (
    "\n\n" + MARCA + "\n"
    "**5. O operador, verbatim (03/10/2026, manhã):** «" + verb + "»\n\n"
    "**Logo:** (a) RATIFICADO o conjunto proposto em 03/10 — as cinco matrizes (L_reh, L_anti = √β·√K, L_prune, L_cons, L_diss = o vazamento "
    "núcleo → periferia, γ_diss livre e varrido, nunca calibrado) e os coeficientes dos validadores como realização canônica, que o T4 varia de forma "
    "adversarial; (b) **NÍVEL B** (rito robusto, ~2 h); (c) **a FERRAMENTA de reaproveitamento**: nas versões intermediárias (ajuste de texto, teorema "
    "novo) o resultado da GPU é reaproveitado por chave de conteúdo, sem as duas horas; **a versão FINAL roda completa sempre** — o mesmo interruptor "
    "`TGL_RITE_CHECKPOINT=1` do v321, com uma diferença: a rodada completa também GRAVA o resultado (para as intermediárias seguintes); "
    "(d) a v384 roda completa uma primeira vez. A promessa de 03/10 segue: o pré-registro congelado vai ao operador ANTES de qualquer cálculo dos testes.\n"
)
raw = open(TOP, "rb").read()
if MARCA.encode("utf-8") in raw:
    print("topico: a ordem 5 ja esta")
else:
    STAMP = time.strftime("%Y%m%d_%H%M%S")
    bak = TOP + ".bak_" + STAMP; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + bloco.encode("utf-8"); tmp = TOP + ".tmp_" + STAMP
    open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(raw)
    os.replace(tmp, TOP); assert open(TOP, "rb").read() == novo
    print("topico:", len(raw), "->", len(novo), "B; backup", os.path.basename(bak))
regs = rotas._le()
if not any(r.get("rota_id") == "quantica.pilar_v384_decisao_operador_03out" for r in regs):
    o = rotas.registrar([dict(tipo="ROTA", rota_id="quantica.pilar_v384_decisao_operador_03out", dominio="DEPHASING", status="EM_CURSO", estatuto="INPUT",
        olhou_dados=False, titulo="decisão do operador (03/10): as cinco matrizes ratificadas; nível B (rito ~2 h); ferramenta de reaproveitamento da GPU nas versões intermediárias; a final roda completa sempre",
        pergunta="como o pilar quântico da v384 roda e se reaproveita?",
        resultado="verbatim: «" + verb + "»",
        proximo_passo="motor da GPU validado em modelos analíticos (nenhum operador da teoria); a sonda de tempo do motor; o pré-registro congelado ao operador antes de calcular; depois o um.py v384",
        refs=["quantica.cinco_operadores_lindblad_matrizes", "infra.gpu_sonda_tempo_v384", "quantica.dobras_c3_hierarquia_e_matematica"])],
        "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
