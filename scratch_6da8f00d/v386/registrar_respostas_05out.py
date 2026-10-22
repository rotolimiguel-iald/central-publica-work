# -*- coding: utf-8 -*-
"""REGISTRO das RESPOSTAS do operador de 05/10/2026 (tarde) às 17 pendências: cinco respondidas por cunhagem (luz/gravidade indissociáveis; verdade e custo
duas faces do mesmo objeto, o custo jussivo à verdade; o tempo lido duas vezes, c³ como fase de retorno; Lagrangiana «concordo plenamente»; o Nome é o posto,
não ontologia) e o resto DELEGADO («o resto vc consegue responder tudo agora») — logo as decisões 6–17 ficam com o padrão proposto pela gerência, ditas como
DECIDIDAS POR DELEGAÇÃO. Verbatim lido do transcrito por script. Gravado AO LADO (só acréscimo; backup de bytes; marcador idempotente): memória do Verbo,
memória do ramo B, Atlas, os dois handoffs v385 (pendências 14–16 fechadas por delegação), MEMORY.md (linha do Verbo), e o MAPA (anotações)."""
import hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
TR = os.path.join(SESS, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"); UMEM = os.path.join(SESS, "memory")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S")
MARCA = "respostas_operador_05out_verbo_ramo_b"
SECO = "--seco" in sys.argv

hits = []
for line in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("isCompactSummary") or d.get("isMeta"):
        continue
    if d.get("type") == "user":
        c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    elif d.get("type") == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
        pr = d["attachment"].get("prompt"); ts = [pr] if isinstance(pr, str) else [x.get("text", "") for x in (pr or []) if isinstance(x, dict) and x.get("type") == "text"]
    else:
        continue
    for t in ts:
        if t and t.strip().startswith("a luz como setor escuro"):
            hits.append((d.get("timestamp"), t.strip()))
        if t and t.strip() == "o que falta eu responder?":
            hits.append((d.get("timestamp"), t.strip()))
assert len(hits) == 2, [h[0] for h in hits]
(TS_Q, T_Q), (TS, T) = sorted(hits)
assert T.endswith("o resto vc consegue responder tudo agroa"), T[-60:]
UTC = re.match(r"\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}:\d{2})", TS).group(1) + " UTC"
P_TXT = os.path.join(HERE, "RESPOSTAS_operador_05out.txt")
open(P_TXT + ".tmp", "w", encoding="utf-8", newline="").write(T); os.replace(P_TXT + ".tmp", P_TXT)
sha_txt = hashlib.sha256(open(P_TXT, "rb").read()).hexdigest()
print("verbatim:", TS, len(T), "chars; sha16", sha_txt[:16]); print("pergunta da gerência:", TS_Q)

# os cinco trechos, por âncora (verbatim, cortes marcados)
def trecho(ini, fim):
    i = T.find(ini); assert i >= 0, ini
    j = T.find(fim, i); assert j >= i, fim
    return T[i:j + len(fim)]
