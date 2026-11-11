# -*- coding: utf-8 -*-
# [ADAPTADO v410 R1/R4, 10/11/2026, agente de adaptacao, a servico do construtor claude-construtor-v410] as falas (DL.N_FALAS_V410: 06 a 10/11), as decisoes (D63 em diante: ESPERADOS[decisoes_v410_ids]) e as erratas (E29 em diante: DL.ERRATAS_V410) sao LIDAS do delta e dos ESPERADOS; nenhuma contagem digitada; a prosa abaixo, da epoca da R3, fica como registro
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] D80 e D82 a D87: os registros a_escala_v410 (a pedra AEscala; validade no kernel, a creditacao e' do Clay) e h0dn_fontes_hms13_v410 (o recibo documental HMS/13: cobertura documental de fontes, não covariância física fechada; nada aberto) conferidos no core, no selo, no artigo (A Escala entre a IALD2 e o H0DN; o paragrafo do HMS/13 no fim da secao do H0DN) e no .md (quatro linhas da v410, na ordem); bundle de DOIS modulos, 22 + 38 ancoras, 84 bandeiras em duas series; D63 a D92, E29, E30, E31 e E32 (tudo lido do delta, do FLAGS e dos ESPERADOS)
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_conferidores_v410.py] D72: o SEGUNDO registro com funcao, h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido), conferido no core, no selo, no artigo (a secao depois da IALD2, antes da v409; _tt rende \times) e no .md
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a v410 (IALD2): o registro novo iald2_v410; os herdados traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406; RN409 recriados e RN410 novos; os bundles da v409, v408, v407 e v406 como registro; a linha do .md da v410 antes da da v409; MONTADO por _adapt_forkB_conferir_rito_v410.py a partir do ORIGINAL da v409 (nao da subida mecanica); fork B do claude-construtor-v410
"""conferir_rito_v410.py -- confere, DEPOIS do rito v410, o que tinha de mudar e o que NAO podia (ESPERADOS_v410.json; so leitura do Nos). Molde: conferir_rito_v409.py (a cadeia de CONTEUDO), montado em 06/11/2026 por claude-construtor-v410 (fork B) a v410, IALD2: o modelo e' o de BUNDLE PEQUENO (1 modulo novo em TGLExt/: IALD2).
Mudancas ditas: as chaves novas no core (o registro com FUNCAO iald2_v410 e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410) e o resumo delas no selo (iald2_v410 e registros_v410); o selo pela propria tecnologia (v399) muda so' nos hashes do novo um.py; a versao (um_version v410, sha256);
o modulo novo de TGLExt/ no kernel do Nos (sha pinado; os 2 modulos da v409, os 4 do terminal da v408, os 9 do psion da v407, os 301 do fecho da v406 e as pedras SELADAS das versoes anteriores ficam com o mesmo sha, como registro), a raiz do candidato (mais um import) e o Audit (inalterado); NENHUMA chave antiga muda: a chave do lema
(testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) segue LIDA do kernel e le True, com o dict elo_v407 como na v409 selada; as quatro chaves da v406 seguem True; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA;
os registros herdados traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 sao RECRIADOS e seguem selados (a escada do contrato deles sobe pela C12; kh_n1_cobertura_v409 ganha pisos pela C13).
A TROCA DITA e' so' de numeros (a escada e a cobertura crescem com o bundle; o estatuto da prova, que carrega o hash do proprio um.py): NENHUM veredito muda de texto.
O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado e a regra da ordem do 4,44 (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma).
NENHUM outro veredito da v409 muda. O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v409 (os checks, a letra do veredito, as 18 bandeiras); a funcao do neutrino NAO e' reescrita e o numero da massa NAO muda. A MOLDURA: os textos novos nao afirmam demais (a guarda das frases da v410 sobre os registros novos e a secao nova do artigo;
o qualificador da D64 -- relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora -- nos dois artigos; validade no kernel, nao creditacao; o gate nao se move). A secao do selo pela propria tecnologia (v399/v400) e a declaracao do operador continuam: os itens C1 a C16, o round trip e o sidecar um_absoluto_selo_acom.json.
uso: python -B -X utf8 conferir_rito_v410.py [sufixo]   (SEM -I: o conferidor importa o um.py instalado, que precisa do numpy do usuario; com -I o import falha e o controle negativo fica vazio, nao vale; o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso; _CONTROLE_NEGATIVO_PRE_RITO e _POSITIVO_FALSO_NOS sao os sufixos da cadeia)
Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V410_NOS=<pasta>  (padrao: o Nos real, so' leitura)."""
# [v410-patch]
import hashlib, importlib.util, io, json, math, os, re, shutil, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
import acom_conferencias_v410 as AC  # noqa: E402
NOS = os.environ.get("V410_NOS") or DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
UM_BYTES = open(os.path.join(NOS, "um.py"), "rb").read(); UM_FULL = sha(UM_BYTES); umsha = UM_FULL[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v410.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}; TRIO = DL.TRIO_SET
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
J = lambda x: json.dumps(x, sort_keys=True, default=str)
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
rd_ = lambda p: open(p, "r", encoding="utf-8", errors="replace").read()
raw_txt = {l: (rd_(os.path.join(NOS, "um_absoluto_%s.txt" % l)) if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "") for l in ("pt", "en")}
txt = {l: re.sub(r"\s+", " ", raw_txt[l]) for l in ("pt", "en")}
toc = {l: (re.sub(r"(\\[A-Za-z]+) (?=[$}0-9])", r"\1", rd_(os.path.join(NOS, "um_absoluto_%s.toc" % l)).replace("\n", "")) if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}   # (v409: o .toc grava «$\beta $»; so' esse espaco mecanico sai)
_tt = lambda m_: re.sub(r"\\[td]?frac\s*(\d)\s*(\d)", r"\1/\2", m_.replace(chr(92) + "beta", "β").replace(chr(92) + "times", "×"))   # (parte 2: o titulo da secao A Escala traz $\tfrac12$; o TXT do artigo o rende 1/2)   # (v410, D72: o titulo da secao do H0DN traz $\times$; o TXT do artigo (um.py:_tex_to_txt) o rende ×) (v409) o titulo e as marcas da secao nova trazem $\beta$ (LaTeX); o TXT do artigo os rende $β$
fc = rd_(os.path.join(NOS, "um_absoluto_forma_canonica.md")) if os.path.exists(os.path.join(NOS, "um_absoluto_forma_canonica.md")) else ""
mf = rd_(os.path.join(NOS, "um_absoluto_manifest.md")) if os.path.exists(os.path.join(NOS, "um_absoluto_manifest.md")) else ""
std = rd_(os.path.join(NOS, "rodada_v410_stdout.txt")) if os.path.exists(os.path.join(NOS, "rodada_v410_stdout.txt")) else ""
reused = qp.get("mode") == "REUSE"
E = ESP["escada"]
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
IX = "the_iald_index"


def _feq(a, b):
    """igualdade dos NUMEROS do registro: floats com tolerancia relativa 1e-12 (a mesma maquina deve dar igual), o resto exato; recursiva em dict/list."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


def _sha_k(rel):
    p = os.path.join(NK, *rel.split("/"))
    return sha(open(p, "rb").read()) if os.path.exists(p) else None


# o RESULTADO pinado do Teste da Unica Palavra (v397; o QUADRO do topo): o original (so' leitura) se o sha256 bate; senao a copia duravel; os numeros do quadro sao comparados com ESTES
EV = ESP["veracidade"]; EQ = ESP["quadro"]
_orig_ok = os.path.exists(EV["resultado"]["original"]) and sha(open(EV["resultado"]["original"], "rb").read()) == EV["resultado"]["sha256"]
_dur_ok = os.path.exists(EV["resultado"]["duravel"]) and sha(open(EV["resultado"]["duravel"], "rb").read()) == EV["resultado"]["sha256"]
RES = json.load(open(EV["resultado"]["original"] if _orig_ok else EV["resultado"]["duravel"], encoding="utf-8")) if (_orig_ok or _dur_ok) else {}
NUM = {k: DL.lido(RES, c) for k, c in DL.F9_CAMINHOS.items()} if RES else {}
bundle_ok = all(_sha_k(rel) == s for rel, s in ESP["bundle_sha256"].items())   # o modulo do bundle da v410 (IALD2) no kernel do Nos, com o sha do candidato
bundle_v409_ok = bool(len(ESP["bundle_v409_sha256"]) > 0 and all(_sha_k(rel) == s and (kf.get("formal_files_sha256") or {}).get(rel) == s for rel, s in ESP["bundle_v409_sha256"].items()))   # os 2 modulos do bundle da v409 (a traducao e o par na face de Fock) seguem no kernel (e no hash formal do core) com o mesmo sha: registro
bundle_v408_ok = bool(len(ESP["bundle_v408_sha256"]) > 0 and all(_sha_k(rel) == s and (kf.get("formal_files_sha256") or {}).get(rel) == s for rel, s in ESP["bundle_v408_sha256"].items()))   # os 4 modulos do bundle da v408 (o terminal) seguem no kernel (e no hash formal do core) com o mesmo sha: registro
bundle_v407_ok = bool(len(ESP["bundle_v407_sha256"]) > 0 and all(_sha_k(rel) == s and (kf.get("formal_files_sha256") or {}).get(rel) == s for rel, s in ESP["bundle_v407_sha256"].items()))   # os 9 modulos do bundle da v407 (o psion e o canto) seguem no kernel (e no hash formal do core) com o mesmo sha: registro
bundle_v406_ok = bool(len(ESP["bundle_v406_sha256"]) > 0 and all(_sha_k(rel) == s and (kf.get("formal_files_sha256") or {}).get(rel) == s for rel, s in ESP["bundle_v406_sha256"].items()))   # os 301 modulos do fecho da v406 seguem no kernel (e no hash formal do core) com o mesmo sha: registro
RN = sorted(ESP["registros_v399"]); RN401 = sorted(ESP["registros_v401"]); RN402 = sorted(ESP["registros_v402"]); RN403 = sorted(ESP["registros_v403"]); RN404 = sorted(ESP["registros_v404"]); RN405 = sorted(ESP["registros_v405"]); RN406 = sorted(ESP["registros_v406"]); RN407 = sorted(ESP["registros_v407"]); RN408 = sorted(ESP["registros_v408"]); RN409 = sorted(ESP["registros_v409"]); RN410 = sorted(ESP["registros_v410"])   # (os registros por spec de cada versao: RN406, RN407, RN408 e RN409, RECRIADOS; RN410 = os desta versao, NOVOS)
TV = core.get("teste_de_veracidade_fase9_v397") or {}; CG = core.get("cunhagens_v399") or {}; KH = core.get("kh_n1_cobertura_v399") or {}
SA = core.get("selo_pela_propria_tecnologia_v399") or {}; DC = core.get("declaracao_do_operador_v399") or {}
FA = core.get("falsidade_da_inercia_v401") or {}; CG1 = core.get("cunhagens_v401") or {}; KH1 = core.get("kh_n1_cobertura_v401") or {}
CG2 = core.get("cunhagens_v402") or {}; KH2 = core.get("kh_n1_cobertura_v402") or {}; CG3 = core.get("cunhagens_v403") or {}; KH3 = core.get("kh_n1_cobertura_v403") or {}; CG4 = core.get("cunhagens_v404") or {}; KH4 = core.get("kh_n1_cobertura_v404") or {}; CG5 = core.get("cunhagens_v405") or {}; CF5 = core.get("campos_fechados_e_leituras_v405") or {}; KH5 = core.get("kh_n1_cobertura_v405") or {}
CG6 = core.get("cunhagens_v406") or {}; KH6 = core.get("kh_n1_cobertura_v406") or {}; FE = core.get("fechamento_v406") or {}
CG7 = core.get("cunhagens_v407") or {}; KH7 = core.get("kh_n1_cobertura_v407") or {}; PCV = core.get("psion_canto_v407") or {}
CG8 = core.get("cunhagens_v408") or {}; KH8 = core.get("kh_n1_cobertura_v408") or {}; TTV = core.get("tetelestai_terminal_v408") or {}
CG9 = core.get("cunhagens_v409") or {}; KH9 = core.get("kh_n1_cobertura_v409") or {}; TUV = core.get("traducao_turing_v409") or {}
CG10 = core.get("cunhagens_v410") or {}; KH10 = core.get("kh_n1_cobertura_v410") or {}; IV = core.get("iald2_v410") or {}; HV = core.get("h0dn_bg1_v410") or {}; AEV = core.get("a_escala_v410") or {}; HMV = core.get("h0dn_fontes_hms13_v410") or {}   # (D72; D82 a D87: a_escala_v410; D80: h0dn_fontes_hms13_v410) o SEGUNDO registro com FUNCAO da v410: pré-registrado; nenhum dado observado lido
LD = TV.get("lido") or {}
q_pt = QV.confere_txt(raw_txt["pt"], RES, "pt") if (RES and raw_txt["pt"]) else {"ok": False}; q_en = QV.confere_txt(raw_txt["en"], RES, "en") if (RES and raw_txt["en"]) else {"ok": False}
q_md = QV.confere_md(fc, RES) if (RES and fc) else {"ok": False}
V398_NOMES = ["sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394",
              "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "cunhagens_v399", "kh_n1_cobertura_v399", "declaracao_do_operador_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404",
              "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405",
              "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409"]
_td_txt = ESP.get("troca_dita_textual") or {}   # os vereditos da troca dita que mudam em TEXTO (nenhum na v410: o dict e' vazio por asseveracao do gerar_esperados); os demais mudam so' em numeros
trocas_ok = bool(set(_td_txt) <= set(ESP["troca_dita"]) and all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v409"][k]
                 and ((V(k) == _td_txt[k]["depois"] and ESP["vereditos_v409"][k] == _td_txt[k]["antes"]) if k in _td_txt else _num(_nc(V(k))) == _num(_nc(ESP["vereditos_v409"][k]))) for k in ESP["troca_dita"]))   # MUDOU de fato; so' em numeros, exceto o de texto pinado
REL5_ = {s["key"]: s["rel"] for s in DL.D5.STONES}   # as OITO pedras da v408 (PonteDaMassa ... PontoZeroDoPsion), RECRIADAS e seladas: ficam no kernel como registro
REL4_ = {s["key"]: s["rel"] for s in DL.D4.STONES}   # as DUAS pedras da v404 (ProjecaoTransversalDaMeiaNat, Jo8v32), RECRIADAS e seladas
REL3_ = {s["key"]: s["rel"] for s in DL.D3.STONES}   # as TRES pedras da v403 (Caminho, Vida, VerdadeAdendo), RECRIADAS e seladas
src_ = kf.get("declaration_sources_v394") or {}
pedras_no_kernel = all(kf.get(ESP["bandeiras_das_pedras_v405"][k]) is True and set(axr.get(ESP["teoremas_das_pedras_v405"][k]) or []) <= TRIO and src_.get(ESP["teoremas_das_pedras_v405"][k]) == REL5_[k]
                       and all(t_ in axr and set(axr[t_]) <= TRIO and src_.get(t_) == REL5_[k] for t_ in ESP["contrato_das_pedras_v405"][k]) for k in REL5_)   # as oito pedras da v408 seguem no kernel do rito
suporte_ok = all(set(axr.get(t_) or []) <= TRIO and t_ in axr and (kf.get("declaration_sources_v394") or {}).get(t_) == p_ for k in REL5_ for t_, p_ in ESP["suporte_das_pedras_v405"][k].items())

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# O SELO PELA PROPRIA TECNOLOGIA: os 14 itens do estudo (C1 a C14) e o round trip do um.py INSTALADO. O codigo do proprio um.py instalado e' importado de uma COPIA de bytes (o Nos so' e' lido; nada e' escrito nele).
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ACOM = {}   # id -> (ok, detalhe)
um_c = None
_cp = os.path.join(HERE, "conferidor_import_" + umsha); os.makedirs(_cp, exist_ok=True)
if not (os.path.exists(os.path.join(_cp, "um.py")) and open(os.path.join(_cp, "um.py"), "rb").read() == UM_BYTES):
    open(os.path.join(_cp, "um.py.tmp"), "wb").write(UM_BYTES); os.replace(os.path.join(_cp, "um.py.tmp"), os.path.join(_cp, "um.py"))
try:
    _spec = importlib.util.spec_from_file_location("um_conferido", os.path.join(_cp, "um.py")); um_c = importlib.util.module_from_spec(_spec)
    _o = sys.stdout; sys.stdout = io.StringIO()
    try:
        _spec.loader.exec_module(um_c)
    finally:
        sys.stdout = _o; sys.stdout.reconfigure(encoding="utf-8")
except Exception as _e:   # noqa: BLE001
    um_c = None; ACOM["import_do_um_py_instalado"] = (False, repr(_e)[:200])
SC = {}
_scp = os.path.join(NOS, DL.SIDECAR_NOME)
if os.path.exists(_scp):
    try:
        SC = json.load(open(_scp, encoding="utf-8"))
    except Exception as _e:   # noqa: BLE001
        ACOM["sidecar_legivel"] = (False, repr(_e)[:200])
OBJ = {o_["nome"]: o_ for o_ in (SC.get("objetos") or [])}
BYTES_OBJ = {"um.py": UM_BYTES, "um_absoluto.json": open(os.path.join(NOS, "um_absoluto.json"), "rb").read(), "um_absoluto_selo.json": open(os.path.join(NOS, "um_absoluto_selo.json"), "rb").read()}
ESA = ESP["selo_acom"]; EDC = ESP["declaracao"]
if um_c is not None and hasattr(um_c, "ACOM_PROVENIENCIA") and hasattr(um_c, "selo_acom_sidecar_v399"):   # o um.py instalado e' o da v410 (no controle negativo, antes do rito, o Nos ainda e' a v409: o bloco inteiro nao roda e todos os itens C ficam falsos)
    _um_txt = UM_BYTES.decode("utf-8"); _RT = open(os.path.join(DL.V400, "runtime_v400.py"), "rb").read().decode("utf-8")   # a secao do selo ACOM (a v410 NAO a muda: o runtime dela e o da v400)
    # C1: o bloco embutido do um.py instalado == a copia refeita das fontes do operador (5 substituicoes declaradas); o runtime da secao (o da v408) esta no um.py, byte a byte
    _emb, _hemb, _ = AC.bloco_das_fontes(); _blk = AC.extrair_bloco(_um_txt)
    ACOM["C1"] = (bool(_blk == _emb and _hemb == um_c.ACOM_PROVENIENCIA["bloco_embutido_sha256"] == ESP["acom_estudo"]["bloco_embutido_sha256"] == SA.get("values", {}).get("bloco_embutido_sha256") and um_c.conferir_bloco_embutido()["confere"] is True
                       and sha(_RT.encode("utf-8")) == ESP["acom_estudo"]["runtime_sha256"] and _RT.replace("\n", "\r\n") in _um_txt), _hemb[:16])
    # C2: os pinos das 6 fontes do operador (constantes do um.py instalado) == os arquivos duraveis == os ESPERADOS
    _pv = um_c.ACOM_PROVENIENCIA; _fo = os.path.join(DL.V400, "insumos", "acom", "fontes_operador")
    _pins = {"acom_mirror.py": _pv["codigo_embutido_de"][0]["sha256"], "acom_crypto.py": _pv["codigo_embutido_de"][1]["sha256"], "Acom_v17_mirror_crypto.py": _pv["origem_funcional_do_operador"]["sha256"], "run_tests.py": _pv["testes_do_operador"]["sha256"], "tgl_core.py": _pv["tgl_core"]["sha256"], "ACOM_Mirror_Crypto_PI_INPI.tex": _pv["patentes"][1]["sha256"]}
    ACOM["C2"] = (bool(len(_pins) == 6 and all(sha(open(os.path.join(_fo, n_), "rb").read()) == h_ == ESP["acom_estudo"]["fontes_do_operador"][n_] for n_, h_ in _pins.items())), len(_pins))
    # C3: nenhum nome de nivel de modulo da secao esta definido duas vezes no um.py instalado (so' os imports do mesmo modulo; a secao NAO define ALPHA_FINE_CODATA_2018: le o SEALED_CODATA_ALPHA do programa)
    import ast as _ast
    _tr = _ast.parse(_um_txt); _cont = {}
    for _n in _tr.body:
        _nomes = [_n.name] if isinstance(_n, (_ast.FunctionDef, _ast.ClassDef)) else [t_.id for t_ in getattr(_n, "targets", []) if isinstance(t_, _ast.Name)] if isinstance(_n, _ast.Assign) else []
        for _x in _nomes:
            _cont[_x] = _cont.get(_x, 0) + 1
    _rtn = AC.nomes_de_nivel_de_modulo(_RT); _permitido = {"hashlib", "math", "time", "np", "json", "os"}
    _dup = sorted(n_ for n_ in _rtn if _cont.get(n_, 0) > 1 and n_ not in _permitido)
    ACOM["C3"] = (bool(not _dup and not hasattr(um_c, "ALPHA_FINE_CODATA_2018") and "ALPHA_FINE_CODATA_2018" not in _rtn and hasattr(um_c, "SEALED_CODATA_ALPHA")), _dup[:5])
    # C4, C5, C6, C7: refazer a Dobra dos TRES objetos FINAIS (9 itens de verificar()), a reconstrucao exata, o alfabeto exato e a separacao nao vazia; o SHA-256 do arquivo == o do sidecar == o do selo primario
    _v4 = {}; _ok5 = _ok6 = _ok7 = True; _t_ver = {}
    for _nm, _b in BYTES_OBJ.items():
        _o = OBJ.get(_nm)
        if _o is None:
            _v4[_nm] = False; _ok5 = _ok6 = _ok7 = False; continue
        _t0 = time.perf_counter(); _vv = um_c.verificar(_b, _o); _t_ver[_nm] = round(time.perf_counter() - _t0, 2)
        _v4[_nm] = bool(_vv["ok"] and len(_vv["checks"]) == 9 and all(_vv["checks"].values()) and _o["sha256"] == sha(_b) and _o["bytes"] == len(_b))
        _pr = _o["acom"]["prova_de_reconstrucao"]; _al = _pr["alfabeto_do_objeto"]
        _ok5 = _ok5 and _pr["igual_ao_objeto_byte_a_byte"] is True and _pr["bytes_divergentes"] == 0 and _pr["reconstruido_sha256"] == sha(_b)
        _ok6 = _ok6 and _al["exato"] is True and _al["injetivo"] is True and _pr["erro_real_maximo_antes_do_rint"] < 0.5 and _al["lut_sha256"] == _o["acom"]["kappa"]["campos"]["lut_sha256"]
        _au = _o["acom"]["auditoria_de_separacao"]; _ok7 = _ok7 and _au["psi_redundante"] is False and not any(_au["basta"].values())
    _selo_prim = selo.get("sha256", {}).get("um.py")
    ACOM["C4"] = (bool(_v4 and all(_v4.values()) and len(_v4) == 3 and _selo_prim == UM_FULL == (OBJ.get("um.py") or {}).get("sha256") == ((SA.get("selo") or {}).get("sha256"))), {"verificar": _v4, "tempo_s": _t_ver})
    ACOM["C5"] = (bool(_ok5), UM_FULL[:16]); ACOM["C6"] = (bool(_ok6 and (OBJ.get("um.py") or {}).get("acom", {}).get("kappa", {}).get("campos", {}).get("lut_sha256") == ESA["lut_sha256"]), ESA["lut_sha256"][:16]); ACOM["C7"] = (bool(_ok7), None)
    # o ROUND TRIP do um.py instalado refeito por uma CONTA INDEPENDENTE: so' das tres partes cruas (formula da Dobra + rint + centro), sem as funcoes de reconstrucao do selo
    import numpy as _np
    _sl, _pp = um_c.selar(UM_BYTES, "um.py", devolver_partes=True); _kp = _sl["acom"]["kappa"]["campos"]
    _st = um_c._unpack2bits(_pp["psi_raw"], _kp["n_elements"]); _th = _np.frombuffer(_pp["theta_raw"], dtype=_np.uint8)
    _real = (math.sqrt(_kp["m_max_abs"]) * _np.sin(_th.astype(_np.float64) / 255 * (math.pi / 2))) ** 2
    _rec = (_np.where(_st >= 2, -1, 1) * _np.rint(_real).astype(_np.int64) + um_c.CENTRO).astype(_np.uint8).tobytes()
    ACOM["round_trip_do_um_py_instalado_independente"] = (bool(_rec == UM_BYTES and sha(_rec) == UM_FULL and _sl["acom"]["psi"]["sha256"] == OBJ["um.py"]["acom"]["psi"]["sha256"] and _sl["acom"]["theta"]["sha256"] == OBJ["um.py"]["acom"]["theta"]["sha256"]
                                                           and _sl["acom"]["kappa"]["sha256"] == OBJ["um.py"]["acom"]["kappa"]["sha256"]) if "um.py" in OBJ else False, UM_FULL[:16])
    del _real, _rec, _st, _th
    # C8: os 13 controles negativos (sobre a amostra de 1 MiB, no core; e sobre o um.py INTEIRO, aqui) todos recusados
    _cn = SA.get("controles_negativos") or {}; _t0 = time.perf_counter(); _cc = um_c.controles_negativos(UM_BYTES); _t_cc = round(time.perf_counter() - _t0, 2)
    ACOM["C8"] = (bool(_cn.get("n_controles") == 13 and _cn.get("todos_recusados") is True and _cc["n_controles"] == 13 and _cc["todos_recusados"] is True and all(c_["obtido"].startswith("RECUSOU:") for c_ in _cc["controles"])), {"inteiro_s": _t_cc, "obtidos": {c_["id"]: c_["obtido"] for c_ in _cc["controles"]}})
    # C9: beta de runtime (alfa CODATA x raiz de e), nenhum literal de beta no codigo da v410
    ACOM["C9"] = (bool(abs((SA.get("values") or {}).get("beta", 0.0) - um_c.SEALED_CODATA_ALPHA * math.sqrt(math.e)) <= 1e-15 and abs((SA.get("values") or {}).get("beta", 0.0) - core.get("beta", 1.0)) <= 1e-9 * abs(core.get("beta", 1.0)) and (SA.get("values") or {}).get("beta_core") == core.get("beta") and (SA.get("values") or {}).get("rel_beta_vs_core") is not None and (SA.get("values") or {}).get("rel_beta_vs_core") < 1e-9 and not AC.literais_de_beta(_RT)), core.get("beta"))   # o beta do registro e' EXATAMENTE alfa x raiz de e; o do core concorda a 1e-9 relativo (a mesma tolerancia da v408)
    # C10: determinismo: Psi, Theta e kappa do um.py no sidecar == no core == os ESPERADOS (calculados pelo ensaio sobre os MESMOS bytes do candidato)
    _a = (OBJ.get("um.py") or {}).get("acom") or {}; _ac = ((SA.get("selo") or {}).get("acom")) or {}
    ACOM["C10"] = (bool(_a and _a["psi"]["sha256"] == _ac["psi"]["sha256"] == ESA["psi"]["sha256"] and _a["theta"]["sha256"] == _ac["theta"]["sha256"] == ESA["theta"]["sha256"] and _a["kappa"]["sha256"] == _ac["kappa"]["sha256"] == ESA["kappa"]["sha256"] and _a["kappa"]["campos"]["lut_sha256"] == ESA["lut_sha256"]
                        and _a["kappa"]["campos"]["m_max_abs"] == ESA["m_max_abs"] and _a["estrutura"]["f_exp"] == ESA["f_exp"]), {"psi": _a.get("psi", {}).get("sha256", "")[:16], "theta": _a.get("theta", {}).get("sha256", "")[:16], "kappa": _a.get("kappa", {}).get("sha256", "")[:16]})
    # C11: a declaracao: a fala embutida == o arquivo do operador (sha256); as dez ancoras e a pedra no axiom_report do rito e no trio; a trava existe uma vez so' no programa instalado
    _dsha = sha(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read()); _dd = DC.get("declaration") or {}   # (VERBATIM_ORIGEM/DECLARACAO_IDX: as de 24/10, da v399; as de 25/10 sao VERBATIM_ORIGEM_V406)
    _trava = "lock(" + '"O UM nao foi inscrito. A execucao foi travada.", "EXECUTION_LOCKED_' + 'NOT_ONE")'
    ACOM["C11"] = (bool(DC.get("all_verified") is True and _dd.get("verbatim_sha256") == _dsha == um_c._V399_DECLARACAO_SHA256 == EDC["verbatim_sha256"] and _dd.get("statement_verbatim") == um_c._V399_DECLARACAO_TXT and sha(um_c._V399_DECLARACAO_TXT.encode("utf-8")) == _dsha
                        and len(_dd.get("kernel_anchors_REAL") or []) == 10 and all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] and a_["termo"] in axr and set(axr[a_["termo"]]) <= TRIO for a_ in _dd["kernel_anchors_REAL"]) and [a_["termo"] for a_ in _dd["kernel_anchors_REAL"]] == EDC["ancoras"]
                        and all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] and a_["termo"] in axr and set(axr[a_["termo"]]) <= TRIO for a_ in _dd.get("pedra_instalada") or []) and [a_["termo"] for a_ in _dd["pedra_instalada"]] == EDC["pedra"]
                        and sum(1 for l_ in _um_txt.split("\n") if _trava in l_) == 1), _dsha[:16])
    # C12: honestidade, direcao e palavra proibida: o sidecar traz a honestidade; nenhuma alegacao de confidencialidade; a direcao do testemunho dita nos registros; nenhuma frase poe a IALD como quem testifica DO operador (fora da fala em que ele a recusa)
    _hn = SC.get("honestidade") or {}
    _RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")

    def _inv(t_):
        for m_ in _RX_INV.finditer(t_):
            ant_ = t_[max(0, m_.start() - 40):m_.start()].lower()
            if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
                return True
        return False

    _tx12 = json.dumps({"sc": SC, "sa": {k_: SA.get(k_) for k_ in ("theorem", "direcao_do_testemunho", "statuses", "verdict")}, "dc": {k_: DC.get(k_) for k_ in ("declaration", "statuses", "verdict")}}, ensure_ascii=False)
    ACOM["C12"] = (bool(all(k_ in _hn for k_ in ("primitiva_de_integridade", "o_que_a_segunda_testemunha_acrescenta", "ofuscacao_xor", "confidencialidade", "dobra", "estatuto")) and "SHA-256" in _hn.get("primitiva_de_integridade", "") and "NAO alegada" in _hn.get("confidencialidade", "") and "NAO acrescenta resistencia criptografica independente" in _hn.get("o_que_a_segunda_testemunha_acrescenta", "")
                        and not um_c._v392_guarda_texto(_tx12) and not GUARDA.search(_tx12) and not _inv(_tx12) and not re.search(r"(?i)(inviol|indecifr|quantum[- ]safe|seguranca criptografica garantida)", _tx12)
                        and "a IALD nao testifica do operador" in (SA.get("direcao_do_testemunho") or "") and (_dd.get("direcao_do_testemunho") or {}).get("a_IALD", "").startswith("NAO testifica do operador") and (_dd.get("direcao_do_testemunho") or {}).get("o_um_py", "").startswith("testifica EM HASH")), "honestidade+direcao")
    # C13: fail-closed: os dois registros selaram, nao movem o gate; o sidecar sem recusas
    ACOM["C13"] = (bool(SA.get("all_verified") is True and DC.get("all_verified") is True and SA.get("does_not_gate_core") is True and DC.get("does_not_gate_core") is True and SC.get("recusas") == [] and str(SC.get("veredito", "")).startswith("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED")
                        and SC.get("esquema") == "um_absoluto_selo_acom/v1 (v399)" and [o_["nome"] for o_ in (SC.get("objetos") or [])] == ESP["sidecar"]["objetos"]), (SC.get("veredito") or "")[:60])
    # C14: orcamento de tempo: ~3 s por rito (selagem do um.py <= 10 s no core; o sidecar nao registra o tempo: o stdout traz a linha de fechamento e nenhum AVISO dos blocos novos)
    ACOM["C14"] = (bool(0 < (SA.get("values") or {}).get("tempo_total_s", 99.0) <= 10.0 and ("[selo_acom] TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED" in std) and "AVISO: o selo ACOM nao rodou" not in std and "AVISO: a declaracao do operador nao rodou" not in std
                         and "nao consegui escrever o sidecar" not in std and "o resumo do selo ACOM nao entrou no selo" not in std), (SA.get("values") or {}).get("tempo_total_s"))
    # C15 [v409, LICAO NOVA]: as guardas ESTATICAS da Bancada (a FUNCAO ler_nos do esboco R3.5 pinado) sobre o um.py INSTALADO: UMA so' linha de alfa e UMA so' de UM_VERSION na coluna 0, nenhuma indentada, e o beta do core == o de runtime (o defeito que recusou a v399)
    _esb = AC.esboco_da_bancada(os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf")
    import pathlib as _pl
    _sd = os.path.join("C:" + os.sep, "t", "vb18", "conf_%s" % umsha); shutil.rmtree(_sd, ignore_errors=True); os.makedirs(_sd)
    open(os.path.join(_sd, "um.py"), "wb").write(UM_BYTES); json.dump({"um_version": "v410", "sha256": {"um.py": UM_FULL}}, open(os.path.join(_sd, "um_absoluto_selo.json"), "w", encoding="utf-8")); json.dump({"core": {"beta": core.get("beta")}}, open(os.path.join(_sd, "um_absoluto.json"), "w", encoding="utf-8"))
    try:
        _ni = _esb.ler_nos(_pl.Path(_sd), "v410")
        ACOM["C15"] = (bool(_ni["alpha"]["n_linhas_nao_indentadas"] == 1 and _ni["alpha"]["n_reatribuicoes_indentadas"] == 0 and _ni["um_version_linhas"] == {"nao_indentadas": 1, "indentadas": 0}), {"alfa": _ni["alpha"], "beta_rel_diff": _ni["core"]["beta_rel_diff"]})
    except _esb.Recusa as _e:
        ACOM["C15"] = (False, str(_e)[:160])
    finally:
        shutil.rmtree(_sd, ignore_errors=True)
    # C16 [v400]: com o Nos REAL, a funcao ler_nos do esboco aceita o Nos INTEIRO (o selo pina o um.py, o core e o manifesto do kernel; alfa unico; beta do core == runtime): o que o B(n) fara. Na emulacao (V410_NOS) o Nos falso nao tem os pinos reais.
    if os.environ.get("V410_NOS"):
        ACOM["C16"] = (True, "emulacao (V410_NOS): o Nos falso nao tem os pinos reais do core e do manifesto; a leitura inteira so' vale no Nos real")
    else:
        try:
            _nr = _esb.ler_nos(_pl.Path(NOS), "v410")
            ACOM["C16"] = (bool(_nr["um_py"]["sha256"] == UM_FULL and _nr["kernel"] is not None and _nr["alpha"]["n_linhas_nao_indentadas"] == 1), {"kernel_manifesto": (_nr["kernel"] or {}).get("sha256"), "alfa_linha": _nr["alpha"]["linha"], "beta_rel_diff": _nr["core"]["beta_rel_diff"]})
        except _esb.Recusa as _e:
            ACOM["C16"] = (False, str(_e)[:160])
acom_ok = bool(um_c is not None and all(ACOM.get(k_, (False,))[0] for k_ in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "round_trip_do_um_py_instalado_independente")) and "import_do_um_py_instalado" not in ACOM and "sidecar_legivel" not in ACOM)
selo_reg_ok = bool(SA.get("all_verified") is True and V("selo_pela_propria_tecnologia_v399") == ESA["verdict"] and len(SA.get("checks") or []) == ESA["n_checks"] and all(v_ for _, v_ in (SA.get("checks") or [])) and (SA.get("values") or {}).get("perfil") == ESA["perfil"] and SA.get("does_not_gate_core") is True
                   and (SA.get("selo") or {}).get("sha256") == UM_FULL and (SA.get("controles_negativos") or {}).get("todos_recusados") is True and not GUARDA.search(V("selo_pela_propria_tecnologia_v399")))
decl_reg_ok = bool(DC.get("all_verified") is True and V("declaracao_do_operador_v399") == EDC["verdict"] and len(DC.get("checks") or []) == EDC["n_checks"] and all(v_ for _, v_ in (DC.get("checks") or [])) and DC.get("does_not_gate_core") is True and not GUARDA.search(V("declaracao_do_operador_v399")))
def _iald2_ok():
    """iald2_v410 (o registro com FUNCAO, novo): veredito == o do ensaio, as checagens do calculo (DL.N_CHECKS_FECHO), os valores == os do ensaio, as ancoras da pedra IALD2 (todas), o modulo do bundle por sha256, a escada exata, beta, a ancora principal, NENHUMA chave antiga,
    as respostas do operador, a instancia SAT da v409 decidida (SIM com solucao, NAO sem), o alcance relativo ao leitor (a frase da D64), e nao move o gate"""
    R_ = IV; E_ = ESP["registros_funcao_v410"][DL.TESTEMUNHA["key"]]; m_ = R_.get("mechanics") or {}; v_ = V(DL.FECHO_REGISTRO); vv_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == DL.N_BUNDLE
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v410"]) == len(DL.ANCORAS) and all((R_.get("anchors") or {}).values()) and R_.get("ancora_principal") == DL.ANCORA_PRINCIPAL and list(R_.get("ancoras_principais") or []) == list(DL.ANCORAS_PRINCIPAIS)
                and R_.get("chaves_antigas_que_mudam") == [] and vv_.get("respostas_ok") is True
                and ((vv_.get("instancia_sim") or {}).get("solucoes") or 0) >= 1 and (vv_.get("instancia_nao") or {}).get("solucoes") == 0 and (R_.get("alcance") or {}).get("frase") == DL.FRASE_D64_PT
                and v_.startswith(DL.VEREDITO_OK_PREFIXO) and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _h0dn_ok():
    """h0dn_bg1_v410 (D72; o SEGUNDO registro com FUNCAO, novo; pré-registrado; nenhum dado observado lido): veredito == o do ensaio == o PRE-REGISTRADO (DL.VEREDITO_H0DN_OK); as 12 checagens; observed_vector_read False (no registro e nos valores); os pinos todos batendo; os 6 ramos da funcao de veredito congelada nos vetores deterministicos;
    o sha256 do texto-fonte da funcao == o do ensaio; o gate == o da v409 selada; nenhum caminho tocado sob a pasta vedada (a entrega do Kimi) nem com nome vedado -- MEDIDO pelo proprio registro (c7) e relido aqui caminho a caminho; os valores == os do ensaio (menos os caminhos tocados, que dependem da pasta do rito); nao move o gate"""
    R_ = HV; E_ = ESP["registros_funcao_v410"]["h0dn"]; m_ = R_.get("mechanics") or {}; v_ = V(DL.H0DN_REGISTRO); vv_ = R_.get("values") or {}
    _nrm_ = lambda p_: os.path.normcase(os.path.normpath(str(p_))); _ved_ = _nrm_(DL.H0DN_PASTA_VEDADA); _toc_ = vv_.get("caminhos_tocados") or []
    _nomes_ = tuple(n_.lower() for n_ in DL.H0DN_NOMES_VEDADOS)
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == DL.VEREDITO_H0DN_OK and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and R_.get("observed_vector_read") is False and vv_.get("observed_vector_read") is False
                and m_.get("passed") is True and m_.get("n_checks") == DL.N_CHECKS_H0DN == E_["n_checks"] and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("beta_ok") is True
                and vv_.get("n_pinos") == E_["values"]["n_pinos"] == len(vv_.get("pinos") or {}) and all(p_.get("sha256_ok") is True and p_.get("bytes_ok") is True for p_ in (vv_.get("pinos") or {}).values()) and vv_.get("ramos_vistos") == [1, 2, 3, 4, 5, 6] and all(x_.get("ok") is True for x_ in vv_.get("vetores_c6") or [])
                and R_.get("veredito_h0dn_source_sha256") == vv_.get("veredito_h0dn_source_sha256") == E_["values"]["veredito_h0dn_source_sha256"] and vv_.get("gate_verdict") == ESP["qg_closure_gate_verdict_v409"]
                and vv_.get("sob_pasta_vedada") == [] and vv_.get("com_nome_vedado") == [] and isinstance(vv_.get("n_caminhos_tocados"), int) and vv_.get("n_caminhos_tocados") == len(_toc_) > 0
                and not [p_ for p_ in _toc_ if _nrm_(p_) == _ved_ or _nrm_(p_).startswith(_ved_ + os.sep) or any(n_ in os.path.basename(_nrm_(p_)) for n_ in _nomes_)]
                and "NOT_FALSIFIED" not in v_ and not GUARDA.search(v_) and v_.endswith("__GATE_UNMOVED")
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _aescala_ok():
    """a_escala_v410 (D82 a D87; o registro com FUNCAO da pedra TGLExt.AEscala; validade no kernel, a creditacao e' do Clay): veredito == o do ensaio == o do delta; as checagens de DL.N_CHECKS_AESCALA; as ancoras da pedra (todas, no trio, com proveniencia e bandeira); as bandeiras ext_aescala_410_*; a pedra por sha256 == o hash formal;
    as falas por sha256; os numeros (fracoes exatas e o projetor de Bell) == os do delta e do ensaio; a frase canonica e a forma da D83; os nomes do modulo e das declaracoes RATIFICADOS (D87); nenhuma chave antiga; o gate == o da v409 selada; os valores == os do ensaio; nao move o gate"""
    R_ = AEV; E_ = ESP["registros_funcao_v410"]["aescala"]; m_ = R_.get("mechanics") or {}; v_ = V(DL.AESCALA_REGISTRO); vv_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == DL.VEREDITO_AESCALA_OK and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and R_.get("beta_ok") is True
                and m_.get("passed") is True and m_.get("n_checks") == DL.N_CHECKS_AESCALA == E_["n_checks"] and all(c_["ok"] for c_ in m_.get("checks") or [])
                and vv_.get("n_ancoras_ok") == vv_.get("n_ancoras") == len(ESP["estrelas_aescala_v410"]) == len(DL.ANCORAS_AESCALA) == len(vv_.get("ancoras") or {}) and all((vv_.get("ancoras") or {}).values()) and R_.get("ancora_principal") == DL.ANCORA_PRINCIPAL_AESCALA and list(R_.get("ancoras_de_secao") or []) == list(DL.ANCORAS_DE_SECAO_AESCALA)
                and vv_.get("n_flags_true") == vv_.get("n_flags") == ESP["aescala"]["n_flags"] == ESP["n_bandeiras_por_grupo"]["aescala"] and all(f_.startswith(DL.FLAG_PREFIX_AESCALA) and x_ is True for f_, x_ in (vv_.get("flags") or {}).items()) and (vv_.get("pedra_sha256_embutida") == vv_.get("pedra_sha256_formal") == ESP["bundle_sha256"][DL.MODULO_AESCALA])
                and vv_.get("n_falas_ok") == vv_.get("n_falas") == len(ESP["aescala"]["falas"]) and all((vv_.get("falas") or {}).values()) and dict(vv_.get("numeros") or {}) == dict(DL.NUMEROS_AESCALA) and R_.get("nomes_ratificados") is True and list(R_.get("nomes") or []) == list(DL.NOMES_AESCALA) and vv_.get("nomes_declarados") == vv_.get("n_nomes") == len(DL.NOMES_AESCALA)
                and R_.get("nomes_novos_da_pedra") == list(DL.NOMES_NOVOS_AESCALA) == list(ESP["aescala"]["nomes_novos_da_pedra"]) and R_.get("n_nomes_novos") == len(DL.NOMES_NOVOS_AESCALA) == vv_.get("nomes_novos_declarados") == vv_.get("n_nomes_novos") and bool(DL.NOMES_NOVOS_AESCALA) and all((vv_.get("nomes_novos") or {}).values()) and all((vv_.get("campos_novos_na_estrutura") or {}).values()) and bool(vv_.get("campos_novos_na_estrutura")) and vv_.get("nomes_novos_ok") is True
                and R_.get("campos_novos_da_estrutura") == list(DL.CAMPOS_NOVOS_AESCALA) and R_.get("estatuto_dos_nomes_ratificados_d101") == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in str(R_.get("estatuto_dos_nomes_ratificados_d101")) and "a ratificar" not in str(R_.get("estatuto_dos_nomes_ratificados_d101")) and R_.get("ratificacao_pendente") == DL.RATIFICACAO_PENDENTE_AESCALA and R_.get("ponte") == DL.PONTE_AESCALA and (vv_.get("ponte") or {}).get("ok") is True
                and (vv_.get("tetelestai") or {}).get("ok") is True and (vv_.get("clausula_r5") or {}).get("ok") is True and (vv_.get("ratificacao_d101") or {}).get("ok") is True and (vv_.get("ratificacao_d101") or {}).get("fala_sha256") == DL.RATIFICACAO_D101_SHA256 == ESP["aescala"]["ratificacao_D101"]["sha256"]
                and list((vv_.get("ratificacao_d101") or {}).get("pendentes") or []) == list(DL.NOMES_PENDENTES_AESCALA) == list(ESP["aescala"]["nomes_pendentes"]) and set(vv_.get("teoremas_r5") or {}) == set(DL.TEOREMAS_R5_AESCALA) | set(DL.AUXILIARES_R5_AESCALA) and all((vv_.get("teoremas_r5") or {}).values())
                and R_.get("acom_mirror_runner") == DL.ACOM_MIRROR_RUNNER == ESP["aescala"]["acom_mirror_runner"] and R_.get("anuncio_da_clausula_do_tetelestai_pt") == DL.ANUNCIO_TETELESTAI_PT
                and vv_.get("canonica_pt_no_texto") is True and vv_.get("canonica_en_no_texto") is True and vv_.get("canonica_pt_na_pedra") is True and vv_.get("d83_na_pedra") is True and R_.get("frase_canonica_pt") == DL.FRASE_CLAY_CANONICA_PT and R_.get("frase_d83_pt") == DL.FRASE_D83_OBRIGATORIA_PT
                and R_.get("chaves_antigas_que_mudam") == [] and vv_.get("gate_verdict") == ESP["qg_closure_gate_verdict_v409"] and not vv_.get("p18_violacoes") and not vv_.get("frases_violacoes") and all((vv_.get("c9_partes") or {"x": False}).values())
                and "NOT_FALSIFIED" not in v_ and not GUARDA.search(v_) and v_.endswith("__GATE_UNMOVED")
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _hms13_ok():
    """h0dn_fontes_hms13_v410 (D80; o recibo documental das 18 fontes primarias dos 13 calibradores; ADITIVO e POSTERIOR ao FREEZE_R2; cobertura documental de fontes, não covariância física fechada; nada aberto): veredito == o do ensaio == o do delta; as checagens de DL.N_CHECKS_HMS13; os dez campos da ORDEM == DL.HMS13_CAMPOS;
    observed_vector_read e le_em_rito False (no registro e nos valores); os quatro artefatos embutidos por sha256 e bytes; os 13 calibradores e as 18 fontes; a funcao de veredito do H0DN intocada (o mesmo sha256 do texto-fonte); o gate == o da v409 selada; nenhum caminho tocado sob a pasta vedada (a entrega do Kimi: em rito nada da pasta kimi e' aberto) nem com nome vedado,
    MEDIDO pelo proprio registro (c7) e relido aqui caminho a caminho; os valores == os do ensaio (menos os caminhos tocados); nao move o gate"""
    R_ = HMV; E_ = ESP["registros_funcao_v410"]["hms13"]; m_ = R_.get("mechanics") or {}; v_ = V(DL.HMS13_REGISTRO); vv_ = R_.get("values") or {}
    _nrm_ = lambda p_: os.path.normcase(os.path.normpath(str(p_))); _ved_ = _nrm_(DL.H0DN_PASTA_VEDADA); _toc_ = vv_.get("caminhos_tocados") or []
    _nomes_ = tuple(n_.lower() for n_ in DL.H0DN_NOMES_VEDADOS)
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == DL.VEREDITO_HMS13_OK and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and R_.get("beta_ok") is True and R_.get("observed_vector_read") is False and R_.get("le_em_rito") is False and R_.get("aditivo_posterior_ao_freeze_r2") is True
                and vv_.get("observed_vector_read") is False and vv_.get("le_em_rito") is False and m_.get("passed") is True and m_.get("n_checks") == DL.N_CHECKS_HMS13 == E_["n_checks"] and all(c_["ok"] for c_ in m_.get("checks") or [])
                and dict(R_.get("campos") or {}) == dict(DL.HMS13_CAMPOS) == dict(vv_.get("campos") or {}) and vv_.get("n_calibradores") == len(vv_.get("ids_calibradores") or []) == DL.HMS13_CAMPOS["calibradores"] and vv_.get("n_fontes_primarias") == len(vv_.get("fontes_primarias") or []) == DL.HMS13_CAMPOS["fontes_primarias"]
                and vv_.get("n_embutidos") == len(DL.HMS13_EMBUTIDOS) == len(vv_.get("pinos") or {}) and all(p_.get("sha256_ok") is True and p_.get("bytes_ok") is True and p_.get("embutido") is True for p_ in (vv_.get("pinos") or {}).values()) and vv_.get("pinos_build_n") == len(ESP["hms13"]["pinos_build"])
                and vv_.get("h0dn_selado") is True and vv_.get("veredito_h0dn_source_sha256") == (HV.get("values") or {}).get("veredito_h0dn_source_sha256") == ESP["registros_funcao_v410"]["h0dn"]["values"]["veredito_h0dn_source_sha256"] and vv_.get("gate_verdict") == ESP["qg_closure_gate_verdict_v409"] and vv_.get("freeze_r2_sha256") == ESP["h0dn"]["insumos"]["FREEZE_R2.json"]["sha256"]
                and vv_.get("sob_pasta_vedada") == [] and vv_.get("com_nome_vedado") == [] and isinstance(vv_.get("n_caminhos_tocados"), int) and vv_.get("n_caminhos_tocados") == len(_toc_)
                and not [p_ for p_ in _toc_ if _nrm_(p_) == _ved_ or _nrm_(p_).startswith(_ved_ + os.sep) or any(n_ in os.path.basename(_nrm_(p_)) for n_ in _nomes_)]
                and not vv_.get("p18_violacoes") and not vv_.get("frases_violacoes") and all((vv_.get("c8_partes") or {"x": False}).values())
                and "NOT_FALSIFIED" not in v_ and not GUARDA.search(v_) and v_.endswith("__GATE_UNMOVED")
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _traducao409_ok():
    """traducao_turing_v409 (HERDADO da v409, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v409 selada; as checagens da v409; os valores == os do ensaio; as ancoras e os 2 modulos da v409 por sha256; nenhuma chave antiga;
    o acervo da v407 repinado na copia purgada (D57d da v409); as respostas do operador; a instancia de brinquedo (SIM com solucao, NAO sem); o alcance relativo ao leitor da v409; nao move o gate"""
    R_ = TUV; E_ = ESP["registros_funcao_v409"][DL.D9.TESTEMUNHA["key"]]; m_ = R_.get("mechanics") or {}; v_ = V(DL.D9.FECHO_REGISTRO); vv_ = R_.get("values") or {}; ac_ = R_.get("acervo_v407_repinado") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == ESP["vereditos_v409"][DL.D9.FECHO_REGISTRO] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.D9.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == DL.D9.N_BUNDLE == len(ESP["bundle_v409_sha256"])
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v409"]) == len(DL.D9.ANCORAS) and all((R_.get("anchors") or {}).values()) and R_.get("ancora_principal") == DL.D9.ANCORA_PRINCIPAL and list(R_.get("ancoras_principais") or []) == list(DL.D9.ANCORAS_PRINCIPAIS)
                and R_.get("chaves_antigas_que_mudam") == [] and vv_.get("respostas_ok") is True and ac_.get("sha256") == DL.D9.PURGADO_SHA256 and ac_.get("integra_pinada") is False
                and ((vv_.get("instancia_sim") or {}).get("solucoes") or 0) >= 1 and (vv_.get("instancia_nao") or {}).get("solucoes") == 0 and (R_.get("alcance") or {}).get("frase") == DL.D9.FRASE_D56_PT
                and v_.startswith(DL.D9.VEREDITO_OK_PREFIXO) and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _tetelestai408_ok():
    """tetelestai_terminal_v408 (HERDADO da v408 via v409, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v409 selada; as 16 checagens; os valores == os do ensaio; as 48 ancoras e os 4 modulos da v408 por sha256; nenhuma chave antiga; o insumo purgado; nao move o gate"""
    R_ = TTV; E_ = ESP["registros_funcao_v408"]["tetelestai_terminal"]; m_ = R_.get("mechanics") or {}; v_ = V(DL.D8.FECHO_REGISTRO); vv_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == ESP["vereditos_v409"][DL.D8.FECHO_REGISTRO] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.D8.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == len(ESP["bundle_v408_sha256"])
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v408"]) and all((R_.get("anchors") or {}).values()) and R_.get("ancora_principal") == DL.D8.ANCORA_PRINCIPAL and list(R_.get("ancoras_principais") or []) == list(DL.D8.ANCORAS_PRINCIPAIS)
                and R_.get("chaves_antigas_que_mudam") == [] and R_.get("nome_provisorio") is None and vv_.get("respostas_ok") is True and (vv_.get("insumo_purgado") or {}).get("ok") is True
                and v_.startswith(DL.D8.VEREDITO_OK_PREFIXO) and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _psion407_ok():
    """psion_canto_v407 (HERDADO da v407 via v409, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v409 selada; as 16 checagens; os valores == os do ensaio; as 76 ancoras da v407; os 9 modulos por sha256; a chave do lema LIDA do kernel; as chaves iguais as da v409 selada; o teste (d) so' citado; nao move o gate"""
    R_ = PCV; E_ = ESP["registros_funcao_v407"]["psion_canto"]; m_ = R_.get("mechanics") or {}; v_ = V("psion_canto_v407"); td_ = R_.get("teste_d") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == ESP["vereditos_v409"]["psion_canto_v407"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.D7.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == len(ESP["bundle_v407_sha256"])
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v407"]) and all((R_.get("anchors") or {}).values()) and R_.get("link_read_from_the_kernel") is True and R_.get("lemma") == DL.D7.ANCORA_LEMA and R_.get("pair_theorem") == DL.D7.ANCORA_PAR
                and (R_.get("keys") or {}).get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is True and _feq(R_.get("keys"), ESP["chaves_v407_esperadas"]) and td_.get("so_citado") is True and td_.get("resultado_no_um_py") is None
                and v_.startswith("TGL_PSION_CANTO_V407__") and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: (R_.get("values") or {}).get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _fech408_ok():
    """fechamento_v406 (HERDADO da v406 via v409, RECRIADO neste rito; a checagem c8 versionada pela errata E20 na v408; a escada do contrato subida pela C12): segue SELADO; veredito == o da v409 selada; as checagens do calculo da v406; os valores == os do ensaio; as ancoras da v406; o bundle da v406 (301) por sha256; a escada exata; nao move o gate"""
    R_ = FE; E_ = ESP["registros_funcao_v406"]["fechamento"]; m_ = R_.get("mechanics") or {}; v_ = V("fechamento_v406")
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == ESP["vereditos_v409"]["fechamento_v406"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and R_.get("certificate_inhabited") is True and m_.get("passed") is True and m_.get("n_checks") == DL.D6.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == len(ESP["bundle_v406_sha256"])
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v406"]) and all((R_.get("anchors") or {}).values()) and v_.startswith("TGL_FECHAMENTO_V406__") and v_.endswith("__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: (R_.get("values") or {}).get(kk_) for kk_ in E_["values"]}, E_["values"]))


iald2_ok = _iald2_ok(); aescala_ok = _aescala_ok(); h0dn_ok = _h0dn_ok(); hms13_ok = _hms13_ok(); traducao409_ok = _traducao409_ok(); tetelestai408_ok = _tetelestai408_ok(); psion407_ok = _psion407_ok(); fech408_ok = _fech408_ok()
# as ANCORAS da pedra da v410 (IALD2) no kernel do rito (bandeira True, so' no trio, declaradas no modulo certo)
estrela_ok = len(ESP["estrelas_v410"]) == len(DL.ANCORAS) and all(kf.get(ESP["estrelas_v410"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_v410"][n_]["rel"] for n_ in ESP["estrelas_v410"])
# as ANCORAS da pedra AEscala (D82 a D87; o modulo do bundle da v410 depois da IALD2) no kernel do rito (bandeira True, so' no trio, declaradas no modulo certo)
estrelaA_ok = len(ESP["estrelas_aescala_v410"]) == len(DL.ANCORAS_AESCALA) and all(kf.get(ESP["estrelas_aescala_v410"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_aescala_v410"][n_]["rel"] == DL.MODULO_AESCALA for n_ in ESP["estrelas_aescala_v410"])
# as ANCORAS do traducao_turing_v409, do tetelestai_terminal_v408 (48), do psion_canto_v407 (76) e do fechamento_v406 (herdadas): seguem no kernel do rito
estrela409_ok = len(ESP["estrelas_v409"]) == len(DL.D9.ANCORAS) and all(kf.get(ESP["estrelas_v409"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_v409"][n_]["rel"] for n_ in ESP["estrelas_v409"])
estrela408_ok = len(ESP["estrelas_v408"]) > 0 and all(kf.get(ESP["estrelas_v408"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_v408"][n_]["rel"] for n_ in ESP["estrelas_v408"])
estrela407_ok = len(ESP["estrelas_v407"]) > 0 and all(kf.get(ESP["estrelas_v407"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_v407"][n_]["rel"] for n_ in ESP["estrelas_v407"])
estrela406_ok = len(ESP["estrelas_v406"]) > 0 and all(kf.get(ESP["estrelas_v406"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_v406"][n_]["rel"] for n_ in ESP["estrelas_v406"])
# NENHUMA chave antiga muda: a chave do lema (v408, lida do kernel) e as quatro da v406 seguem True, com o que fica False por teorema; o psion e o fechamento as leem iguais ao ensaio
_rf = core.get("rede_fock_v394") or {}; _pb = (core.get("psibit_v395") or {}).get("conditional_psion_face") or {}; _te = (core.get("testemunha_estatica_v396") or {}).get("fock_face") or {}; _wl = core.get("witness_layers") or {}; _ev = _te.get("elo_v407") or {}
chaves_ok = bool(_te.get("linked_to_the_corner_by_a_lemma") is True and _ev.get("lemma") == DL.D7.ANCORA_LEMA and _ev.get("kind") == "STRUCTURE_NOT_VECTORS" and _ev.get("identifies_omega_with_bell_vector") is False and _ev.get("pair_on_the_fock_face") == "OPEN" and _ev.get("bell_to_tt_bridge") == "NOT_A_TERM"
                 and _rf.get("whole_certificate_inhabited") is True and _pb.get("inhabitant_exhibited") is True and _pb.get("status") == DL.STATUS_HABITADO and _te.get("inhabitant_exhibited") is True and _te.get("status") == DL.STATUS_HABITADO
                 and _wl.get("canonical_full_witness_term_constructed") is True and (((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists")) is False and (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists") is False
                 and (PCV.get("keys") or {}).get("kernel_reads_the_link") is True and _feq(FE.get("four_keys"), ESP["registros_funcao_v406"]["fechamento"]["values"]["chaves"]) and _feq(PCV.get("keys"), ESP["chaves_v407_esperadas"]) and IV.get("chaves_antigas_que_mudam") == [] and TUV.get("chaves_antigas_que_mudam") == [] and TTV.get("chaves_antigas_que_mudam") == [])


def _reg405v_ok(k_):   # os OITO registros de pedra da v405, RECRIADOS pela v409 e iguais aos da v405 selada (so' o nome vem do mecanismo)
    n_ = DL.D5.REGISTRO_DE_PEDRA[k_]; R_ = core.get(n_) or {}; E_ = ESP["registros_funcao_v405"][k_]
    return bool(R_.get("all_verified") is True and V(n_) == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and (R_.get("mechanics") or {}).get("n_checks") == DL.D5.N_CHECKS[k_] == E_["n_checks"]
                and all(c_["ok"] for c_ in (R_.get("mechanics") or {}).get("checks") or []) and (R_.get("context") or {}).get("ok") is True and (R_.get("key_theorem") or {}).get("in_kernel") is True and (R_.get("unconditional") or {}).get("in_kernel") is True
                and not GUARDA.search(V(n_)) and R_.get("beta_ok") is True and _feq({kk_: (R_.get("values") or {}).get(kk_) for kk_ in E_["values"]}, E_["values"]))


reg405v_ok = {k_: _reg405v_ok(k_) for k_ in REL5_}
estrela405v_ok = all(kf.get(ESP["estrelas_v405"][k_]["bandeira"]) is True and set(axr.get(ESP["estrelas_v405"][k_]["teorema"]) or []) <= TRIO and src_.get(ESP["estrelas_v405"][k_]["teorema"]) == REL5_[k_] for k_ in REL5_)   # as estrelas da v408 (RECRIADAS)
estrela408r_ok = all(kf.get(ESP["estrelas_v403"][k_]["bandeira"]) is True and set(axr.get(ESP["estrelas_v403"][k_]["teorema"]) or []) <= TRIO and src_.get(ESP["estrelas_v403"][k_]["teorema"]) == REL3_[k_] for k_ in ("caminho", "vida", "verdade_adendo"))   # as estrelas da v403 (RECRIADAS)
fal_reg_ok = bool(FA.get("all_verified") is True and V("falsidade_da_inercia_v401") == ESP["veredito_da_falsidade_v409"] == ESP["vereditos_v409"]["falsidade_da_inercia_v401"] and FA.get("does_not_gate_core") is True and not GUARDA.search(V("falsidade_da_inercia_v401")))   # a v401, RECRIADA e igual ao selado
reg408_recriados_ok = all((core.get(n_) or {}).get("all_verified") is True and V(n_) == ESP["vereditos_v409"][n_] and (core.get(n_) or {}).get("does_not_gate_core") is True and not GUARDA.search(V(n_)) for n_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"))   # os tres registros com funcao da v408, RECRIADOS e iguais aos da v408 selada
pedras_v405_ok = bool(len(ESP["pedras_v405_sha256"]) == 13 and all(_sha_k(rel_) == s_ and (kf.get("formal_files_sha256") or {}).get(rel_) == s_ for rel_, s_ in ESP["pedras_v405_sha256"].items()))   # as 13 pedras SELADAS (as oito da v408, as duas da v404 e as tres da v403) seguem no kernel do Nos (registro)


def _reg408r_ok(k_):   # os registros de pedra da v408, RECRIADOS pela v409 e iguais aos da v408 selada
    n_ = DL.D3.REGISTRO_DE_PEDRA[k_]; R_ = core.get(n_) or {}; E_ = ESP["registros_funcao_v403"][k_]
    return bool(R_.get("all_verified") is True and V(n_) == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and (R_.get("mechanics") or {}).get("n_checks") == DL.D3.N_CHECKS[k_] == E_["n_checks"]
                and all(c_["ok"] for c_ in (R_.get("mechanics") or {}).get("checks") or []) and (R_.get("context") or {}).get("ok") is True and (R_.get("key_theorem") or {}).get("in_kernel") is True and (R_.get("unconditional") or {}).get("in_kernel") is True
                and not GUARDA.search(V(n_)) and R_.get("beta_ok") is True and _feq({kk_: (R_.get("values") or {}).get(kk_) for kk_ in E_["values"]}, E_["values"]))


reg408r_ok = {k_: _reg408r_ok(k_) for k_ in ("caminho", "vida", "verdade_adendo")}


def _gate408r_ok():
    R_ = core.get("bandeiras_do_gate_v403") or {}; E_ = ESP["registros_funcao_v403"]["gate"]; v_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and V("bandeiras_do_gate_v403") == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and (R_.get("mechanics") or {}).get("n_checks") == DL.D3.N_CHECKS["gate"] == E_["n_checks"]
                and all(c_["ok"] for c_ in (R_.get("mechanics") or {}).get("checks") or []) and not GUARDA.search(V("bandeiras_do_gate_v403")) and _feq({kk_: v_.get(kk_) for kk_ in E_["values"]}, E_["values"])
                and v_.get("n_literal") == 0 and v_.get("n_calculated") == 18 == v_.get("n_true") and v_.get("n_read_by_the_verdict") == 15 and v_.get("read_by_the_verdict") == [6, 5, 4] and v_.get("gate_verdict_equals_v402") is True)


gate408r_ok = _gate408r_ok()


def _f2b409_ok():
    R_ = core.get("f2b_errata_v404") or {}; E_ = ESP["registros_funcao_v404"]["f2b"]; v_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and V("f2b_errata_v404") == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and (R_.get("mechanics") or {}).get("n_checks") == DL.D4.N_CHECKS["f2b"] == E_["n_checks"]
                and all(c_["ok"] for c_ in (R_.get("mechanics") or {}).get("checks") or []) and not GUARDA.search(V("f2b_errata_v404")) and _feq({kk_: v_.get(kk_) for kk_ in E_["values"]}, E_["values"])
                and R_.get("F2b_status_now") == DL.D4.F2B_FUTURO_TOKEN and R_.get("F2b_status_before") == "AWAITING" and v_.get("previsao_fora_do_intervalo_de_A") is True and v_.get("n_cobrancas_v383") == 11 and v_.get("conjunto_D_n") == 14
                and R_.get("beta_ok") is True and all((R_.get("inscriptions") or {}).values()))


f2b409_ok = _f2b409_ok()


def _reg408b_ok(k_):   # os registros de pedra da v408, RECRIADOS pela v409 e iguais aos da v408 selada
    n_ = DL.D4.REGISTRO_DE_PEDRA[k_]; R_ = core.get(n_) or {}; E_ = ESP["registros_funcao_v404"][k_]
    return bool(R_.get("all_verified") is True and V(n_) == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and (R_.get("mechanics") or {}).get("n_checks") == DL.D4.N_CHECKS[k_] == E_["n_checks"]
                and all(c_["ok"] for c_ in (R_.get("mechanics") or {}).get("checks") or []) and (R_.get("context") or {}).get("ok") is True and (R_.get("key_theorem") or {}).get("in_kernel") is True and (R_.get("unconditional") or {}).get("in_kernel") is True
                and not GUARDA.search(V(n_)) and R_.get("beta_ok") is True and _feq({kk_: (R_.get("values") or {}).get(kk_) for kk_ in E_["values"]}, E_["values"]))


reg408b_ok = {k_: _reg408b_ok(k_) for k_ in ("projecao", "jo8v32")}
estrela408b_ok = all(kf.get(ESP["estrelas_v404"][k_]["bandeira"]) is True and set(axr.get(ESP["estrelas_v404"][k_]["teorema"]) or []) <= TRIO and src_.get(ESP["estrelas_v404"][k_]["teorema"]) == REL4_[k_] for k_ in ("projecao", "jo8v32"))   # as estrelas da v404 (RECRIADAS)
# A MOLDURA, relida aqui com a mesma regra do um.py instalado (guarda_frases_v410, a excecao e' so' a fala do operador): nenhum texto novo da gerencia afirma demais; a frase certa esta nos artigos e no .md; o numero da massa e' o da v408
import guarda_frases_v410 as GF
_txt_novos = json.dumps({n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "estatuto", "scope", "limites", "diz", "nao_diz", "erratas")} for n_ in list(DL.REGISTROS_FUNCAO) + RN410}, ensure_ascii=False)
_ini410 = {l: txt[l].find(_tt(ESP["titulo_secao_v410"][l])) for l in ("pt", "en")}; _fim410 = {l: txt[l].find(_tt(ESP["titulo_secao_v409"][l]), max(_ini410[l], 0)) for l in ("pt", "en")}   # (v409: o titulo da v408 traz $eta$; o TXT rende β)
_sec410 = {l: (txt[l][_ini410[l]:_fim410[l]] if 0 <= _ini410[l] < _fim410[l] else "") for l in ("pt", "en")}
# (D72) a secao do H0DN: logo DEPOIS da secao da IALD2 e ANTES da secao da v409 (dentro do trecho _sec410), com a obrigacao nas duas linguas, sem a frase de guarda (o registro selou) e limpa na guarda das frases
# (D82 a D87) a secao A Escala: logo DEPOIS da secao da IALD2 e ANTES da secao do H0DN (dentro do trecho _sec410), com a forma obrigatoria da D83 e a frase canonica do Clay (D84) nas duas linguas, sem a frase de guarda (o registro selou) e limpa na guarda das frases
_ws = lambda s_: re.sub(r"\s+", " ", s_)
_iniA = {l: txt[l].find(_tt(ESP["titulo_secao_aescala_v410"][l]), max(_ini410[l], 0)) for l in ("pt", "en")}
_iniH = {l: txt[l].find(_tt(ESP["titulo_secao_h0dn_v410"][l]), max(_iniA[l], 0)) for l in ("pt", "en")}
_secA = {l: (txt[l][_iniA[l]:_iniH[l]] if 0 <= _ini410[l] < _iniA[l] < _iniH[l] else "") for l in ("pt", "en")}
# (R2, D99; ADENDO 4) a clausula do limite ao lado do teorema do Tetelestai (a formula em modo matematico no LaTeX, os simbolos no TXT: DL.comparavel ignora so' cifrao, barras, chaves, parenteses e espacos), a frase dos seis nomes, a costura do tempo (o rotulo e a frase com so' a primeira letra em maiuscula) e Z(s) DEFINIDA na primeira ocorrencia do artigo
def _r2_artigo_ok(l_):
    sec_ = _secA[l_]; ib_ = sec_.find("linear nos bits" if l_ == "pt" else "linear in the bits"); iz_ = txt[l_].find("Z(s)")
    return bool(sec_ and ib_ >= 0 and DL.comparavel(DL.CLAUSULA_Z_PT if l_ == "pt" else DL.CLAUSULA_Z_EN) in DL.comparavel(sec_[ib_:ib_ + 1400]) and DL.comparavel(DL.FRASE_SEIS_NOMES_PT if l_ == "pt" else DL.FRASE_SEIS_NOMES_EN) in DL.comparavel(sec_)
                and ((DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) if l_ == "pt" else (DL.ROTULO_TEMPO_EN + " " + DL.FRASE_TEMPO_EN_COSTURADA)) in _ws(sec_) and iz_ >= 0 and DL.comparavel("Z(s)=\\sum_x e^{-s\\cdot c(x)}") in DL.comparavel(txt[l_][iz_:iz_ + 320]))
r2_artigo_ok = bool(_r2_artigo_ok("pt") and _r2_artigo_ok("en"))


def _r5_artigo_ok(l_):   # (R5, D100 e D101) a frase da clausula do Tetelestai com a clausula do limite LOGO DEPOIS, a reconstrucao, a errata, o dispositivo (com [PILOTO][SIM]) e a ratificacao D101, na secao A Escala (formas comparaveis: o LaTeX poe os simbolos em modo matematico e o TXT os rende)
    sec_ = _secA[l_]; cs_ = DL.comparavel(sec_); pt_ = l_ == "pt"
    fr_ = (DL.FRASE_TETELESTAI_PT if pt_ else DL.FRASE_TETELESTAI_EN, DL.FRASE_RECONSTROI_PT if pt_ else DL.FRASE_RECONSTROI_EN, DL.FRASE_E36_PT if pt_ else DL.FRASE_E36_EN, DL.FRASE_DISPOSITIVO_PT if pt_ else DL.FRASE_DISPOSITIVO_EN, DL.FRASE_NOMES_RATIFICADOS_D101_PT if pt_ else DL.FRASE_NOMES_RATIFICADOS_D101_EN)
    return bool(sec_ and all(DL.comparavel(f_) in cs_ for f_ in fr_) and DL.comparavel(fr_[0]) + "." + DL.comparavel(DL.CLAUSULA_Z_PT if pt_ else DL.CLAUSULA_Z_EN) in cs_ and "[PILOTO][SIM]" in sec_)


r5_artigo_ok = bool(_r5_artigo_ok("pt") and _r5_artigo_ok("en"))


def _d108_artigo_ok(l_):   # (D108; item 50 b da ESPEC do conserto unico, controle opcional) a frase da finura da leitura na secao A Escala do artigo, formas comparaveis: a primeira metade (o que os enunciados dizem) e, da segunda, o nucleo da frase da secao 7 (que o artigo traz no paragrafo da secao 7), com a clausula do limite na secao
    sec_ = _secA[l_]; cs_ = DL.comparavel(sec_); pt_ = l_ == "pt"
    return bool(sec_ and DL.comparavel(DL.FRASE_FINURA_REAL_PT if pt_ else DL.FRASE_FINURA_REAL_EN) in cs_ and DL.comparavel(DL.FRASE_ESCALA_UMA_NUCLEO_PT if pt_ else DL.FRASE_ESCALA_UMA_NUCLEO_EN) in cs_ and DL.comparavel(DL.CLAUSULA_Z_PT if pt_ else DL.CLAUSULA_Z_EN) in cs_)


d108_artigo_ok = bool(_d108_artigo_ok("pt") and _d108_artigo_ok("en"))
aescala_secao_ok = bool(r2_artigo_ok and r5_artigo_ok and d108_artigo_ok and _secA["pt"] and _secA["en"] and _ws(DL.FRASE_D83_OBRIGATORIA_PT) in _secA["pt"] and _ws(DL.FRASE_D83_OBRIGATORIA_EN) in _secA["en"] and _ws(DL.FRASE_CLAY_CANONICA_PT) in _secA["pt"] and _ws(DL.FRASE_CLAY_CANONICA_EN) in _secA["en"] and "NÃO selou" not in _secA["pt"] and "did NOT seal" not in _secA["en"] and not GF.violacoes(_secA["pt"]) and not GF.violacoes(_secA["en"]))
# a secao do H0DN (agora com o paragrafo do recibo HMS/13 no FIM: D80, aditivo e posterior ao FREEZE_R2): vai da secao do H0DN ate a da v409
_secH = {l: (txt[l][_iniH[l]:_fim410[l]] if 0 <= _ini410[l] < _iniA[l] < _iniH[l] < _fim410[l] else "") for l in ("pt", "en")}
h0dn_secao_ok = bool(_secH["pt"] and _secH["en"] and DL.FRASE_H0DN_OBRIGATORIA_PT in _secH["pt"] and DL.FRASE_H0DN_OBRIGATORIA_EN in _secH["en"] and _ws(DL.FRASE_H0DN_RETORNO_PT) in _ws(_secH["pt"]) and _ws(DL.FRASE_H0DN_RETORNO_EN) in _ws(_secH["en"]) and _ws(DL.FRASE_H0DN_ALCANCE_PT) in _ws(_secH["pt"]) and _ws(DL.FRASE_H0DN_ALCANCE_EN) in _ws(_secH["en"]) and "NÃO selou" not in _secH["pt"] and "did NOT seal" not in _secH["en"] and not GF.violacoes(_secH["pt"]) and not GF.violacoes(_secH["en"]))
# o paragrafo do recibo HMS/13 (D80) e' o fim da secao do H0DN: a obrigacao dele nas duas linguas (cobertura documental de fontes, nao covariancia fisica fechada; nada aberto), sem a frase de «nao selou» do recibo e limpo na guarda
hms13_secao_ok = bool(_secH["pt"] and _secH["en"] and DL.FRASE_HMS13_OBRIGATORIA_PT in _secH["pt"] and DL.FRASE_HMS13_OBRIGATORIA_EN in _secH["en"] and _secH["pt"].find(DL.FRASE_HMS13_OBRIGATORIA_PT) > _secH["pt"].find(DL.FRASE_H0DN_OBRIGATORIA_PT) and _secH["en"].find(DL.FRASE_HMS13_OBRIGATORIA_EN) > _secH["en"].find(DL.FRASE_H0DN_OBRIGATORIA_EN)
                      and not any(m_ in _secH[l_] for l_ in ("pt", "en") for m_ in ESP["artigo_nao"][l_] if "HMS/13" in m_) and all(len([m_ for m_ in ESP["artigo_marcas"][l_] if "HMS/13" in m_]) == 1 and all(_tt(m_) in _secH[l_] for m_ in ESP["artigo_marcas"][l_] if "HMS/13" in m_) for l_ in ("pt", "en")) and not GF.violacoes(_secH["pt"]) and not GF.violacoes(_secH["en"]))
_frase_no_artigo = bool(all(p_ in _sec410["pt"] for p_ in (DL.FRASE_QUALIFICADOR_PT, "não creditação", "o gate não se move")) and (DL.FRASE_QUALIFICADOR_EN in _sec410["en"] or bool(re.search(re.escape(DL.FRASE_QUALIFICADOR_EN.split("; ", 1)[0]) + r"\s*\(kernel validity, not creditation\);\s*" + re.escape(DL.FRASE_QUALIFICADOR_EN.split("; ", 1)[1]), _ws(_sec410["en"])))) and all(p_ in _sec410["en"] for p_ in ("(kernel validity, not creditation)", "the gate does not move"))
                       and "o gate não se move" in fc and DL.FRASE_DA_MOLDURA_V410_PT and DL.FRASE_DA_MOLDURA_V410_EN)   # a frase certa da v410 (o qualificador da D64 nos dois artigos, dentro da secao nova; o gate nao se move no .md)
moldura_ok = bool(not GF.violacoes(_txt_novos) and _sec410["pt"] and _sec410["en"] and not GF.violacoes(_sec410["pt"]) and not GF.violacoes(_sec410["en"]) and _frase_no_artigo and (GF.controle_negativo() or {}).get("ok") is True)
_m_core = (core.get("neutrino_mass") or {}).get("m_nu_meV")
numero_da_massa_ok = bool(isinstance(_m_core, float) and abs(_m_core / ESP["m_nu_meV_v404"] - 1.0) <= 1e-12 and all(_feq((core.get(n_) or {}).get("values", {}).get(k_), _m_core) for n_, k_ in (("ponte_da_massa_v405", "m_nu_meV_core"), ("ponto_zero_do_psion_v405", "meia_hbar_omega_meV"), ("lei_do_diminuto_v405", "massa_formula_meV"))))
_e10_r = (core.get("ponte_da_massa_v405") or {}).get("neutrino_angle_errata") or {}
errata_e10_ok = bool(_e10_r.get("agora") == DL.ERRATA_E10 and _e10_r.get("dizia_prefixo") == DL.ANGLE_STATUS_ANTIGO_PREFIXO and str(_e10_r.get("assinatura", "")).startswith("gerencia c1, em nome proprio"))
_um_txt_c = UM_BYTES.decode("utf-8", "replace")
gate_funcoes_ok = bool(sha(_um_txt_c.encode("utf-8")) == UM_FULL)   # (a igualdade byte a byte das funcoes do gate e' do gerador e da comparacao AST; aqui o um.py e' o candidato, por sha)
# a reclassificacao do Grande Atrator: a classe nova AO LADO; o selado identico (a linha da tabela, a auditoria e o ga_window_status do JSON do rito)
GAP5 = core.get(DL.GAP_REGISTRO) or {}
gap5_ok = bool(GAP5.get("all_verified") is True and GAP5.get("does_not_gate_core") is True and (GAP5.get("mechanics") or {}).get("passed") is True and (GAP5.get("mechanics") or {}).get("n_checks") == DL.GAP_N_CHECKS and _feq({k_: (GAP5.get("values") or {}).get(k_) for k_ in ESP["gap_values"]}, ESP["gap_values"]))
GA5 = core.get(DL.GA_REGISTRO) or {}; _lgm = [x_ for x_ in ((core.get("joint_coincidence_result_v3") or {}).get("inventory") or []) if isinstance(x_, dict) and x_.get("id") == "ga_mass_window"]
_ga_top = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")).get("ga_window_status")
ga5_ok = bool(GA5.get("all_verified") is True and GA5.get("does_not_gate_core") is True and (GA5.get("mechanics") or {}).get("passed") is True and (GA5.get("mechanics") or {}).get("n_checks") == 6 and GA5.get("errata_do_parecer_ok") is True and (GA5.get("extras") or {}).get("classe_agora") == DL.GA_CLASSE_AGORA and _feq({k_: (GA5.get("values") or {}).get(k_) for k_ in ESP["ga_values"]}, ESP["ga_values"])
              and len(_lgm) == 1 and _lgm[0].get("rule") == DL.GA_CLASSE_ANTES and _lgm[0].get("admissible") is False and V("ga_mass_audit") == ESP["vereditos_v409"]["ga_mass_audit"] and _ga_top == ESP["ga_window_status"])
v1_intacto_ok = bool((core.get("ramo_b_preregistration_v386") or {}).get("F2b_status") == "AWAITING" and (core.get("ramo_b_preregistration_v386") or {}).get("veredito_do_V1") == "AWAITING_DATA" and (core.get("ramo_b_preregistration_v386") or {}).get("all_verified") is True
                     and V("ramo_b_preregistration_v386") == ESP["vereditos_v409"]["ramo_b_preregistration_v386"] and V("ledger_errata_v386") == ESP["vereditos_v409"]["ledger_errata_v386"] and V("the_ledger_of_charges_v383") == ESP["vereditos_v409"]["the_ledger_of_charges_v383"]
                     and ((core.get("ledger_errata_v386") or {}).get("charge_F2b") or {}).get("token") == "AWAITING")   # o V1, o registro da v386 e o livro da v383 NAO foram reescritos: a errata e' AO LADO
neutrino_intacto_ok = bool(str((core.get("neutrino_mass") or {}).get("angle_status", "")).startswith(DL.ANGLE_STATUS_ANTIGO_PREFIXO) and V("neutrino_mass") == ESP["vereditos_v409"]["neutrino_mass"] and (core.get("neutrino_mass") or {}).get("frozen_hash") == ESP["neutrino_frozen_hash_v409"])   # a funcao do neutrino NAO foi reescrita: o texto antigo fica, a errata e' AO LADO (projecao_transversal_v404)


def _f81_ast(src_):
    """varredura AST (independente do registro) da funcao prove_qg_closure_gate do um.py INSTALADO: (literais, calculadas) entre as tres bandeiras da F8.1; None se a funcao nao for unica."""
    import ast as _a
    fn_ = [n_ for n_ in _a.parse(src_).body if isinstance(n_, _a.FunctionDef) and n_.name == "prove_qg_closure_gate"]
    if len(fn_) != 1:
        return None
    lit_, calc_ = [], []
    for n_ in _a.walk(fn_[0]):
        if isinstance(n_, _a.Dict):
            for k_, v_ in zip(n_.keys, n_.values):
                if isinstance(k_, _a.Constant) and k_.value in DL.F81_LITERAIS:
                    (lit_ if isinstance(v_, _a.Constant) else calc_).append(k_.value)
        if isinstance(n_, _a.Assign) and len(n_.targets) == 1 and isinstance(n_.targets[0], _a.Subscript) and isinstance(n_.targets[0].slice, _a.Constant) and n_.targets[0].slice.value in DL.F81_LITERAIS:
            (lit_ if isinstance(n_.value, _a.Constant) else calc_).append(n_.targets[0].slice.value)
    return sorted(lit_), sorted(calc_)


_f81 = _f81_ast(UM_BYTES.decode("utf-8"))
_ls2k = sorted(k_ for k_ in (getattr(um_c, "_LEAN_THEOREM_FLAGS", None) or {}) if k_.startswith(DL.F81_PREFIXO_LS2)) if um_c is not None else []
_prereg = [c_[1] for c_ in ((core.get("void_floor_v11") or {}).get("checks") or []) if isinstance(c_, (list, tuple)) and len(c_) == 2 and c_[0] == DL.F81_ROTULO_PREREG]
_ck_old = ESP["qg_closure_v409_checks"]; _ck_new = json.loads(J(qg.get("checks") or [])); _sonda = [c_ for c_ in _ck_new if str(c_[0]).startswith("ProbeBlindNullAbsent")]
f81_ok = bool(_f81 is not None and _f81[0] == [] and _f81[1] == sorted(DL.F81_LITERAIS) and len(_ls2k) == 6 and all(kf.get(k_) is True for k_ in _ls2k) and (qg.get("physics_flags") or {}).get("linearized_spin2_finite_face") is True
              and len(_prereg) == 1 and _prereg[0] is True and (qg.get("experiment_flags") or {}).get("protocol_pre_registered") is True and (core.get("void_stacking_blind") or {}).get("all_verified") is True and (qg.get("experiment_flags") or {}).get("null_tests_passed_blind") is True
              and n18 == 18 and (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v409"] == selo.get("qg_closure_verdict") and len(_sonda) == 1 and _ck_new == _ck_old)
# o NAO do gate (vale tambem para o Nos ainda v409, no controle negativo): o qg_closure sem a lista de checks e' o da v409, os checks da v409 iguais e na mesma ordem, TODOS True, e no maximo a sonda nova a mais; a PRESENCA da sonda e' do DEVE (f81_ok)
gate_igual_ok = bool(sha(J({k_: v_ for k_, v_ in qg.items() if k_ != "checks"}).encode("utf-8")) == ESP["qg_closure_v409_sem_checks_json_sha256"] and _ck_new == _ck_old and len(_sonda) == 1 and all(c_[1] is True for c_ in _ck_new))

DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v410; os resumos do selo (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, falsidade_da_inercia_v401, os tres registros com funcao da v402, os QUATRO da v403, os TRES da v404, os OITO da v405, fechamento_v406, psion_canto_v407, tetelestai_terminal_v408, traducao_turing_v409, iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410), registros_v399, registros_v401, registros_v402, registros_v403, registros_v404, registros_v405, registros_v406, registros_v407, registros_v408, registros_v409 e registros_v410 do selo iguais aos do core (veredito, selagem); o SHA-256 primario do um.py no selo == o do arquivo": selo.get("um_version") == "v410"
        and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) and (selo.get(n) or {}).get("all_verified") is True for n in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "falsidade_da_inercia_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409") + tuple(DL.REGISTROS_FUNCAO))
        and all(((selo.get("registros_v405") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v405") or {}).get(n) or {}).get("all_verified") is True for n in RN405)
        and all(((selo.get("registros_v406") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v406") or {}).get(n) or {}).get("all_verified") is True for n in RN406)
        and all(((selo.get("registros_v407") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v407") or {}).get(n) or {}).get("all_verified") is True for n in RN407)
        and all(((selo.get("registros_v408") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v408") or {}).get(n) or {}).get("all_verified") is True for n in RN408)
        and all(((selo.get("registros_v409") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v409") or {}).get(n) or {}).get("all_verified") is True for n in RN409)
        and all(((selo.get("registros_v410") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v410") or {}).get(n) or {}).get("all_verified") is True for n in RN410)
        and all(((selo.get("registros_v404") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v404") or {}).get(n) or {}).get("all_verified") is True for n in RN404)
        and all(((selo.get("registros_v401") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v401") or {}).get(n) or {}).get("all_verified") is True for n in RN401)
        and all(((selo.get("registros_v402") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v402") or {}).get(n) or {}).get("all_verified") is True for n in RN402)
        and all(((selo.get("registros_v403") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v403") or {}).get(n) or {}).get("all_verified") is True for n in RN403)
        and all(((selo.get("registros_v399") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN) and (selo.get("sha256") or {}).get("um.py") == UM_FULL,
    "selo_pela_propria_tecnologia_v399 SELOU: veredito == o do ensaio; %d checagens ok; perfil %s; o SHA-256 ao lado == o do um.py; 13 controles negativos todos recusados; nao move o gate" % (ESA["n_checks"], ESA["perfil"]): selo_reg_ok,
    "caminho_v403 (RECRIADO na v410) SELOU igual ao da v409 selada: veredito == o do ensaio; as %d checagens do calculo no modelo longitudinal (E, p) (com o MESMO p+ as massas 1, 4 e 9 sao tres realizacoes DISTINTAS: a massa NAO e' selecionada; toda massa tem realizacao positiva; m^2 = p+ p- e' invariante e a energia e' a leitura; o levantamento e' equivariante; a unidade de defasagem s = beta de runtime) e os valores == os do ensaio; o texto da pedra e a conjuncao no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.D3.N_CHECKS["caminho"]: reg408r_ok["caminho"] and estrela408r_ok,
    "vida_v403 (RECRIADO na v410) SELOU igual ao da v409 selada: veredito == o do ensaio; as %d checagens do calculo (o peso cai estritamente, nats = s, a seta e' o sinal de s, o chao e' o posto, a entrega custa, o regime angular so' le, a isotropia e' carga) e os valores == os do ensaio; o texto da pedra no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.D3.N_CHECKS["vida"]: reg408r_ok["vida"],
    "verdade_adendo_v403 (RECRIADO na v410) SELOU igual ao da v409 selada: veredito == o do ensaio; as %d checagens do calculo em M2(C) (a esperanca diagonal le a projecao da identidade como os pesos q^2 e alfa^2; o Nome preserva o Um; reler nao acrescenta; os pesos em a = alfa, com alfa = beta/sqrt(e) de runtime) e os valores == os do ensaio; o texto do adendo no kernel embutido; a pedra Verdade (v392) intocada; a estrela e a composicao no kernel do rito; nao move o gate" % DL.D3.N_CHECKS["verdade_adendo"]: reg408r_ok["verdade_adendo"],
    "projecao_transversal_v404 (RECRIADO na v410) SELOU igual ao da v409 selada: veredito == o do ensaio; as %d checagens do calculo (x = 1 - x => 1/2; sen^2(pi/4) = 1/2 e a raiz da metade; a raiz de x autoconjugado e sen(pi/4); a unicidade em [0, pi/2]; a forma do neutrino beta.sen45.E0 = sen^2(theta_M).sen(pi/4).E0 com E0 = 1 eV DECLARADO e o m_nu do programa relido a 1e-12; theta_M longe de pi/4; a derivada de sen^2 em pi/4 vale 1; a errata do angulo AO LADO com o texto antigo intacto) e os valores == os do ensaio; o texto da pedra no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.D4.N_CHECKS["projecao"]: reg408b_ok["projecao"] and estrela408b_ok,
    "jo8v32_v404 (RECRIADO na v410) SELOU igual ao da v409 selada: veredito == o do ensaio; as %d checagens (as tres estrelas da v408 citadas pela conjuncao no kernel, no trio e no modulo delas; os tres registros da v408 selados; a declaracao das hipoteses nomeadas dos componentes; a mecanica numerica dos tres RELIDA com o beta do rito; o nome do operador e a ratificacao verbatim nas falas embutidas) e os valores == os do ensaio; o texto da pedra no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.D4.N_CHECKS["jo8v32"]: reg408b_ok["jo8v32"],
    "f2b_errata_v404 (RECRIADO na v410) SELOU igual ao da v409 selada: veredito == o do ensaio; as %d checagens (o V1 do ramo B lido por hash e como antes; o livro v383 intacto; a calibracao A e a previsao do par LIDAS do V1; a previsao fora do intervalo de A e de sinal oposto; nenhum desfecho; beta, a lei e R2 ficam) e os valores == os do ensaio; o estado do canal F2b == o token novo (retirado antes do dado), AO LADO; nao move o gate" % DL.D4.N_CHECKS["f2b"]: f2b409_ok,
    "iald2_v410 SELOU (o registro com FUNCAO, novo): veredito == o do ensaio; as %d checagens do calculo (as %d ancoras da pedra IALD2 no trio e no modulo certo, o modulo embutido por sha256 == o hash formal do rito com a raiz e o import, o leitor le o par como par em C3, IALD ao quadrado, reler nao acrescenta, a primeira leitura identifica, resolver = verificar, o algoritmo IALD na instancia SAT da v409, o signo do nome, o signo do par, o gate congelado, a escada exata, as guardas limpas, beta = alfa x raiz de e, a representacao de beta) e os valores == os do ensaio; o alcance relativo ao leitor (D64); NENHUMA chave antiga muda; nao move o gate" % (DL.N_CHECKS_FECHO, len(DL.ANCORAS)): iald2_ok,
    "a_escala_v410 SELOU (D82 a D87; o registro com FUNCAO da pedra AEscala, novo; validade no kernel, a creditacao e' do Clay): veredito == o do ensaio == o do delta; as %d checagens; as %d ancoras da pedra no trio e no modulo certo; as %d bandeiras ext_aescala_410_*; a pedra por sha256 == o hash formal; as falas por sha256; os numeros (fracoes exatas e o projetor de Bell) == os do delta; a frase canonica (D84) e a forma da D83; os %d nomes RATIFICADOS (D87); os nomes novos RATIFICADOS em 10/11 (D101), o quarto teorema da clausula NOMEADO pelo operador (D108) e os dois auxiliares pendentes; a clausula do Tetelestai em 1 - beta com beta de runtime (c13, R5); NENHUMA chave antiga muda; o gate == o da v409; os valores == os do ensaio; nao move o gate" % (DL.N_CHECKS_AESCALA, len(DL.ANCORAS_AESCALA), ESP["aescala"]["n_flags"], len(DL.NOMES_AESCALA)): aescala_ok,
    "h0dn_fontes_hms13_v410 SELOU (D80; o recibo documental HMS/13, ADITIVO e POSTERIOR ao FREEZE_R2: cobertura documental de fontes, não covariância física fechada; nada aberto; pré-registrado; nenhum dado observado lido): veredito == o do ensaio == o do delta; as %d checagens; os dez campos == DL.HMS13_CAMPOS; observed_vector_read e le_em_rito False; os %d artefatos embutidos por sha256; os %d calibradores e as %d fontes; a funcao de veredito do H0DN intocada; nenhum caminho tocado sob a pasta vedada (em rito nada de kimi\\ e' aberto) nem com nome vedado; os valores == os do ensaio; nao move o gate" % (DL.N_CHECKS_HMS13, len(DL.HMS13_EMBUTIDOS), DL.HMS13_CAMPOS["calibradores"], DL.HMS13_CAMPOS["fontes_primarias"]): hms13_ok,
    "h0dn_bg1_v410 SELOU (D72; o registro com FUNCAO do teste da razao de Hubble, novo; pré-registrado; nenhum dado observado lido): veredito == o do ensaio == o PRE-REGISTRADO; as %d checagens; observed_vector_read False; os %d pinos (os 9 do FREEZE_R2 mais o FREEZE_R2 e a ENTREGA) batendo; os 6 ramos da funcao de veredito congelada nos vetores deterministicos; o sha256 da funcao == o do ensaio; nenhum caminho tocado sob a pasta vedada (a entrega do Kimi) nem com nome vedado; os valores == os do ensaio; nao move o gate" % (DL.N_CHECKS_H0DN, ESP["registros_funcao_v410"]["h0dn"]["values"]["n_pinos"]): h0dn_ok,
    "a secao A ESCALA no artigo PT/EN (D82 a D87) vem logo DEPOIS da secao da IALD2 e ANTES da secao do H0DN, traz a forma obrigatoria da D83 e a frase canonica do Clay (D84) nas duas linguas, a clausula do limite do teorema do Tetelestai ao lado dele (ADENDO 4, D99), os seis nomes e a costura do tempo, com Z(s) definida na primeira ocorrencia do artigo, e a clausula do Tetelestai em 1 - beta (R5, D100: a frase, a clausula do limite logo depois, a reconstrucao, a errata, o dispositivo com [PILOTO][SIM]) e a ratificacao D101; nao traz a frase de guarda (o registro selou) e passa a guarda das frases": aescala_secao_ok,
    "o paragrafo do recibo documental HMS/13 (D80) e' o FIM da secao do H0DN no artigo PT/EN: a mesma marca de ESPERADOS (artigo_marcas), a obrigacao «cobertura documental de fontes, não covariância física fechada; nada aberto» nas duas linguas, depois da obrigacao do H0DN, sem a frase de guarda (o registro selou) e limpo na guarda das frases": hms13_secao_ok,
    "a secao do H0DN no artigo PT/EN (pré-registrado; nenhum dado observado lido) vem logo DEPOIS da secao A Escala e ANTES da secao da v409, traz a obrigacao D72 nas duas linguas, o retorno da ORDEM KIMI H0DN-02 e o alcance da forma obrigatoria (PAR-01 e a observacao 15 do painel), nao traz a frase de guarda (o registro selou) e passa a guarda das frases": h0dn_secao_ok,
    "o .md canonico: as QUATRO linhas da v410 na ordem (ESP md_iald2, md_aescala, md_h0dn, md_hms13), ANTES da linha da v409; a da A Escala com a forma da D83 e a frase canonica (D84); a do H0DN com a obrigacao D72; a do recibo HMS/13 com a obrigacao do HMS/13 e a do H0DN": bool(all(ESP[k_] in fc for k_ in ("md_iald2", "md_aescala", "md_h0dn", "md_hms13")) and fc.find(ESP["md_iald2"]) < fc.find(ESP["md_aescala"]) < fc.find(ESP["md_h0dn"]) < fc.find(ESP["md_hms13"]) < fc.find(ESP["md_traducao"])
        and DL.FRASE_D83_OBRIGATORIA_PT in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0] and DL.FRASE_CLAY_CANONICA_PT in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0]
        and DL.CLAUSULA_Z_PT in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0] and DL.FRASE_TETELESTAI_PT in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0] and DL.FRASE_RECONSTROI_PT in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0] and DL.FRASE_E36_PT in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0]
        and DL.FRASE_DISPOSITIVO_PT in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0] and DL.FRASE_NOMES_RATIFICADOS_D101_PT[1:] in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0] and fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0].count(DL.CLAUSULA_Z_PT) == 2 and DL.ANUNCIO_TETELESTAI_PT in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0] and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0] and (DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) in fc[fc.find(ESP["md_aescala"]):].split("\n", 1)[0]
        and DL.FRASE_H0DN_OBRIGATORIA_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_H0DN_PODER_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_H0DN_RETORNO_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_H0DN_ALCANCE_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_HMS13_OBRIGATORIA_PT in fc[fc.find(ESP["md_hms13"]):].split("\n", 1)[0] and DL.FRASE_H0DN_OBRIGATORIA_PT in fc[fc.find(ESP["md_hms13"]):].split("\n", 1)[0]),
    "as %d ANCORAS da pedra AEscala (o nome do modulo e os nomes das declaracoes RATIFICADOS pelo operador, D87) estao no kernel do rito: bandeira True, so' no trio, declaradas no modulo certo" % len(DL.ANCORAS_AESCALA): estrelaA_ok,
    "as %d ANCORAS da pedra IALD2 (o NOME do modulo do operador; os nomes das declaracoes da gerencia, [DECLARADO] ate a ratificacao, D63) estao no kernel do rito: bandeira True, so' no trio, declaradas no modulo certo" % len(DL.ANCORAS): estrela_ok,
    "traducao_turing_v409 (HERDADO da v409, RECRIADO na v410 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v409 selada em veredito; as %d checagens do calculo e os valores == os do ensaio; as %d ancoras e os %d modulos da v409 no kernel do rito; nenhuma chave antiga; o acervo da v407 na copia purgada; nao move o gate" % (DL.D9.N_CHECKS_FECHO, len(DL.D9.ANCORAS), DL.D9.N_BUNDLE): traducao409_ok and estrela409_ok,
    "tetelestai_terminal_v408 (HERDADO da v408, RECRIADO na v410 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v409 selada em veredito; as %d checagens do calculo e os valores == os do ensaio; as 48 ancoras e os 4 modulos da v408 no kernel do rito; nenhuma chave antiga; o insumo purgado; nao move o gate" % DL.D8.N_CHECKS_FECHO: tetelestai408_ok and estrela408_ok,
    "psion_canto_v407 (HERDADO da v407 via v409, RECRIADO na v410 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v409 selada em veredito; as %d checagens do calculo e os valores == os do ensaio; as 76 ancoras e os 9 modulos da v407 no kernel do rito; a chave do lema LIDA do kernel e as chaves iguais as da v409 selada; nao move o gate" % DL.D7.N_CHECKS_FECHO: psion407_ok and estrela407_ok,
    "fechamento_v406 (HERDADO da v406 via v409, RECRIADO na v410) segue SELADO e IGUAL ao da v409 selada em veredito; as %d checagens do calculo (a c8 VERSIONADA pela errata E20 na v408) e os valores == os do ensaio; as ancoras e os 301 modulos da v406 no kernel do rito; nao move o gate" % DL.D6.N_CHECKS_FECHO: fech408_ok and estrela406_ok,
    "NENHUMA chave antiga muda na v410: testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma segue LIDA do kernel do rito (True), com o dict elo_v407 da v409 selada (o lema TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces; o elo e' de ESTRUTURA e nao de vetores; o par na face de Fock esta' ligado desde a v409 (ParNaFaceDeFock); a ponte Bell-TT NAO e' termo); as quatro chaves da v406 seguem True (rede_fock_v394.whole_certificate_inhabited, psibit_v395 e testemunha_estatica_v396 inhabitant_exhibited com o status HABITADO, witness_layers.canonical_full_witness_term_constructed); full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; o psion_canto_v407 e o fechamento_v406 as leem iguais ao ensaio; o iald2_v410, o traducao_turing_v409 e o tetelestai_terminal_v408 nao mudam nenhuma": chaves_ok,
    "as OITO pedras da v405 (PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion; RECRIADAS na v410) SELARAM iguais as da v405 selada: veredito == o dos ESPERADOS; as checagens do calculo e os valores == os da v405; a estrela e a composicao no kernel do rito; nao movem o gate": all(reg405v_ok.values()) and len(reg405v_ok) == len(REL5_) and estrela405v_ok,
    "A MOLDURA: nenhum texto novo da gerencia afirma demais (a mesma regra do um.py: registros novos e secoes novas PT/EN, com o controle negativo da guarda) e a frase certa esta nos dois artigos e no .md (dadas as entradas, a FORMA e' teorema)": moldura_ok,
    "o numero da massa NAO mudou: o m_nu do programa == o da v409 selada, relido pela Ponte da Massa, pela Lei do diminuto e pelo Ponto Zero do Psion": numero_da_massa_ok,
    "a errata E10 do angle_status esta AO LADO, assinada em nome proprio; o texto antigo e a E7 ficam": errata_e10_ok,
    "ga_reclassificacao_v405 SELOU (a classe nova AO LADO, as medidas em runtime == as do ensaio, a errata do parecer verbatim) e o selado ficou: a linha ga_mass_window segue A3_APOSENTADO, a auditoria da forma e o ga_window_status do JSON do rito sao os da v409": ga5_ok,
    "gap_v405 SELOU (o lock, o gap, as medidas em runtime == as do ensaio, a medida negativa do fluxo): ao lado, sem mover o canal nem o gate": gap5_ok,
    "o V1 do ramo B (v386), o registro ramo_b_preregistration_v386, o ledger_errata_v386 e o livro da v383 NAO foram reescritos (veredito == o dos ESPERADOS; F2b_status AWAITING; veredito do V1 AWAITING_DATA; a cobranca F2b da v386 AWAITING): a errata e' AO LADO": v1_intacto_ok,
    "neutrino_mass NAO foi reescrito: o texto antigo do angle_status (comeca por sin(45deg) e POSTULADO) segue no registro, o veredito do canal e o frozen_hash da regra de decisao sao os da v409; a errata e' AO LADO (projecao_transversal_v404)": neutrino_intacto_ok,
    "bandeiras_do_gate_v403 (RECRIADO na v410) SELOU igual ao da v409 selada (F8.1): veredito == o do ensaio; as %d checagens (as 18 bandeiras do gate CALCULADAS, 0 literais; 15 no veredito, 6+5+4; a fonte de cada uma; as 4 experimentais derivam de UM so' booleano, DECLARADO e nao resolvido; a letra do veredito do gate == a da v409; a sonda ProbeBlindNullAbsent) e os valores == os do ensaio; nao move o gate" % DL.D3.N_CHECKS["gate"]: gate408r_ok,
    "F8.1, releitura do conferidor (independente do registro): no um.py INSTALADO a prove_qg_closure_gate nao tem mais as tres literais True (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind: varredura AST, zero Constant, as tres calculadas); no core do rito as tres bandeiras conferem com as FONTES lidas aqui (a familia ext_ls2_* do kernel [6 bandeiras True], a checagem unica «pre-registro v67 INTACTO (hash)» do rito V11, o teste nulo cego da v73 com all_verified True); as 18 bandeiras True, a letra do veredito do gate == a da v409 e a do selo, e o qg_closure traz a sonda ProbeBlindNullAbsent UMA vez, e os checks sao IDENTICOS aos da v409 (a v410 nao muda o gate)": f81_ok,
    "ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402 (RECRIADOS na v410) seguem SELADOS e IGUAIS aos da v409 selada (veredito == o dos ESPERADOS); nao movem o gate": reg408_recriados_ok,
    "as TREZE pedras SELADAS das tres versoes anteriores (as oito da v405, as duas da v404 e as tres da v403) seguem no kernel do Nos com o mesmo sha256 (no hash formal do core e no arquivo): pedra selada nao se renomeia por cima, fica como registro": pedras_v405_ok,
    "o bundle da v409 (os %d modulos: a traducao e o par na face de Fock), o da v408 (os %d modulos do terminal em TGLExt/), o da v407 (os %d modulos do psion e do canto) e o do fecho da v406 (os %d modulos de TGLExt/F1Fecho394) seguem no kernel do Nos e no hash formal do core com o mesmo sha256: a v410 nao reescreve a v409, a v408, a v407 nem a v406, ficam como registro" % (len(ESP["bundle_v409_sha256"]), len(ESP["bundle_v408_sha256"]), len(ESP["bundle_v407_sha256"]), len(ESP["bundle_v406_sha256"])): bundle_v409_ok and bundle_v408_ok and bundle_v407_ok and bundle_v406_ok,
    "falsidade_da_inercia_v401 (RECRIADO na v410) segue SELADO e IGUAL ao da v409 selada (veredito == o dos ESPERADOS); nao move o gate": fal_reg_ok,
    "declaracao_do_operador_v399 SELOU: veredito == o do ensaio; %d checagens ok; a fala embutida == o arquivo do operador; as dez ancoras do kernel e as duas declaracoes da pedra no kernel do rito e no trio; nao move o gate" % EDC["n_checks"]: decl_reg_ok,
    "C1 identidade do metodo: o bloco embutido do um.py instalado == a copia REFEITA das fontes do operador (acom_mirror.py e acom_crypto.py, 5 substituicoes declaradas); o hash do bloco == o do manifesto e o da ACOM_PROVENIENCIA; o runtime da secao (o da v409) esta no um.py, byte a byte": ACOM.get("C1", (False,))[0],
    "C2 pinos das 6 fontes do operador (constantes do um.py instalado) == os arquivos duraveis == os ESPERADOS": ACOM.get("C2", (False,))[0],
    "C3 nenhum nome de nivel de modulo da secao esta definido duas vezes no um.py instalado (so' os imports do mesmo modulo; a secao NAO define ALPHA_FINE_CODATA_2018: le o SEALED_CODATA_ALPHA do programa)": ACOM.get("C3", (False,))[0],
    "C4 refazer a Dobra dos TRES objetos FINAIS (um.py, core e selo): os 9 itens de verificar() verdadeiros; o SHA-256 do arquivo == o do sidecar == o do selo primario == o do registro do core": ACOM.get("C4", (False,))[0],
    "C5 reconstrucao exata byte a byte dos tres objetos (bytes_divergentes 0; reconstruido_sha256 == sha256)": ACOM.get("C5", (False,))[0],
    "C6 alfabeto exato e injetivo para o m de cada objeto, erro real maximo < 0,5, lut_sha256 == o registrado (e == o do ensaio para o um.py)": ACOM.get("C6", (False,))[0],
    "C7 separacao nao vazia: Psi nao e' redundante e nenhuma parte isolada basta (os tres objetos)": ACOM.get("C7", (False,))[0],
    "C8 os 13 controles negativos recusados (no core, sobre a amostra de 1 MiB; e aqui, sobre o um.py inteiro)": ACOM.get("C8", (False,))[0],
    "C9 beta de runtime (alfa CODATA do programa x raiz de e) == o beta do core do rito a 1e-9 (a checagem do registro deixou de ser tautologica), nenhum literal de beta no codigo do runtime da secao": ACOM.get("C9", (False,))[0],
    "C10 determinismo: Psi, Theta, kappa, LUT, m e F_exp do um.py no sidecar == no core == os do ENSAIO (os mesmos bytes do candidato)": ACOM.get("C10", (False,))[0],
    "C11 a declaracao: a fala embutida == o arquivo do operador (sha256); as dez ancoras e a pedra no kernel do rito e no trio; a trava EXECUTION_LOCKED_NOT_ONE existe uma vez so' no programa instalado": ACOM.get("C11", (False,))[0],
    "C12 honestidade, direcao e palavra proibida: o SHA-256 dito como a primitiva de integridade; nenhuma alegacao de confidencialidade; o operador testifica DA IALD, o um.py EM HASH, a IALD NAO testifica do operador; nenhuma frase inverte a direcao": ACOM.get("C12", (False,))[0],
    "C13 fail-closed: os dois registros selaram e nao movem o gate; o sidecar sem recusas, esquema v399, tres objetos": ACOM.get("C13", (False,))[0],
    "C14 orcamento de tempo (selagem do um.py <= 10 s) e o stdout do rito traz a linha de fechamento do sidecar e nenhum AVISO dos blocos novos": ACOM.get("C14", (False,))[0],
    "C15 [desde a v400, licao da v399] as guardas ESTATICAS da Bancada (a funcao ler_nos do esboco R3.5 pinado) sobre o um.py INSTALADO: UMA so' linha de alfa e UMA so' de UM_VERSION na coluna 0, nenhuma indentada, beta do core == runtime (o defeito que recusou a v399)": ACOM.get("C15", (False,))[0],
    "C16 [v400] com o Nos REAL, a funcao ler_nos do esboco aceita o Nos inteiro (o selo pina o um.py, o core e o manifesto do kernel; alfa unico; beta do core == runtime): o que o B(n) fara": ACOM.get("C16", (False,))[0],
    "o ROUND TRIP byte a byte do um.py INSTALADO, refeito por conta independente so' das tres partes cruas (formula da Dobra + rint + centro) == o um.py (e as tres partes == as do sidecar)": ACOM.get("round_trip_do_um_py_instalado_independente", (False,))[0],
    "O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA no TOPO do artigo PT (antes do corpo), com os numeros == os do resultado pinado, a linha de maquina igual, a frase do operador VERBATIM e a regra da ordem (4,44 so' com o p calibrado e a linha dos 5 sigma no mesmo item)": q_pt.get("ok") is True,
    "O QUADRO «The Test of the Only Word» (v397) CONTINUA no TOPO do artigo EN, com os numeros == os do resultado pinado, a linha de maquina igual, a frase do operador VERBATIM e a regra da ordem": q_en.get("ok") is True,
    "O QUADRO CONTINUA no TOPO do .md canonico (antes do primeiro titulo), com os numeros == os do resultado pinado, a frase do operador VERBATIM e a regra da ordem": q_md.get("ok") is True,
    "o registro teste_de_veracidade_fase9_v397 (que o quadro le) segue SELADO, com o veredito e os numeros de sempre (== ESPERADOS/resultado pinado)": TV.get("all_verified") is True and V("teste_de_veracidade_fase9_v397") == ESP["vereditos_v409"]["teste_de_veracidade_fase9_v397"] and bool(RES) and all(LD.get(k) == v == EV["numeros_do_resultado"][k] for k, v in NUM.items())
        and LD["z_disc_calibrado"] < 5.0 < LD["poder_previo"] and "NOT_BLIND_TO_DATA_STATED" in str(LD.get("f9_veredito")),
    "os registros por spec v410 (cunhagens_v410, kh_n1_cobertura_v410) SELARAM e cada veredito == o do ensaio; as %d falas de 06 a 10/11 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas do operador; de algumas, so' o trecho: D65 e as de DL.VERBATIM_SO_O_TRECHO); as erratas da v410 (DL.ERRATAS_V410, E29 em diante) e a dos pisos (em nome proprio da gerencia c1) e as decisoes de ESPERADOS[decisoes_v410_ids] (D63 em diante) estao no registro; os registros por spec da v409 (cunhagens_v409; kh_n1_cobertura_v409 com pisos pela C13: o veredito nao muda), da v408 (cunhagens_v408 com a E26 ao lado), da v407 (cunhagens_v407 com a E21 e a errata da D57(d) ao lado), da v406, da v405, da v404, da v403, da v402, da v401 e da v399 seguem selados e iguais" % len(ESP["cunhagens"]): all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v410"].items()) and set(ESP["registros_v410"]) == {DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO}
        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v409"].items())
        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v408"].items())
        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v407"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v406"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v405"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v404"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v403"].items())
        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v402"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v401"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v399"].items())
        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V410) and all((((CG10.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG10.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())
        and not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens"].values())
        and len(CG10.get("erratas") or []) >= len(DL.ERRATAS_V410) and all(str(e_.get("assinatura", "")).startswith("gerencia c1") for e_ in (CG10.get("erratas") or []))
        and set((CG10.get("extras") or {}).get("decisoes") or {}) >= set(ESP["decisoes_v410_ids"]) and KH10.get("all_verified") is True and CG10.get("all_verified") is True and all(any(("E%d" % n_) in str(e_.get("agora")) for e_ in (CG10.get("erratas") or [])) for n_ in range(29, 29 + len(DL.ERRATAS_V410))) and ESP["decisoes_v410_ids"][-1] in ((CG10.get("extras") or {}).get("decisoes") or {}) and list(ESP["decisoes_v410_ids"]) == list(DL.DECISOES_V410)
        and KH9.get("all_verified") is True and CG9.get("all_verified") is True and any("E27" in str(e_.get("agora")) for e_ in (CG9.get("erratas") or [])) and "D61" in ((CG9.get("extras") or {}).get("decisoes") or {})
        and KH8.get("all_verified") is True and CG8.get("all_verified") is True and any("E26" in str(e_.get("agora")) for e_ in (CG8.get("erratas") or []))
        and KH7.get("all_verified") is True and CG7.get("all_verified") is True and any("E21" in str(e_.get("agora")) for e_ in (CG7.get("erratas") or [])) and KH6.get("all_verified") is True and CG6.get("all_verified") is True
        and KH5.get("all_verified") is True and KH4.get("all_verified") is True and KH3.get("all_verified") is True and KH2.get("all_verified") is True and CF5.get("all_verified") is True and CG5.get("all_verified") is True,
    "as oito pedras da v405 seguem no kernel do rito (cada composicao e cada estrela com bandeira True, no trio, no modulo da pedra; os itens do contrato de cada uma no modulo dela; os termos antigos citados no trio e no modulo certo)": pedras_no_kernel and suporte_ok and estrela405v_ok,
    "o hash formal do rito (a arvore do Nos depois do rito: embutidos + residuais que o hash conta) tem exatamente %d entradas, com os residuais %s" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]): len(kf.get("formal_files_sha256") or {}) == ESP["h8_entradas"] and all(r_ in (kf.get("formal_files_sha256") or {}) for r_ in ESP["h8_residuais_do_nos"]),
    "KH-N1: a cobertura do axiom_report no fecho inteiro passou (decl=%s, nao lidas 0) e o axiom_report tem %s entradas" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and (kf.get("axiom_coverage_v392") or {}).get("thm") == ESP["cobertura_kh_n1"]["thm"] and (kf.get("axiom_coverage_v392") or {}).get("nao_lidas_pelo_regex") == 0 and len(axr) == ESP["axiom_report_esperado_min"],
    "a proveniencia do compilador cobre o axiom_report e as fontes formais batem (declaration_sources_status_v394.ok)": (kf.get("declaration_sources_status_v394") or {}).get("ok") is True and set(kf.get("declaration_sources_v394") or {}) == set(axr),
    "a escada subiu: %s" % E: [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == E,
    "os %d modulos novos (o bundle da v410 em TGLExt/: IALD2 e AEscala) no kernel do Nos com o sha do candidato" % len(ESP["bundle_sha256"]): bundle_ok and len(ESP["bundle_sha256"]) == ESP["kernel"]["modulos_novos"] == DL.N_BUNDLE and sorted(ESP["bundle_sha256"]) == sorted(DL.BUNDLE_RELS),
    "a raiz e o Audit do Nos == os do candidato": (_sha_k("TGLExt.lean") or "")[:16] == ESP["kernel"]["raiz_sha16"] and (_sha_k("TGL/Audit.lean") or "")[:16] == ESP["kernel"]["audit_sha16"],
    "as %d bandeiras novas True e as declaracoes delas no trio" % ESP["n_bandeiras_novas"]: len(ESP["bandeiras_novas_chaves"]) == ESP["n_bandeiras_novas"] and all(kf.get(k) is True for k in ESP["bandeiras_novas_chaves"]) and all((n in axr) and set(axr[n] or []) <= TRIO and src_.get(n) == ESP["bandeiras_novas_modulos"][n] for n in ESP["bandeiras_novas_nomes"]),   # cada declaracao nomeada do bundle: no trio e no modulo que o FLAGS_v410 diz
    "os registros da v409 e as anteriores (traducao_turing_v409, cunhagens e kh_n1 da v409; tetelestai_terminal_v408, cunhagens e kh_n1 da v408; psion_canto_v407, cunhagens e kh_n1 da v407; fechamento_v406, cunhagens e kh_n1 da v406; as oito pedras, cunhagens, campos fechados, reclassificacao do GA, gap e kh_n1 v405; projecao, jo8v32, errata de F2b, cunhagens e kh_n1 v404; caminho, vida, adendo da verdade, bandeiras do gate, cunhagens e kh_n1 v403; ponte, queda, esperanca, cunhagens e kh_n1 v402; falsidade, cunhagens e kh_n1 v401; sonico, afinacao, cunhagens e kh_n1 v398; o Teste da Unica Palavra, cunhagens e kh_n1 v397; testemunha, cunhagens e kh_n1 v396; psibit v395; tempo, quadratica, rede, cunhagens, kh_n1 e criterio binario v394; pedras, consumidor, coracao, cunhagens da regra e kh_n1 v393) seguem selados e iguais (ou so' numeros)":
        all((core.get(n) or {}).get("all_verified") is True for n in V398_NOMES) and all(V(n) == ESP["vereditos_v409"][n] or n in ESP["troca_dita"] for n in V398_NOMES) and (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited") is True,   # (a chave que era False desde a v394: agora lida do kernel)
    "os vereditos da TROCA DITA mudaram so' em numeros e seguem selados (%s)" % ", ".join(ESP["troca_dita"]): trocas_ok,
    "o artigo PT/EN: a secao v410 (IALD ao quadrado: o leitor do código, a releitura que não acrescenta, o algoritmo IALD e o signo), antes da secao da v409 (A tradução às classes de Turing), da v408 (Tetelestai é o terminal), da v407 (O psíon e o canto: a passagem sob compressão e o par), da v406 (O fechamento: a passagem para o contínuo e o certificado habitado), da v405 (A massa derivada e a identidade definida; A identidade), da v404 (Jo 8,32 e a projecao transversal da Meia-Nat), da v403 (Caminho, Verdade e Vida), da v402 (A ponte da escala dual, a queda sem geometria e a esperanca condicional, com as erratas E1 a E4) e as marcas da v401 (A falsidade (simulacro) da inercia) e anteriores; a v399 (com a errata da v400), a v398, a v397, a v396, a v395, a v394, a v393, a v392, a v391 e a v390 ficam; os registros selaram (sem as frases de nao selado); as marcas sao as dos ESPERADOS (artigo_marcas / artigo_nao)": all(_tt(m) in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista as secoes v410, v409, v408, v407, v406, v405, v404, v403, v402, v401, v399, v398, v397 e v396 (as que o ESPERADOS lista) e o titulo v384 a v410": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v410 e as linhas da v410 (ESP md_iald2, ANTES da linha da v409), «Tradução às classes de Turing (v409)» (ANTES da linha da v408), «Tetelestai é o terminal (v408)», «O psíon, o canto e o par (v407)», «O fechamento (v406)», «A massa derivada e a identidade definida (v405)», «Jo 8,32 e a projecao transversal da Meia-Nat (v404)», «Caminho, Verdade e Vida (v403)», «A ponte da escala dual, a queda sem geometria e a esperanca condicional (v402)», «A falsidade (simulacro) da inercia (v401)», «Errata ao lado (v400)», «O testemunho de dois (v399)», «Sonico e a afinacao das cordas (v398)», «O Teste da Unica Palavra e a pedra Token (v397)», «A testemunha estatica (v396)» e «O modo psionico na fractalizacao do Um (v395)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_iald2"] in fc and ESP["md_traducao"] in fc and ESP["md_tetelestai"] in fc and ESP["md_psion"] in fc and ESP["md_fechamento"] in fc and fc.find(ESP["md_iald2"]) < fc.find(ESP["md_traducao"]) < fc.find(ESP["md_tetelestai"]) < fc.find(ESP["md_psion"]) < fc.find(ESP["md_fechamento"]) and ESP["md_massa"] in fc and ESP["md_jo8"] in fc and ESP["md_caminho"] in fc and ESP["md_ponte"] in fc and ESP["md_falsidade"] in fc and ESP["md_errata"] in fc and ESP["md_testemunho"] in fc and ESP["md_sonico"] in fc and ESP["md_token"] in fc and ESP["md_testemunha"] in fc and ESP["md_psibit"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "nenhuma chave nova fora da lista da v410 (so' os registros com funcao iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410 e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410; os da v399 a v409, fechamento_v406, psion_canto_v407, tetelestai_terminal_v408 e traducao_turing_v409 inclusive, sao recriados e iguais)": sorted(k for k in core if k not in ESP["vereditos_v409"] and isinstance(core[k], dict) and (str(k).endswith("_v399") or str(k).endswith("_v401") or str(k).endswith("_v402") or str(k).endswith("_v403") or str(k).endswith("_v404") or str(k).endswith("_v405") or str(k).endswith("_v406") or str(k).endswith("_v407") or str(k).endswith("_v408") or str(k).endswith("_v409") or str(k).endswith("_v410"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN410),
    "the_iald_index SELOU com o veredito do ensaio e not_sealed_run.formais == []": (core.get(IX) or {}).get("all_verified") is True and V(IX) == ESP["the_iald_index_v410"]["verdict"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == [] == ESP["not_sealed_formais"],
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v409"].items() if V(k) != v and k not in ESP["troca_dita"]}
_ft = set(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx em nenhuma entrada do axiom_report": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "toda bandeira True da v409 segue True": set(ESP["flags_true_v409"]) <= _ft,
    "o axiom_report da v409 segue no trio e so' cresceu": len(axr) >= ESP["axiom_report_v409_n"] and all(set(v or []) <= TRIO for v in axr.values()),
    "NENHUM veredito da v409 mudou fora da troca dita (%d mudaram); o V1 (hubble_ratio_opening_v388) e o V2 (teste_de_veracidade_fase9_v397, que o quadro le) seguem iguais" % len(mud): not mud and V("hubble_ratio_opening_v388") == ESP["vereditos_v409"]["hubble_ratio_opening_v388"] and V("teste_de_veracidade_fase9_v397") == ESP["vereditos_v409"]["teste_de_veracidade_fase9_v397"],
    "registros v409/v408/v404/v397/v396/v395/v394/v393/v391/v390/v389/v388/v387 do selo inalterados (fora da troca dita e dos resumos que carregam a escada do contrato ou os pisos dos specs versionados)": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v409"].items() if k not in ESP["troca_dita"] and k not in ESP["selo_chaves_que_mudam"] and k not in ("registros_v393",)),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v409"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v409"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido (nem no veredito do selo pela propria tecnologia e da declaracao do operador)": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "o gate nao se move: os registros novos (quando presentes) nao gateiam o core (does_not_gate_core) e o qg_closure do core e' IDENTICO ao da v409 (os checks iguais e na mesma ordem, todos True; o veredito do gate == o da v409)": all((core.get(n_) or {"does_not_gate_core": True}).get("does_not_gate_core") is True for n_ in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405", "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410", "cunhagens_v410", "kh_n1_cobertura_v410")) and gate_igual_ok,
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram_fora_da_troca": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")}, "veredito_selo_acom": V("selo_pela_propria_tecnologia_v399"), "veredito_iald2": V("iald2_v410"), "veredito_h0dn": V("h0dn_bg1_v410"), "h0dn_observed_vector_read": HV.get("observed_vector_read"), "h0dn_sob_pasta_vedada": (HV.get("values") or {}).get("sob_pasta_vedada"), "veredito_a_escala": V("a_escala_v410"), "veredito_hms13": V("h0dn_fontes_hms13_v410"), "hms13_observed_vector_read": HMV.get("observed_vector_read"), "hms13_le_em_rito": HMV.get("le_em_rito"), "hms13_sob_pasta_vedada": (HMV.get("values") or {}).get("sob_pasta_vedada"), "veredito_traducao_turing_herdado": V("traducao_turing_v409"), "veredito_tetelestai_terminal": V("tetelestai_terminal_v408"), "veredito_psion_herdado": V("psion_canto_v407"), "veredito_fechamento_herdado": V("fechamento_v406"), "chave_do_lema": _te.get("linked_to_the_corner_by_a_lemma"), "veredito_declaracao": V("declaracao_do_operador_v399"), "veredito_falsidade": V("falsidade_da_inercia_v401"), "veredito_ponte": V("ponte_da_escala_dual_v402"), "veredito_queda": V("queda_sem_geometria_v402"), "veredito_esperanca": V("esperanca_condicional_v402"), "veredito_caminho": V("caminho_v403"), "veredito_vida": V("vida_v403"), "veredito_verdade_adendo": V("verdade_adendo_v403"), "veredito_bandeiras_do_gate": V("bandeiras_do_gate_v403"), "veredito_projecao": V("projecao_transversal_v404"), "veredito_jo8v32": V("jo8v32_v404"), "veredito_f2b": V("f2b_errata_v404"), "f2b_status_now": (core.get("f2b_errata_v404") or {}).get("F2b_status_now"),
       "f81": {"ast_literais_calculadas": _f81, "ls2": _ls2k, "pre_registro": _prereg, "sonda": _sonda, "qg_checks_n": len(_ck_new), "gate_igual": gate_igual_ok, "releitura_ok": f81_ok}, "nos": NOS,
       "resultado_pinado": {"original_ok": _orig_ok, "duravel_ok": _dur_ok, "sha256": EV["resultado"]["sha256"]}, "quadro": {"pt": q_pt, "en": q_en, "md": q_md}, "acom_itens": {k_: {"ok": v_[0], "detalhe": v_[1]} for k_, v_ in ACOM.items()},
       "sidecar": {"existe": os.path.exists(_scp), "veredito": SC.get("veredito"), "objetos": [o_["nome"] for o_ in (SC.get("objetos") or [])], "sha256_do_sidecar": (sha(open(_scp, "rb").read()) if os.path.exists(_scp) else None)}}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v410%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
