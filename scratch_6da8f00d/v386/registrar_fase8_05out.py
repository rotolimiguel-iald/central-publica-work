# -*- coding: utf-8 -*-
"""REGISTRO da Fase 8 (o efeito de β no Big Bang / era da radiação): a pergunta do operador verbatim, a resposta por dados (lentes + crítico), a ERRATA da
gerência («só-matéria ⟹ ~0» não tem registro; «0,70σ» é separação, não tensão), as decisões D1–D11; copia ao ORDEM_018_INSUMOS o rascunho do V1 da Fase 8,
o poder e a crítica; memória nova + ponteiro no MEMORY.md; Atlas (append datado); mapa (ROTA nova + ANOTACAO na rota do canal N_eff)."""
import hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); SB = os.path.dirname(HERE); F8 = os.path.join(SB, "fase8_big_bang")
SESS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes"); TR = os.path.join(SESS, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"); UMEM = os.path.join(SESS, "memory")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md"); MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
INS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "PARA_CHATGPT", "ORDEM_018_INSUMOS")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S"); MARCA = "fase8_big_bang_05out"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


hit = None
for line in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("isCompactSummary") or d.get("isMeta") or d.get("type") != "user":
        continue
    c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    for t in ts:
        if t and t.strip().startswith("usando a nossa bancada de teste você consegue examinar o efeito de Betatgl no Big bang"):
            hit = (d.get("timestamp"), t.strip())
assert hit; TS, T = hit; UTC = re.match(r"\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}:\d{2})", TS).group(1) + " UTC"
R = json.load(open(os.path.join(F8, "FASE8_workflow_resultado.json"), encoding="utf-8")); C = R["critico"]
resp = C.get("resposta_curta_ao_operador", ""); dec = C.get("decisoes_do_operador", [])
# cópias ao ORDEM_018_INSUMOS (rascunho V1, poder, crítica) — bytes conferidos
cop = []
for rel in (("pre_registro", "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.md"), ("pre_registro", "PODER_FASE8_UNIVERSO_PRIMORDIAL.json"), ("pre_registro", "poder_fase8_universo_primordial.py"), ("critico", "CRITICA_FASE8.md")):
    src = os.path.join(F8, *rel)
    if os.path.exists(src):
        dst = os.path.join(INS, "FASE8__" + rel[-1]); b = open(src, "rb").read()
        if not (os.path.exists(dst) and open(dst, "rb").read() == b):
            open(dst + ".tmp", "wb").write(b); assert open(dst + ".tmp", "rb").read() == b; os.replace(dst + ".tmp", dst)
        cop.append((dst, sha(dst)[:16], len(b)))
