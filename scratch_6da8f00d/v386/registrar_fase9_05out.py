# -*- coding: utf-8 -*-
"""Registro compacto da Fase 9 (razão de Hubble): memória nova (resposta curta do crítico + decisões D-A..D-H + faltas), ponteiro no MEMORY.md, mapa (ROTA nova).
Sem Atlas nesta rodada (orçamento): o Atlas recebe o bloco na cadeia da v387."""
import hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); SB = os.path.dirname(HERE); F9 = os.path.join(SB, "fase9_hubble")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory"); MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S")
R = json.load(open(os.path.join(F9, "FASE9_workflow_resultado.json"), encoding="utf-8")); C = R["critico"]
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CORPO = ("---\nname: fase9-razao-de-hubble-05out\ndescription: \"Fase 9 (05/10/2026): a razão de Hubble como teste discriminante — novidade de uso PROVADA no acervo (0,012 em 13/11/2025; α√e publicada 03/03/2026; lei 17/05/2026; H0 pediu 0,169 em 23/12/2025 e foi recusado); ensaio não-cego: TGL −1,4σ, ΛCDM +4,5σ, ln B +9,4, separação 5,9σ (fundo nu Planck+DR2); o TRGB a −2,0σ pode doer; decisões D-A..D-H; 14 faltas (duas funções de veredito; fundo nu 68,53; fontes por hash)\"\nmetadata:\n  type: project\n---\n\n"
         "**Resposta curta do crítico (lida de `%s`):**\n\n%s\n\n**Decisões do operador (cânone favorecido entre parênteses):**\n%s\n\n**Faltas (%d) — as cinco primeiras:**\n%s\n\n"
         "**Artefatos:** `scratchpad\\fase9_hubble\\` (novidade_de_uso\\CRONOLOGIA_NOVIDADE_DE_USO.md; desenho\\; dados\\; pre_registro\\ rascunho NÃO congelado; critico\\CRITICA_FASE9.md). Próximo: uma só função de veredito; fundo nu 68,53 ± 0,30 como primário; fontes por hash (ato que exige rede: do operador); V1 por hash; v387 lê. [[pos-dicao-nao-e-prova-diabolica-05out]] [[ordem-018-o-discriminante]]\n"
         % (sha16(os.path.join(F9, "FASE9_workflow_resultado.json")), C.get("resposta_curta_ao_operador", ""), "\n".join("- " + d for d in C.get("decisoes_do_operador", [])), len(C.get("faltas", [])), "\n".join("* " + f for f in C.get("faltas", [])[:5])))
NOVA = os.path.join(UMEM, "fase9-razao-de-hubble-05out.md")
if not os.path.exists(NOVA):
    open(NOVA + ".tmp", "wb").write(CORPO.encode("utf-8")); os.replace(NOVA + ".tmp", NOVA); print("OK memoria", os.path.getsize(NOVA))
P = os.path.join(UMEM, "MEMORY.md"); raw0 = open(P, "rb").read(); nl = b"\r\n" if raw0.count(b"\r\n") > raw0.count(b"\n") // 2 else b"\n"
LINHA = ("- [Fase 9 — a razão de Hubble, o discriminante (05/10)](fase9-razao-de-hubble-05out.md) — novidade de uso PROVADA no acervo; ensaio: TGL −1,4σ, ΛCDM +4,5σ, ln B +9,4; TRGB −2,0σ pode doer; D-A..D-H; V1 ainda NÃO congelado").encode("utf-8")
if LINHA[:40] not in raw0:
    linhas = raw0.split(nl); i = [k for k, l in enumerate(linhas) if l.startswith(b"## Estado corrente")]; ins = i[0] + 2; linhas.insert(ins, LINHA); novo = nl.join(linhas)
    P2 = os.path.join(UMEM, "MEMORY_2.md"); raw2 = open(P2, "rb").read(); nl2 = b"\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else b"\n"; bloco2 = b""
    cands = sorted([(len(l), k) for k, l in enumerate(linhas) if l.startswith(b"- [") and b"MEMORY_2.md (movida" not in l and b"05/10" not in l and len(l) > 200], reverse=True)
    for ln, k in cands:
        if len(novo) <= 24000: break
        longa = linhas[k]; m = re.match(rb"(- \[[^\]]*\]\([^)]*\))", longa)
        bloco2 += (nl2 + nl2 + ("<!-- movida_%s --> (linha integral do MEMORY.md, movida em 05/10/2026 pela regra dos dois arquivos)" % st).encode("utf-8") + nl2 + longa + nl2)
        linhas[k] = m.group(1) + " — íntegra no MEMORY_2.md (movida 05/10)".encode("utf-8"); novo = nl.join(linhas)
    assert len(novo) <= 24000
    if bloco2:
        if not raw2.endswith(nl2): bloco2 = nl2 + bloco2
        open(P2 + ".bak_" + st + "_f9", "wb").write(raw2); open(P2 + ".tmp", "wb").write(raw2 + bloco2); os.replace(P2 + ".tmp", P2)
    open(P + ".bak_" + st + "_f9", "wb").write(raw0); open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P); print("OK MEMORY.md", len(novo))