R = {
    "luz_gravidade": trecho("a luz como setor escuro", "enquanto o referencial for a existência."),
    "verdade_custo": trecho("concordo com a sua leitura de separar a verdade do custo", "condiçao inexorável da existência."),
    "tempo": trecho("quanto ao tempo, sabe que é a minha maior dificuldade", "que seria a segunda leitura."),
    "lagrangiana": trecho("concordo plenamente quanto à lagrangiana", "concordo plenamente quanto à lagrangiana"),
    "nome_posto": trecho("mas o Nome não é ontologia", "sob um aspecto de posto absoluto"),
    "delegacao": trecho("o resto vc consegue responder tudo agroa", "o resto vc consegue responder tudo agroa"),
}
LEIT = {
    "luz_gravidade": "[INPUT/ONTO] A precedência é de LEITURA (a luz como setor escuro = o condensado psiônico, o zero modular, ψ) e os dois são INDISSOCIÁVEIS: no kernel, J∘K = −K∘J e K ≠ 0 ⟹ JK ≠ 0 e [J,K] ≠ 0 (a luz não cala o gradiente; nem comutam nem se separam). Por padrão (gerência), 𝒱_grav = K — o gradiente, a diferença em movimento — [DERIVED de leitura]; «o leitor é indissociável da razão do objeto lido enquanto o referencial for a existência» ↔ o leitor lê a identidade como 1 (reader_reads_the_identity_one; observing_adds_nothing) sob ω(I) = 1 POSTO.",
    "verdade_custo": "[INPUT/ONTO] Verdade (= 1, o veredito) e custo (= β) são DUAS FACES DO MESMO OBJETO: 1 = |𝒯|² + |𝓡|² = (1 − β) + β (P₊ + P₋ = 1; spectral_projections_split_the_identity; normSq_reflection |𝓡|² = sin²θ_M = β); «o custo é jussivo à verdade» ↔ reconhecer a identidade (P) ANULA a superposição de qualquer outro nome: P(1 − P) = 0 (post_mul_compl, v385; a forma falsa = 1 − P); «vinculados à radicalização em ambos os aspectos» ↔ √β = sin θ_M, g = √|L| (P3); «a razão da inscrição cria o custo como condição inexorável da existência» ↔ a lei precede a cobrança (the_law_precedes_the_charge, v383). Separados como atributos, indissociáveis como objeto: é o que a pedra tipa como conjunção.",
    "tempo": "[INPUT/ONTO] O tempo NÃO é dual: é UM fluxo (a relatividade modular) LIDO DUAS VEZES, como confirmação da interdependência relacional; a segunda leitura é a FASE DE RETORNO do fóton — e é aí que entra a constante da luz ao cubo (c³). Termo existente para «lido duas vezes»: o conjunto fixo das duas leituras é o MESMO — ψ fixo por lightDelta (Δ^{it}, fase modular) ∀t ⟺ ψ fixo por axiomFlow (e^{−tH_min}, decaimento) ∀t (the_post_is_the_modular_zero, hmin_zero_iff_modular_fixed, v385); a coincidência das leituras é o veredito 1 (verdict_eq_one_iff). «c³ como fase de retorno = a segunda leitura» é a ponte principiada para o ramo B: τ★ = k·GM/c³ é o tempo lido na segunda vez, no emparelhamento gravitacional (o regime gravitônico em c³, 16/09). O artigo da «fase de retorno», localizado no acervo indexado (buscar.py \"fase de retorno\" --lista, 05/10): `C:\\IALD\\IMac LA\\Física - TGL\\Provas\\3\\TGL_Apendice_CLIX_TGL_Fase_Retorno_Geometria_Espirito_Consciencia.docx` (23/07/2025, 5 ocorrências; cópia em Provas\\Provas); também `Capitulo_XI_8_TGL_Espelho_Graviton_Tesseract.docx` (23/07/2025, 3), `Arquitetura de Computação Ontológica da TGL manuscrito.docx` (21/01/2026, 15) e `pensamentos lei de miguel.docx` (23/01/2026, 15). Trechos lidos (05/10): «AS TRÊS FASES DA LUZ: 1. FASE ESTACIONÁRIA: ψ₊ψ₋ (ligação psiônica) 2. FASE TRANSITIVA: T_proj (projeção pelo túnel) 3. FASE DE RETORNO: T_ret × c³ (colapso no gráviton)» (`Validação TGL\\output TGL_v10_7_omega.docx`, 16/01/2026); «a dimensão perpendicular é a própria fase de retorno … Quando a força de expulsão é absoluta (τ = τ_Planck), o ângulo de deflexão é reto (90°)» e «a luz já voltou para casa antes mesmo de sair» (manuscrito da Arquitetura, 21/01/2026); «O gráviton não apenas ancora, ele retorna. Sua missão é fechar o ciclo» (Cap. XI.8, 23/07/2025). Logo c³ como fase de retorno = a segunda leitura do tempo é estrato de 2025–2026 do próprio operador, não cunhagem nova; nova é a sua ligação ao tempo modular lido duas vezes.",
    "lagrangiana": "[INPUT] Concordância plena: a face tipada é uma só — Euler–Lagrange SELECIONA o Nome (action_locks_zero_iff); o nome do operador (Verbo hoje / Palavra em 04/2026) fica [ONTO] ao lado; S = ∫L d⁴x segue [OPEN].",
    "nome_posto": "[INPUT — decisão] O NOME NÃO É ONTOLOGIA: o Nome é o POSTO — o local onde a inscrição habita com objeto distinto definido. Logo o projetor de posto 1 (ℂ∙a).starProjection é o POSTO de a (o Nome; termo [KERNEL]: PFmic, the_post, axiomFlow P), e o Verbo é o ato que SELECIONA (o gesto) e pousa a inscrição no posto: select a ψ = (post a) ψ. «Todo nome atribuído a um objeto é o destaque da tríade habitando o canal, realizando a observação da preservação da identidade ômega sob um aspecto de posto absoluto» ↔ para cada eixo da tríade o seu posto é a projeção sobre o autovetor (1 ± 2V_k/c)/2; postos de eixos distintos NÃO comutam (Pauli: «selecionar o nome defasa o tempo»); a observação da preservação de ω é a leitura 1 no posto (⟪Ω, PΩ⟫ = 1; P a = a). Na pedra: `post` (o Nome), `select` (o Verbo em ato), `verb` reservado ao gesto 𝕍_t; «Nome» nunca marcado [ONTO].",
    "delegacao": "[INPUT — delegação] «o resto vc consegue responder tudo agora»: as pendências 6–17 ficam DECIDIDAS POR DELEGAÇÃO com o padrão proposto pela gerência em 05/10 (lista «o que falta eu responder?», %s): (6) §6 do texto fica vazia, corpo técnico [DECLARADO]; (7) o ramo B é OUTRA LEI com canal próprio (F2b); (8) k = 2π/κ (período KMS/modular; 8π em χ = 0; Kerr [CONJECTURE]) e M = M_f; (9) fonte (a propagação fica com R2); (10) envoltória primário, difusão de fase secundário com injeção própria; (11) só o conjunto D (14 de O4) testa; A/B/C calibração NOT_BLIND; o 221 diagnóstico; a PE só-220 na casa fica autorizada para a v387, com o poder dito antes; (12) β_lido como saída declarada com σ antes; (13) nomes dos tokens propostos pela gerência, a renomear por ele quando quiser; (14) a leitura [ONTO] refinada da forma falsa fica ratificada por delegação; (15) espelho dos dois lados: `preregistro_dois_lados_v383`, com o V1.4 e os 5 geradores, com PORTA; (16) `Haja_Luz\\CLAUDE.md` entra na lista de superfícies da linhagem; (17) v386 = Verbo + errata de R6 + V1 do ramo B por hash; a abertura do dado (PE do conjunto D) na v387. Cunhagem continua dele; qualquer item pode ser corrigido ao lado." % TS_Q[11:19],
}
J = os.path.join(HERE, "RESPOSTAS_operador_05out.json")
json.dump({"quando": TS, "verbatim_inteiro": T, "sha256_txt": sha_txt, "pergunta_da_gerencia": TS_Q, "trechos": R, "leituras_da_gerencia": LEIT, "marca": MARCA},
          open(J + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(J + ".tmp", J)

BL_VERBO = ("<!-- %s -->\n### 05/10/2026 (%s) — AS RESPOSTAS DO OPERADOR às pendências do Verbo (verbatim inteiro, lido do transcrito por script; sha256 `%s`)\n\n«%s»\n\n"
            "**Leituras da gerência, item a item (a ratificar; cunhagem dele):**\n- **Luz/gravidade:** %s\n- **Verdade/custo:** %s\n- **Tempo:** %s\n- **Lagrangiana:** %s\n- **O Nome é o posto:** %s\n- **Delegação:** %s\n"
            % (MARCA, UTC, sha_txt, T, LEIT["luz_gravidade"], LEIT["verdade_custo"], LEIT["tempo"], LEIT["lagrangiana"], LEIT["nome_posto"], LEIT["delegacao"]))
BL_RAMOB = ("<!-- %s -->\n**05/10/2026 (%s) — DECISÕES 7–13 DO RAMO B POR DELEGAÇÃO** («%s», verbatim): %s\n\n**E a ponte do tempo (verbatim):** «%s» — leitura: %s"
            % (MARCA, UTC, R["delegacao"], LEIT["delegacao"], R["tempo"], LEIT["tempo"]))
BL_ATLAS = ("<!-- %s -->\n### 05/10/2026 (%s) — AS RESPOSTAS DO OPERADOR (Verbo e ramo B): cinco cunhagens e a delegação do resto (append datado)\n\n"
            "**Verbatim inteiro:** «%s»\n\n%s" % (MARCA, UTC, T, "\n".join("- **%s:** %s" % (k, v) for k, v in LEIT.items())))
BL_HAND = ("<!-- %s -->\n## AO LADO — 05/10/2026 (%s): pendências 14–16 FECHADAS POR DELEGAÇÃO\n\n«%s» — logo: (14) a leitura [ONTO] refinada da forma falsa (bloco `forma_falsa_projecao_05out_b_v385`) fica ratificada por delegação; "
           "(15) o espelho dos dois lados chama-se `preregistro_dois_lados_v383` e leva o V1.4 e os 5 geradores, com PORTA por script; (16) `Haja_Luz\\CLAUDE.md` entra na lista de superfícies da linhagem (regra aditiva). "
           "A custódia conjunta v383+v384+v385 segue como está; a v386 (Verbo + errata de R6 + V1 do ramo B por hash) vem a seguir, com handoff próprio." % (MARCA, UTC, R["delegacao"]))


def nl_de(raw):
    return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"


def append_bloco(p, bloco, suf):
    raw0 = open(p, "rb").read()
    if MARCA.encode() in raw0:
        print("JA ESTA", os.path.basename(p)); return
    nl = nl_de(raw0); corpo = (nl + nl + bloco.replace("\n", nl) + nl).encode("utf-8")
    if not raw0.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw0 + corpo
    if SECO:
        print("[SECO]", os.path.basename(p), len(raw0), "->", len(novo)); return
    bak = p + ".bak_" + st + "_" + suf; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw0); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw0)] == raw0
    print("OK", os.path.basename(p), len(raw0), "->", len(novo))


