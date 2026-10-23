# -*- coding: utf-8 -*-
"""p00_precondicoes_v397.py -- confere, SO LENDO, as pre-condicoes de bytes da v397 ANTES de instalar. Nada e escrito fora de PRECONDICOES_v397.json (nesta pasta). Os pinos sao LIDOS do selo/core/arquivos,
nunca digitados. Fail-closed: rc 1 se algo falha. Molde: p00_precondicoes_v396.py. uso: python -I -B -X utf8 p00_precondicoes_v397.py"""
import ast, glob, hashlib, json, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v397 as DL  # noqa: E402
C = "C:" + os.sep
NOS = DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
KS = DL.SANDBOX; KA = DL.ARVORE; KDIR = os.path.join(HERE, DL.KERNEL_DIR); BB = os.path.join(HERE, DL.BASE_DIR)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
res = []; ok_all = True


def chk(nome, cond, det=None):
    global ok_all
    res.append({"checagem": nome, "ok": bool(cond), "detalhe": det}); ok_all = ok_all and bool(cond)
    print(("OK   " if cond else "FALHA"), nome, "" if det is None else "-> " + str(det)[:240])


esp4 = json.load(open(os.path.join(DL.V396, "ESPERADOS_v396.json"), encoding="utf-8"))
raw = rd(os.path.join(NOS, "um.py")); selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
chk("um.py do Nos == o que o selo pina e == o candidato selado da v396 (ESPERADOS_v396)", sha(raw) == selo["sha256"]["um.py"] and selo.get("um_version") == "v396" and sha(raw)[:16] == esp4["candidato_sha16"], sha(raw)[:16])
el = core["external_ladder"]; axr = core["kernel_formalization"]["axiom_report"]
chk("escada v396 fechada (limpos == esperados == a de ESPERADOS_v396) e axiom_report v396 lido do core", el["n_theorems_clean"] == el["n_theorems_expected"] == esp4["escada"][1] and len(axr) == esp4["axiom_report_esperado_min"], [el["n_theorems_clean"], el["n_theorems_expected"], len(axr)])
chk("nenhum registro v397 no core ainda", not any(k.endswith("_v397") for k in core), [k for k in core if k.endswith("_v397")])
_cdir_pilar = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", esp4["pilar"]["key"])
chk("o cache do pilar guarda o resultado que a v396 reaproveitou pela chave (o que a v397 reaproveita e o instalador exige): result.json == o sha256 do selo da v396", os.path.exists(os.path.join(_cdir_pilar, "result.json")) and sha(rd(os.path.join(_cdir_pilar, "result.json"))) == esp4["pilar"]["result_sha256"], esp4["pilar"]["key"][:16])
chk("a copia base_v396 == o Nos (um.py, core, selo, manifesto do kernel, pilar)", all(rd(os.path.join(BB, f)) == rd(os.path.join(NOS, f)) for f in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json")))
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v397.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v397.json"), encoding="utf-8")); PB = json.load(open(os.path.join(HERE, "PINOS_BN_v397.json"), encoding="utf-8"))
cand = os.path.join(HERE, DL.CANDIDATO); cb = rd(cand)
chk("o candidato: sha16 == ESPERADOS == CANDIDATO == PINOS_BN; sha256 == o pino", sha(cb)[:16] == ESP["candidato_sha16"] == CM["sha16"] and sha(cb) == CM["sha256"] == PB["candidato"]["sha256"], [sha(cb)[:16], len(cb)])
chk("ESPERADOS e PINOS_BN pinam os arquivos que estao em disco", all(PB[k]["sha256"] == sha(rd(PB[k]["path"])) for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256") and os.path.exists(PB[k].get("path", ""))), [k for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256")])
chk("os pinos obrigatorios do passo 10 estao em PINOS_BN_v397 (sem cadeia de selos: nao ha salto)", all(k in PB for k in ("criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v396", "kernel_manifesto_anterior_v396")) and "cadeia_de_selos" not in PB)
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v397.json"), encoding="utf-8"))
chk("o ensaio a seco e' deste candidato e deu TUDO PASSOU (e o ESPERADOS pina o ensaio); o QUADRO do Teste da Unica Palavra esta no topo do artigo PT/EN e do .md e os numeros do quadro == os do resultado pinado", ens["veredito"] == "TUDO PASSOU" and ens["quadro"]["ok"] is True and ens["sha16"] == CM["sha16"] and ESP["ensaio_sha16"] == sha(rd(os.path.join(HERE, "ensaio_a_seco_v397.json")))[:16], [ens["veredito"], ens["sha16"]])
try:
    ast.parse(cb.decode("utf-8")); sintaxe = True
except SyntaxError:
    sintaxe = False
chk("ast.parse do candidato", sintaxe)
E1, _, _, h1 = carregar(cand)
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v397.json"), encoding="utf-8"))["novos"]
chk("o kernel embutido do candidato == o sandbox construido (o modulo novo, raiz, Audit e os demais, byte a byte)", all(rd(os.path.join(KS, *k.split("/"))) == v.encode("utf-8") for k, v in E1.items()) and len(E1) == CM["formal_files_n"], len(E1))
chk("o modulo novo (%d, lido da lista) NAO esta no kernel do Nos; as pedras da v394, v395 e v396 estao" % len(nov), nov == [DL.STONE_REL] and not any(os.path.exists(os.path.join(NK, *p.split("/"))) for p in nov) and all(os.path.exists(os.path.join(NK, "TGLExt", n + ".lean")) for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica")))
chk("a raiz e o Audit do Nos == os da v396 embutida (o ANTES)", sha(rd(os.path.join(NK, "TGLExt.lean")))[:16] == CM["kernel"]["raiz_v396_sha16"] and sha(rd(os.path.join(NK, "TGL", "Audit.lean")))[:16] == CM["kernel"]["audit_v396_sha16"])
pb = json.load(open(os.path.join(KDIR, "POS_BUILD_v397.json"), encoding="utf-8"))
chk("pos-build do kernel VERDE (rc 0, zero sorry, trio, .olean Lean 4.31.0; raiz e Audit compilados) e a arvore so-fontes existe", pb["ok"] is True and pb["modo_da_pedra_no_build"] and os.path.isdir(KA), [pb["ok"], pb["modo_da_pedra_no_build"], pb["githash_lean"]])
KR = json.load(open(os.path.join(KDIR, "KERNEL_RECIBO_v397.json"), encoding="utf-8"))
chk("o recibo do kernel pina logs e arvore que existem e conferem; a unica pedra tem declaracoes (nenhum modulo de auditoria)", sha(rd(KR["build_full_log"]["path"])) == KR["build_full_log"]["sha256"] and sha(rd(KR["audit_log"]["path"])) == KR["audit_log"]["sha256"] and os.path.isdir(KR["arvore"]) and len(KR["pedras"]) == len(nov) and all(p["declaracoes"] for p in KR["pedras"]))
MI = json.load(open(os.path.join(HERE, "MANIFESTO_INSUMOS_v397.json"), encoding="utf-8"))
chk("os insumos duraveis == as origens (sha256), exceto a medida do Audit (gerada aqui), e os pinados nos registros conferem", all(sha(rd(os.path.join(HERE, "insumos", k))) == v["sha256"] and (not os.path.exists(v["origem"]) or sha(rd(v["origem"])) == v["sha256"] or k == DL.KH_N1_INSUMO) for k, v in MI.items()), len(MI))
chk("as quatro cunhagens de 23/10: arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == 4 and all(sha(rd(v["origem"])) == v["sha256"] == sha(rd(os.path.join(HERE, "insumos", k))) for k, v in MI.items() if k.startswith("cunhagens/")))
pr = json.load(open(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v397.json"), encoding="utf-8"))
_esc = pr.get("escrita_na_producao") or {}
chk("o recibo pre_selo do B(n) foi GERADO E PINADO ANTES da instalacao: arquivo == pino; utilizavel; do um.py que esta no Nos; veredito de 'ja sincronizada'; a producao (Bancada e Nos) so' foi lida (listas identicas antes e depois)",
    sha(rd(pr["path"])) == pr["sha256"] and pr["utilizavel_como_recibo_pre_selo_do_B_n"] is True and pr["versao_nos"] == "v396" and pr["um_py_sha16_do_nos"] == sha(raw)[:16] and pr["veredito"].startswith("JA_SINCRONIZADA__ENSAIO")
    and (_esc.get("bancada_um") or {}).get("identico") is True and (_esc.get("nos") or {}).get("identico") is True, [pr["veredito"], pr["utilizavel_como_recibo_pre_selo_do_B_n"], _esc.get("bancada_um"), _esc.get("nos")])
prova = json.load(open(os.path.join(HERE, "PROVA_PRODUCAO_INTACTA_v397_pre_selo.json"), encoding="utf-8"))
F9 = DL.f9_fontes(os.path.join(HERE, "insumos", "fase9"))
chk("o Teste da Unica Palavra: o resultado e os tres recibos (copias duraveis em insumos\\fase9) == as origens (sha256, pasta fase9_v2_c1_23out so' leitura); o resultado == o sha256 que a ordem da gerencia deu; as QUATRO falas de 23/10 tem os prefixos de sha256 da ordem",
    all(sha(rd(f["arquivo"])) == f["sha256"] == sha(rd(f["origem"])) for f in F9) and F9[0]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM and len(DL.verbatins(os.path.join(HERE, "insumos", "cunhagens"))) == 4, [f["sha256"][:16] for f in F9])
chk("a prova de que a producao so' foi lida existe (PROVA_PRODUCAO_INTACTA_v397_pre_selo.json: producao_intacta True)", prova.get("producao_intacta") is True)
bm = json.load(open(os.path.join(C, "IALD", "Bancada_Um", "canonical_contracts.json"), encoding="utf-8"))
chk("a Bancada de producao AINDA pina o que o recibo pre_selo diz (versao e um.py): o recibo nao ficou obsoleto", bm["canonical"].get("version") == pr["bancada_pina"]["version"] == "v396" and str(bm["sincronizacao"].get("um_py_sha256"))[:16] == pr["bancada_pina"]["um_py_sha16"], [bm["canonical"].get("version"), str(bm["sincronizacao"].get("um_py_sha256"))[:16]])
sim = json.load(open(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]), encoding="utf-8"))
chk("simular_arvore_do_nos DESTE candidato: o kh_n1_cobertura_v396 sela na arvore simulada do Nos e o hash formal tem %d entradas" % ESP["h8_entradas"], sim["candidato_sha16"] == CM["sha16"] and sim["formal_files_n_no_rito_real"] == ESP["h8_entradas"] and sim["kh_n1_cobertura_v396"]["all_verified"] is True and sim["testemunha_estatica_v396"]["all_verified"] is True and sim["psibit_v395"]["all_verified"] is True and sim["teste_de_veracidade_fase9_v397"]["all_verified"] is True and sim["cunhagens_v397"]["all_verified"] is True and sim["kf_all_verified"] is True, sim["formal_files_n_no_rito_real"])
exm = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % CM["sha16"]), encoding="utf-8"))
chk("exame_pontos_v397 DESTE candidato: nenhum ponto de chamada real da falso (o do psibit_v395 vem logo depois do principio da defasagem fractal, o da testemunha_estatica_v396 logo depois do psibit_v395 e o do teste_de_veracidade_fase9_v397 logo depois do bloco do V1)", exm["sha256"] == CM["sha256"] and exm.get("algum_falso") == [] and exm["ponto_psibit"]["logo_depois_do_principio_da_defasagem_fractal"] is True and exm["ponto_testemunha"]["logo_depois_do_psibit_v395"] is True and exm["ponto_veracidade"]["all_verified"] is True and exm["ponto_veracidade"]["depois_do_psibit_e_da_testemunha"] is True and exm["ponto_veracidade"]["antes_do_bloco_v393"] is True and all(exm["ponto_veracidade"]["numeros_lidos_iguais_ao_resultado_pinado"].values()), exm.get("algum_falso"))
neg = json.load(open(os.path.join(HERE, "conferencia_rito_v397_CONTROLE_NEGATIVO_PRE_RITO.json"), encoding="utf-8")); pos = json.load(open(os.path.join(HERE, "conferencia_rito_v397_POSITIVO_FALSO_NOS.json"), encoding="utf-8"))
chk("o conferidor: controle negativo (Nos ainda v396) tudo_bate False com os nao-pode-mudar todos verdes; caminho positivo (Nos FALSO montado do ensaio) TUDO BATE", neg["tudo_bate"] is False and all(neg["nao_pode_mudar"].values()) and pos["tudo_bate"] is True, [sum(neg["deve_mudar"].values()), len(neg["deve_mudar"])])
cmp_ = json.load(open(os.path.join(HERE, "COMPARACAO_V396_v397.json"), encoding="utf-8"))
chk("nada da v396 perdido: comparacao AST sem no removido nem mudanca sem explicacao", cmp_["ok"] is True and not cmp_["removidos"] and not cmp_["mudados_sem_explicacao"], [cmp_["iguais"], len(cmp_["mudados"]), cmp_["n_novos"]])
cit = json.load(open(os.path.join(HERE, "conferir_citacoes_v397.json"), encoding="utf-8"))
chk("as citacoes do operador embutidas conferem (embutida == arquivo == fonte original)", cit["todas_conferem"] is True)
chk("pdflatex e lake no PATH; Lean 4.31.0 no sandbox", bool(shutil.which("pdflatex")) and bool(shutil.which("lake")) and "4.31.0" in subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KS).stdout)
chk("a pedra: a fonte autoral == a copia duravel pinada (insumos) == a EMBUTIDA no candidato == a do sandbox", sha(rd(DL.STONE_SRC)) == sha(rd(os.path.join(HERE, "insumos", DL.STONE_INSUMO))) == sha(E1[DL.STONE_REL].encode("utf-8")) == sha(rd(os.path.join(KS, *DL.STONE_REL.split("/")))) and sha(rd(DL.STONE_SRC)) == ESP["pedra"]["sha256"], ESP["pedra"]["sha16"])
chk("o hash formal que o RITO vai gerar (a arvore do Nos depois do rito) tem %d entradas, com os residuais %s; o pino h8 do candidato bate" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]), len(ESP["h8_residuais_do_nos"]) + CM["formal_files_n"] == ESP["h8_entradas"] and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in ESP["h8_residuais_do_nos"]), ESP["h8_entradas"])
chk("nenhum marcador de servidor parado nas pastas das duas cadeias (a guarda do rito)", not os.path.exists(os.path.join(DL.V396, ".servidor_parado_pelo_rito")) and not os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito")))
for f in ("delta_v397.py", "preparar_kernel_v397.py", "pos_build_kernel_v397.py", "registros_v397.py", "runtime_quadro_v397.py", "copiar_base_v397.py", "copiar_insumos_v397.py", "diff_e_pinos_v397.py", "gerar_esperados_v397.py", "derivar_instalar_rito_v397.py", "simular_arvore_do_nos_v397.py", "exame_pontos_v397.py",
          "instalar_v397.py", "reverter_v397.py", "refazer_arvore_v397_pos_selo.py", "conferir_rito_v397.py", "gerar_candidato_v397.py", "ensaio_a_seco_v397.py", "comparar_v396_v397.py", "conferir_citacoes_v397.py", "teste_conferidor_positivo_v397.py", "regras_v397.py", "guarda_p18_v397.py", "derivar_encanamento_v397.py", "derivar_encanamento_v397_regras.py", "derivar_encanamento_v397_regras_B.py", "quadro_v397.py"):
    try:
        ast.parse(open(os.path.join(HERE, f), encoding="utf-8").read()); s_ = True
    except (SyntaxError, OSError):
        s_ = False
    chk("ast.parse de %s" % f, s_)
for f in ("rito_v397.sh", "refazer_sandbox_v397.sh", "refazer_sandbox_v397_pos_selo.sh", "construir_kernel_v397.sh", os.path.join("pos_rito", "chain_pos_rito_v397.sh")):
    chk("sh -n de %s" % f, os.path.exists(os.path.join(HERE, f)) and subprocess.run(["sh", "-n", os.path.join(HERE, f)], capture_output=True).returncode == 0)
dv = json.load(open(os.path.join(HERE, "DERIVACAO_v397.json"), encoding="utf-8"))
chk("a derivacao do rito/instalar/reverter: zero falha nos invariantes e a sintaxe de todos", not dv["falhas"] and all(("ok" in v or "rc=0" in v) for v in dv["sintaxe"].values()), [sum(len(x) for x in dv["invariantes"].values())])
marcas = [f for f in glob.glob(os.path.join(HERE, "pos_rito", "*.py")) if "TEXTO_A_REESCREVER" in open(f, encoding="utf-8", errors="replace").read().replace('"TEXTO_A_REESCREVER" +', "").replace("_MARCA_PENDENTE = ", "")]
chk("nenhum texto do pos_rito com a marca TEXTO_A_REESCREVER como comentario pendente", not [m for m in marcas if re.search(r"(?m)^\s*#\s*TEXTO_A_REESCREVER", open(m, encoding="utf-8", errors="replace").read())], [os.path.basename(m) for m in marcas][:4])
print("\nPRECONDICOES v397:", "TODAS PASSARAM" if ok_all else "FALHOU")
json.dump({"ok": ok_all, "checagens": res}, open(os.path.join(HERE, "PRECONDICOES_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0 if ok_all else 1)
