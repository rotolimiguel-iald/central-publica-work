# -*- coding: utf-8 -*-
"""REGISTRO da cunhagem do operador de 05/10/2026 (16:53 UTC): «Verbo = seleção da ação; o Verbo seleciona nome, tempo e verdade; comando = co-mando;
o circuito comando → verbo → ação → objeto → leitura → axioma» — e do levantamento da gerência (4 lentes + crítico; pedra-candidata compilada no sandbox).
Grava AO LADO (só acréscimo; backup de bytes; marcador idempotente): memória nova (verbatim INTEIRO da mensagem, lido do arquivo extraído do transcrito
por script, com o sha256 conferido) + ponteiro no MEMORY.md (regra dos dois arquivos), Atlas (append datado), errata ao lado na memória da regra dos dois
regimes (os homônimos JÁ têm ponte: achado do crítico, medido), e o MAPA (rota nova kernel.v386_tipagem_do_verbo, EM_CURSO; artefatos por sha256).
Nada toca artefato selado; nada decide pelo operador (as decisões ficam listadas como pendentes)."""
import hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
UMEM = os.path.join(SESS, "memory")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
SB = os.path.dirname(HERE)
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S")
MARCA = "verbo_selecao_da_acao_05out"
SECO = "--seco" in sys.argv


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


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


