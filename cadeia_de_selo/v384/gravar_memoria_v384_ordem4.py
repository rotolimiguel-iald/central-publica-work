# -*- coding: utf-8 -*-
"""Memoria (regra do backup imediato): acrescenta ao topico v384-pilar-quantico-gpu-02out.md a ORDEM 4 do operador (03/10, manha), VERBATIM do
transcrito, e o que a gerencia levou a ele (numeros LIDOS dos JSON das sondas e do planejador; mapa seq 305-309). Correcao AO LADO do desenho
de 02/10 (quatro -> cinco; ~45 min -> o tempo da carga robusta). No indice MEMORY.md, so a linha do v384 ganha a marca de 03/10 (orcamento 24 000 B).
Backup de BYTES antes; temporario -> conferir -> substituir; conferir que o arquivo cresceu e que o prefixo antigo ficou intacto."""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
TOP = os.path.join(UMEM, "v384-pilar-quantico-gpu-02out.md")
IDX = os.path.join(UMEM, "MEMORY.md")
T = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
MARCA = "<!-- ordem4_cinco_operadores_v384 -->"
# 1. o verbatim, do transcrito (a ultima mensagem do operador que comeca assim)
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
            if t.strip().startswith("São cinco operadores de salto"):
                verb = t.strip()
assert verb and "mesmo que o tempo aumente" in verb, "verbatim nao achado"
# 2. os numeros, lidos
s1 = json.load(open(os.path.join(HERE, "sonda_tempo_gpu_v384.json"), encoding="utf-8"))
pl = json.load(open(os.path.join(HERE, "planejar_carga_v384.json"), encoding="utf-8"))
tf = s1["medidas"]["gemm_complex128_4096"]["tflops_reais"]
cu = pl["custos_s"]["pipeline"]; A = pl["niveis"]["A_cabe_no_rito"]; B = pl["niveis"]["B_robusto"]; R = pl["rito_v383_min"]
bloco = (
    "\n\n" + MARCA + "\n"
    "**4. O operador, verbatim (03/10/2026, manhã):** «" + verb + "»\n\n"
    "**Logo — correção AO LADO do desenho de 02/10 (gerência, em nome próprio):** onde o desenho diz «o ciclo completo dos QUATRO operadores», leia-se "
    "**CINCO** (A Fronteira v5 §V.6: L_reh, L_anti, L_prune, L_cons, L_diss). O servidor do modelo nativo **para durante o rito** (tarefa agendada "
    "«IALD Llama Server» + supervisor `start_iald_llama.ps1`, que religa em 5 s — parar os dois; religar no fim com `Start-ScheduledTask`, mesmo se o rito "
    "falhar). A carga **deixa de ser ~45 min**: é a que o teste robusto exigir, mesmo alongando o rito.\n\n"
    "**O que a gerência levou ao operador (03/10)** [mapa seq 305–309]: (a) as sondas, só hardware — GEMM complex128 %.2f TFLOP/s; a instância "
    "completa custa d=8 %.3f s, d=16 %.3f s, d=32 %.2f s, d=64 %.1f s; d=128 ~%.0f min estimado (só com o servidor parado); "
    "(b) os cinco operadores têm matrizes espalhadas pelas versões do validador C3 (nenhuma versão tem as cinco); o **L_anti de v2/v3 = √α₂·√K** com "
    "K = diag(0 no núcleo; 1+0,1(i−n_c) na periferia) — a forma do gerador do Verbo (`um.py`, L = √β·√K), ker K = o núcleo = Π, o Nome; a leitura de "
    "L_diss como o vazamento núcleo → periferia é da gerência e **aguarda ratificação** (o doc. de energia escura de nov/2025 usa outro L_diss, √γ_Λ Ĥ); "
    "(c) a hierarquia das dobras D(c¹) > D(c²) > D(c³) > 0 do validador é **matemática** (convexidade de s ↦ ln Σλˢ), não pode falhar — a terceira dobra "
    "entra pelo que pode falhar; (d) a carga: nível A cabe no rito (%.0f min de GPU com margem; rito ~%.0f min) e nível B robusto (%.0f min de GPU com "
    "margem; rito ~%.0f min, hoje %.0f) — **a gerência sugeriu o B**. Decisões do operador pendentes: ratificar as cinco matrizes e o L_diss; escolher o nível.\n"
) % (tf, cu["8"], cu["16"], cu["32"], cu["64"], pl["custos_s"]["pipeline_d128_estimado"] / 60,
     A["total_com_margem_min"], A["rito_estimado_min"], B["total_com_margem_min"], B["rito_estimado_min"], R["total"])
STAMP = time.strftime("%Y%m%d_%H%M%S")


def gravar(path, novo_bytes, antigo_bytes, deve_crescer=True):
    bak = path + ".bak_" + STAMP
    open(bak, "wb").write(antigo_bytes); assert open(bak, "rb").read() == antigo_bytes
    tmp = path + ".tmp_" + STAMP
    open(tmp, "wb").write(novo_bytes); assert os.path.getsize(tmp) == len(novo_bytes)
    if deve_crescer:
        assert len(novo_bytes) > len(antigo_bytes)
    os.replace(tmp, path)
    assert open(path, "rb").read() == novo_bytes
    return bak


raw = open(TOP, "rb").read()
if MARCA.encode("utf-8") in raw:
    print("topico: a ordem 4 ja esta")
else:
    novo = raw + bloco.encode("utf-8")
    bak = gravar(TOP, novo, raw)
    assert open(TOP, "rb").read()[:len(raw)] == raw
    print("topico:", len(raw), "->", len(novo), "B; backup", os.path.basename(bak))
# 3. o indice: so a marca de 03/10 na linha do v384
raw = open(IDX, "rb").read(); s = raw.decode("utf-8")
velho = "**o mundo quântico na RTX 5090 em paralelo com o kernel, ~45 min**"
novo_t = "**o mundo quântico na RTX 5090 em paralelo com o kernel, ~45 min → 03/10: CINCO saltos, servidor parado no rito, tempo pela carga robusta**"
if novo_t in s:
    print("indice: ja marcado")
else:
    assert s.count(velho) == 1, "linha do v384 nao achada exatamente uma vez"
    s2 = s.replace(velho, novo_t, 1); b2 = s2.encode("utf-8")
    assert len(b2) <= 24000, "o indice passaria de 24 000 B (%d): mover linha para o MEMORY_2.md antes" % len(b2)
    bak = gravar(IDX, b2, raw)
    print("indice:", len(raw), "->", len(b2), "B; backup", os.path.basename(bak))