json.dump({"quando": agora, "FASE8_workflow_resultado_sha16": sha(os.path.join(F8, "FASE8_workflow_resultado.json"))[:16], "copiados": [(os.path.basename(a), b, c) for a, b, c in cop]},
          open(os.path.join(INS, "FASE8__MANIFESTO_COPIA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ERR = ("**ERRATA da gerência, em nome próprio (05/10, %s):** (1) a opção «só sobre a matéria ⟹ efeito ~0 na era da radiação» que eu listei NÃO tem registro na casa: a lei veste o fluido total — "
       "ρ_TGL = β(ρ+p) = β[(4/3)ρ_r + ρ_m] (pedra 105 `RhoPlusPClosure`: `hubble_form` = (1+4β/3)ρ_r + (1+β)ρ_m + ρ_Λ; derivação do operador de 08/08; worker V3; errata de maio); "
       "(2) «0,70σ contra Planck 2018» é a SEPARAÇÃO TGL–SM em σ, não a tensão contra o centro medido (1,02σ Planck+lensing+BAO; 1,61σ CMB-SPA; 2,49σ ACT+Planck+BBN; os centros estão ABAIXO do padrão e a TGL prevê +0,12 acima); "
       "(3) o ΔN-equivalente é 0,0985 na BBN (antes da aniquilação e±) e 0,1195 depois (CMB): o exato é o speed-up S = 1,007989 num código de BBN (não instalado; tabelas existem no camb). O resto da resposta está na memória." % agora)
CORPO = ("---\nname: fase8-universo-primordial-05out\ndescription: \"Fase 8 (05/10/2026): o efeito de β no Big Bang / era da radiação — a pergunta do operador verbatim; a resposta por dados: a lei dá o MÁXIMO na radiação (4β/3) e zero no atrator; ΔN_eff = +0,1195 (identidade ρ+p, pedra 105; o número da casa a 1e-12); poder hoje nulo (Planck 1,0–2,5σ contra o centro; Nível 2 INCAPAZ; BBN σ/β = 2,6); CMB-S4 ~4σ; 'condição de existência' provada só como face de kernel; errata da gerência (só-matéria sem registro; separação ≠ tensão); decisões D1–D11\"\nmetadata:\n  type: project\n---\n\n"
         "<!-- %s -->\n**O OPERADOR (05/10/2026, %s, verbatim):** «%s»\n\n**Resposta por dados (crítico de completude da Fase 8, lido do relatório `%s`):**\n\n%s\n\n%s\n\n**Decisões do operador (D1–D11), com a opção favorecida:**\n%s\n\n"
         "**Artefatos:** rascunho do V1 da Fase 8, poder (só σ) e crítica copiados a `ORDEM_018_INSUMOS\\FASE8__*` (%s). [[tres-testes-de-estresse-conjuntos-05out]] [[ordem-018-o-discriminante]] [[pos-dicao-nao-e-prova-diabolica-05out]]\n"
         % (MARCA, UTC, T, sha(os.path.join(F8, "FASE8_workflow_resultado.json"))[:16], resp, ERR, "\n".join("- " + d for d in dec), "; ".join("%s `%s`" % (os.path.basename(a), b) for a, b, c in cop)))
NOVA = os.path.join(UMEM, "fase8-universo-primordial-05out.md")
if not os.path.exists(NOVA):
    open(NOVA + ".tmp", "wb").write(CORPO.encode("utf-8")); os.replace(NOVA + ".tmp", NOVA); print("OK memoria", os.path.getsize(NOVA), "B")


def nl_de(raw):
    return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"


BL = ("<!-- %s -->\n### 05/10/2026 (%s) — FASE 8: β no Big Bang / era da radiação (append datado)\n\n**O OPERADOR (verbatim):** «%s»\n\n%s\n\n%s" % (MARCA, UTC, T, resp, ERR))
raw0 = open(ATLAS, "rb").read()
if MARCA.encode() not in raw0:
    nl = nl_de(raw0); corpo = (nl + nl + BL.replace("\n", nl) + nl).encode("utf-8")
    if not raw0.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw0 + corpo; bak = ATLAS + ".bak_" + st + "_f8"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(ATLAS + ".tmp", "wb").write(novo); assert os.path.getsize(ATLAS + ".tmp") == len(novo) > len(raw0); os.replace(ATLAS + ".tmp", ATLAS); print("OK Atlas", len(raw0), "->", len(novo))
P = os.path.join(UMEM, "MEMORY.md"); raw0 = open(P, "rb").read(); nl = nl_de(raw0).encode()
LINHA = ("- [Fase 8 — β no Big Bang / era da radiação (05/10)](fase8-universo-primordial-05out.md) — máximo na radiação (4β/3 ⟹ ΔN_eff +0,12, identidade ρ+p); poder hoje nulo; CMB-S4 ~4σ; «condição de existência» provada só como face de kernel; D1–D11").encode("utf-8")
if LINHA[:40] not in raw0:
    linhas = raw0.split(nl); i = [k for k, l in enumerate(linhas) if l.startswith(b"## Estado corrente")]; assert len(i) == 1
    ins = i[0] + 2; assert linhas[ins - 1] == b""; linhas.insert(ins, LINHA); novo = nl.join(linhas)
    P2 = os.path.join(UMEM, "MEMORY_2.md"); raw2 = open(P2, "rb").read(); nl2 = nl_de(raw2).encode(); bloco2 = b""; movidas = []
    cands = sorted([(len(l), k) for k, l in enumerate(linhas) if l.startswith(b"- [") and b"MEMORY_2.md (movida" not in l and b"05/10" not in l and len(l) > 220], reverse=True)
    for ln, k in cands:
        if len(novo) <= 24000:
            break
        longa = linhas[k]; m = re.match(rb"(- \[[^\]]*\]\([^)]*\))", longa); assert m
        bloco2 += (nl2 + nl2 + ("<!-- movida_%s --> (linha integral do MEMORY.md, movida em 05/10/2026 pela regra dos dois arquivos)" % st).encode("utf-8") + nl2 + longa + nl2)
        linhas[k] = m.group(1) + " — íntegra no MEMORY_2.md (movida 05/10)".encode("utf-8"); novo = nl.join(linhas); movidas.append(longa); print("movida:", longa[:70].decode("utf-8", "replace"))
    assert len(novo) <= 24000, len(novo)
    if movidas:
        if not raw2.endswith(nl2):
            bloco2 = nl2 + bloco2
        bak2 = P2 + ".bak_" + st + "_f8"; open(bak2, "wb").write(raw2); assert open(bak2, "rb").read() == raw2
        open(P2 + ".tmp", "wb").write(raw2 + bloco2); assert os.path.getsize(P2 + ".tmp") == len(raw2) + len(bloco2); os.replace(P2 + ".tmp", P2)
    bak = P + ".bak_" + st + "_f8"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P); print("OK MEMORY.md", len(raw0), "->", len(novo))
# mapa
quem = None
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("seq") == 344:
        quem = d["quem"]
arts = [os.path.join(F8, "pre_registro", "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.md"), os.path.join(F8, "pre_registro", "PODER_FASE8_UNIVERSO_PRIMORDIAL.json"), os.path.join(F8, "critico", "CRITICA_FASE8.md"), os.path.join(F8, "FASE8_workflow_resultado.json")]
arts = [a for a in arts if os.path.exists(a)]
REG = [{"tipo": "ROTA", "rota_id": "primordial.fase8_era_da_radiacao", "dominio": "D1_FUNDO_COSMOLOGICO", "status": "PROPOSTA", "estatuto": "DERIVED", "olhou_dados": False,
        "titulo": "Fase 8 — beta no Big Bang / era da radiacao: a lei da-lhe o MAXIMO (4beta/3 ⟹ delta N_eff = +0,1195 pela identidade rho+p, pedra 105); poder hoje nulo; CMB-S4 ~4sigma; rascunho do V1 por hash",
        "pergunta": "«usando a nossa bancada de teste voce consegue examinar o efeito de Betatgl no Big bang?» (operador, 05/10 %s)" % UTC,
        "dados": ["Planck 2018 N_eff (2,99 +- 0,17 +lensing+BAO; 2,92 +- 0,19 TTTEEE); ACT DR6+Planck+BBN 2,89 +- 0,11; CMB-SPA 2,97 +- 0,12 [DECLARADO: frozen 10_frozen_neff_v1 com arXiv; PDFs nao em disco]", "Nivel 2 (TGL no CAMB, plik_lite em disco): beta = -0,0024 +- 0,0176 (N2_INCAPAZ)", "BBN descircularizado: beta = 0,0126 +- 0,0318 (expoente 0,57 [INPUT sem fonte legivel])"],
        "metodo": "lei delta<K_d> = beta|1+w| por era; identidade rho+p (hubble_form); tres instrumentos (N_eff no CMB; Nivel 2; speed-up S = 1,007989 na BBN com tabelas PRIMAT/PArthENoPE como bracket); poder so com sigma; uma entrada de beta por instrumento",
        "resultado": "separacao TGL-SM 0,70sigma (Planck+lensing+BAO) mas tensao contra o centro 1,02 / 1,61 / 2,49 sigma (os centros estao abaixo do padrao); delta N-equivalente 0,0985 (BBN) / 0,1195 (CMB); Y_p +0,0013 (0,3-0,5 sigma), D/H +0,03e-5 (0,4-1,3 sigma); NOT_FALSIFIED_UNDERPOWERED predeterminado hoje; CMB-S4 (sigma 0,03) 3,98 sigma se o centro migrar ao padrao, 6,45 se ficar em 2,97; 5 sigma pedem sigma(N_eff) <= 0,0239",
        "veredito": "", "defeito": "a opcao «so-materia» listada pela gerencia nao tem registro (errata ao lado); fontes com sha256 ausentes (D8); expoente do D/H 0,57 vs 1,57-1,62 (a ler da fonte); Nivel 2 canonico vs copia do Nos (D11)",
        "nao_refazer": "o canal N_eff, o Nivel 2 e o BBN descircularizado ja foram rodados (agosto/2026; frozen 96b51333, 664fc4cf): nao refazer; o numero 0,1195 e' o da casa; «Big Bang = ato de inscricao originario» e' ONTO/CONJECTURE (a face de kernel provada e' the_zero_is_the_false_witness + haja_luz)",
        "proximo_passo": "decisoes do operador D1-D11 (D1: a radiacao paga 4beta/3; D2: TGL-S primario, L cego; D3: uma entrada por instrumento; D4: Bancada antes do um.py; D5: tabelas como bracket, codigo de BBN = ato dele; D6: omega_b do CMB; D7: sinal fixado; D8: fontes por sha256; D9: duas convencoes de citacao; D10: ONTO; D11: Nivel 2 canonico); depois: canal N_eff na Bancada (fiacao), V1 por hash, ORDEM 018 ao ChatGPT (R-B/R-M)",
        "onde": F8, "artefatos": arts, "refs": ["cmb.neff_e_rho_mais_p", "estatistica.auditoria_da_evidencia", "d1.fase1_eff_30set", "discriminante.ordem_018_chatgpt_codex"],
        "nota": "NOT_FALSIFIED nunca e' CONFIRMED; nenhum dado baixado; o gate nao se move"},
       {"tipo": "ANOTACAO", "rota_id": "cmb.neff_e_rho_mais_p", "dominio": "D1_FUNDO_COSMOLOGICO", "status": "PROPOSTA", "estatuto": "REAL", "olhou_dados": False,
        "titulo": "Fase 8 (05/10): a FONTE dos literais tens_now/tens_act EXISTE na bancada (10_frozen_neff_v1.py, 5 medidas com arXiv) — fiacao, nao falta; o canal N_eff e' a identidade rho+p (pedra 105); duas convencoes de citacao (separacao TGL-SM vs tensao contra o centro)",
        "resultado": "delta N_eff = +0,119466 (dN_eff/dbeta = 9,9296); N_eff_TGL = 3,1635; tensoes contra o centro: 1,02 (Planck+lensing+BAO), 1,28 (Planck TTTEEE), 1,61 (CMB-SPA), 2,33 (ACT DR6+Planck), 2,49 (ACT+Planck+BBN); CMB-S4 3,98/6,45 sigma conforme o centro",
        "proximo_passo": "ligar o modulo a fonte datada do frozen (arXiv) em vez de literais; Bancada antes do um.py", "artefatos": arts[:1] + arts[-1:], "refs": ["primordial.fase8_era_da_radiacao"], "nota": "nenhum numero novo de memoria"}]
REGJ = os.path.join(HERE, "registro_mapa_fase8_05out.json")
json.dump(REG, open(REGJ + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(REGJ + ".tmp", REGJ)
r = subprocess.run([sys.executable, os.path.join(MAPA, "rotas.py"), "registrar", REGJ, "--quem", quem], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa rc", r.returncode, re.findall(r'"seq": (\d+)', r.stdout), r.stderr[-300:])
print("FIM", agora)