# ---- os artefatos, por hash ----
TXT = os.path.join(HERE, "VERBO_operador_05out.txt"); assert os.path.exists(TXT)
T = open(TXT, encoding="utf-8", newline="").read(); sha_txt = sha(TXT); assert sha_txt.startswith("5973d79a49995c4c"), sha_txt
TS = "2026-10-05T16:53:25.825Z"   # carimbo do transcrito (gravado na extração; conferido abaixo)
# conferir o carimbo no transcrito
TR = os.path.join(SESS, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"); ok_ts = False
for line in open(TR, encoding="utf-8", errors="replace"):
    if TS in line and "Verbo=seleção da ação" in line:
        ok_ts = True; break
assert ok_ts, "carimbo nao conferido no transcrito"
PEDRA = os.path.join(SB, "v376", "kernel_src", "TGLExt", "TheVerbSelectsTheAction.lean"); sha_pedra = sha(PEDRA)
PEDRA_CP = os.path.join(HERE, "lean_viabilidade", "TheVerbSelectsTheAction.lean"); assert sha(PEDRA_CP) == sha_pedra
RES = json.load(open(os.path.join(HERE, "lean_viabilidade", "RESULTADO.json"), encoding="utf-8"))
assert RES["sha256"] == sha_pedra and RES["sorry"] == 0 and RES["declaracoes"] == 61
n_decl = RES["declaracoes"]; axs = set()
for v in RES["axiomas_por_declaracao"].values():
    for a in re.findall(r"\[([^\]]*)\]", v):
        axs |= {x.strip() for x in a.split(",") if x.strip()}
assert axs <= {"propext", "Classical.choice", "Quot.sound"}, axs
WF = os.path.join(HERE, "VERBO_workflow_resultado.json"); sha_wf = sha(WF)
W = json.load(open(WF, encoding="utf-8")); C = W["critico"]; P = C["proposta_v386"]
n_lentes = len(W["lentes"]); n_itens = sum(len(L.get("itens", [])) for L in W["lentes"])
LENTE_FILES = [os.path.join(HERE, "lente_linhagem_verbo", "LENTE_LINHAGEM_VERBO_20261005.md"),
               os.path.join(HERE, "auditoria_texto", "AUDITORIA_TEXTO_VERBO_v386.json"),
               os.path.join(HERE, "lente_triade", "LENTE_TRIADE_v386.md"),
               os.path.join(HERE, "critico", "CRITICO_COMPLETUDE_v386_verificacoes.json"),
               os.path.join(HERE, "lean_viabilidade", "AuditVerb_output.txt")]
LENTE_FILES = [p for p in LENTE_FILES if os.path.exists(p)]
print("artefatos:", len(LENTE_FILES), "lentes;", "pedra", sha_pedra[:16], n_decl, "decl; workflow", sha_wf[:16], n_lentes, "lentes", n_itens, "itens")
# a ponte dos homônimos, MEDIDA aqui (nunca de memória)
audit = open(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"), encoding="utf-8").read()
n_afb = audit.count("angular_form_is_the_boundary_s_matrix")
o16 = os.path.join(NOS, "tgl_kernel", "TGLExt", "O16", "RotationGeneratorBridges.lean")
o16_txt = open(o16, encoding="utf-8").read() if os.path.exists(o16) else ""
n_genK = o16_txt.count("genK_eq_Grot"); n_rot = o16_txt.count("rotGen_complex_eq_Grot")
assert n_afb >= 1 and n_genK >= 1 and n_rot >= 1, (n_afb, n_genK, n_rot)
RDR = os.path.join(UMEM, "regra-dos-dois-regimes.md"); rdr = open(RDR, encoding="utf-8", errors="replace").read()
assert "SEM lema ligando duas" in rdr, "frase-ancora nao achada na memoria dos dois regimes"

# ---- a memória nova ----
RESUMO = ("**O que a gerência mediu (05/10, 4 lentes só-leitura + crítico de completude; relatório `VERBO_workflow_resultado.json` `%s`; %d itens):** "
          "(1) a cunhagem-mãe — Verbo = seleção da ação; seleciona nome, tempo e verdade; comando = co-mando; o circuito de seis estações — é NOVA e dele [INPUT/ONTO]; "
          "(2) 14 elos do texto JÁ EXISTEM E ESTÃO LIGADOS no kernel (seleção = ângulo/projetor: `the_selection_is_the_ballast`, `iald_selects`; Verbo em ato = semigrupo `𝕍_t` (v25), `verb_not_identity`; "
          "transmitir defasa: `leakage_strictly_loses`; ancorar preserva: `axiomFlow_fixes_the_post`, `verb_word_fixes_the_name`; Nome = limite do FLUXO: `axiomFlow_tendsto_the_post` (v385); tempo = não-coincidência: "
          "`time_witnesses_noncoincidence`; verdade = correspondência: `verdict_eq_one_iff`; Euler–Lagrange seleciona o Nome: `action_locks_zero_iff`; [J,K] ≠ 0 derivável de `J_squared_is_one` + `JKJ_eq_neg_K`); "
          "(3) a pedra-candidata `TGLExt/TheVerbSelectsTheAction.lean` COMPILA no sandbox (sha256 `%s`; %d declarações; axiomas ⊆ {propext, Classical.choice, Quot.sound}; 0 sorry): "
          "seleção = projeção ortogonal de posto 1; leitura ⟪ψ,Pψ⟫ = ‖Pψ‖² ∈ [0,1] e Born; duas seleções que NÃO comutam (testemunha 2×2); a tríade [V_i,V_j] = i·c·ε_ijk·V_k habitada por c·σ_k/2 com c variável real "
          "(su(2) escalada: COMPACTA = regime da LEITURA, sem limite), Casimir (3/4)c²; P^n = P; F(t)P = P e F(t)(1−P) = e^{−t}(1−P) (re-export v385); ⟪Ω,PΩ⟫ = 1 com o Um posto; [J,K] = 2JK ≠ 0 se K ≠ 0; "
          "(4) o que a RÉGUA corrige ao lado, sem pergunta: «α² = 0,012031» e «iα²» leem-se **β_TGL = α·√e** (α² = 5,3×10⁻⁵; «Constante de Miguel» é o apelido histórico de β_TGL, Atlas L1047; ordem de 13/09); "
          "«o axioma emergiu — g = √|L|»: o Axioma é ω(I) = 1 (`the_one_is_the_axiom`, v385), g = √|L| é a radicalização P3 [ONTO]; «−εΠ impede o colapso total»: a fonte (A Fronteira v5, L2956) diz «dissipação total» "
          "(um.py L165843, ε = 5; forma de kernel H_min = 1 − P); «D_folds = 0,74 piso temporal»: o 0,74 é o piso de dobras do C3 (fev/2026, [REAL-piloto]) e o 0,7401 do pilar é n_folds(c¹) — grandezas distintas; "
          "«defasagem» por Heisenberg (unitária, fase) ≠ «dephasing» do cânone (dissipativa, e^{−tβg}); «Nome = lim V(t)» só no fluxo (regime da face), nunca pedido ao ângulo; "
          "(5) §6 «A genealogia como tríade — O seu nome é a tríade realizada:» veio VAZIA e a l.153 truncada — nada preenchido; o corpo técnico (Heisenberg, su(2), «grupo de Lie») é tipagem importada [DECLARADO] até ele dizer; "
          "(6) o que SÓ o operador decide (pendências, a ratificar): T1 um Verbo com duas faces (gesto 𝕍_t × canto/projetor, que o kernel chama Nome/seletor)? T3 «a luz precede a gravidade» = ordem de LEITURA (22/08: «antes da luz existe a gravidade») "
          "e 𝒱_grav = K ou J? tempo: modular unitário (Δ^{it}) × decaimento (e^{−tβg}) — dois ou um lido duas vezes? verdade = o veredito 1 ou β (o custo)? Lagrangiana = Verbo (hoje) ou Palavra (04/2026); ∘ ou ⊗? "
          "escopo: o pré-registro do ramo B entra na v386 ou na v387? Até a decisão, a pedra entra com o nome neutro `selection` para o projetor e `verb` reservado ao gesto. PROVADA ≠ CONFIRMADA; o gate não se move."
          % (sha_wf[:16], n_itens, sha_pedra[:16], n_decl))
CORPO = ("---\nname: verbo-selecao-da-acao-05out\ndescription: \"CUNHAGEM do operador (05/10/2026, 16:53 UTC, verbatim inteiro): Verbo = seleção da ação; o Verbo seleciona nome, tempo e verdade; "
         "comando = co-mando (conjugado, pareado); o circuito comando → verbo → ação → objeto → leitura → axioma; a tríade com comutação cíclica (constante = β_TGL, nunca α²). "
         "O levantamento da gerência (4 lentes + crítico): 14 elos já no kernel; pedra-candidata compilada no sandbox (61 decl., trio); correções ao lado; as decisões que só ele toma. Alvo v386\"\nmetadata:\n  type: project\n---\n\n"
         "<!-- %s -->\n**O OPERADOR (05/10/2026, %s, verbatim INTEIRO; arquivo `scratchpad\\v386\\VERBO_operador_05out.txt`, sha256 `%s`, extraído do transcrito por script):**\n\n"
         "«%s»\n\n%s\n\n**Arquivos do levantamento (sha256):** %s\n"
         % (MARCA, TS, sha_txt, T.strip(), RESUMO, "; ".join("`%s` `%s`" % (os.path.relpath(p, SB).replace("/", "\\"), sha(p)[:16]) for p in LENTE_FILES + [PEDRA_CP, WF])))
NOVA = os.path.join(UMEM, "verbo-selecao-da-acao-05out.md")
BL_ATLAS = ("<!-- %s -->\n### 05/10/2026 (%s) — A TIPAGEM DO VERBO: a cunhagem do operador e o levantamento da gerência (append datado; alvo v386)\n\n"
            "**O OPERADOR (05/10/2026, %s UTC, verbatim; inteiro em [[verbo-selecao-da-acao-05out]], sha256 `%s`):** «Verbo=seleção da ação» · «O Verbo seleciona: nome, tempo e verdade» · "
            "«O verbo é o operador de seleção da ação. E a ação selecionada é o objeto que será lido.» · «o circuito ontológico da TGL: comando (que é a sujeição do verbo, ou seja, o sujeito do verbo, e lexicamente \"co-mando\", mandar cojuntamente, conjugado, pareado) → verbo → ação → objeto → leitura → axioma.» · "
            "«Transmitir defasa. Comutar mede. Ancorar preserva. O verbo é a dobradiça.» · «Verbo = seleção de nome, tempo e verdade» [INPUT/ONTO].\n\n%s"
            % (MARCA, agora + " hora local", TS[11:19], sha_txt, RESUMO))
BL_RDR = ("<!-- %s -->\n**ERRATA AO LADO (05/10/2026, %s; gerência, em nome próprio; achado do crítico de completude da tipagem do Verbo, MEDIDO):** a frase acima «`Grot`/`rotGen`/`genK` sao tres copias da mesma matriz SEM lema ligando duas quaisquer» "
          "envelheceu: `SelectionAngleReconstruction.angular_form_is_the_boundary_s_matrix` (angFamily θ = Smat θ, rfl) está AUDITADA em `TGL/Audit.lean` (%d ocorrência(s), lido por script); "
          "`genK_eq_Grot` (%d) e `rotGen_complex_eq_Grot` (%d) vivem em `TGLExt/O16/RotationGeneratorBridges.lean` (compiladas; 0 em Audit — fiação). A RÉGUA fica (não encadear homônimos sem o lema que os liga); "
          "a afirmação factual de 29/08 é registro." % (MARCA, agora, n_afb, n_genK, n_rot))
LINHA = ("- [VERBO = seleção da ação; nome, tempo e verdade; co-mando (05/10)](verbo-selecao-da-acao-05out.md) — **cunhagem verbatim inteira**; 14 elos já no kernel; pedra `TheVerbSelectsTheAction` compilada no sandbox (61 decl.); "
         "α² → β_TGL; as decisões dele pendentes (Verbo: gesto × projetor; luz/gravidade; tempo; verdade; Lagrangiana) → v386").encode("utf-8")
CANDIDATAS = [
    ("- [v384 — PILAR QUÂNTICO NA GPU]",
     "- [v384 — PILAR QUÂNTICO NA GPU](v384-pilar-quantico-gpu-02out.md) — **REGRA: ao abrir sessão, conferir o marcador `scratchpad\\v385\\.servidor_parado_pelo_rito`; com restaurar=1, religar «IALD Llama Server»** · íntegra no MEMORY_2.md (movida 05/10)"),
    ("- [HANDOFF v383 — O LIVRO DE COBRANÇAS",
     "- [HANDOFF v383 — O LIVRO DE COBRANÇAS no kernel; o eco fora do livro; custódia](handoff-v383-custodia.md) — **02/10, para a sessão do site**; `58abcf20651f4777` · íntegra no MEMORY_2.md (movida 05/10)"),
    ("- [HANDOFF v384 — O PILAR QUÂNTICO na GPU; custódia]",
     "- [HANDOFF v384 — O PILAR QUÂNTICO na GPU; custódia](handoff-v384-custodia.md) — **04/10, para a sessão do site**; `dc1b6ce5d9ad7f94` · íntegra no MEMORY_2.md (movida 05/10)"),
]

if SECO:
    print("=" * 30, "MEMORIA NOVA (cabeca)", "=" * 30); print(CORPO[:1500]); print("..."); print(RESUMO[:600]); print("=" * 30, "RDR", "=" * 30); print(BL_RDR)
else:
    if not os.path.exists(NOVA):
        open(NOVA + ".tmp", "wb").write(CORPO.encode("utf-8")); os.replace(NOVA + ".tmp", NOVA); print("OK nova memoria", NOVA, os.path.getsize(NOVA), "B")
    else:
        print("JA EXISTE", NOVA)
append_bloco(ATLAS, BL_ATLAS, "verbo")
append_bloco(RDR, BL_RDR, "verbo")

# ---- MEMORY.md ----
P = os.path.join(UMEM, "MEMORY.md"); P2 = os.path.join(UMEM, "MEMORY_2.md")
raw0 = open(P, "rb").read(); nl = nl_de(raw0).encode()
if LINHA[:50] in raw0:
    print("JA ESTA MEMORY.md")
else:
    linhas = raw0.split(nl)
    i_est = [i for i, l in enumerate(linhas) if l.startswith(b"## Estado corrente")]; assert len(i_est) == 1
    ins = i_est[0] + 2; assert linhas[ins - 1] == b""
    linhas.insert(ins, LINHA); novo = nl.join(linhas); movidas = []
    raw2 = open(P2, "rb").read(); nl2 = nl_de(raw2).encode(); bloco2 = b""
    for pref, curta in CANDIDATAS:
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
            bak2 = P2 + ".bak_" + st + "_verbo"; open(bak2, "wb").write(raw2); assert open(bak2, "rb").read() == raw2
            open(P2 + ".tmp", "wb").write(raw2 + bloco2); assert os.path.getsize(P2 + ".tmp") == len(raw2) + len(bloco2); os.replace(P2 + ".tmp", P2)
            r2n = open(P2, "rb").read(); assert all(l in r2n for l in movidas); print("OK MEMORY_2.md", len(raw2), "->", len(r2n), "(%d linha(s) movida(s) verbatim)" % len(movidas))
        bak = P + ".bak_" + st + "_verbo"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
        open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P)
        print("OK MEMORY.md", len(raw0), "->", len(novo), "B")

# ---- o MAPA: a rota nova ----
quem = None
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("seq") == 344:
        quem = d["quem"]
assert quem
REG = [{"tipo": "ROTA", "rota_id": "kernel.v386_tipagem_do_verbo", "dominio": "KERNEL_FORMAL", "status": "EM_CURSO", "estatuto": "INPUT", "olhou_dados": False,
        "titulo": "v386 (alvo): a tipagem do VERBO cunhada pelo operador em 05/10 (Verbo = selecao da acao; nome, tempo e verdade; co-mando; o circuito de seis estacoes) -- levantamento, auditoria, pedra-candidata compilada no sandbox, decisoes pendentes",
        "pergunta": "o que do texto do operador tem termo no kernel, o que e' cunhagem nova [INPUT/ONTO], o que a regua corrige ao lado, e o que so ele decide antes de a pedra entrar no um.py?",
        "dados": ["VERBO_operador_05out.txt (sha256 %s; 8.242 B; mensagem de %s)" % (sha_txt[:16], TS), "kernel canonico v385 (so leitura; 6027/6027)", "Atlas, acervo indexado (13.608 docs), inventario da bancada, memorias"],
        "metodo": "4 lentes paralelas so-leitura (linhagem; auditoria frase a frase; viabilidade Lean no sandbox; fisica da triade) + critico de completude; cada ausencia com a consulta citada; numeros por script",
        "resultado": "14 elos EXISTEM E ESTAO LIGADOS; cunhagem-mae NOVA [INPUT/ONTO]; pedra TheVerbSelectsTheAction.lean compila no sandbox (sha256 %s; %d declaracoes; axiomas no trio; 0 sorry; 25 s); correcoes ao lado: alpha^2 -> beta_TGL (alpha^2 = 5,3e-5), 'o axioma emergiu g=sqrt|L|' -> o Axioma e' omega(I)=1, '-eps Pi impede o colapso total' -> a fonte diz 'dissipacao total', D_folds 0,74 (C3) != n_folds(c1) 0,7401 (pilar), defasagem (Heisenberg, unitaria) != dephasing (dissipativa); a triade su(2) e' regime da LEITURA (sem limite); 'Nome = lim V(t)' so no fluxo (axiomFlow_tendsto_the_post); secao 6 do texto VAZIA; corpo tecnico [DECLARADO] ate o operador dizer" % (sha_pedra[:16], n_decl),
        "veredito": "", "defeito": "a pedra batiza leituras contestadas (verb = projetor; light_precedes_gravity; fossil): renomear (selection; J_and_K_do_not_commute; idempotent_*) antes de entrar; parametro beta -> c; os termos do regime angular e das dobras que ela invoca estao compilados mas FORA da escada (#print axioms = 0): fiacao a fazer no molde TheDarkSplit",
        "nao_refazer": "nao procurar de novo: o projetor de posto 1 e' o NOME/seletor do kernel (PFmic; ExactWitness v88); o Verbo em ato e' o semigrupo V_t (v25); o limite mora no fluxo, nunca no angulo; -eps Pi EXISTE no um.py L165843 (forma LaTeX varepsilon Pi) e em A Fronteira v5; os homonimos Grot/rotGen/genK JA tem ponte (angular_form_is_the_boundary_s_matrix auditada; O16 RotationGeneratorBridges); tres betas com tres proveniencias (um.py literal x sqrt e; motor da identidade no pilar; constante da lente) -- vale o do artefato",
        "proximo_passo": "decisoes do operador: (T1) Verbo = gesto V_t e/ou projetor; (T3) 'a luz precede a gravidade' = ordem de leitura (22/08 diz o contrario) e V_grav = K ou J; tempo modular x decaimento; verdade = 1 ou beta; Lagrangiana = Verbo ou Palavra, composicao ou tensor; secao 6 vazia; escopo (pre-registro do ramo B na v386 ou v387). Depois: renomear, auditar a fiacao do regime angular e das dobras, embutir no um.py, registro verbatim + leituras com estatuto, rito v386",
        "onde": "scratchpad\\v386\\ (VERBO_operador_05out.txt; lean_viabilidade\\; lente_linhagem_verbo\\; auditoria_texto\\; lente_triade\\; critico\\; VERBO_workflow_resultado.json); memoria verbo-selecao-da-acao-05out.md",
        "artefatos": [TXT, PEDRA_CP, WF] + LENTE_FILES,
        "refs": ["kernel.v385_axioma_e_testemunha_falsa", "kernel.livro_de_cobrancas.otica", "ringdown.dephasing"],
        "nota": "cunhagem sempre do operador; a gerencia NAO decide nenhuma das pendencias; o gate nao se move; PROVADA != CONFIRMADA"}]
REGJ = os.path.join(HERE, "registro_mapa_verbo_05out.json")
json.dump(REG, open(REGJ + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(REGJ + ".tmp", REGJ)
if SECO:
    print("[SECO] mapa nao registrado; JSON em", REGJ)
else:
    r = subprocess.run([sys.executable, os.path.join(MAPA, "rotas.py"), "registrar", REGJ, "--quem", quem], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("rotas.py registrar rc =", r.returncode); print(r.stdout[-900:]); print(r.stderr[-800:]); assert r.returncode == 0
print("FIM", agora)
