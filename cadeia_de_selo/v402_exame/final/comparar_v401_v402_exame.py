# -*- coding: utf-8 -*-
"""comparar_v401_v402_exame.py -- exame final v402 (examinador final unico, 27/10/2026): comparacao ESTRUTURAL (AST/literal_eval) entre a v401
selada (A = copia base_v401, sha conferido) e o candidato v402 (B). Molde: comparar_v398_v399_exame.py. So' le; escreve so' o json de saida. A palavra proibida da regua e' montada por codigo de caractere.
uso: python -I -B -X utf8 comparar_v395_v396_exame.py <A.py> <B.py> <saida.json> <diff_normal.txt>"""
import ast, json, re, sys, hashlib, difflib, os
A_, B_, S_ = sys.argv[1:4]
NOSK = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
sa, sb = open(A_, "rb").read().decode("utf-8"), open(B_, "rb").read().decode("utf-8")
TA, TB = ast.parse(sa), ast.parse(sb)
def top(T):
    d, anon = {}, []
    for n in T.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): d[n.targets[0].id] = n
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name): d[n.target.id] = n
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): d[n.name] = n
        else: anon.append(ast.unparse(n))
    return d, anon
(dA, anA), (dB, anB) = top(TA), top(TB)
lit = lambda d, k: ast.literal_eval(d[k].value)
R = {}
dump = {}
def dmp(d, k):
    if k not in dump:
        dump[k] = ast.dump(d[k])
    return dump[k]
mud = sorted(k for k in dA if k in dB and ast.dump(dA[k]) != ast.dump(dB[k]))
R["nos"] = {"n_A": len(dA), "n_B": len(dB), "mudados": mud, "novos": sorted(set(dB) - set(dA)), "removidos": sorted(set(dA) - set(dB)),
            "anonimos_so_A": [s[:200] for s in anA if s not in anB], "anonimos_so_B": [s[:300] for s in anB if s not in anA]}
AUX = re.compile(r"^(_proof_\d+(_\d+)*|_simp_\d+(_\d+)*|match_\d+|_sunfold|eq_\d+|eq_def|congr_simp)$")
fa, fb = lit(dA, "_LEAN_THEOREM_FLAGS"), lit(dB, "_LEAN_THEOREM_FLAGS")
add = {k: v for k, v in fb.items() if k not in fa}
R["bandeiras"] = {"n_A": len(fa), "n_B": len(fb), "removidas": sorted(set(fa) - set(fb)), "mudadas": [k for k in fa if k in fb and fa[k] != fb[k]],
                  "acrescentadas": len(add), "prefixos": sorted(set(re.sub(r"_\d+$", "", k) for k in add)),
                  "acrescentadas_auxiliares": sorted(v for v in add.values() if AUX.match(v.split(".")[-1])),
                  "acrescentadas_fora_das_pedras": sorted(v for v in add.values() if not v.startswith(("TGLExt.PonteDaEscalaDual.", "TGLExt.QuedaSemGeometria.", "TGLExt.EsperancaCondicional."))),
                  "acrescentadas_por_pedra": {p: sum(1 for v in add.values() if v.startswith("TGLExt.%s." % p)) for p in ("PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional")},
                  "nomes_novos_repetidos": len(add) - len(set(add.values())), "nome_novo_ja_tinha_bandeira": sorted(set(add.values()) & set(fa.values()))}
def escada(T):
    for n in T.body:
        if isinstance(n, ast.FunctionDef) and n.name == "prove_external_ladder":
            for m in ast.walk(n):
                if isinstance(m, (ast.List, ast.Tuple, ast.Set)) and len(m.elts) > 1000 and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in m.elts):
                    return [e.value for e in m.elts]
la, lb = escada(TA), escada(TB)
R["escada"] = {"n_A": len(la), "n_B": len(lb), "B_igual_A_mais_novas": set(lb) == set(la) | set(add), "A_contida_em_B": set(la) <= set(lb), "sem_repetidos_B": len(lb) == len(set(lb))}
# prove_external_ladder sem a lista grande
def sem_lista(fn):
    fn = ast.parse(ast.unparse(fn)).body[0]
    for m in ast.walk(fn):
        if isinstance(m, (ast.List, ast.Tuple, ast.Set)) and len(m.elts) > 1000:
            m.elts = [ast.Constant("<LISTA %d>" % len(m.elts))]
    return ast.unparse(fn).splitlines()
