# -*- coding: utf-8 -*-
"""p00_precondicoes_v408.py -- confere, SO LENDO, as pre-condicoes de bytes da v408 ANTES de instalar. Nada e escrito fora de PRECONDICOES_v408.json (nesta pasta). Os pinos sao LIDOS do selo/core/arquivos,
nunca digitados. Fail-closed: rc 1 se algo falha. Molde: p00_precondicoes_v407.py (a cadeia de CONTEUDO), adaptado em 04/11/2026 a v408 por claude-construtor-v408 (Tetelestai e' o terminal: bundle de 4 modulos em TGLExt/, registro tetelestai_terminal_v408, 41 ancoras, 12 falas de 04/11; nenhuma chave antiga muda).
PENDENTE nao e' falha: o que so' passa a existir depois de OUTRO passo da cadeia (o ensaio a seco e os ESPERADOS; o B(n) pre-selo: PINO_RECIBO_PRE_SELO_v408.json e PROVA_PRODUCAO_INTACTA_v408_pre_selo.json; as guardas/harnesses/derivacoes/comparacao/citacoes; o pino da memoria PINO_MEMORIA_PY_v408.json; o caso em que o MEMORY.md real nao comporta o handoff novo e a gerencia decide)
sai como PENDENTE, com o motivo (e quem o produz); o veredito final e' TODAS PASSARAM so' sem falha E sem pendente (rc 0); NENHUMA FALHA, N PENDENTES sai com rc 3; FALHOU com rc 1. Uma checagem que levanta excecao vira FALHA visivel (nunca 'ok' falso).
Tambem RECUSA (falha) todo arquivo da cadeia que ainda traga a marca `# [A ADAPTAR v408]` (copia mecanica de rotulo, nunca adaptada) fora de .bak_*, bump/ e do gerador do bump.
uso: python -I -B -X utf8 p00_precondicoes_v408.py"""
import ast, glob, hashlib, json, os, re, shutil, subprocess, sys
# [v408-patch]
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v408 as DL  # noqa: E402
import acom_conferencias_v408 as AC  # noqa: E402
C = "C:" + os.sep
NOS = DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
KS = DL.SANDBOX; KA = DL.ARVORE; KDIR = os.path.join(HERE, DL.KERNEL_DIR); BB = os.path.join(HERE, DL.BASE_DIR)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
lj = lambda p: json.load(open(p, encoding="utf-8"))
res = []; ok_all = True; PEND = []


def tenta(p):
    """o JSON lido, ou None (o chamador diz PENDENTE)"""
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def pend(nome, motivo):
    """PENDENTE: ainda nao existe o que esta checagem le (nao e' erro do script nem falha do candidato); o veredito final nao e' TODAS PASSARAM enquanto houver pendente"""
    PEND.append({"checagem": nome, "motivo": motivo}); res.append({"checagem": nome, "ok": None, "pendente": True, "detalhe": motivo})
    print("PEND ", nome[:160], "-> " + str(motivo)[:240])


def chk(nome, cond, det=None):
    global ok_all
    res.append({"checagem": nome, "ok": bool(cond), "detalhe": det}); ok_all = ok_all and bool(cond)
    print(("OK   " if cond else "FALHA"), nome[:160], "" if det is None else "-> " + str(det)[:240])


def dep(nome, deps, fn):
    """roda `fn` (devolve cond ou (cond, detalhe)); se alguma dependencia (dict nome->objeto lido) e' None a checagem e' PENDENTE; excecao vira FALHA visivel"""
    falta = [k for k, v in deps.items() if v is None]
    if falta:
        pend(nome, "depende de %s, que ainda nao existe (e' produzido por outro passo da cadeia)" % ", ".join(falta)); return
    try:
        r = fn()
    except Exception as e:   # noqa: BLE001
        chk(nome, False, "EXCECAO: %r" % (e,)); return
    cond, det = r if isinstance(r, tuple) else (r, None)
    chk(nome, cond, det)