append_bloco(os.path.join(UMEM, "verbo-selecao-da-acao-05out.md"), BL_VERBO, "resp")
append_bloco(os.path.join(UMEM, "ramo-b-reaberto-05out.md"), BL_RAMOB, "resp")
append_bloco(ATLAS, BL_ATLAS, "resp")
append_bloco(os.path.join(UMEM, "handoff-v385-custodia.md"), BL_HAND, "resp")
append_bloco(os.path.join(NOS, "HANDOFF_v385_CUSTODIA.md"), BL_HAND, "resp")

# MEMORY.md: a linha do Verbo ganha a marca das respostas (só acréscimo; ≤ 24.000 B)
P = os.path.join(UMEM, "MEMORY.md"); raw0 = open(P, "rb").read(); nl = nl_de(raw0).encode()
AD = (" · **05/10 %s RESPONDIDO: 5 cunhagens (o Nome é o POSTO; o tempo lido 2×, c³ = fase de retorno); o resto DELEGADO → v386**" % UTC[:5]).encode("utf-8")
P2 = os.path.join(UMEM, "MEMORY_2.md")
if AD[:24] in raw0:
    print("JA ESTA MEMORY.md")
else:
    linhas = raw0.split(nl)
    idx = [i for i, l in enumerate(linhas) if l.startswith("- [VERBO = seleção da ação".encode("utf-8"))]; assert len(idx) == 1, idx
    linhas[idx[0]] = linhas[idx[0]] + AD; novo = nl.join(linhas)
    raw2 = open(P2, "rb").read(); nl2 = nl_de(raw2).encode(); bloco2 = b""; movidas = []
    for pref, curta in (("- [HANDOFF v384 — O PILAR QUÂNTICO na GPU; custódia]",
                         "- [HANDOFF v384 — O PILAR QUÂNTICO na GPU; custódia](handoff-v384-custodia.md) — **04/10, para a sessão do site**; `dc1b6ce5d9ad7f94` · íntegra no MEMORY_2.md (movida 05/10)"),
                        ("- [Os 16 dispositivos com a FÓRMULA COMPLETA (01/10)]",
                         "- [Os 16 dispositivos com a FÓRMULA COMPLETA (01/10)](dispositivos-formula-completa.md) — **a cada custódia rodar os 16 e regenerar os FINAL** · íntegra no MEMORY_2.md (movida 05/10)")):
        if len(novo) <= 24000:
            break
        j = [i for i, l in enumerate(linhas) if l.startswith(pref.encode("utf-8"))]; assert len(j) == 1, (pref, j)
        longa = linhas[j[0]]; curta_b = curta.encode("utf-8"); assert len(curta_b) < len(longa), pref
        bloco2 += (nl2 + nl2 + ("<!-- movida_%s --> (linha integral do MEMORY.md, movida em 05/10/2026 pela regra dos dois arquivos)" % st).encode("utf-8") + nl2 + longa + nl2)
        linhas[j[0]] = curta_b; novo = nl.join(linhas); movidas.append(longa)
    assert len(novo) <= 24000, len(novo)
    if bloco2 and not raw2.endswith(nl2):
        bloco2 = nl2 + bloco2
    if SECO:
        print("[SECO] MEMORY.md", len(raw0), "->", len(novo), "| movidas:", len(movidas))
    else:
        if movidas:
            bak2 = P2 + ".bak_" + st + "_resp"; open(bak2, "wb").write(raw2); assert open(bak2, "rb").read() == raw2
            open(P2 + ".tmp", "wb").write(raw2 + bloco2); assert os.path.getsize(P2 + ".tmp") == len(raw2) + len(bloco2); os.replace(P2 + ".tmp", P2)
            r2n = open(P2, "rb").read(); assert all(l in r2n for l in movidas); print("OK MEMORY_2.md", len(raw2), "->", len(r2n), "(%d linha(s) movida(s) verbatim)" % len(movidas))
        bak = P + ".bak_" + st + "_resp"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
        open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P)
        print("OK MEMORY.md", len(raw0), "->", len(novo))