dd = [l for l in difflib.unified_diff(sem_lista(dA["prove_external_ladder"]), sem_lista(dB["prove_external_ladder"]), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
R["prove_external_ladder_fora_da_lista"] = dd[:20]
for c in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V401_FALSIDADE_CONTRACT"):
    a, b = lit(dA, c), lit(dB, c)
    R[c] = {k: {"A": a.get(k) if not isinstance(a.get(k), (list, dict)) else "len %d" % len(a.get(k)), "B": b.get(k) if not isinstance(b.get(k), (list, dict)) else "len %d" % len(b.get(k))} for k in set(a) | set(b) if a.get(k) != b.get(k)}
def specs_diff(nome_lista):
    sA, sB = {s["nome"]: s for s in lit(dA, nome_lista)}, {s["nome"]: s for s in lit(dB, nome_lista)}
    out = {}
    for n in sorted(set(sA) | set(sB)):
        a, b = sA.get(n), sB.get(n)
        if a == b: continue
        if a is None or b is None: out[n] = "so_A" if b is None else "so_B"; continue
        ca, cb = {c["id"]: c for c in a.get("checks", [])}, {c["id"]: c for c in b.get("checks", [])}
        sv = lambda v: ("dict(%d)" % len(v)) if isinstance(v, dict) else v
        out[n] = {"checks_mudados": {i: {"A": [ca[i].get("op"), sv(ca[i].get("valor"))], "B": [cb[i].get("op"), sv(cb[i].get("valor"))], "outras": sorted(k for k in set(ca[i]) | set(cb[i]) if k not in ("op", "valor") and ca[i].get(k) != cb[i].get(k))} for i in ca if i in cb and ca[i] != cb[i]},
                  "checks_novos": sorted(set(cb) - set(ca)), "checks_removidos": sorted(set(ca) - set(cb)), "outras_chaves": sorted(k for k in set(a) | set(b) if k != "checks" and a.get(k) != b.get(k)),
                  "erratas_B_novas": [e for e in (b.get("erratas") or []) if e not in (a.get("erratas") or [])]}
    return out
for nm in ("_V392_SPECS", "_V393_SPECS", "_V394_SPECS", "_V395_SPECS", "_V396_SPECS", "_V397_SPECS", "_V398_SPECS", "_V399_SPECS", "_V401_SPECS"):
    if nm in dA and nm in dB:
        R["specs_%s_mudados" % nm] = specs_diff(nm)
sp6 = {s["nome"]: s for s in lit(dB, "_V402_SPECS")}
R["v402_specs"] = {n: [(c.get("id"), c.get("onde"), c.get("caminho"), c.get("op"), ("dict(%d)" % len(c["valor"])) if isinstance(c.get("valor"), dict) else (c.get("valor") if not isinstance(c.get("valor"), (list, str)) or len(str(c.get("valor"))) < 120 else str(c.get("valor"))[:120])) for c in s.get("checks", [])] for n, s in sp6.items()}
kh6 = sp6.get("kh_n1_cobertura_v402") or {}
pin = next((c["valor"] for c in kh6.get("checks", []) if isinstance(c.get("valor"), dict) and c.get("caminho") == ["formal_files_sha256"]), None)
embB = lit(dB, "_EMBEDDED_KERNEL_FILES"); embA = lit(dA, "_EMBEDDED_KERNEL_FILES")
alvo = {rel: hashlib.sha256(c.encode("utf-8")).hexdigest() for rel, c in embB.items()}
for f in ("_check_damming.lean",):
    p = os.path.join(NOSK, f)
    if os.path.exists(p): alvo[f] = hashlib.sha256(open(p, "rb").read()).hexdigest()
R["h8_v402"] = {"n_pino": len(pin) if pin else None, "pino_igual_embutidos_mais_residual": pin == alvo if pin else None, "difere": sorted(k for k in set(pin or {}) | set(alvo) if (pin or {}).get(k) != alvo.get(k))[:10]}
R["_EMBEDDED_KERNEL_FILES"] = {"n_A": len(embA), "n_B": len(embB), "novos": sorted(set(embB) - set(embA)), "removidos": sorted(set(embA) - set(embB)), "mudados": sorted(k for k in embA if k in embB and embA[k] != embB[k])}
for k in R["_EMBEDDED_KERNEL_FILES"]["mudados"]:
    R["_EMBEDDED_KERNEL_FILES"]["diff_" + k] = [l for l in difflib.unified_diff(embA[k].splitlines(), embB[k].splitlines(), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))][:10]
R["pedras_sha16_embutidas"] = {k: hashlib.sha256(embB.get(k, "").encode("utf-8")).hexdigest()[:16] for k in ("TGLExt/PonteDaEscalaDual.lean", "TGLExt/QuedaSemGeometria.lean", "TGLExt/EsperancaCondicional.lean")}
R["_ESQUELETO_STONES_so_B"] = [list(x) for x in lit(dB, "_ESQUELETO_STONES") if tuple(x) not in set(map(tuple, lit(dA, "_ESQUELETO_STONES")))]
R["_ESQUELETO_STONES_so_A"] = [list(x) for x in lit(dA, "_ESQUELETO_STONES") if tuple(x) not in set(map(tuple, lit(dB, "_ESQUELETO_STONES")))]
for f in ("build_pt", "build_en", "emit_canonical_md", "main", "_unified_main"):
    a, b = ast.unparse(dA[f]).splitlines(), ast.unparse(dB[f]).splitlines()
    dd = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    R["diff_" + f] = {"removidas": [l[:400] for l in dd if l.startswith("-")][:30], "n_acrescentadas": sum(1 for l in dd if l.startswith("+")), "n_removidas": sum(1 for l in dd if l.startswith("-")),
                      "acrescentadas_amostra": [l[:300] for l in dd if l.startswith("+")][:8]}
# colisoes de chave das fontes/falas
def keys(name, T):
    for n in T.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", None) == name:
            return set(ast.literal_eval(n.value).keys())
    return set()
NF = ("392", "393", "394", "395", "396", "397", "398", "399", "401")
FB = {nm: keys(nm, TB) for nm in ["_V%s_FONTES" % v for v in NF + ("402",)] + ["_V%s_VERBATINS2" % v for v in NF + ("402",)]}
R["colisoes_v402"] = {"fontes": sorted(FB["_V402_FONTES"] & set().union(*[FB["_V%s_FONTES" % v] for v in NF])), "falas": sorted(FB["_V402_VERBATINS2"] & set().union(*[FB["_V%s_VERBATINS2" % v] for v in NF]))}
# quem cita diagFlow / TheGreatAttractor fora do kernel embutido e das bandeiras
def cita(d, pat):
    out = []
    for k, n in d.items():
        if k in ("_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "prove_external_ladder"):
            continue
        s = ast.unparse(n) if k not in ("main",) else ast.unparse(n)
        if re.search(pat, s):
            out.append(k)
    return sorted(out)
R["cita_diagFlow_A"], R["cita_diagFlow_B"] = cita(dA, r"diagFlow"), cita(dB, r"diagFlow")
R["cita_TheGreatAttractor_A"], R["cita_TheGreatAttractor_B"] = cita(dA, r"TheGreatAttractor"), cita(dB, r"TheGreatAttractor")
# os nos MUDADOS: so' os declarados?
decl = {"UM_VERSION", "_EMBEDDED_KERNEL_FILES", "_ESQUELETO_STONES", "_LEAN_THEOREM_FLAGS", "_V394_FORMAL_CONTRACT", "_V394_NETWORK_CONTRACT", "_V394_QUADRATIC_CONTRACT",
        "_V395_PSIBIT_CONTRACT", "_V401_SPECS", "_V401_FALSIDADE_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V398_SONICO_CONTRACT", "build_en", "build_pt", "emit_canonical_md", "main", "prove_external_ladder"}
R["novos_declarados"] = sorted(set(dB) - set(dA)) == sorted(["_V402_CONTRACTS", "_V402_FONTES", "_V402_NOMES_REGISTROS", "_V402_RECUSA", "_V402_SPECS", "_V402_TEXTS", "_V402_VERBATINS2", "_v402_close", "_v402_formal", "_v402_registro", "_v402_rodar_specs", "esperanca_condicional_v402", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "v402_esperanca_mechanics", "v402_ponte_mechanics", "v402_queda_mechanics"])
R["n_funcoes_A_iguais"] = sum(1 for k, n in dA.items() if isinstance(n, ast.FunctionDef) and k in dB and k not in mud)
R["n_dados_A_iguais"] = sum(1 for k, n in dA.items() if not isinstance(n, (ast.FunctionDef, ast.ClassDef)) and k in dB and k not in mud)
R["mudados_nao_declarados"] = sorted(set(mud) - decl)
R["declarados_nao_mudados"] = sorted(decl - set(mud))
# funcoes seladas que mudaram (qualquer FunctionDef de A mudado)
R["funcoes_mudadas"] = sorted(k for k in mud if isinstance(dA[k], ast.FunctionDef))
# varredura das linhas novas (fora do corpo do kernel embutido): literais de beta/alfa/sqrt(e), palavra proibida, atribuicoes ao gate
lb_ = sb.splitlines()
novas = []
for hl in open(sys.argv[4], encoding="utf-8", errors="replace").read().splitlines():   # o diff normal do GNU diff (A -> B)
    m_ = re.fullmatch(r"(\d+)(?:,(\d+))?([acd])(\d+)(?:,(\d+))?", hl)
    if m_ and m_.group(3) in "ac":
        j1, j2 = int(m_.group(4)), int(m_.group(5) or m_.group(4))
        novas += [(j, lb_[j - 1]) for j in range(j1, j2 + 1)]
emb_ini = dB["_EMBEDDED_KERNEL_FILES"].lineno; emb_fim = dB["_EMBEDDED_KERNEL_FILES"].end_lineno
fora = [(n, l) for n, l in novas if not (emb_ini <= n <= emb_fim)]
pal = "".join(chr(c) for c in (67, 79, 78, 70, 73, 82, 77, 69, 68))
pats = {"beta_literal": r"0[.,]0120\d|1[.,]203\d*e-0?2|0[.,]01203", "alfa_literal": r"0[.,]00729\d|7[.,]2973\d*e-0?3|137[.,]0359", "sqrt_e_literal": r"1[.,]64872\d",
        "palavra": r"(?<!NOT_)(?<!UN)" + pal, "palavra_ci": "(?i)" + pal[:7], "PROVED_BY": r"(?<!AP)PROVED_BY", "TGL_PROVED": "TGL_PROVED", "CONSC": "CONSCIOUSNESS_PROVED",
        "gate_atribuido": r"core\[\s*['\"]qg_closure['\"]\s*\]\s*=|qg_closure_verdict['\"]?\s*\]?\s*=(?!=)|prove_qg_closure_gate\("}
R["varredura_linhas_novas"] = {"n_novas_total": len(novas), "n_novas_fora_do_kernel": len(fora), "hits": {k: [(n, l.strip()[:200]) for n, l in fora if re.search(p, l)][:12] for k, p in pats.items()}}
R["varredura_linhas_novas"]["hits_n"] = {k: len(v) for k, v in R["varredura_linhas_novas"]["hits"].items()}
# o gate: a funcao do gate e as do veredito iguais?
for f in ("prove_qg_closure_gate", "prove_qg_closure", "selftest_fail_closed", "verify_tgl_kernel_formalization", "parse_lean_axioms_v394", "parse_lean_provenance_v394", "_v392_axiom_coverage",
          "prove_the_iald_index", "sha256_directory", "_v392_registro", "_v392_guarda_texto", "psibit_v395", "_v395_rodar_specs", "_v394_rodar_specs", "testemunha_estatica_v396", "_v396_rodar_specs", "hubble_ratio_opening_v388", "v396_static_witness_mechanics", "rede_fock_v394", "regra_quadratica_v394", "tempo_frequencia_v394",
          "_v397_rodar_specs", "_v397_quadro_tex", "_v397_quadro_md", "_v397_atomos", "_v397_linha_de_maquina", "_v397_fmt", "_v397_num", "_v394_rodar_specs",
          "sonico_v398", "afinacao_das_cordas_v398", "v398_sonico_mechanics", "v398_afinacao_mechanics", "_v398_formal", "_v398_beta", "_v398_h2", "_v398_bernoulli", "_v398_bernoulli_poly", "_v398_rodar_specs",
          "selo_acom_v399", "declaracao_do_operador_v399", "registro_core_v399", "_beta_runtime", "_theta_m_runtime", "selar", "controles_negativos", "conferir_bloco_embutido", "resumos_do_selo_v399", "selo_acom_sidecar_v399", "sidecar", "_v399_rodar_specs", "_v376_same_alpha_literal",
          "falsidade_da_inercia_v401", "_v401_rodar_specs", "_v401_registro", "_v401_formal", "_v400_rodar_specs", "parse_lean_axioms", "verify_lean_kernel", "selo_acom_sidecar_v399"):
    if f in dA and f in dB:
        R.setdefault("funcoes_seladas_iguais", {})[f] = ast.dump(dA[f]) == ast.dump(dB[f])
for f in ("_V397_VERACIDADE_SPEC", "_V397_FONTES", "_V397_VERBATINS2", "_V397_FRASE_444", "_V397_CHAVES_NUM", "_V396_SPECS", "_V395_SPECS", "_V394_SPECS", "_V393_SPECS", "_V392_SPECS", "_V392_FONTES", "_V392_VERBATINS2", "_V398_VERBATINS2", "_V398_FONTES", "_V398_SONICO_TEXT", "_V398_AFINACAO_TEXT", "_V397_SPECS", "_V398_SPECS", "_V399_FONTES", "_V399_VERBATINS2", "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256", "ACOM_PROVENIENCIA", "PERFIL_ID", "CENTRO", "_V401_FONTES", "_V401_VERBATINS2", "_V401_TEXTS", "_V401_RECUSA", "_V401_CONTRACTS", "_V400_SPECS", "_V400_FONTES", "_V400_VERBATINS2"):
    if f in dA and f in dB:
        R.setdefault("dados_selados_iguais", {})[f] = ast.dump(dA[f]) == ast.dump(dB[f])
json.dump(R, open(S_, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str)[:30000])