esp4 = json.load(open(os.path.join(DL.V407, "ESPERADOS_v407.json"), encoding="utf-8"))
raw = rd(os.path.join(NOS, "um.py")); selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
chk("um.py do Nos == o que o selo pina e == o candidato selado da v407 (ESPERADOS_v407)", sha(raw) == selo["sha256"]["um.py"] and selo.get("um_version") == "v407" and sha(raw)[:16] == esp4["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM, sha(raw)[:16])
el = core["external_ladder"]; axr = core["kernel_formalization"]["axiom_report"]
chk("escada v407 fechada (limpos == esperados == a de ESPERADOS_v407) e axiom_report v407 lido do core", el["n_theorems_clean"] == el["n_theorems_expected"] == esp4["escada"][1] and len(axr) == esp4["axiom_report_esperado_min"], [el["n_theorems_clean"], el["n_theorems_expected"], len(axr)])
_chaves_base = sorted(set(esp4["vereditos_v406"]) | set(esp4["vereditos_novos_v407"]))   # todo registro da v407 selada: os da base de entao (a v406) e os tres novos da v407 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407)
chk("nenhum registro v408 no core ainda; todos os registros da v407 selada ja estao (%d chaves lidas de ESPERADOS_v407); a chave do lema (testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) ja e' LIDA do kernel e le True no selado, como as quatro chaves da v406 (nenhuma chave antiga muda na v408); o psion_canto_v407 selado esta' no core" % len(_chaves_base),
    not any(k.endswith("_v408") for k in core) and all(k in core for k in _chaves_base) and core["rede_fock_v394"]["whole_certificate_inhabited"] is True
    and core["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] is True and core["testemunha_estatica_v396"]["fock_face"]["inhabitant_exhibited"] is True and (core.get("psion_canto_v407") or {}).get("all_verified") is True, [k for k in core if k.endswith("_v408")])
_cdir_pilar = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", esp4["pilar"]["key"])
chk("o cache do pilar guarda o resultado que a v407 reaproveitou pela chave (o que a v408 reaproveita e o instalador exige): result.json == o sha256 do selo da v407", os.path.exists(os.path.join(_cdir_pilar, "result.json")) and sha(rd(os.path.join(_cdir_pilar, "result.json"))) == esp4["pilar"]["result_sha256"], esp4["pilar"]["key"][:16])
chk("a copia base_v407 == o Nos (um.py, core, selo, manifesto do kernel, pilar)", all(rd(os.path.join(BB, f)) == rd(os.path.join(NOS, f)) for f in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json")))
ESP = tenta(os.path.join(HERE, "ESPERADOS_v408.json")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v408.json"), encoding="utf-8")); PB = tenta(os.path.join(HERE, "PINOS_BN_v408.json"))
_rt = rd(os.path.join(HERE, "runtime_v408.py")).decode("utf-8")
chk("o runtime novo (runtime_v408.py: o registro com FUNCAO tetelestai_terminal_v408, escrito a mao) e' o que o candidato embute: o sha256 do CANDIDATO_v408.json == o do arquivo; o bloco extraido do candidato (v408_pins.py) o contem; nenhum literal de beta no codigo (C9); a secao do selo ACOM (a da v407) NAO mudou: o hash do bloco embutido e' o que a v407 pinou",
    CM["runtime"]["sha256"] == sha(rd(os.path.join(HERE, "runtime_v408.py"))) and _rt.rstrip("\n") in rd(os.path.join(HERE, "v408_pins.py")).decode("utf-8") and not AC.literais_de_beta(_rt) and CM["acom"].get("nota") and AC.bloco_das_fontes()[1] == esp4["acom_estudo"]["bloco_embutido_sha256"], [CM["runtime"]["sha256"][:16], CM["runtime"]["bytes"]])
chk("as 6 fontes do operador do ACOM (a origem so' leitura == a copia duravel da cadeia v400 == os pinos do ESPERADOS_v407)", all(sha(rd(o_)) == sha(rd(os.path.join(DL.V400, "insumos", "acom", "fontes_operador", n_))) == esp4["acom_estudo"]["fontes_do_operador"][n_] for n_, o_ in DL.ACOM_FONTES_OPERADOR.items()), len(DL.ACOM_FONTES_OPERADOR))


def _bundle_ok():
    nov_ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v408.json"), encoding="utf-8"))["novos"]
    bf_ = DL.bundle_fontes()   # le os 4 modulos do sandbox e CONFERE o sha256 de cada um contra o BUNDLE_v408.json (aborta se difere)
    tf_ = DL.testemunha_fonte()   # a TetelestaiTerminal (a pedra principal): origem == bundle, sha16 == o do recibo dos nomes
    ped_ = {p_["rel"]: p_ for p_ in DL.PEDRAS_V408}
    origem_ok_ = all(sha(rd(ped_[r_]["origem"])) == DL.BUNDLE_POR_REL[r_]["sha256_origem"] == ped_[r_]["sha256_origem"] for r_ in DL.BUNDLE_RELS)   # a fonte de origem (pedras_candidatas_04nov) == a que o preparo pinou
    copia_ok_ = all(sha(rd(ped_[r_]["src"])) == DL.BUNDLE_POR_REL[r_]["sha256"] == sha(rd(os.path.join(KS, *r_.split("/")))) for r_ in DL.BUNDLE_RELS)   # a copia normalizada (v408\pedra) == o bundle == o sandbox
    imports_ = [l_ for l_ in DL.ROOT_SUFFIX.replace("\r\n", "\n").split("\n") if l_.strip()]
    raiz_ok_ = imports_ == ["import " + m_ for m_ in DL.BUNDLE_MODS] and len(imports_) == DL.N_BUNDLE == 4
    vb_ = DL.verbatins408(os.path.join(HERE, "insumos", "cunhagens"))   # aborta se uma fala-chave diverge do prefixo da ordem ou se um trecho citado nao e' verbatim
    cond_ = bool(nov_ == list(DL.BUNDLE_RELS) and len(bf_) == DL.N_BUNDLE == 4 and DL.BUNDLE_DA_BANCADA == [] and DL.BUNDLE_DA_GERENCIA == list(DL.BUNDLE_RELS) and origem_ok_ and copia_ok_ and raiz_ok_
                 and tf_["sha256_origem"][:16] == DL.TESTEMUNHA["sha16_da_ordem"] and len(vb_) == len(DL.VERBATIM_ORIGEM_V408) == DL.N_FALAS_V408 == 15 and set(DL.VERBATIM_PREFIXOS_DA_ORDEM_V408.values()) <= {v_["sha16"] for v_ in vb_})
    return cond_, [len(bf_), tf_["sha256_origem"][:16], len(vb_), origem_ok_, copia_ok_, raiz_ok_]


dep("o BUNDLE (%d modulos novos em TGLExt/, provas da gerencia com os nomes do operador): a lista dos modulos novos (kernel_modulos_novos_v408.json) == DL.BUNDLE_RELS; o sha256 de cada um no sandbox == o do BUNDLE_v408.json; a fonte de origem de cada um == a que o preparo pinou e a copia normalizada v408\\pedra == o bundle; a raiz tem exatamente os quatro imports; a TetelestaiTerminal e' a que o recibo dos nomes pinou (sha16); as 12 falas de 04/11 tem os prefixos de sha256 do DESENHO e cada trecho citado e' verbatim (nas duas de autor misto, so' o paragrafo do operador; as falas de 02 e 03/11 ja estao no um.py v407 e nao entram de novo)" % DL.N_BUNDLE, {}, _bundle_ok)


def _ancoras_ok():
    fj_ = lj(os.path.join(KDIR, "FLAGS_v408.json"))
    return bool(len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 48 == len(fj_["ancoras"]) == len(CM["n_axiomas_das_ancoras"]) and set(DL.ANCORAS) == set(fj_["ancoras"]) == set(CM["n_axiomas_das_ancoras"]) and all(a_["rel"] in DL.BUNDLE_RELS for a_ in DL.ANCORAS.values())
                and sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) == DL.N_ANCORAS_ESPERADAS and all(a_ in DL.ANCORAS for a_ in DL.ANCORAS_PRINCIPAIS) and len(DL.ANCORAS_PRINCIPAIS) == DL.N_BUNDLE and fj_["n_flags"] == CM["n_bandeiras"] == sum(fj_["n_por_modulo"].values())
                and all(set(a_["axioms"]) <= DL.TRIO_SET for a_ in fj_["ancoras"].values())), [len(DL.ANCORAS), fj_["n_flags"]]


dep("as 48 ancoras (#print axioms deixados pela autora das provas, lidos das fontes de origem, nunca digitados): DL.ANCORAS == o FLAGS_v408.json == o n_axiomas_das_ancoras do candidato; cada uma num modulo do bundle e so' no trio; as quatro ancoras principais (tetelestai, o_tempo_e_a_moeda, o_ponto_de_contradicao, p_igual_np) estao entre elas; as bandeiras novas somam n_por_modulo", {}, _ancoras_ok)
cand = os.path.join(HERE, DL.CANDIDATO); cb = rd(cand)
chk("o candidato: sha16 == CANDIDATO; sha256 == o pino do CANDIDATO_v408.json", sha(cb)[:16] == CM["sha16"] and sha(cb) == CM["sha256"] and len(cb) == CM["bytes"], [sha(cb)[:16], len(cb)])
dep("o candidato: sha16 == ESPERADOS; sha256 == o pino de PINOS_BN", {"ESPERADOS_v408.json": ESP, "PINOS_BN_v408.json": PB}, lambda: (sha(cb)[:16] == ESP["candidato_sha16"] == CM["sha16"] and sha(cb) == PB["candidato"]["sha256"], [sha(cb)[:16], len(cb)]))
dep("ESPERADOS e PINOS_BN pinam os arquivos que estao em disco", {"PINOS_BN_v408.json": PB}, lambda: (all(PB[k]["sha256"] == sha(rd(PB[k]["path"])) for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256") and os.path.exists(PB[k].get("path", ""))), [k for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256")]))
dep("os pinos obrigatorios do passo 10 estao em PINOS_BN_v408 (sem cadeia de selos: nao ha salto)", {"PINOS_BN_v408.json": PB}, lambda: all(k in PB for k in ("criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v407", "kernel_manifesto_anterior_v407")) and "cadeia_de_selos" not in PB)
ens = tenta(os.path.join(HERE, "ensaio_a_seco_v408.json"))
ESBOCO = os.path.join(WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"); ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
gb = tenta(os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v408.json"))
dep("[LICAO DA v407] as guardas ESTATICAS do esboco R3.5 da Bancada (a funcao ler_nos do esboco pinado) sobre o CANDIDATO: passa (uma so' linha de alfa e de UM_VERSION); a v399 selada e' recusada com a mensagem EXATA do recibo da Bancada; os 9 controles negativos recusam; o ensaio as rodou", {"GUARDAS_ESTATICAS_BANCADA_v408.json": gb, "ensaio_a_seco_v408.json": ens},
    lambda: (gb["veredito"].startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and gb["candidato"]["sha16"] == CM["sha16"] and gb["esboco"]["sha256"] == ESBOCO_SHA256 == sha(rd(ESBOCO)) and gb["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"] is True
             and len(gb["controles_negativos"]) == 9 and all(v["ok"] for v in gb["controles_negativos"].values()) and gb["contagem_direta"] == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0} and ens.get("guardas_estaticas_bancada", {}).get("veredito") == gb["veredito"], [gb["candidato_v408"]["alpha"]["n_linhas_nao_indentadas"], gb["contagem_direta"]]))
dep("o ensaio a seco e' deste candidato e deu TUDO PASSOU (e o ESPERADOS pina o ensaio); o QUADRO do Teste da Unica Palavra esta no topo do artigo PT/EN e do .md e os numeros do quadro == os do resultado pinado", {"ensaio_a_seco_v408.json": ens, "ESPERADOS_v408.json": ESP},
    lambda: (ens["veredito"] == "TUDO PASSOU" and ens["quadro"]["ok"] is True and ens["sha16"] == CM["sha16"] and ESP["ensaio_sha16"] == sha(rd(os.path.join(HERE, "ensaio_a_seco_v408.json")))[:16], [ens.get("veredito"), ens.get("sha16")]))
try:
    ast.parse(cb.decode("utf-8")); sintaxe = True
except SyntaxError:
    sintaxe = False
chk("ast.parse do candidato", sintaxe)
_gf = lj(os.path.join(HERE, "GUARDA_FRASES_v408.json"))
chk("[v408, a MOLDURA] a guarda das frases: o controle negativo passou (cada frase proibida reprovada, a frase certa e os identificadores aceitos, a fala do operador so' pela excecao), o gerador achou zero frase proibida no texto novo do candidato e as 4 pedras estao limpas; os registros novos do candidato sao exatamente tetelestai_terminal_v408, cunhagens_v408 e kh_n1_cobertura_v408", _gf.get("ok") is True and _gf.get("pedras_limpas") is True and len(_gf.get("pedras") or {}) == DL.N_BUNDLE and CM["guarda_frases"]["controle_negativo"] is True and CM["guarda_frases"]["violacoes_no_texto_novo"] == 0 and sorted(CM["registros"]) == sorted([DL.FECHO_REGISTRO, DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]), CM["guarda_frases"])
_cong = lj(os.path.join(HERE, "VERBATIM_CONGELADO_v408.json"))
_glob_agora = sorted(os.path.basename(p_) for p_ in DL.verbatim_origem_pelo_glob408())
_novas_depois = sorted(set(_glob_agora) - set(os.path.basename(p_) for p_ in _cong["arquivos"]))
chk("[v408] a lista das falas embutidas esta congelada (VERBATIM_CONGELADO_v408.json) e e' a do candidato; fala nova depois do congelamento NAO entra nesta versao e NAO reprova o conferidor (fica dita no detalhe)", list(DL.VERBATIM_ORIGEM_V408) == list(_cong["arquivos"]) and len(_cong["arquivos"]) == len(CM["cunhagens"]) == DL.N_FALAS_V408 == 15, {"embutidas": len(_cong["arquivos"]), "falas_novas_depois_do_congelamento": _novas_depois})
chk("[v408, a lista de exclusao] nenhuma fala de VERBATIM_EXCLUIDAS_V408 esta no candidato: o sha16 nao aparece nas cunhagens do CANDIDATO_v408.json nem na copia duravel insumos\\cunhagens", not any(k_ in json.dumps(CM["cunhagens"]) for k_ in DL.VERBATIM_EXCLUIDAS_V408) and not any(os.path.basename(p_)[:16] in DL.VERBATIM_EXCLUIDAS_V408 for p_ in glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*"))), sorted(DL.VERBATIM_EXCLUIDAS_V408))
cit = tenta(os.path.join(HERE, "conferir_citacoes_v408.json"))
dep("[v408] a conferencia de citacoes conferiu a docstring das 4 pedras (zero reprovada; o que bate so' sem acento e as apontadas a gerencia ficam ditas no JSON) e a guarda das frases achou zero frase proibida no texto novo", {"conferir_citacoes_v408.json": cit},
    lambda: (not cit["varredura_das_pedras"]["reprovadas"] and CM["guarda_frases"]["violacoes_no_texto_novo"] == 0, {"conferidas": cit["varredura_das_pedras"]["citacoes_conferidas"], "so_sem_acento": cit["varredura_das_pedras"].get("so_sem_acento"), "apontadas_a_gerencia_aspas": len(cit.get("apontadas_a_gerencia_aspas") or [])}))
E1, _, _, h1 = carregar(cand)
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v408.json"), encoding="utf-8"))["novos"]
chk("o kernel embutido do candidato == o sandbox construido (os 4 modulos novos, raiz, Audit e os demais, byte a byte)", all(rd(os.path.join(KS, *k.split("/"))) == v.encode("utf-8") for k, v in E1.items()) and len(E1) == CM["formal_files_n"], len(E1))
chk("os modulos novos (%d, lidos da lista) NAO estao no kernel do Nos; as pedras da v394 a v407 (os %d modulos da v407 e os %d do fecho da v406 por sha256, as oito da v405, as duas da v404 e as tres da v403 inclusive) estao" % (len(nov), len(esp4["bundle_sha256"]), len(esp4["bundle_v406_sha256"])),
    nov == list(DL.BUNDLE_RELS) and not any(os.path.exists(os.path.join(NK, *p.split("/"))) for p in nov) and all(os.path.exists(os.path.join(NK, "TGLExt", n + ".lean")) for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional"))
    and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in list(DL.D3.STONE_RELS) + list(DL.D4.STONE_RELS) + list(DL.D5.STONE_RELS)) and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_sha256"].items()) and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_v406_sha256"].items()))
chk("a raiz e o Audit do Nos == os da v407 embutida (o ANTES)", sha(rd(os.path.join(NK, "TGLExt.lean")))[:16] == CM["kernel"]["raiz_v407_sha16"] and sha(rd(os.path.join(NK, "TGL", "Audit.lean")))[:16] == CM["kernel"]["audit_v407_sha16"] == CM["kernel"]["audit_sha16"])
pb = json.load(open(os.path.join(KDIR, "POS_BUILD_v408.json"), encoding="utf-8"))
chk("pos-build do kernel VERDE (rc 0, zero sorry, trio, .olean Lean 4.31.0; raiz e Audit compilados; os 4 modulos Built e nenhum Replayed) e a arvore so-fontes existe", pb["ok"] is True and pb["modo_da_pedra_no_build"] and os.path.isdir(KA) and pb["modos_contagem"] == {"Built": DL.N_BUNDLE, "Replayed": 0} and not pb["falhas"], [pb["ok"], pb["modo_da_pedra_no_build"], pb["githash_lean"]])
KR = json.load(open(os.path.join(KDIR, "KERNEL_RECIBO_v408.json"), encoding="utf-8"))
chk("o recibo do kernel pina logs e arvore que existem e conferem; cada um dos %d modulos do bundle tem declaracoes (nenhum modulo de auditoria)" % len(nov), sha(rd(KR["build_full_log"]["path"])) == KR["build_full_log"]["sha256"] and sha(rd(KR["audit_log"]["path"])) == KR["audit_log"]["sha256"] and os.path.isdir(KR["arvore"]) and len(KR["pedras"]) == len(nov) == DL.N_BUNDLE and all(p["declaracoes"] for p in KR["pedras"]))
MI = json.load(open(os.path.join(HERE, "MANIFESTO_INSUMOS_v408.json"), encoding="utf-8"))
chk("os insumos duraveis == as origens (sha256), exceto a medida do Audit (gerada aqui), e os pinados nos registros conferem", all(sha(rd(os.path.join(HERE, "insumos", k))) == v["sha256"] and (not os.path.exists(v["origem"]) or sha(rd(v["origem"])) == v["sha256"] or k == DL.KH_N1_INSUMO) for k, v in MI.items()), len(MI))
_vb12 = DL.verbatins408(os.path.join(HERE, "insumos", "cunhagens")); _n_misto = sum(1 for v_ in _vb12 if "sha256_arquivo_inteiro" in v_)
chk("as 12 falas de 04/11 (todas do operador; duas de autor misto): a copia duravel de cada texto embutido == sha256 embutido; a fonte original == sha256 do arquivo inteiro (nas duas de autor misto a copia do arquivo inteiro tambem esta' em insumos\\cunhagens, e o manifesto traz 12 + 2 entradas); toda entrada cunhagens/ do manifesto == o arquivo",
    len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V408 + _n_misto == 17 and len(_vb12) == DL.N_FALAS_V408 == 15 and _n_misto == 2
    and all(sha(rd(v_["arquivo"])) == v_["sha256"] and sha(rd(v_["fonte_original"])) == (v_.get("sha256_arquivo_inteiro") or v_["sha256"]) and (("sha256_arquivo_inteiro" not in v_) or sha(rd(v_["arquivo_inteiro"])) == v_["sha256_arquivo_inteiro"]) for v_ in _vb12)
    and all(sha(rd(os.path.join(HERE, "insumos", k))) == v["sha256"] for k, v in MI.items() if k.startswith("cunhagens/")), [len(_vb12), _n_misto])
pr = tenta(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v408.json"))
_esc = (pr or {}).get("escrita_na_producao") or {}
if pr is None:
    pend("o recibo pre_selo do B(n) foi GERADO E PINADO ANTES da instalacao", "PINO_RECIBO_PRE_SELO_v408.json ainda nao existe: o B(n) pre-selo da v408 (bateria_pre_selo/rodar_bn_pre_selo_v408.sh, passo B(n) = %s, Bancada de producao pina %s) nao rodou" % (DL.B_N_SEGUINTE, DL.BANCADA_PINA_HOJE["deployment_id"]))
else:
    chk("o recibo pre_selo do B(n) foi GERADO E PINADO ANTES da instalacao: arquivo == pino; utilizavel; do um.py que esta no Nos; veredito de 'ja sincronizada'; a producao (Bancada e Nos) so' foi lida (listas identicas antes e depois)",
        sha(rd(pr["path"])) == pr["sha256"] and pr["utilizavel_como_recibo_pre_selo_do_B_n"] is True and pr["versao_nos"] == "v407" and pr["um_py_sha16_do_nos"] == sha(raw)[:16] and pr["veredito"].startswith("JA_SINCRONIZADA__ENSAIO")
        and (_esc.get("bancada_um") or {}).get("identico") is True and (_esc.get("nos") or {}).get("identico") is True, [pr["veredito"], pr["utilizavel_como_recibo_pre_selo_do_B_n"], _esc.get("bancada_um"), _esc.get("nos")])
prova = tenta(os.path.join(HERE, "PROVA_PRODUCAO_INTACTA_v408_pre_selo.json"))
F9 = [(c_, os.path.join(DL.F9_DIR_DURAVEL, n_)) for c_, n_ in (("f9v2_resultado", DL.F9_RESULTADO_NOME), ("f9v2_congelamento", "RECIBO_DE_CONGELAMENTO.json"), ("f9v2_abertura", "RECIBO_DE_ABERTURA.json"), ("f9v2_consumida", "ABERTURA_CONSUMIDA.json"))]
chk("o Teste da Unica Palavra (v397, o QUADRO do topo): o resultado e os tres recibos (copias duraveis em v397/insumos/fase9) == os sha256 que a v407 pinou (ESPERADOS_v407); o resultado == o sha256 da ordem da v397; as falas-chave desta versao tem os prefixos de sha256 que a ordem da gerencia deu (todas do operador)",
    all(sha(rd(p_)) == esp4["veracidade"]["fontes"][c_] for c_, p_ in F9) and sha(rd(F9[0][1])) == DL.F9_RESULTADO_SHA256_DA_ORDEM and len(DL.verbatins408(os.path.join(HERE, "insumos", "cunhagens"))) == len(DL.VERBATIM_ORIGEM_V408), [sha(rd(p_))[:16] for _, p_ in F9])
if prova is None:
    pend("a prova de que a producao so' foi lida (PROVA_PRODUCAO_INTACTA_v408_pre_selo.json: producao_intacta True)", "PROVA_PRODUCAO_INTACTA_v408_pre_selo.json ainda nao existe: o B(n) pre-selo nao rodou")
else:
    chk("a prova de que a producao so' foi lida existe (PROVA_PRODUCAO_INTACTA_v408_pre_selo.json: producao_intacta True)", prova.get("producao_intacta") is True)
bm = json.load(open(os.path.join(C, "IALD", "Bancada_Um", "canonical_contracts.json"), encoding="utf-8"))
chk("a Bancada de producao AINDA pina a v407 (o B(n) da v408 e' um passo simples %s -> %s): versao v407 e o deployment lido do manifesto dela == DL.BANCADA_PINA_HOJE" % (DL.BANCADA_PINA_HOJE["deployment_id"], DL.B_N_SEGUINTE), bm["canonical"].get("version") == "v407" and str(bm.get("deployment_id")) == DL.BANCADA_PINA_HOJE["deployment_id"] and DL.BANCADA_PINA_HOJE["n"] + 1 == int(DL.B_N_SEGUINTE[1:]), [bm["canonical"].get("version"), bm.get("deployment_id")])
if pr is None:
    pend("a Bancada de producao AINDA pina o que o recibo pre_selo diz (versao e um.py): o recibo nao ficou obsoleto", "depende do recibo pre_selo, que ainda nao existe")
else:
    chk("a Bancada de producao AINDA pina o que o recibo pre_selo diz (versao e um.py): o recibo nao ficou obsoleto", bm["canonical"].get("version") == pr["bancada_pina"]["version"] == "v407" and str(bm["sincronizacao"].get("um_py_sha256"))[:16] == pr["bancada_pina"]["um_py_sha16"], [bm["canonical"].get("version"), str(bm["sincronizacao"].get("um_py_sha256"))[:16]])
sim = tenta(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]))
_NOVOS_V408 = (DL.FECHO_REGISTRO, DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)
_HERDADOS_V407 = ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406")   # (os herdados da v407 e da v406, recriados no rito)
dep("simular_arvore_do_nos DESTE candidato: o registro com funcao tetelestai_terminal_v408 e os registros por spec v408 (cunhagens_v408, kh_n1_cobertura_v408) selam na arvore simulada do Nos, assim como os herdados da v407 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407) e da v406 (fechamento_v406, cunhagens_v406, kh_n1_cobertura_v406) e todos os anteriores que a simulacao registra; o hash formal tem a contagem do ESPERADOS", {"SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]: sim, "ESPERADOS_v408.json": ESP},
    lambda: (sim["candidato_sha16"] == CM["sha16"] and sim["formal_files_n_no_rito_real"] == ESP["h8_entradas"] == CM["h8"]["entradas"] and all(isinstance(sim.get(k_), dict) and sim[k_].get("all_verified") is True for k_ in _NOVOS_V408 + _HERDADOS_V407) and all(v_.get("all_verified") is True for v_ in sim.values() if isinstance(v_, dict) and "all_verified" in v_) and sim["kf_all_verified"] is True, sim["formal_files_n_no_rito_real"]))
exm = tenta(os.path.join(HERE, "EXAME_PONTOS_%s.json" % CM["sha16"]))


def _exame_ok():
    pontos_ = {k_: v_ for k_, v_ in exm.items() if k_.startswith("ponto_") and isinstance(v_, dict)}
    return bool(exm["sha256"] == CM["sha256"] and exm.get("algum_falso") == [] and pontos_ and all(v_.get("all_verified") is True for v_ in pontos_.values() if "all_verified" in v_) and any("tetelestai" in k_ for k_ in pontos_)
                and all(not v_ for v_ in exm["nao_verdes"].values())), sorted(pontos_)


dep("exame_pontos_v408 DESTE candidato: nenhum ponto de chamada real da falso; o tetelestai_terminal_v408 e' chamado IMEDIATAMENTE depois do bloco da v407 (psion_canto_v407 e os specs da v407) e antes do emit_figures, dentro do bloco executado, e chama os specs da v408; os pontos herdados seguem certos (all_verified); nenhum registro nao verde", {"EXAME_PONTOS_%s.json" % CM["sha16"]: exm}, _exame_ok)
neg = tenta(os.path.join(HERE, "conferencia_rito_v408_CONTROLE_NEGATIVO_PRE_RITO.json")); pos = tenta(os.path.join(HERE, "conferencia_rito_v408_POSITIVO_FALSO_NOS.json"))
dep("o conferidor: controle negativo (Nos ainda v407) tudo_bate False com os nao-pode-mudar todos verdes; caminho positivo (Nos FALSO montado do ensaio) TUDO BATE", {"conferencia_rito_v408_CONTROLE_NEGATIVO_PRE_RITO.json": neg, "conferencia_rito_v408_POSITIVO_FALSO_NOS.json": pos}, lambda: (neg["tudo_bate"] is False and all(neg["nao_pode_mudar"].values()) and pos["tudo_bate"] is True, [sum(neg["deve_mudar"].values()), len(neg["deve_mudar"])]))
cmp_ = tenta(os.path.join(HERE, "COMPARACAO_V407_v408.json"))
dep("nada da v407 perdido: comparacao AST sem no removido nem mudanca sem explicacao", {"COMPARACAO_V407_v408.json": cmp_}, lambda: (cmp_["ok"] is True and not cmp_["removidos"] and not cmp_["mudados_sem_explicacao"], [cmp_["iguais"], len(cmp_["mudados"]), cmp_["n_novos"]]))
dep("as citacoes do operador embutidas conferem (embutida == arquivo == fonte original)", {"conferir_citacoes_v408.json": cit}, lambda: cit["todas_conferem"] is True)
chk("pdflatex e lake no PATH; Lean 4.31.0 no sandbox", bool(shutil.which("pdflatex")) and bool(shutil.which("lake")) and "4.31.0" in subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KS).stdout)
dep("a TetelestaiTerminal (a pedra principal: o terminal e' a leitura): a fonte de origem (pedras_candidatas_04nov) == o pino do bundle (sha256_origem; sha16 == o da ordem); a copia normalizada v408\\pedra == a copia duravel pinada (insumos) == a EMBUTIDA no candidato == a do sandbox == o pino dos ESPERADOS (bundle_sha256) == o sha256 do BUNDLE_v408.json", {"ESPERADOS_v408.json": ESP},
    lambda: (sha(rd(DL.TESTEMUNHA["origem"])) == DL.BUNDLE_POR_REL[DL.TESTEMUNHA["rel"]]["sha256_origem"] and sha(rd(DL.TESTEMUNHA["origem"]))[:16] == DL.TESTEMUNHA["sha16_da_ordem"]
             and sha(rd(DL.TESTEMUNHA["src"])) == sha(rd(os.path.join(HERE, "insumos", DL.TESTEMUNHA["insumo"]))) == sha(E1[DL.TESTEMUNHA["rel"]].encode("utf-8")) == sha(rd(os.path.join(KS, *DL.TESTEMUNHA["rel"].split("/")))) == ESP["bundle_sha256"][DL.TESTEMUNHA["rel"]] == DL.BUNDLE_POR_REL[DL.TESTEMUNHA["rel"]]["sha256"], DL.TESTEMUNHA["sha16_da_ordem"]))
ML_ = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")
ML_N = len(open(ML_, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(ML_) else -1
ML_B = os.path.getsize(ML_) if os.path.exists(ML_) else -1
_NOME_MEM = "o MEMORY.md real cabe com o handoff novo e o gancho da missao: o handoff entra (+1 linha) e o gancho SUBSTITUI a linha velha (saldo +1); linhas hoje + 1 <= 195 e bytes hoje + 900 < 24000 (a linha nova do handoff tem de ter ate 900 B; a superficie do pos-rito NAO compacta: se nao couber, ela RECUSA com rc 3 e a gerencia decide o que sai do indice -- PARE e diga)"
# v408 (herdado da v407; conferido em 04/11/2026 por claude-construtor-v408): a estimativa pessimista (+900 B) deu lugar a SIMULACAO EXATA da superficie: aplica sobre o MEMORY.md real, EM MEMORIA (nada e' escrito), as mesmas duas edicoes de pos_rito/superficies_v408.py (o gancho da missao SUBSTITUI a linha velha; o handoff entra ANTES da linha do handoff da v407) com as funcoes
# REAIS de pos_rito/textos_v408.py e um V sintetico de largura igual a do rito (data, sha16 do candidato, teor 'N/N' da escada); o resultado e' comparado aos limites da superficie (24.000 B, 195 linhas). A superficie do pos-rito segue sendo a guarda real (RECUSA com rc 3, sem compactar); este check so' antecipa o que ela vai medir. Sem as ancoras ou sem o textos: PENDENTE, nunca ok.
def _simular_memory_md():
    import importlib.util
    sp = importlib.util.spec_from_file_location("textos_v408_do_p00", os.path.join(HERE, "pos_rito", "textos_v408.py"))
    T_ = importlib.util.module_from_spec(sp); sp.loader.exec_module(T_)
    esc_ = ESP.get("escada") if isinstance(ESP.get("escada"), list) else CM.get("escada")
    V_ = {"data": "04/11/2026", "s16": CM["sha16"], "teor": "%d/%d" % (esc_[1], esc_[1])}
    ls_ = open(ML_, "rb").read().decode("utf-8").split("\n")
    nova_ = "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — " + T_.marca_missao(V_) + "íntegra anterior no MEMORY_2.md (movida %s)" % V_["data"][:5]
    k1_ = [i for i, l in enumerate(ls_) if "(missao-ultima-flag-um-py.md)" in l and l.startswith("- [")]
    k2_ = [i for i, l in enumerate(ls_) if "(handoff-v407-custodia.md)" in l and l.startswith("- [")]
    if len(k1_) != 1 or len(k2_) != 1:
        return None, ["ancoras do indice: missao %d, handoff v407 %d (esperado 1 e 1)" % (len(k1_), len(k2_))]
    ls_[k1_[0]] = nova_
    ls_.insert(k2_[0], T_.linha_handoff(V_))
    nb_ = "\n".join(ls_).encode("utf-8")
    return (len(nb_), nb_.count(b"\n")), [ML_B, ML_N]


try:
    _sim, _ant = _simular_memory_md() if (0 < ML_N and 0 < ML_B) else (None, ["MEMORY.md ausente"])
except Exception as _e_sim:  # noqa: BLE001
    _sim, _ant = None, ["simulacao falhou: %r" % (_e_sim,)]
if _sim is not None and _sim[0] <= 24000 and _sim[1] <= 195:
    chk(_NOME_MEM + " [SIMULACAO EXATA da superficie: %d B e %d linhas DEPOIS (hoje %d B e %d linhas); limites 24000 B e 195 linhas; folga %d B]" % (_sim[0], _sim[1], ML_B, ML_N, 24000 - _sim[0]), True, [_sim, 24000, 195])
else:
    pend(_NOME_MEM, "a simulacao exata da superficie sobre o MEMORY.md real NAO fecha (%s; depois: %s; limites 24000 B e 195 linhas): a decisao do que sai do indice e' da gerencia c1 (so' ela escreve o MEMORY.md); a superficie do pos-rito RECUSA com rc 3 se nao couber, e o p00 nao compacta" % (_ant, _sim))
_MEMD = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory"); _MEMPY = os.path.join(_MEMD, "fila", "memoria.py")
_pm = tenta(os.path.join(HERE, "PINO_MEMORIA_PY_v408.json"))
if _pm is None:
    pend("[v408, a FILA DA MEMORIA] memoria.py e' o que a preparacao pinou (PINO_MEMORIA_PY_v408.json)", "PINO_MEMORIA_PY_v408.json ainda nao existe (pino_memoria_py_v408.py e' ato da gerencia/preparacao)")
else:
    _ver = subprocess.run([sys.executable, "-X", "utf8", _MEMPY, "verificar"], capture_output=True, text=True, encoding="utf-8")
    chk("[v408, a FILA DA MEMORIA] memoria.py e' o que a preparacao pinou (sha16 lido do arquivo agora == PINO_MEMORIA_PY_v408.json == o declarado pela gerencia); a pausa do vigia NAO existe agora (o pos-rito a cria antes do indice e a remove depois do pino); e 'memoria.py verificar' (so leitura) esta VERDE agora (rc 0): o pos-rito parte de um indice sem violacao",
        sha(rd(_MEMPY))[:16] == _pm["sha16"] == _pm["declarado_pela_gerencia_sha16"] and not os.path.exists(os.path.join(_MEMD, "fila", "PAUSA_VIGIA.json")) and _ver.returncode == 0, [sha(rd(_MEMPY))[:16], _ver.returncode, os.path.exists(os.path.join(_MEMD, "fila", "PAUSA_VIGIA.json"))])
dep("o hash formal que o RITO vai gerar (a arvore do Nos depois do rito) tem a contagem do ESPERADOS, com os residuais lidos; o pino h8 do candidato bate (entradas = residuais + embutidas)", {"ESPERADOS_v408.json": ESP},
    lambda: (len(ESP["h8_residuais_do_nos"]) + CM["formal_files_n"] == ESP["h8_entradas"] == CM["h8"]["entradas"] and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in ESP["h8_residuais_do_nos"]), [ESP["h8_entradas"], ESP["h8_residuais_do_nos"]]))
chk("nenhum marcador de servidor parado nas pastas das duas cadeias (a guarda do rito)", not os.path.exists(os.path.join(DL.V407, ".servidor_parado_pelo_rito")) and not os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito")))
_pys = sorted(f for f in os.listdir(HERE) if f.endswith(".py") and ".bak" not in f)
for f in _pys:
    try:
        ast.parse(open(os.path.join(HERE, f), encoding="utf-8").read()); s_ = True
    except (SyntaxError, OSError):
        s_ = False
    chk("ast.parse de %s" % f, s_)
for f in ("rito_v408.sh", "construir_kernel_v408.sh", "copiar_k408c.sh", "refazer_candidato_v408.sh", "refazer_sandbox_v408_pos_selo.sh", os.path.join("pos_rito", "chain_pos_rito_v408.sh")):
    chk("sh -n de %s" % f, os.path.exists(os.path.join(HERE, f)) and subprocess.run(["sh", "-n", os.path.join(HERE, f)], capture_output=True).returncode == 0)
dv = tenta(os.path.join(HERE, "DERIVACAO_v408.json"))
dep("a conferencia do instalar/reverter/rito: zero falha nos invariantes (a lista de modulos novos LIDA tem %d elementos e e a dos ESPERADOS; o sidecar entra nos backups; o recibo pre_selo e' o da v408; a Bancada que JA pina a v407) e a sintaxe de todos" % DL.N_BUNDLE, {"DERIVACAO_v408.json": dv}, lambda: (not dv["falhas"] and all(("ok" in v or "rc=0" in v) for v in dv["sintaxe"].values()), [sum(len(x) for x in dv["invariantes"].values())]))
_MARCA_ADAPTAR = "# [A ADAPTAR v408]"
_com_marca = []
for _d, _ds, _fs in os.walk(HERE):
    _ds[:] = [d_ for d_ in _ds if d_ not in ("bump", "__pycache__", "base_v407", "kernel", "insumos", "revisao_terceiro", "arvore_simulada_h8") and not d_.startswith(("antes_", "dry_", "falso_", "imp_", "sim_", "conferidor_import_", "pilar_anterior_", "quarentena_", "tentativa_"))]
    for _f in _fs:
        if (_f.endswith(".py") or _f.endswith(".sh") or _f.endswith(".semente")) and ".bak" not in _f and _f != "_bump_copia_v408.py":
            try:
                if any(l_.startswith(_MARCA_ADAPTAR) for l_ in open(os.path.join(_d, _f), encoding="utf-8", errors="replace").read().split("\n")[:6]):
                    _com_marca.append(os.path.relpath(os.path.join(_d, _f), HERE))
            except OSError:
                pass
chk("RECUSA: nenhum arquivo da cadeia traz a marca `# [A ADAPTAR v408]` (a copia mecanica de rotulo da v407, ainda nao adaptada; a marca so' sai quando o arquivo foi adaptado de verdade)", not _com_marca, sorted(_com_marca))
marcas = [f for f in glob.glob(os.path.join(HERE, "pos_rito", "*.py")) if "TEXTO_A_REESCREVER" in open(f, encoding="utf-8", errors="replace").read().replace('"TEXTO_A_REESCREVER" +', "").replace("_MARCA_PENDENTE = ", "")]
chk("nenhum texto do pos_rito com a marca TEXTO_A_REESCREVER como comentario pendente", not [m for m in marcas if re.search(r"(?m)^\s*#\s*TEXTO_A_REESCREVER", open(m, encoding="utf-8", errors="replace").read())], [os.path.basename(m) for m in marcas][:4])
_veredito = "TODAS PASSARAM" if (ok_all and not PEND) else ("NENHUMA FALHA, %d PENDENTE(S): %s" % (len(PEND), "; ".join(p_["checagem"][:80] for p_ in PEND)) if ok_all else "FALHOU")
print("\nPRECONDICOES v408:", _veredito)
json.dump({"ok": bool(ok_all and not PEND), "sem_falha": bool(ok_all), "pendentes": PEND, "veredito": _veredito, "checagens": res}, open(os.path.join(HERE, "PRECONDICOES_v408.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0 if (ok_all and not PEND) else (3 if ok_all else 1))
