# -*- coding: utf-8 -*-
r"""AUTO-AUDITORIA CETICA da RODADA 3 (redator da gerencia c1, em nome proprio). Mede, por script, e grava
5_R3\AUTO_AUDITORIA_R3.json:
 (a) ASPAS: toda citacao «...» nos COMENTARIOS da pedra r3 (e nos .md de 5_R3), classificada por fonte onde o texto esta,
     byte a byte (com quebra de linha normalizada para espaco): V1..V5 (verbatins do operador), um.py v391 (na linha
     citada ou em qualquer linha), kernel do Nos (todo .lean fora de .lake), relatorio final / pre-registro (textos da
     gerencia), ou NENHUMA (rotulo da propria pedra). Para cada «...» SEM fonte, confere o contexto (±240 caracteres):
     se o contexto atribui a frase ao operador (menciona V1..V5, «operador», «cunhagem», «verbatim»), e VIOLACAO.
 (b) um.py: toda citacao «um.py v391 (`8e7b9927ceae64b8`) l.NNNN» (ou l.NNNN–MMMM) confere o hash do um.py e a
     presenca, na linha citada dos BYTES, de um fragmento listado nesta tabela (fragmento <-> linha);
 (c) citacoes de linha do kernel (Arquivo.lean l.N / Arquivo:N) conferidas nos bytes do kernel do Nos (so leitura);
 (d) a palavra vedada pela regua (a 'confirmacao' em ingles maiusculo, como veredito) e sua forma portuguesa maiuscula
     em TODOS os artefatos de 5_R3 (fora toolchain/build/.olean); beta literal (os digitos de beta) em codigo e em texto;
 (e) NOMES: as 190 declaracoes de r3 com as palavras de peso no nome e, para cada uma, o que o enunciado diz (justificativa
     escrita aqui, lida contra o tipo impresso em TIPOS_R2_VS_R3.json);
 (f) o registro do mapa (registro_mapa_F1.FREQUENCIA_R3.json) contra os campos de `rotas.py modelo` (sem registrar).
Nao escreve fora de 5_R3; nada e executado do um.py (so bytes)."""
import hashlib, json, os, re, subprocess, sys, time