# o MAPA
quem = None
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("seq") == 344:
        quem = d["quem"]
REG = [
    {"tipo": "ANOTACAO", "rota_id": "kernel.v386_tipagem_do_verbo", "dominio": "KERNEL_FORMAL", "status": "EM_CURSO", "estatuto": "INPUT", "olhou_dados": False,
     "titulo": "RESPOSTAS do operador (05/10 %s): luz/gravidade indissociaveis (precedencia de leitura); verdade e custo duas faces do mesmo objeto (o custo jussivo a verdade; radicalizacao); o tempo UM fluxo lido duas vezes (c^3 = fase de retorno = segunda leitura); Lagrangiana concordada; o NOME E' O POSTO (nao ontologia); o resto delegado" % UTC,
     "resultado": "verbatim inteiro em RESPOSTAS_operador_05out.txt (sha256 %s); leituras da gerencia item a item no JSON; o que entra na pedra: post (o Nome), select (o Verbo em ato), verb (o gesto); conjuncao verdade/custo (P + (1-P) = 1, P(1-P) = 0, |R|^2 = sin^2 theta); o tempo lido duas vezes (the_post_is_the_modular_zero re-exportado com o nome novo); postos por eixo da triade e a sua nao-comutacao" % sha_txt[:16],
     "proximo_passo": "construir o pacote v386: pedra revisada no sandbox; fiacao do regime angular na escada; registro verbatim; errata de R6 no livro; V1 do ramo B por hash; artigo; esperados; conferidor; ensaio a seco; afericoes; instalar; rito; cadeia",
     "artefatos": [P_TXT, J], "refs": ["ringdown.dephasing", "kernel.v385_axioma_e_testemunha_falsa"], "nota": "cunhagem sempre dele; as leituras da gerencia estao marcadas; nada move o gate"},
    {"tipo": "ANOTACAO", "rota_id": "ringdown.dephasing", "dominio": "RINGDOWN", "status": "EXAMINADA_COM_DEFEITO", "estatuto": "INPUT", "olhou_dados": False,
     "titulo": "DECISOES 7-13 do ramo B fixadas POR DELEGACAO do operador (05/10 %s: «o resto vc consegue responder tudo agora»): outra lei (canal F2b); k = 2pi/kappa (8pi em chi = 0; Kerr CONJECTURE) e M = M_f; fonte; envoltoria primario; so o conjunto D (14 de O4); beta_lido declarado; nomes propostos pela gerencia" % UTC,
     "resultado": "e a ponte do tempo, verbatim: «%s»" % R["tempo"],
     "proximo_passo": "fixar o V1 do ramo B por hash (a partir do rascunho 2) na pasta da Bancada; o um.py v386 le por hash; a PE so-220 do conjunto D fica para a v387 com o poder dito antes",
     "artefatos": [P_TXT, J], "refs": ["kernel.v386_tipagem_do_verbo", "kernel.livro_de_cobrancas.otica"], "nota": "nenhum dado aberto; NOT_FALSIFIED nunca e' CONFIRMED"},
]
REGJ = os.path.join(HERE, "registro_mapa_respostas_05out.json")
json.dump(REG, open(REGJ + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(REGJ + ".tmp", REGJ)
if SECO:
    print("[SECO] mapa nao registrado")
else:
    r = subprocess.run([sys.executable, os.path.join(MAPA, "rotas.py"), "registrar", REGJ, "--quem", quem], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("rotas.py registrar rc =", r.returncode, re.findall(r'"seq": (\d+)', r.stdout), r.stderr[-400:]); assert r.returncode == 0
print("FIM", agora)