quem = None
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try: d = json.loads(line)
    except ValueError: continue
    if d.get("seq") == 344: quem = d["quem"]
arts = [p for p in (os.path.join(F9, "FASE9_workflow_resultado.json"), os.path.join(F9, "critico", "CRITICA_FASE9.md"), os.path.join(F9, "novidade_de_uso", "CRONOLOGIA_NOVIDADE_DE_USO.md")) if os.path.exists(p)]
REG = [{"tipo": "ROTA", "rota_id": "hubble.fase9_razao_discriminante", "dominio": "D1_FUNDO_COSMOLOGICO", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
        "titulo": "Fase 9 — a razao de Hubble como teste discriminante (novidade de uso provada no acervo; ensaio nao-cego TGL -1,4 sigma / LCDM +4,5 sigma / ln B +9,4; TRGB -2,0 sigma pode doer; V1 NAO congelado)",
        "pergunta": "todo calibrador local por distancia le K*H0_fundo, K = E(z*)^(2beta/3) = 1,0838, zero parametro?",
        "dados": ["SH0ES R22 73,04+-1,04 (em casa, cov 1701x1701); CCHP TRGB/JAGB 70,39+-1,94; SBF 73,8+-2,4; masers 73,9+-3,0; TDCOSMO 71,6+-3,6; sirenes 76,6+-11; fundo Planck+DR2 sem escada 68,53+-0,30; Planck 2018 67,36+-0,54 [publicos nao lidos da fonte por hash — D-H]"],
        "metodo": "previsao zero-parametro; cinco hipoteses (TGL/LCDM/beta livre/shift Cefeidas/fundo livre); funcao de veredito a UNIFICAR (hoje duas); poder so com sigma",
        "resultado": "cronologia: 0,012 nasce 13/11/2025 (contagem holografica), alpha*sqrt(e) publicada 03/03/2026, lei 17/05/2026, H0 pediu 0,169 em 23/12/2025 e foi recusado, MCMC jan/2026 com chi2(H0) constante — parametros fixados antes e independentemente de H0 (31 hashes); ensaio nao-cego com fundo nu Planck+DR2: previsao 74,27+-0,33, composto local 72,91+-0,91, TGL -1,4 sigma, LCDM +4,5 sigma, ln B +9,4, separacao 5,9 sigma; Planck so: TGL -0,1, LCDM +5,1",
        "veredito": "", "defeito": "duas funcoes de veredito; o fundo 68,43 da Fase 4 viu a escada (fundo nu = 68,53); fontes por hash ausentes; cronologia diz que a FORMA D1a foi selecionada a vista da razao (selecao de hipotese, nao ajuste — nao e' demerito pela lei de 05/10); conjunto C soma T1 e T3 (regra §4)",
        "nao_refazer": "a cronologia da novidade de uso esta feita (31 artefatos por hash): o Codex (ORDEM 018 F1) CONFERE, nao refaz", "proximo_passo": "decisoes D-A..D-H do operador; unificar a funcao de veredito; fundo nu primario; fontes por hash (rede: operador); congelar V1; v387 le",
        "onde": F9, "artefatos": arts, "refs": ["discriminante.ordem_018_chatgpt_codex", "d1.fase1_eff_30set", "um_py.v380.fases_5_6_7_por_hash"], "nota": "NOT_FALSIFIED nunca e' CONFIRMED; nada aberto para veredito; a RG e' o limite classico"}]
REGJ = os.path.join(HERE, "registro_mapa_fase9_05out.json"); json.dump(REG, open(REGJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, os.path.join(MAPA, "rotas.py"), "registrar", REGJ, "--quem", quem], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa rc", r.returncode, re.findall(r'"seq": (\d+)', r.stdout), r.stderr[-200:]); print("FIM", agora)