R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNID = os.path.dirname(R3)
WORK = os.path.dirname(UNID)
PEDRA = os.path.join(R3, "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
UMPY_SHA16 = "8e7b9927ceae64b8"
KERNEL = r"\\?\C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
VERB = {
    "V1": os.path.join(WORK, "cunhagens_12out", "OPERADOR_10out_posto_rank_texto_verbatim.txt"),
    "V2": os.path.join(WORK, "cunhagens_12out", "OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"),
    "V3": os.path.join(WORK, "cunhagens_10out", "OPERADOR_10out_posto_rank_verbatim.txt"),
    "V4": os.path.join(WORK, "cunhagens_10out", "OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"),
    "V5": os.path.join(WORK, "cunhagens_12out", "OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt"),
}
VERB_SHA16 = {"V1": "8d252f24e2806ff3", "V2": "2c8b7b712aa9ad7f", "V3": "5b9afcc691a0e1e4", "V4": "b365591ceb346cdf",
              "V5": "78ef70e6f9868281"}
GERENCIA = [os.path.join(UNID, "4_RELATORIO", "RELATORIO_FINAL.md"), os.path.join(UNID, "1_PREREGISTRO", "PREREGISTRO.md")]
# (b) fragmentos que TEM de estar na linha citada dos bytes do um.py
FRAG_UMPY = {
    6488: ["def fractal_dephasing_principle(ONE)"],
    6489: ["[CONJECTURE ontologica; ancoras REAL]"],
    6502: ["{Q,rho*}=0 EXATO so' em theta_M->0"],
    6512: ["P = np.array([[1.0, 0.0], [0.0, 0.0]])"],
    6513: ["omega_I = float(np.trace(P))"],
    6514: ["Q0 = np.eye(2) - P"],
    6515: ["limite inalcancavel"],
    6518: ["R = np.array([[c, -s], [s, c]])", "Qth = R @ Q0 @ R.T"],
    6526: ["Tudo = D_beta(F(1)) = VERDADE"],
}
# (c) citacoes de linha do kernel: (arquivo, linha, fragmento que tem de estar na linha)
KERNEL_LINHAS = [
    ("TGLExt/SMatrix.lean", 81, "theorem Smat_mul"),
    ("TGLExt/GlobalLiftLadder.lean", 219, "theorem dephased_rhoOut_zero_zero"),
    ("TGLExt/GlobalLiftLadder.lean", 228, "theorem dephased_rhoOut_one_one"),
    ("TGLExt/TheTraceIsNotErasable.lean", 96, "theorem dephase_preserves_trace"),
    ("TGLExt/CondExpect.lean", 114, "theorem trace_diagExpect"),
    ("TGLExt/CondExpect.lean", 87, "def diagExpect"),
    ("TGLExt/Ergodicity.lean", 184, "def dephase"),
    ("TGLExt/TheVerbSelectsTheAction.lean", 529, "theorem transmission_dephases"),
    ("TGLExt/TheAxiomAndTheFalseWitness.lean", 104, "def axiomFlow"),
    ("TGLExt/QuantumCollapseWitness.lean", 146, "theorem selective_branch_formula"),
    ("TGLExt/QuantumCollapseWitness.lean", 48, "def qubitReduction"),
    ("TGLExt/TheNameOperator.lean", 49, "def nameOp"),
]
VEDADA = re.compile(r"\bCONFIRMED\b")
VEDADA_PT = re.compile(r"\bCONFIRMAD[AO]S?\b")
BETA_LIT = re.compile(r"0[.,]0120313004008\d*")
PESO = ["unit", "atom", "name", "post", "attractor", "nothing", "transmission", "transmit", "truth", "cost", "fractal",
        "inscription", "nada", "verdade", "honest", "literal", "selective", "pole", "survives", "leak", "reading",
        "dephas"]
JUST = {  # nome -> o que o TERMO diz (lido contra o tipo impresso); «ok» = o nome nao afirma mais que o termo
    "rhoStar_unit": "Tr ρ* = 1 ∧ posto ρ* = 1 ∧ ρ*² = ρ* ∧ ρ*ᴴ = ρ*: «unit» = traço 1 e posto 1 do objeto ρ*; ok",
    "fractal_one_is_rank_one": "ρ_out θ tem posto 1, traço 1, idempotente, hermitiana, pureza 1: «fractal» é o nome [ONTO] de F_θ = Ad S(θ) (docstring); o termo só afirma posto 1 de F_θ(1); ok",
    "name_meets_rank_only_at_the_atom": "Tr ρ² = Tr ρ ⟺ posto P = 1 para ρ = P/posto P: «name» = Tr ρ (o nome, cego ao posto), «atom» = d = 1; ok",
    "normalized_projection_name": "Tr(P/d) = 1: «name» = o traço normalizado; ok",
    "normalized_projection_index": "Tr((P/d)²) = 1/d: «index» = a pureza; ok",
    "reading_returns_the_post": "⟨a,Xa⟩⁻¹ • (P X P) = P com P = |a⟩⟨a|: «post» = o projetor de posto 1 devolvido (homônimo de TheVerbSelectsTheAction.post, dito na docstring); nome mantido por ser resíduo do operador; ok",
    "selective_reading_of_half_identity": "Tr(ρ*·I/2) = 1/2 ∧ (Tr)⁻¹ • (ρ*·I/2·ρ*) = ρ*: «selective reading» = compressão por ρ* normalizada pelo peso; «half identity» = I/2 = halfId; sem peso emprestado; ok (RENOMEADA)",
    "reading_weights_are_truth_and_cost": "Tr(ρ*·diag(1−b,b)) = 1−b ∧ Tr(Q₀·diag(1−b,b)) = b: «truth/cost» são leituras [ONTO] das duas entradas (docstring); o termo só lê as entradas; nome herdado da rodada 1, não listado para esta rodada; ok com a ressalva da docstring",
    "zero_angle_pole": "Tr(ρ*Q₀) = 0 ∧ {Q₀,ρ*} = 0 ∧ ρ_out 0 = ρ* ∧ D_t(ρ_out 0) = ρ_out 0 ∧ posto ρ* = 1 ∧ Tr ρ*² = 1: «zero angle pole» = o polo θ = 0; sem «nada»; ok (RENOMEADA)",
    "axiomFlow_complement_decay_reexport": "axiomFlow P t * (1 − P) = e^{−t} • (1 − P): «axiomFlow», «complement» (1 − P), «decay» (e^{−t}), «reexport»; sem «transmissão»; ok (RENOMEADA)",
    "literal_transmission_does_not_force_dephasing": "¬ ∀ θ, |𝓣|² > 0 → D atua: «literal transmission» = a leitura literal |𝓣|² > 0; o termo é a negação; ok",
    "literal_leak_does_not_force_dephasing": "¬ ∀ θ, |𝓡|² > 0 → D atua: idem para o vazamento; ok",
    "dephasing_acts_iff_transmits_and_leaks": "D atua ⟺ |𝓣|² > 0 ∧ |𝓡|² > 0: «transmits» = |𝓣|² > 0, «leaks» = |𝓡|² > 0 (nomes dos pesos da matriz-S, SMatrix); ok",
    "transmission_without_dephasing_at_zero": "|𝓣(0)|² = 1 ∧ ¬ D atua em 0: «transmission» = |𝓣|²; ok",
    "leak_without_dephasing_at_half_pi": "|𝓡(π/2)|² = 1 ∧ ¬ D atua em π/2: «leak» = |𝓡|²; ok",
    "inscription_at_thetaMiguel": "D atua em θ_M ∧ (D_∞F(1))₁₁ = β: «inscription» é leitura [INPUT da gerência] (docstring); o termo é a conjunção; ok com a ressalva da docstring",
    "trace_survives_dephasing": "Tr D_∞F_θ(1) = Tr F_θ(1): «survives» = igualdade do traço; ok",
    "rank_not_preserved_by_dephasing": "¬ ∀ θ, posto D_∞F_θ(1) = posto F_θ(1) (com c : TGLCoupling supérflua, dita na docstring): ok",
    "leak_survives_dephasing": "Tr(ρ*·D_t Q_θ) = sin²θ ∀ t: «leak» = Tr(ρ*Q_θ); ok",
    "leak_eq": "Tr(ρ*·Q_θ) = sin²θ: ok", "leak_eq_rhoOut": "idem, lido em ρ_out: ok", "leak_eq_reflected_weight": "idem = |𝓡|²: ok",
    "leak_at_thetaMiguel": "Tr(ρ*·Q_θM) = β (identidade de θ_M := arcsin √β): ok",
    "leak_after_n_passes": "|𝓡|² após n passagens = sin²(nθ): ok", "leak_of_complement": "Tr(ρ*(1 − F_θ(1))) = sin²θ: ok",
    "angular_leak_no_limit": "sin θ ≠ 0 → ¬ ∃ L, sin²(nθ) → L: ok", "angular_leak_zero_converges": "sin θ = 0 → sin²(nθ) = 0 e → 0: ok",
    "angular_leak_zero_at_pi": "sin²(kπ) = 0: ok", "angular_reflected_weight_no_limit": "idem no peso refletido: ok",
    "compression_by_rank_one": "P X P = ⟨a,Xa⟩ P ∧ Tr(PX) = ⟨a,Xa⟩: ok", "compression_by_rank_one_literal": "idem com _ha sem peso (dito): ok",
    "reading_needs_weight": "controle C4: ok", "reading_needs_rank_one": "controle C5: ok",
    "reading_weights_at_theta": "Tr(ρ*·D_∞F) = |𝓣|² ∧ Tr(Q₀·D_∞F) = |𝓡|²: ok", "reading_weights_at_thetaMiguel": "idem em θ_M: ok",
    "nondiagonal_reader_sees_time": "controle C10: ok", "trace_one_not_rank_one": "controle C3: ok", "trace_one_not_rank_one'": "controle C3: ok",
    "psd_is_necessary": "controle C1: ok", "psd_is_necessary'": "controle C1: ok", "normalization_is_necessary": "controle C2: ok",
    "normalization_is_necessary'": "controle C2: ok", "nonunitary_changes_trace": "controle C6: ok", "singular_kills_rank": "controle C7: ok",
    "endpoint_rank_one_at_poles": "controle C8, os dois polos: ok", "zero_rate_no_dephasing": "controle C9: ok",
    "dephasing_has_limit": "re-exportação de dephase_tendsto_expectation: ok", "dephasing_trivial_iff": "∀ t D_t F = F ⟺ sin 2θ = 0: ok",
    "dephasing_trivial_at_thetaMiguel": "idem em θ_M(b): ok", "dephasingActs": "def ∃ t, D_t F ≠ F: ok", "dephasingActs_iff": "ok",
    "dephasingActs_iff_forward": "ok", "dephase_fixed_iff_neg": "ok", "dephased_rhoOut_eq": "ok", "dephased_det": "ok",
    "dephased_rank_two_iff": "ok", "dephased_rank_at_zero": "ok", "dephased_trace": "ok", "dephased_Qtheta_eq": "ok",
    "dephase_rhoStar": "ok", "dephase_Q0": "ok", "anticomm_dephased_eq": "ok", "anticomm_dephased_entry00": "ok",
    "anticomm_dephased_zero_iff": "ok", "anticomm_dephased_tendsto": "ok", "endpoint_purity": "ok",
    "probe_fixed_neg_both_sides": "sonda: ok", "probe_forward_both_sides": "sonda: ok", "probe_two_readings_of_Q": "sonda: ok",
    "rankOne_density": "ψ ≠ 0 → posto |ψ⟩⟨ψ| = 1: ok", "rankOne_density_normalized": "ok", "pure_iff_rank_one": "ok", "pure_iff_idempotent": "ok",
    "normalized_projection_literal": "forma literal de P4 (P² = P = Pᴴ, d ≥ 1): as quatro conclusões; _hH sem peso, dito na docstring: ok",
    "unitRates": "def g i j = if i = j then 0 else 1: «unit» = taxas de valor 1 (unitárias), não a unidade ρ*: ok",
    "unitRates_spec": "g_ii = 0 ∧ 0 < g 0 1 ∧ 0 < g 1 0 para as taxas unitárias: ok",
    "probe_name_rank_both_sides": "sonda P4: os dois lados de name_meets_rank_only_at_the_atom (ρ*: igual; 1 em M₂: diferente): «name» = Tr ρ: ok",
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def norm(s):
    return re.sub(r"[ \t\n]+", " ", s).strip()


t0 = time.time()
out = {"documento": "AUTO-AUDITORIA CETICA — RODADA 3 — TheUnitIsTheRank — 13/10/2026", "quando_local": time.strftime("%Y-%m-%d %H:%M:%S")}
pedra = open(PEDRA, "rb").read()
out["pedra_r3"] = {"arquivo": PEDRA, "bytes": len(pedra), "sha256": sha(PEDRA)}
ped = pedra.decode("utf-8")

# fontes
fontes = {}
for k, p in VERB.items():
    b = open(p, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    if h[:16] != VERB_SHA16[k]:
        raise SystemExit("FALHA VISIVEL: %s nao confere: %s" % (k, h[:16]))
    fontes[k] = norm(b.decode("utf-8"))
out["verbatins"] = {k: {"arquivo": VERB[k], "sha16": VERB_SHA16[k], "confere": True} for k in VERB}
umb = open(UMPY, "rb").read()
umh = hashlib.sha256(umb).hexdigest()
if umh[:16] != UMPY_SHA16:
    raise SystemExit("FALHA VISIVEL: um.py nao e a v391 esperada: " + umh[:16])
um_lines = umb.split(b"\n")
um_norm = norm(umb.decode("utf-8", "replace"))
ger = norm("\n".join(open(p, encoding="utf-8").read() for p in GERENCIA))
kern = []
for dp, dns, fns in os.walk(KERNEL):
    if ".lake" in dp.split(os.sep):
        continue
    for fn in fns:
        if fn.endswith(".lean"):
            kern.append(open(os.path.join(dp, fn), "rb").read().decode("utf-8", "replace"))
kern_norm = norm("\n".join(kern))
out["kernel_lean_lidos"] = len(kern)

# (a) aspas
ATRIB = re.compile(r"V[1-5]\b|operador|cunhagem|verbatim", re.I)


def classificar_aspas(texto, rotulo):
    itens = []
    for m in re.finditer(r"«([^«»]*)»", texto):
        q = norm(m.group(1))
        if not q:
            continue
        # «…» marca elisao: os fragmentos tem de estar TODOS na mesma fonte, nesta ordem (como em CITACOES_R2.json)
        frags = [norm(f) for f in q.split("…") if norm(f)]

        def esta(f_norm):
            pos = 0
            for fr in frags:
                i = f_norm.find(fr, pos)
                if i < 0:
                    return False
                pos = i + len(fr)
            return True
        onde = []
        for k, f in fontes.items():
            if esta(f):
                onde.append(k)
        if esta(um_norm):
            onde.append("um.py")
        if esta(kern_norm):
            onde.append("kernel")
        if esta(ger):
            onde.append("gerencia(relatorio/preregistro)")
        ctx = texto[max(0, m.start() - 240):m.end() + 240]
        atrib = bool(ATRIB.search(ctx))
        viol = (not any(o in ("V1", "V2", "V3", "V4", "V5") for o in onde)) and atrib and \
            not re.search(r"rótulo|renderizad|paráfrase|forma ASCII|lê-se|leitura|rotulo|nao e citacao|não é citação", ctx, re.I)
        itens.append({"aspas": m.group(1), "fontes": onde, "contexto_atribui": atrib,
                      "classe": ("VERBATIM_OPERADOR" if any(o.startswith("V") for o in onde) else
                                 "um.py" if "um.py" in onde else "kernel" if "kernel" in onde else
                                 "gerencia" if onde else "ROTULO_DA_PEDRA"),
                      "VIOLACAO_candidata": viol, "linha": texto.count("\n", 0, m.start()) + 1})
    return itens


asp = classificar_aspas(ped, "pedra")
out["aspas_pedra"] = {"n": len(asp), "por_classe": {}, "itens": asp}
for it in asp:
    out["aspas_pedra"]["por_classe"][it["classe"]] = out["aspas_pedra"]["por_classe"].get(it["classe"], 0) + 1
out["aspas_pedra"]["violacoes_candidatas"] = [it for it in asp if it["VIOLACAO_candidata"]]
mds = {}
for fn in ("RESULTADO_R3.md", "ADENDO_PREREGISTRO_ADITIVO_R3.md", "TABELA_R2_R3.md"):
    p = os.path.join(R3, fn)
    if os.path.exists(p):
        a = classificar_aspas(open(p, encoding="utf-8").read(), fn)
        mds[fn] = {"n": len(a), "violacoes_candidatas": [it for it in a if it["VIOLACAO_candidata"]],
                   "sem_fonte": [it["aspas"] for it in a if it["classe"] == "ROTULO_DA_PEDRA"]}
out["aspas_md"] = mds

# (b) um.py
cit = []
for m in re.finditer(r"um\.py v391 \(`" + UMPY_SHA16 + r"`\)[^\n]*?l\.(\d{4})(?:[–-](\d{4}))?", ped):
    a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
    for ln in range(a, b + 1):
        linha = um_lines[ln - 1].decode("utf-8", "replace")
        frags = FRAG_UMPY.get(ln)
        ok = frags is not None and all(f in linha for f in frags)
        # o fragmento tambem tem de estar no texto da pedra (perto da citacao ou em qualquer lugar)
        na_pedra = frags is not None and all(f in ped for f in frags)
        cit.append({"linha": ln, "fragmentos_esperados": frags, "na_linha_dos_bytes": ok, "fragmento_na_pedra": na_pedra,
                    "linha_bytes_inicio": linha.strip()[:100], "pos_pedra_linha": ped.count("\n", 0, m.start()) + 1})
sem_versao = [ped[p - 30:p + 40] for p in [m.start() for m in re.finditer(r"um\.py", ped)]
              if not ped.startswith("um.py v391 (`" + UMPY_SHA16 + "`)", p)]
out["citacoes_um_py"] = {"um_py_sha256": umh, "um_py_bytes": len(umb), "n_citacoes_de_linha": len(cit),
                         "linhas": sorted(set(c["linha"] for c in cit)),
                         "todas_conferem_nos_bytes": all(c["na_linha_dos_bytes"] and c["fragmento_na_pedra"] for c in cit),
                         "ocorrencias_sem_versao_hash": sem_versao, "itens": cit}

# (c) kernel linhas
kl = []
for rel, ln, frag in KERNEL_LINHAS:
    p = os.path.join(KERNEL, rel.replace("/", os.sep))
    linhas = open(p, "rb").read().decode("utf-8", "replace").split("\n")
    ok = ln <= len(linhas) and frag in linhas[ln - 1]
    citada = (("%s:%d" % (rel.split("/")[-1].replace(".lean", ""), ln)) in ped) or \
             (("%s l.%d" % (rel.split("/")[-1], ln)) in ped) or (("%s, l.%d" % (rel.split("/")[-1], ln)) in ped)
    kl.append({"arquivo": rel, "linha": ln, "fragmento": frag, "confere_nos_bytes": ok, "citada_na_pedra_r3": citada})
out["citacoes_kernel"] = {"todas_conferem": all(x["confere_nos_bytes"] for x in kl), "itens": kl}

# (d) palavra vedada e beta literal em TODOS os artefatos de 5_R3
ved, blit_cod, blit_txt, arts = [], [], [], {}
for dp, dns, fns in os.walk(R3):
    dns[:] = [d for d in dns if d not in ("toolchain_v4.31.0", "build")]
    for fn in fns:
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, R3)
        if fn.endswith(".olean"):
            arts[rel] = {"bytes": os.path.getsize(p), "sha256": sha(p)}
            continue
        t = open(p, "rb").read().decode("utf-8", "replace")
        arts[rel] = {"bytes": os.path.getsize(p), "sha256": sha(p)}
        for i, l in enumerate(t.split("\n"), 1):
            if VEDADA.search(l) or VEDADA_PT.search(l):
                ved.append([rel, i, l.strip()[:100]])
            if BETA_LIT.search(l):
                (blit_cod if fn.endswith((".py", ".lean")) else blit_txt).append([rel, i])
out["palavra_vedada"] = ved
out["beta_literal_em_codigo"] = blit_cod
out["beta_literal_em_texto"] = blit_txt
out["artefatos_5_R3"] = arts

# (e) nomes
decl = re.findall(r"^(?:theorem|def|noncomputable def) ([A-Za-z0-9_']+)", ped, flags=re.M)
tip = {}
tp = os.path.join(R3, "TIPOS_R2_VS_R3.json")
if os.path.exists(tp):
    for x in json.load(open(tp, encoding="utf-8"))["tabela"]:
        tip[x["r3"]] = x["tipo"]
nomes = []
for n in decl:
    pes = [w for w in PESO if w in n.lower()]
    nomes.append({"nome": n, "palavras_de_peso": pes, "justificativa": JUST.get(n, "ok (nome descritivo da conta)" if not pes else "SEM JUSTIFICATIVA ESCRITA"),
                  "tipo": tip.get(n, "")[:300]})
out["nomes"] = {"n": len(decl), "com_peso": sum(1 for x in nomes if x["palavras_de_peso"]),
                "sem_justificativa": [x["nome"] for x in nomes if x["justificativa"] == "SEM JUSTIFICATIVA ESCRITA"],
                "nomes_antigos_no_codigo": [a for a in ("nothing_branch", "reading_of_the_attractor_state", "transmission_dephases_reexport")
                                            if re.search(r"^(?:theorem|def) " + a + r"\b", ped, flags=re.M)],
                "itens": nomes}

# (f) registro do mapa
reg = {}
rp = os.path.join(R3, "registro_mapa_F1.FREQUENCIA_R3.json")
if os.path.exists(rp):
    modelo = json.loads(subprocess.run([sys.executable, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "modelo"],
                                       capture_output=True, text=True, encoding="utf-8").stdout)
    d = json.load(open(rp, encoding="utf-8"))
    reg = {"tipo": d.get("tipo"), "rota_id": d.get("rota_id"),
           "campos_faltando_do_modelo": sorted(set(modelo) - set(d) - {"corrige"}),
           "campos_fora_do_modelo": sorted(set(d) - set(modelo)),
           "artefatos_sao_lista_de_caminhos_existentes": isinstance(d.get("artefatos"), list) and
           all(isinstance(a, str) and os.path.exists(a) for a in d["artefatos"]), "n_artefatos": len(d.get("artefatos", []))}
out["registro_mapa"] = reg

problemas = []
if out["aspas_pedra"]["violacoes_candidatas"]:
    problemas.append("aspas atribuidas sem fonte na pedra")
if any(v["violacoes_candidatas"] for v in mds.values()):
    problemas.append("aspas atribuidas sem fonte em .md")
if not out["citacoes_um_py"]["todas_conferem_nos_bytes"] or sem_versao:
    problemas.append("citacao do um.py nao confere")
if not out["citacoes_kernel"]["todas_conferem"]:
    problemas.append("citacao de linha do kernel nao confere")
if ved:
    problemas.append("palavra vedada")
if blit_cod:
    problemas.append("beta literal em codigo")
if out["nomes"]["sem_justificativa"] or out["nomes"]["nomes_antigos_no_codigo"] or out["nomes"]["n"] != 190:
    problemas.append("nomes")
if reg and (reg["campos_faltando_do_modelo"] or reg["campos_fora_do_modelo"] or not reg["artefatos_sao_lista_de_caminhos_existentes"]):
    problemas.append("registro do mapa")
out["problemas"] = problemas
out["veredito"] = "LIMPO" if not problemas else "FALHA_VISIVEL: " + "; ".join(problemas)
out["segundos"] = round(time.time() - t0, 1)
dst = os.path.join(R3, "AUTO_AUDITORIA_R3.json")
tmp = dst + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
os.replace(tmp, dst)
res = {k: out[k] for k in ("veredito", "problemas", "palavra_vedada", "beta_literal_em_codigo", "beta_literal_em_texto", "registro_mapa")}
res["aspas_pedra"] = {k: v for k, v in out["aspas_pedra"].items() if k != "itens"}
res["aspas_md"] = {k: {kk: vv for kk, vv in v.items()} for k, v in mds.items()}
res["citacoes_um_py"] = {k: v for k, v in out["citacoes_um_py"].items() if k != "itens"}
res["citacoes_kernel"] = out["citacoes_kernel"]
res["nomes"] = {k: v for k, v in out["nomes"].items() if k != "itens"}
print(json.dumps(res, ensure_ascii=False, indent=1))
