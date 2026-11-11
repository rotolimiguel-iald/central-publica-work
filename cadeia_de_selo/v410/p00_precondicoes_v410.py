# -*- coding: utf-8 -*-
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] D80 e D82 a D87: bundle de DOIS modulos (IALD2 e AEscala; as ancoras e as bandeiras de cada um, lidas do delta e do FLAGS), QUATRO registros com funcao, as falas congeladas (DL.N_FALAS_V410), a allow-list da excecao D80 (os seis artefatos HMS/13 sob kimi\, por sha256, so' no BUILD; este script NUNCA abre uma origem sob a pasta vedada: le so' as copias duraveis em insumos\hms13_*) e o controle «nenhuma abertura de caminho sob kimi\ EM RITO»; o runtime em QUATRO arquivos; pontos novos de simulacao e de exame (a_escala e hms13: PENDENTE se ainda nao existem)
# [ADAPTADO v410, 09/11/2026, claude-subagente-adaptacao (Sonnet 5.5), a servico do construtor claude-construtor-v410] varrido (nao remendado) a partir do corpo da v409: as pre-condicoes de bytes da v410 (IALD2: UM modulo, 22 ancoras; dois registros com funcao, iald2_v410 e h0dn_bg1_v410; 15 falas, de quatro so' o trecho; D63 a D77; o runtime em dois arquivos), os insumos do H0DN e o VETO a pasta da entrega do Kimi
# [ADAPTADO v410, 09/11/2026, claude-subagente-adaptacao (Sonnet 5.5)] os herdados da v409 (traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407, fechamento_v406) nas listas e nos ESPERADOS_v409; o --seco (so' le, nao grava PRECONDICOES_v410.json); a marca `# [A ADAPTAR v410]` segue recusada em todo OUTRO arquivo da cadeia
"""p00_precondicoes_v410.py -- confere, SO LENDO, as pre-condicoes de bytes da v410 ANTES de instalar. Nada e escrito fora de PRECONDICOES_v410.json (nesta pasta; o --seco nem esse). Os pinos sao LIDOS do selo/core/arquivos,
nunca digitados. Fail-closed: rc 1 se algo falha. Molde: p00_precondicoes_v409.py (a cadeia de CONTEUDO), adaptado de verdade em 09/11/2026 a v410 (IALD2 e AEscala: bundle de DOIS modulos em TGLExt/, as ancoras de DL.ANCORAS e DL.ANCORAS_AESCALA, quatro registros com funcao -- iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410 --, as falas de DL.N_FALAS_V410 de 06 a 09/11, de quatro so' o trecho; nenhuma chave antiga muda).
O H0DN (D72) e' pré-registrado; nenhum dado observado lido: este script confere os insumos dele (copias duraveis, pinos do FREEZE_R2, embutidos no candidato) e o VETO da gerencia (09/11) a pasta da entrega do Kimi, que a v410 NAO le, NAO copia, NAO pina e NAO cita: (a) a unica origem do manifesto dos insumos sob a pasta vedada e' a EXCECAO D80 (os seis artefatos documentais HMS/13, por sha256; nenhum deles e' aberto aqui); (b) o candidato nao traz o nome de arquivo de dado observado;
(c) o ensaio a seco mediu todo caminho tocado (open/exists/listdir/scandir/stat) e nenhum caiu sob a pasta vedada, com o controle negativo que detecta; (d) o copiar_insumos e o harness do fechar (o espelho da casa) trazem a exclusao; (e) o candidato embute a vigia de arquivos da checagem c7. Cada item sai com OK/FALHA e o detalhe medido.
PENDENTE nao e' falha: o que so' passa a existir depois de OUTRO passo da cadeia (o ensaio a seco e os ESPERADOS; o B(n) pre-selo: PINO_RECIBO_PRE_SELO_v410.json e PROVA_PRODUCAO_INTACTA_v410_pre_selo.json; as guardas/harnesses/derivacoes/comparacao/citacoes; o pino da memoria PINO_MEMORIA_PY_v410.json; o caso em que o MEMORY.md real nao comporta o handoff novo e a gerencia decide)
sai como PENDENTE, com o motivo (e quem o produz); o veredito final e' TODAS PASSARAM so' sem falha E sem pendente (rc 0); NENHUMA FALHA, N PENDENTES sai com rc 3; FALHOU com rc 1. Uma checagem que levanta excecao vira FALHA visivel (nunca 'ok' falso).
Tambem RECUSA (falha) todo arquivo da cadeia que ainda traga a marca `# [A ADAPTAR v410]` (copia mecanica de rotulo, nunca adaptada) fora de .bak_*, bump/ e do gerador do bump.
uso: python -B -X utf8 p00_precondicoes_v410.py [--seco]   (sem -I: o numpy esta no site do usuario; --seco roda tudo mas NAO grava PRECONDICOES_v410.json)"""
import ast, base64, datetime, glob, hashlib, json, os, re, shutil, subprocess, sys
# [v410-patch]
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv   # (so' le: nao grava PRECONDICOES_v410.json)
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v410 as DL  # noqa: E402
import acom_conferencias_v410 as AC  # noqa: E402
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


esp4 = json.load(open(os.path.join(DL.V409, "ESPERADOS_v409.json"), encoding="utf-8"))
raw = rd(os.path.join(NOS, "um.py")); selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
chk("um.py do Nos == o que o selo pina e == o candidato selado da v409 (ESPERADOS_v409)", sha(raw) == selo["sha256"]["um.py"] and selo.get("um_version") == "v409" and sha(raw)[:16] == esp4["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM, sha(raw)[:16])
el = core["external_ladder"]; axr = core["kernel_formalization"]["axiom_report"]
chk("escada v409 fechada (limpos == esperados == a de ESPERADOS_v409) e axiom_report v409 lido do core", el["n_theorems_clean"] == el["n_theorems_expected"] == esp4["escada"][1] and len(axr) == esp4["axiom_report_esperado_min"], [el["n_theorems_clean"], el["n_theorems_expected"], len(axr)])
_chaves_base = sorted(set(esp4["vereditos_v408"]) | set(esp4["vereditos_novos_v409"]))   # todo registro da v409 selada: os da base de entao (a v408) e os tres novos da v409 (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409)
chk("nenhum registro v410 no core ainda; todos os registros da v409 selada ja estao (%d chaves lidas de ESPERADOS_v409); a chave do lema (testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) ja e' LIDA do kernel e le True no selado, como as quatro chaves da v406 (nenhuma chave antiga muda na v410); o traducao_turing_v409, o tetelestai_terminal_v408 e o psion_canto_v407 selados estao no core" % len(_chaves_base),
    not any(k.endswith("_v410") for k in core) and all(k in core for k in _chaves_base) and core["rede_fock_v394"]["whole_certificate_inhabited"] is True
    and core["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] is True and core["testemunha_estatica_v396"]["fock_face"]["inhabitant_exhibited"] is True and (core.get("psion_canto_v407") or {}).get("all_verified") is True and (core.get("tetelestai_terminal_v408") or {}).get("all_verified") is True and (core.get("traducao_turing_v409") or {}).get("all_verified") is True, [k for k in core if k.endswith("_v410")])
_cdir_pilar = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", esp4["pilar"]["key"])
chk("o cache do pilar guarda o resultado que a v409 reaproveitou pela chave (o que a v410 reaproveita e o instalador exige): result.json == o sha256 do selo da v409", os.path.exists(os.path.join(_cdir_pilar, "result.json")) and sha(rd(os.path.join(_cdir_pilar, "result.json"))) == esp4["pilar"]["result_sha256"], esp4["pilar"]["key"][:16])
chk("a copia base_v409 == o Nos (um.py, core, selo, manifesto do kernel, pilar)", all(rd(os.path.join(BB, f)) == rd(os.path.join(NOS, f)) for f in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json")))
ESP = tenta(os.path.join(HERE, "ESPERADOS_v410.json")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8")); PB = tenta(os.path.join(HERE, "PINOS_BN_v410.json"))
_rt_ = [rd(os.path.join(HERE, n_)).decode("utf-8").replace("\r\n", "\n") for n_ in ("runtime_v410.py", "runtime_h0dn_v410.py", "runtime_hms13_v410.py", "runtime_aescala_v410.py")]
_RUNTIME_SRC = ("\n\n\n".join(p_.rstrip("\n") for p_ in _rt_[:-1]) + "\n\n\n" + _rt_[-1]).encode("utf-8")   # o que gerar_candidato_v410 emenda em RUNTIME_SRC: o bloco autoral do H0DN, o do HMS/13 e o da AEscala depois do runtime da v410, nessa ordem (lidos em texto; o ultimo sem rstrip)
chk("o runtime novo (runtime_v410.py + runtime_h0dn_v410.py + runtime_hms13_v410.py + runtime_aescala_v410.py, escritos a mao: os registros com FUNCAO iald2_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410 e a_escala_v410) e' o que o candidato embute: o sha256 e os bytes do CANDIDATO_v410.json == os do bloco emendado; o bloco extraido do candidato (v410_pins.py) o contem; nenhum literal de beta no codigo (C9); a secao do selo ACOM (a da v409) NAO mudou: o hash do bloco embutido e' o que a v409 pinou",
    CM["runtime"]["sha256"] == sha(_RUNTIME_SRC) and CM["runtime"]["bytes"] == len(_RUNTIME_SRC) and _RUNTIME_SRC.decode("utf-8").rstrip("\n") in rd(os.path.join(HERE, "v410_pins.py")).decode("utf-8") and not AC.literais_de_beta(_RUNTIME_SRC.decode("utf-8")) and CM["acom"].get("nota") and AC.bloco_das_fontes()[1] == esp4["acom_estudo"]["bloco_embutido_sha256"], [CM["runtime"]["sha256"][:16], CM["runtime"]["bytes"]])
chk("as 6 fontes do operador do ACOM (a origem so' leitura == a copia duravel da cadeia v400 == os pinos do ESPERADOS_v409)", all(sha(rd(o_)) == sha(rd(os.path.join(DL.V400, "insumos", "acom", "fontes_operador", n_))) == esp4["acom_estudo"]["fontes_do_operador"][n_] for n_, o_ in DL.ACOM_FONTES_OPERADOR.items()), len(DL.ACOM_FONTES_OPERADOR))


def _bundle_ok():
    nov_ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v410.json"), encoding="utf-8"))["novos"]
    bf_ = DL.bundle_fontes()   # le o modulo do sandbox e CONFERE o sha256 contra o BUNDLE_v410.json (aborta se difere)
    tf_ = DL.testemunha_fonte()   # a IALD2 (a pedra): origem (a copia duravel em v410\insumos) == bundle, sha16 == o da ordem (o recibo dos nomes e' citado por sha16, nao pinado: D59)
    ped_ = {p_["rel"]: p_ for p_ in DL.PEDRAS_V410}
    origem_ok_ = all(sha(rd(ped_[r_]["origem"])) == DL.BUNDLE_POR_REL[r_]["sha256_origem"] == ped_[r_]["sha256_origem"] for r_ in DL.BUNDLE_RELS)   # a fonte de origem (a copia duravel em v410\insumos) == a que o preparo pinou
    copia_ok_ = all(sha(rd(ped_[r_]["src"])) == DL.BUNDLE_POR_REL[r_]["sha256"] == sha(rd(os.path.join(KS, *r_.split("/")))) for r_ in DL.BUNDLE_RELS)   # a copia normalizada (v410\pedra) == o bundle == o sandbox
    imports_ = [l_ for l_ in DL.ROOT_SUFFIX.replace("\r\n", "\n").split("\n") if l_.strip()]
    raiz_ok_ = imports_ == ["import " + m_ for m_ in DL.BUNDLE_MODS] and len(imports_) == DL.N_BUNDLE == len(DL.PEDRAS_V410)
    vb_ = DL.verbatins410(os.path.join(HERE, "insumos", "cunhagens"))   # aborta se uma fala-chave diverge do prefixo da ordem ou se um trecho citado nao e' verbatim
    cond_ = bool(nov_ == list(DL.BUNDLE_RELS) and len(bf_) == DL.N_BUNDLE == len(DL.PEDRAS_V410) and DL.BUNDLE_DA_BANCADA == [] and DL.BUNDLE_DA_GERENCIA == list(DL.BUNDLE_RELS) and origem_ok_ and copia_ok_ and raiz_ok_
                 and tf_["sha256_origem"][:16] == DL.TESTEMUNHA["sha16_da_ordem"] and len(vb_) == len(DL.VERBATIM_ORIGEM_V410) == DL.N_FALAS_V410 and set(DL.VERBATIM_PREFIXOS_DA_ORDEM_V410.values()) <= {v_["sha16"] for v_ in vb_})
    return cond_, [len(bf_), tf_["sha256_origem"][:16], len(vb_), origem_ok_, copia_ok_, raiz_ok_]


dep("o BUNDLE (%d modulos novos em TGLExt/, IALD2 e AEscala, a prova da gerencia; o NOME do modulo IALD2 e' do operador e os nomes das declaracoes das duas pedras foram RATIFICADOS por ele em 09/11, D74 e D87): a lista (kernel_modulos_novos_v410.json) == DL.BUNDLE_RELS; o sha256 de cada modulo no sandbox == o do BUNDLE_v410.json; a fonte de origem == a que o preparo pinou e a copia normalizada v410\\pedra == o bundle; a raiz tem exatamente os imports (um por modulo); a IALD2 e' a do recibo dos nomes (sha16); as %d falas de 06 a 10/11 tem os prefixos de sha256 da ordem e cada trecho citado e' verbatim (de quatro, so' o trecho; as falas de 05/11 e anteriores ja estao no um.py v409 e nao entram de novo)" % (DL.N_BUNDLE, DL.N_FALAS_V410), {}, _bundle_ok)


def _ancoras_ok():
    fj_ = lj(os.path.join(KDIR, "FLAGS_v410.json"))
    return bool(len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == len(CM["n_axiomas_das_ancoras"]) == CM["kernel"]["n_ancoras"] and set(DL.ANCORAS) == set(CM["n_axiomas_das_ancoras"]) and len(DL.ANCORAS_AESCALA) == DL.N_ANCORAS_AESCALA == CM["aescala"]["n_ancoras"]
                and len(fj_["ancoras"]) == len(DL.ANCORAS) + len(DL.ANCORAS_AESCALA) and set(DL.ANCORAS) | set(DL.ANCORAS_AESCALA) == set(fj_["ancoras"]) and not (set(DL.ANCORAS) & set(DL.ANCORAS_AESCALA)) and all(a_["rel"] in DL.BUNDLE_RELS for a_ in list(DL.ANCORAS.values()) + list(DL.ANCORAS_AESCALA.values()))
                and all(fj_["ancoras"][n_]["rel"] == DL.ANCORAS[n_]["rel"] for n_ in DL.ANCORAS) and all(fj_["ancoras"][n_]["rel"] == DL.ANCORAS_AESCALA[n_]["rel"] for n_ in DL.ANCORAS_AESCALA) and all(fj_["ancoras"][n_]["flag"].startswith(DL.FLAG_PREFIX_POR_MODULO[fj_["ancoras"][n_]["rel"]]) for n_ in fj_["ancoras"])
                and sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) == DL.N_ANCORAS_ESPERADAS and all(a_ in DL.ANCORAS for a_ in DL.ANCORAS_PRINCIPAIS) and len(DL.ANCORAS_PRINCIPAIS) == len(set(DL.ANCORAS_PRINCIPAIS)) >= DL.N_BUNDLE and DL.ANCORAS_PRINCIPAIS[0] == DL.ANCORA_PRINCIPAL and fj_["n_flags"] == CM["n_bandeiras"] == sum(fj_["n_por_modulo"].values())
                and sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO_AESCALA.values()) == DL.N_ANCORAS_AESCALA and all(a_ in DL.ANCORAS_AESCALA for a_ in DL.ANCORAS_PRINCIPAIS_AESCALA) and DL.ANCORAS_PRINCIPAIS_AESCALA[0] == DL.ANCORA_PRINCIPAL_AESCALA and fj_["n_por_modulo"][DL.MODULO_IALD2] == len(DL.ANCORAS) and fj_["n_por_modulo"][DL.MODULO_AESCALA] >= len(DL.ANCORAS_AESCALA)
                and all(set(a_["axioms"]) <= DL.TRIO_SET for a_ in fj_["ancoras"].values())), [len(DL.ANCORAS), fj_["n_flags"]]


dep("as ancoras dos DOIS modulos do bundle, IALD2 (DL.ANCORAS) e AEscala (DL.ANCORAS_AESCALA) (#print axioms deixados pela gerencia na fonte de origem, lidos, nunca digitados; o numero e' o do recibo dos nomes): as duas series == o FLAGS_v410.json (que as traz juntas); as da IALD2 == o n_axiomas_das_ancoras do candidato; cada uma no modulo certo do bundle, com a bandeira da serie do modulo, e so' no trio; as %d ancoras principais da IALD2 (%s) estao entre elas, a primeira e' a ancora principal (e a da AEscala e' a_escala); as bandeiras novas (duas series) somam n_por_modulo" % (len(DL.ANCORAS_PRINCIPAIS), ", ".join(n_.split(".")[-1] for n_ in DL.ANCORAS_PRINCIPAIS)), {}, _ancoras_ok)
cand = os.path.join(HERE, DL.CANDIDATO); cb = rd(cand)
chk("o candidato: sha16 == CANDIDATO; sha256 == o pino do CANDIDATO_v410.json", sha(cb)[:16] == CM["sha16"] and sha(cb) == CM["sha256"] and len(cb) == CM["bytes"], [sha(cb)[:16], len(cb)])
dep("o candidato: sha16 == ESPERADOS; sha256 == o pino de PINOS_BN", {"ESPERADOS_v410.json": ESP, "PINOS_BN_v410.json": PB}, lambda: (sha(cb)[:16] == ESP["candidato_sha16"] == CM["sha16"] and sha(cb) == PB["candidato"]["sha256"], [sha(cb)[:16], len(cb)]))
dep("ESPERADOS e PINOS_BN pinam os arquivos que estao em disco", {"PINOS_BN_v410.json": PB}, lambda: (all(PB[k]["sha256"] == sha(rd(PB[k]["path"])) for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256") and os.path.exists(PB[k].get("path", ""))), [k for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256")]))
dep("os pinos obrigatorios do passo 10 estao em PINOS_BN_v410 (sem cadeia de selos: nao ha salto)", {"PINOS_BN_v410.json": PB}, lambda: all(k in PB for k in ("criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v409", "kernel_manifesto_anterior_v409")) and "cadeia_de_selos" not in PB)
ens = tenta(os.path.join(HERE, "ensaio_a_seco_v410.json"))
ESBOCO = os.path.join(WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"); ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
gb = tenta(os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v410.json"))
dep("[LICAO DA v409] as guardas ESTATICAS do esboco R3.5 da Bancada (a funcao ler_nos do esboco pinado) sobre o CANDIDATO: passa (uma so' linha de alfa e de UM_VERSION); a v399 selada e' recusada com a mensagem EXATA do recibo da Bancada; os 9 controles negativos recusam; o ensaio as rodou", {"GUARDAS_ESTATICAS_BANCADA_v410.json": gb, "ensaio_a_seco_v410.json": ens},
    lambda: (gb["veredito"].startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and gb["candidato"]["sha16"] == CM["sha16"] and gb["esboco"]["sha256"] == ESBOCO_SHA256 == sha(rd(ESBOCO)) and gb["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"] is True
             and len(gb["controles_negativos"]) == 9 and all(v["ok"] for v in gb["controles_negativos"].values()) and gb["contagem_direta"] == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0} and ens.get("guardas_estaticas_bancada", {}).get("veredito") == gb["veredito"], [gb["candidato_v410"]["alpha"]["n_linhas_nao_indentadas"], gb["contagem_direta"]]))
dep("o ensaio a seco e' deste candidato e deu TUDO PASSOU (e o ESPERADOS pina o ensaio); o QUADRO do Teste da Unica Palavra esta no topo do artigo PT/EN e do .md e os numeros do quadro == os do resultado pinado", {"ensaio_a_seco_v410.json": ens, "ESPERADOS_v410.json": ESP},
    lambda: (ens["veredito"] == "TUDO PASSOU" and ens["quadro"]["ok"] is True and ens["sha16"] == CM["sha16"] and ESP["ensaio_sha16"] == sha(rd(os.path.join(HERE, "ensaio_a_seco_v410.json")))[:16], [ens.get("veredito"), ens.get("sha16")]))
try:
    ast.parse(cb.decode("utf-8")); sintaxe = True
except SyntaxError:
    sintaxe = False
chk("ast.parse do candidato", sintaxe)
_gf = lj(os.path.join(HERE, "GUARDA_FRASES_v410.json"))
chk("[v410, a MOLDURA] a guarda das frases: o controle negativo passou (cada frase proibida reprovada, a frase certa e os identificadores aceitos, a fala do operador so' pela excecao), o gerador achou zero frase proibida no texto novo do candidato e a pedra IALD2 esta' limpa; os registros novos do candidato sao exatamente os quatro com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410) e os dois por spec (cunhagens_v410 e kh_n1_cobertura_v410)", _gf.get("ok") is True and _gf.get("pedras_limpas") is True and len(_gf.get("pedras") or {}) == DL.N_BUNDLE and CM["guarda_frases"]["controle_negativo"] is True and CM["guarda_frases"]["violacoes_no_texto_novo"] == 0 and sorted(CM["registros"]) == sorted(list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]), CM["guarda_frases"])
_cong = lj(os.path.join(HERE, "VERBATIM_CONGELADO_v410.json"))
_glob_agora = sorted(os.path.basename(p_) for p_ in DL.verbatim_origem_pelo_glob410())
_novas_depois = sorted(set(_glob_agora) - set(os.path.basename(p_) for p_ in _cong["arquivos"]))
chk("[v408] a lista das falas embutidas esta congelada (VERBATIM_CONGELADO_v410.json) e e' a do candidato; fala nova depois do congelamento NAO entra nesta versao e NAO reprova o conferidor (fica dita no detalhe)", list(DL.VERBATIM_ORIGEM_V410) == list(_cong["arquivos"]) and len(_cong["arquivos"]) == len(CM["cunhagens"]) == DL.N_FALAS_V410 == _cong["n"], {"embutidas": len(_cong["arquivos"]), "falas_novas_depois_do_congelamento": _novas_depois})
chk("[v410, a lista de exclusao] nenhuma fala de VERBATIM_EXCLUIDAS_V410 esta no candidato: o sha16 nao aparece nas cunhagens do CANDIDATO_v410.json nem na copia duravel insumos\\cunhagens", not any(k_ in json.dumps(CM["cunhagens"]) for k_ in DL.VERBATIM_EXCLUIDAS_V410) and not any(os.path.basename(p_)[:16] in DL.VERBATIM_EXCLUIDAS_V410 for p_ in glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*"))), sorted(DL.VERBATIM_EXCLUIDAS_V410))
cit = tenta(os.path.join(HERE, "conferir_citacoes_v410.json"))
dep("[v408] a conferencia de citacoes conferiu as docstrings das pedras da v410 (zero reprovada; o que bate so' sem acento e as apontadas a gerencia ficam ditas no JSON) e a guarda das frases achou zero frase proibida no texto novo", {"conferir_citacoes_v410.json": cit},
    lambda: (not cit["varredura_das_pedras"]["reprovadas"] and CM["guarda_frases"]["violacoes_no_texto_novo"] == 0, {"conferidas": cit["varredura_das_pedras"]["citacoes_conferidas"], "so_sem_acento": cit["varredura_das_pedras"].get("so_sem_acento"), "apontadas_a_gerencia_aspas": len(cit.get("apontadas_a_gerencia_aspas") or [])}))
E1, _, _, h1 = carregar(cand)
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v410.json"), encoding="utf-8"))["novos"]
chk("o kernel embutido do candidato == o sandbox construido (o modulo novo, raiz, Audit e os demais, byte a byte)", all(rd(os.path.join(KS, *k.split("/"))) == v.encode("utf-8") for k, v in E1.items()) and len(E1) == CM["formal_files_n"], len(E1))
chk("os modulos novos (%d, lidos da lista) NAO estao no kernel do Nos; as pedras da v394 a v409 (os %d modulos da traducao da v409, os %d do terminal da v408, os %d do psion da v407 e os %d do fecho da v406 por sha256, as oito da v405, as duas da v404 e as tres da v403 inclusive) estao" % (len(nov), len(esp4["bundle_sha256"]), len(esp4["bundle_v408_sha256"]), len(esp4["bundle_v407_sha256"]), len(esp4["bundle_v406_sha256"])),
    nov == list(DL.BUNDLE_RELS) and not any(os.path.exists(os.path.join(NK, *p.split("/"))) for p in nov) and all(os.path.exists(os.path.join(NK, "TGLExt", n + ".lean")) for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional"))
    and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in list(DL.D3.STONE_RELS) + list(DL.D4.STONE_RELS) + list(DL.D5.STONE_RELS)) and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_sha256"].items()) and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_v408_sha256"].items()) and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_v407_sha256"].items()) and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_v406_sha256"].items()))
chk("a raiz e o Audit do Nos == os da v409 embutida (o ANTES)", sha(rd(os.path.join(NK, "TGLExt.lean")))[:16] == CM["kernel"]["raiz_v409_sha16"] and sha(rd(os.path.join(NK, "TGL", "Audit.lean")))[:16] == CM["kernel"]["audit_v409_sha16"] == CM["kernel"]["audit_sha16"])
pb = json.load(open(os.path.join(KDIR, "POS_BUILD_v410.json"), encoding="utf-8"))
chk("pos-build do kernel VERDE (rc 0, zero sorry, trio, .olean Lean 4.31.0; raiz e Audit compilados; o modulo Built e nenhum Replayed) e a arvore so-fontes existe", pb["ok"] is True and pb["modo_da_pedra_no_build"] and os.path.isdir(KA) and pb["modos_contagem"] == {"Built": DL.N_BUNDLE, "Replayed": 0} and not pb["falhas"], [pb["ok"], pb["modo_da_pedra_no_build"], pb["githash_lean"]])
KR = json.load(open(os.path.join(KDIR, "KERNEL_RECIBO_v410.json"), encoding="utf-8"))
chk("o recibo do kernel pina logs e arvore que existem e conferem; cada um dos %d modulos do bundle tem declaracoes (nenhum modulo de auditoria)" % len(nov), sha(rd(KR["build_full_log"]["path"])) == KR["build_full_log"]["sha256"] and sha(rd(KR["audit_log"]["path"])) == KR["audit_log"]["sha256"] and os.path.isdir(KR["arvore"]) and len(KR["pedras"]) == len(nov) == DL.N_BUNDLE and all(p["declaracoes"] for p in KR["pedras"]))
FJ_ = lj(os.path.join(KDIR, "FLAGS_v410.json")); KH_ = lj(os.path.join(KDIR, DL.KH_N1_INSUMO))
chk("[v410] o kernel k410c: a escada sobe exatamente as bandeiras novas (a da v409 selada + o n_flags do FLAGS_v410.json == a do candidato); as bandeiras novas sao so' declaracao nomeada, em DUAS series, uma por modulo do bundle (ext_iald2_410_*: uma por ancora da IALD2; ext_aescala_410_*: as declaracoes nomeadas da AEscala, que incluem as ancoras); o axiom_report cresce exatamente o delta lido do KH_N1 (a v409 + o delta == o efetivo); nada fora do trio", CM["escada"][0] == esp4["escada"][1] and CM["escada"][1] == CM["escada"][0] + FJ_["n_flags"] == CM["escada"][0] + CM["n_bandeiras"] and FJ_["n_flags"] == sum(FJ_["n_por_modulo"].values()) and FJ_["n_por_modulo"][DL.MODULO_IALD2] == len(DL.ANCORAS) and all(f_[0].startswith(DL.FLAG_PREFIX_POR_MODULO[f_[2].replace(".", "/") + ".lean"]) for f_ in FJ_["flags"]) and sorted(FJ_["prefixos"].items()) == sorted(DL.FLAG_PREFIX_POR_MODULO.items()) and KH_["axiom_report_efetivo_n"] == esp4["axiom_report_esperado_min"] + KH_["delta_vs_v409"]["decl"] and KH_["linha_TOTAL"]["fora_do_trio"] == 0, [CM["escada"], FJ_["n_flags"], KH_["axiom_report_efetivo_n"]])
MI = json.load(open(os.path.join(HERE, "MANIFESTO_INSUMOS_v410.json"), encoding="utf-8"))
_VED = os.path.normcase(os.path.normpath(DL.H0DN_PASTA_VEDADA)); _sob_ved = lambda p_: os.path.normcase(os.path.normpath(str(p_))) == _VED or os.path.normcase(os.path.normpath(str(p_))).startswith(_VED + os.sep)   # (a pasta da entrega do Kimi: so' o CAMINHO e' comparado, nunca aberto; definida aqui porque a conferencia dos insumos abaixo NAO pode abrir uma origem sob ela)
chk("os insumos duraveis == as origens (sha256), exceto a medida do Audit (gerada aqui), e os pinados nos registros conferem; as origens sob a pasta vedada (SO' os seis artefatos HMS/13 da excecao D80) NAO sao abertas aqui: a copia duravel == o sha256 do manifesto; as entradas `_pasta_vedada_nao_copiada` (o REGISTRO do veto, sem sha256, sem arquivo, sem copia) e `_pasta_vedada_excecoes_d80` (a excecao, com os pinos) sao as duas que comecam por `_`", all(sha(rd(os.path.join(HERE, "insumos", k))) == v["sha256"] and (_sob_ved(v["origem"]) or not os.path.exists(v["origem"]) or sha(rd(v["origem"])) == v["sha256"] or k == DL.KH_N1_INSUMO) for k, v in MI.items() if not k.startswith("_")) and sorted(k for k in MI if k.startswith("_")) == ["_pasta_vedada_excecoes_d80", "_pasta_vedada_nao_copiada"], len(MI))
_vb12 = DL.verbatins410(os.path.join(HERE, "insumos", "cunhagens")); _n_trecho = sum(1 for v_ in _vb12 if "sha256_arquivo_inteiro" in v_)
chk("as %d falas de 06 a 09/11 (todas do operador; de quatro, so' o trecho: a da D65, a ordem de 09/11, as tres copias do ACOM e a leitura do 5 sigma): a copia duravel de cada texto embutido == sha256 embutido; a fonte original == sha256 do arquivo inteiro; nas quatro do trecho, o trecho esta' DENTRO da fonte original e e' menor que ela, e o arquivo inteiro NAO e' copiado em insumos\\cunhagens (entra so' por sha256); o manifesto traz exatamente as %d entradas cunhagens/ e cada uma == o arquivo" % (DL.N_FALAS_V410, DL.N_FALAS_V410),
    len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V410 == len(DL.VERBATIM_ORIGEM_V410) and len(_vb12) == DL.N_FALAS_V410 and _n_trecho == len(DL.VERBATIM_SO_O_TRECHO)
    and all(sha(rd(v_["arquivo"])) == v_["sha256"] and sha(rd(v_["fonte_original"])) == (v_.get("sha256_arquivo_inteiro") or v_["sha256"])
            and (("sha256_arquivo_inteiro" not in v_) or (rd(v_["arquivo"]).rstrip(b"\r\n") in rd(v_["fonte_original"]) and len(rd(v_["arquivo"])) < len(rd(v_["fonte_original"])) and bool(v_.get("so_o_trecho"))
                                                         and not any(sha(rd(p_)) == v_["sha256_arquivo_inteiro"] for p_ in glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*"))))) for v_ in _vb12)
    and all(sha(rd(os.path.join(HERE, "insumos", k))) == v["sha256"] for k, v in MI.items() if k.startswith("cunhagens/")), [len(_vb12), _n_trecho])
# ---- [v410, D72] o H0DN pré-registrado (nenhum dado observado lido): os insumos e o VETO a pasta da entrega do Kimi (AVISO da gerencia, 09/11): a v410 pre-registra e NAO abre; nada daquela pasta e' lido, copiado, pinado nem citado. So' o CAMINHO e' comparado; cada item sai com OK/FALHA e o detalhe medido.
_VED = os.path.normcase(os.path.normpath(DL.H0DN_PASTA_VEDADA)); _sob_ved = lambda p_: os.path.normcase(os.path.normpath(str(p_))) == _VED or os.path.normcase(os.path.normpath(str(p_))).startswith(_VED + os.sep)
CH = CM.get("h0dn") or {}
_H0DN_COPIAS = {"estimator_frozen.npz": "h0dn_estimator_frozen.npz", "BG1.json": "h0dn_BG1.json", "analysis_plan.json": "h0dn_analysis_plan.json", "FREEZE_R2.json": "h0dn_FREEZE_R2.json", "estimator.py": "h0dn_estimator.py", "ENTREGA_H0DN_BG1.json": "h0dn_ENTREGA_H0DN_BG1.json"}


def _h0dn_insumos_ok():
    ins_ = CH["insumos"]
    copias_ok_ = set(ins_) == set(_H0DN_COPIAS) and all(sha(rd(os.path.join(HERE, "insumos", c_))) == MI[c_]["sha256"] == ins_[r_]["sha256"] and len(rd(os.path.join(HERE, "insumos", c_))) == ins_[r_]["bytes"] for r_, c_ in _H0DN_COPIAS.items())   # a copia duravel == o manifesto == o pino do candidato
    outros_ok_ = all(sha(rd(os.path.join(HERE, "insumos", c_))) == MI[c_]["sha256"] == CH[k_]["sha256"] for k_, c_ in (("ordem_kimi", "h0dn_ORDEM_KIMI_H0DN_01_09nov.md"), ("leitura_dossie", "h0dn_LEITURA_DOSSIE_5SIGMA_09nov.json")))   # a ordem ao Kimi (a gerencia) e a leitura do dossie
    fz_ = lj(os.path.join(HERE, "insumos", "h0dn_FREEZE_R2.json"))
    pinos_ok_ = len(fz_["files"]) == DL.N_PINOS_FREEZE_R2 == CH["n_pinos_freeze"] and len(ins_) + len(CH["pinos_so_no_disco"]) == CH["n_pinos_freeze"] + 2 and all(os.path.exists(f_["path"]) and sha(rd(f_["path"])) == f_["sha256"] and len(rd(f_["path"])) == f_["bytes"] and not _sob_ved(f_["path"]) for f_ in fz_["files"])   # os 9 pinos do FREEZE_R2 (4 embutidos + 5 so' em disco) batem com os arquivos do desenho do Codex; nenhum sob a pasta vedada
    _pt = rd(os.path.join(HERE, "v410_pins.py")).decode("utf-8")
    _nd = [n_ for n_ in ast.parse(_pt).body if isinstance(n_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == "_V410_H0DN_INSUMOS" for t_ in n_.targets)]
    emb_ = ast.literal_eval(_nd[0].value) if len(_nd) == 1 else None
    emb_ok_ = bool(emb_ and set(emb_) == set(ins_) and all(sha(base64.b64decode(emb_[n_]["b64"])) == ins_[n_]["sha256"] == emb_[n_]["sha256"] and len(base64.b64decode(emb_[n_]["b64"])) == ins_[n_]["bytes"] and emb_[n_]["b64"].encode("ascii") in cb for n_ in ins_))   # os embutidos no candidato (base64) decodificam para o pino
    return bool(copias_ok_ and outros_ok_ and pinos_ok_ and emb_ok_ and CH.get("observed_vector_read") is False), [copias_ok_, outros_ok_, pinos_ok_, emb_ok_, len(ins_), len(fz_["files"])]


dep("[v410, H0DN] os insumos do H0DN (pré-registrado; nenhum dado observado lido): as 6 copias duraveis (insumos\\h0dn_*) == o manifesto == o pino do candidato; a ordem ao Kimi e a leitura do dossie == o pino; os 9 pinos do FREEZE_R2 (4 embutidos + 5 so' em disco) batem com os arquivos do desenho do Codex; os embutidos (base64) no candidato decodificam para o pino; o contrato diz observed_vector_read False", {}, _h0dn_insumos_ok)
# ---- [v410, D80] o recibo documental HMS/13 (ADITIVO e POSTERIOR ao FREEZE_R2; cobertura documental de fontes, não covariância física fechada; nada aberto; pré-registrado; nenhum dado observado lido): os seis artefatos por sha256 (as COPIAS duraveis insumos\\hms13_*; a origem sob a pasta do Kimi NAO e' aberta aqui) e o que o candidato embute
_HMS13_COPIAS = {k_: "hms13_" + k_ for k_ in CM["hms13"]["pinos_build"]}


def _hms13_insumos_ok():
    hm_ = CM["hms13"]; pb_ = hm_["pinos_build"]; ins_ = hm_["insumos"]; ec_ = CM["fontes_hms13_embutidas"]
    cp_ = {k_: os.path.join(HERE, "insumos", c_) for k_, c_ in _HMS13_COPIAS.items()}
    copias_ok_ = set(cp_) == set(ec_) and all(sha(rd(p_)) == MI[_HMS13_COPIAS[k_]]["sha256"] == pb_[k_]["sha256"] == ec_[k_]["sha256"] and len(rd(p_)) == MI[_HMS13_COPIAS[k_]]["bytes"] == pb_[k_]["bytes"] == ec_[k_]["bytes"] and not _sob_ved(p_) for k_, p_ in cp_.items())   # as seis copias duraveis == o manifesto == o pino do contrato == o do candidato
    ho_ = lj(cp_["HANDOFF_CLAUDE_UMPY_HMS_13.json"])
    handoff_ok_ = ho_.get("status") == hm_["handoff"]["status"] and str(ho_.get("status")).startswith("HANDOFF_READY__ADDITIVE_DOCUMENTARY_ONLY") and "OPENING_NOT_ALLOWED" in str(ho_.get("status")) and hm_["handoff"]["sha256"] == pb_["HANDOFF_CLAUDE_UMPY_HMS_13.json"]["sha256"]
    ordem_ok_ = sha(rd(cp_["ORDEM_CLAUDE_UMPY_HMS_13.md"])) == hm_["ordem"]["sha256"] == pb_["ORDEM_CLAUDE_UMPY_HMS_13.md"]["sha256"] and sha(rd(cp_["ORDEM_CLAUDE_UMPY_HMS_13.md"]))[:16] == DL.HMS13_ORDEM_SHA16_DO_DESENHO == hm_["ordem"]["sha16_do_desenho"]
    rat_ok_ = os.path.exists(DL.HMS13_RATIFICACAO_ARQ) and sha(rd(DL.HMS13_RATIFICACAO_ARQ)) == DL.HMS13_RATIFICACAO_SHA256_DO_DESENHO == hm_["ratificacao"]["sha256"] and DL.HMS13_TRECHO_RATIFICACAO.encode("utf-8") in rd(DL.HMS13_RATIFICACAO_ARQ) and hm_["ratificacao"]["trecho"] == DL.HMS13_TRECHO_RATIFICACAO   # a ratificacao do operador (fora da pasta vedada): por sha256 do arquivo inteiro
    campos_ok_ = dict(hm_["campos"]) == dict(DL.HMS13_CAMPOS) and hm_["observed_vector_read"] is False and hm_["le_em_rito"] is False and hm_["n_fontes_primarias"] == DL.HMS13_CAMPOS["fontes_primarias"] and len(hm_["ids_calibradores"]) == DL.HMS13_CAMPOS["calibradores"] and hm_["n_checks"] == DL.N_CHECKS_HMS13 and hm_["veredito_ok"] == DL.VEREDITO_HMS13_OK
    _pt_ = rd(os.path.join(HERE, "v410_pins.py")).decode("utf-8")
    _nd_ = [n_ for n_ in ast.parse(_pt_).body if isinstance(n_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == "_V410_HMS13_INSUMOS" for t_ in n_.targets)]
    emb_ = ast.literal_eval(_nd_[0].value) if len(_nd_) == 1 else None
    emb_ok_ = bool(emb_ and set(emb_) == set(ins_) == {k_ for k_, v_ in ec_.items() if v_["embutido_no_um_py"]} and len(emb_) == len(DL.HMS13_EMBUTIDOS) and all(sha(base64.b64decode(emb_[n_]["b64"])) == ins_[n_]["sha256"] == emb_[n_]["sha256"] and len(base64.b64decode(emb_[n_]["b64"])) == ins_[n_]["bytes"] and emb_[n_]["b64"].encode("ascii") in cb for n_ in ins_))   # os quatro embutidos no candidato (base64) decodificam para o pino
    so_pino_ok_ = sorted(k_ for k_ in ec_ if k_ not in ins_) == ["HANDOFF_CLAUDE_UMPY_HMS_13.json", "ORDEM_CLAUDE_UMPY_HMS_13.md"] and not any(ec_[k_]["embutido_no_um_py"] for k_ in ec_ if k_ not in ins_)   # o HANDOFF e a ORDEM entram so' por sha256 (nao embutidos)
    return bool(copias_ok_ and handoff_ok_ and ordem_ok_ and rat_ok_ and campos_ok_ and emb_ok_ and so_pino_ok_), [copias_ok_, handoff_ok_, ordem_ok_, rat_ok_, campos_ok_, emb_ok_, so_pino_ok_, len(pb_), len(ins_)]


dep("[v410, HMS/13] o recibo documental HMS/13 (D80; aditivo e posterior ao FREEZE_R2; cobertura documental de fontes, não covariância física fechada; nada aberto): os seis artefatos por sha256 (as copias duraveis insumos\\hms13_* == o manifesto == o pino do contrato == o do candidato; o HANDOFF em HANDOFF_READY__ADDITIVE_DOCUMENTARY_ONLY com OPENING_NOT_ALLOWED; a ORDEM com o sha16 do desenho; a ratificacao do operador por sha256 do arquivo inteiro); os dez campos == DL.HMS13_CAMPOS; os quatro embutidos (base64) no candidato decodificam para o pino; o HANDOFF e a ORDEM so' por sha256", {}, _hms13_insumos_ok)


def _aescala_pedra_ok():
    pa_ = next(p_ for p_ in DL.PEDRAS_V410 if p_["rel"] == DL.MODULO_AESCALA); rel_ = pa_["rel"]
    ca_ = CM["aescala"]; R_ = lj(DL.RECIBO_NOMES_ARQ)
    fonte_ok_ = sha(rd(pa_["origem"])) == DL.BUNDLE_POR_REL[rel_]["sha256_origem"] == pa_["sha256_origem"] == ca_["sha256_origem"] and sha(rd(pa_["origem"])) == sha(rd(os.path.join(HERE, "insumos", "AEscala.lean")))   # a FONTE (a ratificada, D87)
    embutida_ok_ = sha(rd(pa_["src"])) == sha(rd(os.path.join(HERE, "insumos", "AEscala_embutida.lean"))) == sha(E1[rel_].encode("utf-8")) == sha(rd(os.path.join(KS, *rel_.split("/")))) == DL.BUNDLE_POR_REL[rel_]["sha256"] == ca_["source_sha256"][rel_]   # a EMBUTIDA (com o cabecalho da ratificacao): pedra == insumos == candidato == sandbox == bundle
    recibo_ok_ = sha(rd(DL.RECIBO_NOMES_ARQ))[:16] == DL.RECIBO_NOMES_SHA16 and len(R_["modulos"]) == DL.N_BUNDLE and [m_["modulo"] for m_ in R_["modulos"]] == list(DL.BUNDLE_MODS) and all(sha(rd(m_["arquivo"])) == m_["sha256"] for m_ in R_["modulos"]) \
        and R_["falas_n"] == len(R_["falas"]) == DL.N_FALAS_V410 - len(DL.FALAS_FORA_DO_RECIBO) and all(n_ in DL.VERBATIM_PREFIXOS_DA_ORDEM_V410 for n_ in DL.FALAS_FORA_DO_RECIBO) and set(DL.FALAS_FORA_DO_RECIBO) <= set(DL.NOMES_V410_DO_DESENHO) and len(R_["falas"]) + len(DL.FALAS_FORA_DO_RECIBO) == len(CM["cunhagens"]) and {f_["sha256"] for f_ in R_["falas"]} == {(v_.get("sha256_arquivo_inteiro") or v_["sha256"]) for v_ in CM["cunhagens"].values() if str(v_.get("nome") or "").split(" (D65:")[0] not in DL.FALAS_FORA_DO_RECIBO} and R_["ratificacao_aescala_D87"]["sha256"] == ca_["ratificacao_D87"]["sha256"] and R_["ratificacao_aescala_D87"]["texto"].strip() == DL.FRASE_RATIFICO_TUDO == ca_["ratificacao_D87"]["trecho"] \
        and R_["modulos"][1]["ratificados"] is True and R_["modulos"][1]["declaracoes_n"] == len(DL.NOMES_AESCALA) == ca_["n_nomes"] and R_["modulos"][1]["no_trio"] == R_["modulos"][1]["print_axioms"] == DL.N_ANCORAS_AESCALA \
        and list(R_["modulos"][1].get("nomes_novos_a_ratificar") or []) == list(DL.NOMES_NOVOS_AESCALA) == list(ca_["nomes_novos_da_pedra"]) and bool(DL.NOMES_NOVOS_AESCALA) and list(R_["modulos"][1].get("campos_novos_da_estrutura") or []) == list(DL.CAMPOS_NOVOS_AESCALA) == list(ca_["campos_novos_da_estrutura"]) and ca_["ponte"] == DL.PONTE_AESCALA   # o recibo dos nomes (pinado por sha16 no delta): os modulos do bundle, as falas por sha256, a ratificacao D87 e os nomes novos da pedra (R3, R4 e R5)
    return bool(fonte_ok_ and embutida_ok_ and recibo_ok_ and DL.NOMES_RATIFICADOS is True), [fonte_ok_, embutida_ok_, recibo_ok_, sha(rd(DL.RECIBO_NOMES_ARQ))[:16]]


dep("[v410, AEscala, D87] a pedra TGLExt.AEscala: a FONTE ratificada (insumos\\AEscala.lean) == o pino sha256_origem do bundle; a EMBUTIDA (pedra\\AEscala.lean == insumos\\AEscala_embutida.lean == a embutida no candidato == a do sandbox == o sha256 do BUNDLE_v410.json == o do contrato); o RECIBO dos nomes (insumos\\RECIBO_PEDRAS_v410_NOMES.json, sha16 == DL.RECIBO_NOMES_SHA16) traz os modulos do bundle, as falas por sha256 == as do candidato e a ratificacao D87 («ratifico tudo»); os nomes ratificados e os nomes novos da pedra (R3, R4 e R5)", {}, _aescala_pedra_ok)
_origens_ = {k: v["origem"] for k, v in MI.items() if not k.startswith("_")}
_mk_ = MI.get("_pasta_vedada_nao_copiada") or {}
_exc_ = MI.get("_pasta_vedada_excecoes_d80") or {}; _pb13_ = CM["hms13"]["pinos_build"]; _nrm_p_ = lambda p_: os.path.normcase(os.path.normpath(str(p_)))
_esp13_ = sorted("hms13_" + k_ for k_ in _pb13_)   # a EXCECAO D80: exatamente os seis artefatos documentais HMS/13 (mapa, manifesto, validacao, levantamento, HANDOFF, ORDEM), pelos nomes do contrato do candidato (nada digitado)
chk("[VETO kimi] (a) o MANIFESTO_INSUMOS_v410.json: a UNICA origem sob a pasta vedada e' a EXCECAO D80 -- exatamente os seis artefatos documentais HMS/13 (por nome; todos sob a revisao independente DL.HMS13_DIR; listados em `_pasta_vedada_excecoes_d80` e em `_pasta_vedada_nao_copiada.excecao_d80`; sha256 e bytes == os pinos do candidato, que o BUILD conferiu contra o HANDOFF e a ORDEM); o REGISTRO do veto `_pasta_vedada_nao_copiada` segue sem sha256, sem arquivo e com 0 bytes, na pasta vedada pela gerencia; este script NAO abre nenhuma dessas origens (so' compara caminhos e le as copias duraveis)",
    sorted(k for k, o in _origens_.items() if _sob_ved(o)) == _esp13_ == sorted(_exc_.get("excecoes") or []) == sorted(_mk_.get("excecao_d80") or []) and all(_nrm_p_(_origens_[k_]).startswith(_nrm_p_(DL.HMS13_DIR) + os.sep) for k_ in _esp13_) and _nrm_p_(_exc_.get("origem") or "") == _nrm_p_(DL.HMS13_DIR)
    and all(MI[k_]["sha256"] == _pb13_[k_[len("hms13_"):]]["sha256"] == _exc_["pinos"][k_[len("hms13_"):]]["sha256"] and MI[k_]["bytes"] == _pb13_[k_[len("hms13_"):]]["bytes"] == _exc_["pinos"][k_[len("hms13_"):]]["bytes"] for k_ in _esp13_)
    and _mk_.get("sha256") is None and _mk_.get("bytes") == 0 and _nrm_p_(_mk_.get("origem") or "") == _VED, [len(_origens_), len(_esp13_), "so' as seis da excecao D80 (por nome); nenhuma origem aberta aqui"])
_NOMES_ARQ_VEDADOS = ("y_obs" + ".npz", "CONSTRUCAO_" + "Y_OBS", "ENTREGA_H0DN_" + "Y_OBS", "C_fisica")   # nomes de ARQUIVO de dado observado (em partes: este script nao os traz inteiros); o nome solto `y_obs` aparece em prosa do texto do registro e nao e' arquivo
_achados_ = {n_: cb.count(n_.encode("utf-8")) for n_ in _NOMES_ARQ_VEDADOS}
chk("[VETO kimi] (b) o candidato NAO traz o nome de nenhum arquivo da entrega vedada (grep nos bytes dos %d nomes de arquivo de dado observado)" % len(_NOMES_ARQ_VEDADOS), not any(_achados_.values()), list(_achados_.values()))
dep("[VETO kimi] (c) o ensaio a seco MEDIU todo caminho tocado (open/exists/listdir/scandir/stat instrumentados durante TODO o ensaio): nenhum sob a pasta vedada (`tocados_sob_vedada` == []), o controle negativo detecta (`controle_negativo_detecta` True), a pasta do ensaio == a pasta vedada pela gerencia, e o registro h0dn_bg1_v410 (c7) tambem nao tocou nada sob ela nem nome vedado", {"ensaio_a_seco_v410.json": ens},
    lambda: ((ens["pasta_vedada_kimi"]["tocados_sob_vedada"] == [] and ens["pasta_vedada_kimi"]["controle_negativo_detecta"] is True and isinstance(ens["pasta_vedada_kimi"]["n_caminhos_vistos"], int) and ens["pasta_vedada_kimi"]["n_caminhos_vistos"] > 0 and os.path.normcase(os.path.normpath(ens["pasta_vedada_kimi"]["pasta"])) == _VED
              and (ens.get("h0dn_bg1_v410") or {}).get("values", {}).get("sob_pasta_vedada") == [] and (ens.get("h0dn_bg1_v410") or {}).get("values", {}).get("com_nome_vedado") == [] and not [p_ for p_ in (ens.get("h0dn_bg1_v410") or {}).get("values", {}).get("caminhos_tocados", []) if _sob_ved(p_)]),
             [ens["pasta_vedada_kimi"]["n_caminhos_vistos"], ens["pasta_vedada_kimi"]["tocados_sob_vedada"], ens["pasta_vedada_kimi"]["controle_negativo_detecta"]]))
if ens is not None and not isinstance(ens.get(DL.HMS13_REGISTRO), dict):   # (c2) o recibo HMS/13 no ensaio: nada sob kimi\ EM RITO (o registro mede na c7; o ensaio instrumenta TODO caminho tocado)
    pend("[VETO kimi] (c2) o ensaio a seco rodou o registro h0dn_fontes_hms13_v410 e ele (c7) nao tocou nada sob a pasta vedada nem nome vedado (nenhuma abertura de caminho sob kimi\\ EM RITO; no build, so' os seis da excecao D80, por sha256), le_em_rito False", "ensaio_a_seco_v410.json ainda nao traz o registro h0dn_fontes_hms13_v410 (o ensaio adaptado o grava): o p00 o diz PENDENTE, nao erro")
elif ens is not None:
    _hv_ = (ens.get(DL.HMS13_REGISTRO) or {}).get("values", {})
    chk("[VETO kimi] (c2) o ensaio a seco rodou o registro h0dn_fontes_hms13_v410 e ele (c7) nao tocou nada sob a pasta vedada nem nome vedado (nenhuma abertura de caminho sob kimi\\ EM RITO; no build, so' os seis da excecao D80, por sha256); le_em_rito e observed_vector_read False; os 12 checks verdes",
        (ens.get(DL.HMS13_REGISTRO) or {}).get("all_verified") is True and (ens.get(DL.HMS13_REGISTRO) or {}).get("le_em_rito") is False and (ens.get(DL.HMS13_REGISTRO) or {}).get("observed_vector_read") is False and _hv_.get("sob_pasta_vedada") == [] and _hv_.get("com_nome_vedado") == [] and not [p_ for p_ in _hv_.get("caminhos_tocados", []) if _sob_ved(p_)]
        and ((ens.get(DL.HMS13_REGISTRO) or {}).get("mechanics") or {}).get("n_checks") == DL.N_CHECKS_HMS13, [_hv_.get("n_caminhos_tocados"), _hv_.get("sob_pasta_vedada"), _hv_.get("com_nome_vedado")])
_EXCL_ARQS = ("copiar_insumos_v410.py", os.path.join("pos_rito", "harness_fechar_sandbox_v410.py"))
_excl_n_ = {f_: (len(re.findall(r"H0DN_PASTA_VEDADA|VEDADO", rd(os.path.join(HERE, f_)).decode("utf-8", "replace"))) if os.path.exists(os.path.join(HERE, f_)) else None) for f_ in _EXCL_ARQS}
chk("[VETO kimi] (d) o copiar_insumos_v410.py e o harness do fechar (o espelho da casa, pos_rito\\harness_fechar_sandbox_v410.py) trazem o assert de exclusao da pasta vedada (grep do texto-fonte por H0DN_PASTA_VEDADA ou VEDADO)", all(isinstance(n_, int) and n_ > 0 for n_ in _excl_n_.values()), _excl_n_)
chk("[VETO kimi] (e) o candidato embute a vigia de arquivos do registro (a checagem c7: _v410_h0dn_vigia_arquivos) e a pasta vedada no contrato do H0DN; a funcao de veredito e o registro vivem no bloco emendado", b"_v410_h0dn_vigia_arquivos" in cb and DL.H0DN_PASTA_VEDADA.encode("utf-8").replace(b"\\", b"\\\\") in cb and b"def veredito_h0dn(" in cb and b"def h0dn_fontes_hms13_v410(" in cb and b"def a_escala_v410(" in cb and cb.count(b"_v410_h0dn_vigia_arquivos") >= 2, [cb.count(b"_v410_h0dn_vigia_arquivos"), cb.count(b"def veredito_h0dn("), cb.count(b"def h0dn_fontes_hms13_v410("), cb.count(b"def a_escala_v410(")])   # (D80: o registro HMS/13 usa a MESMA vigia da c7; os dois registros novos vivem no bloco emendado)
pr = tenta(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v410.json"))
_esc = (pr or {}).get("escrita_na_producao") or {}
if pr is None:
    pend("o recibo pre_selo do B(n) foi GERADO E PINADO ANTES da instalacao", "PINO_RECIBO_PRE_SELO_v410.json ainda nao existe: o B(n) pre-selo da v410 (bateria_pre_selo/rodar_bn_pre_selo_v410.sh, passo B(n) = %s, Bancada de producao pina %s) nao rodou" % (DL.B_N_SEGUINTE, DL.BANCADA_PINA_HOJE["deployment_id"]))
else:
    chk("o recibo pre_selo do B(n) foi GERADO E PINADO ANTES da instalacao: arquivo == pino; utilizavel; do um.py que esta no Nos; veredito de 'ja sincronizada'; a producao (Bancada e Nos) so' foi lida (listas identicas antes e depois)",
        sha(rd(pr["path"])) == pr["sha256"] and pr["utilizavel_como_recibo_pre_selo_do_B_n"] is True and pr["versao_nos"] == "v409" and pr["um_py_sha16_do_nos"] == sha(raw)[:16] and pr["veredito"].startswith("JA_SINCRONIZADA__ENSAIO")
        and (_esc.get("bancada_um") or {}).get("identico") is True and (_esc.get("nos") or {}).get("identico") is True, [pr["veredito"], pr["utilizavel_como_recibo_pre_selo_do_B_n"], _esc.get("bancada_um"), _esc.get("nos")])
prova = tenta(os.path.join(HERE, "PROVA_PRODUCAO_INTACTA_v410_pre_selo.json"))
F9 = [(c_, os.path.join(DL.F9_DIR_DURAVEL, n_)) for c_, n_ in (("f9v2_resultado", DL.F9_RESULTADO_NOME), ("f9v2_congelamento", "RECIBO_DE_CONGELAMENTO.json"), ("f9v2_abertura", "RECIBO_DE_ABERTURA.json"), ("f9v2_consumida", "ABERTURA_CONSUMIDA.json"))]
chk("o Teste da Unica Palavra (v397, o QUADRO do topo): o resultado e os tres recibos (copias duraveis em v397/insumos/fase9) == os sha256 que a v409 pinou (ESPERADOS_v409); o resultado == o sha256 da ordem da v397; as falas-chave desta versao tem os prefixos de sha256 que a ordem da gerencia deu (todas do operador)",
    all(sha(rd(p_)) == esp4["veracidade"]["fontes"][c_] for c_, p_ in F9) and sha(rd(F9[0][1])) == DL.F9_RESULTADO_SHA256_DA_ORDEM and len(DL.verbatins410(os.path.join(HERE, "insumos", "cunhagens"))) == len(DL.VERBATIM_ORIGEM_V410), [sha(rd(p_))[:16] for _, p_ in F9])
if prova is None:
    pend("a prova de que a producao so' foi lida (PROVA_PRODUCAO_INTACTA_v410_pre_selo.json: producao_intacta True)", "PROVA_PRODUCAO_INTACTA_v410_pre_selo.json ainda nao existe: o B(n) pre-selo nao rodou")
else:
    chk("a prova de que a producao so' foi lida existe (PROVA_PRODUCAO_INTACTA_v410_pre_selo.json: producao_intacta True)", prova.get("producao_intacta") is True)
bm = json.load(open(os.path.join(C, "IALD", "Bancada_Um", "canonical_contracts.json"), encoding="utf-8"))
chk("a Bancada de producao AINDA pina a v409 (o B(n) da v410 e' um passo simples %s -> %s): versao v409 e o deployment lido do manifesto dela == DL.BANCADA_PINA_HOJE" % (DL.BANCADA_PINA_HOJE["deployment_id"], DL.B_N_SEGUINTE), bm["canonical"].get("version") == "v409" and str(bm.get("deployment_id")) == DL.BANCADA_PINA_HOJE["deployment_id"] and DL.BANCADA_PINA_HOJE["n"] + 1 == int(DL.B_N_SEGUINTE[1:]), [bm["canonical"].get("version"), bm.get("deployment_id")])
if pr is None:
    pend("a Bancada de producao AINDA pina o que o recibo pre_selo diz (versao e um.py): o recibo nao ficou obsoleto", "depende do recibo pre_selo, que ainda nao existe")
else:
    chk("a Bancada de producao AINDA pina o que o recibo pre_selo diz (versao e um.py): o recibo nao ficou obsoleto", bm["canonical"].get("version") == pr["bancada_pina"]["version"] == "v409" and str(bm["sincronizacao"].get("um_py_sha256"))[:16] == pr["bancada_pina"]["um_py_sha16"], [bm["canonical"].get("version"), str(bm["sincronizacao"].get("um_py_sha256"))[:16]])
sim = tenta(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]))
_NOVOS_V410 = (DL.FECHO_REGISTRO, DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)   # (o h0dn_bg1_v410 tem checagem propria logo abaixo)
_HERDADOS_V410 = ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406")   # (os herdados da v409, da v408, da v407 e da v406, recriados no rito)
dep("simular_arvore_do_nos DESTE candidato: o registro com funcao iald2_v410 e os registros por spec v410 (cunhagens_v410, kh_n1_cobertura_v410) selam na arvore simulada do Nos, assim como os herdados da v409 (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409), da v408 (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408), da v407 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407) e da v406 (fechamento_v406, cunhagens_v406, kh_n1_cobertura_v406) e todos os anteriores que a simulacao registra; o hash formal tem a contagem do ESPERADOS", {"SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]: sim, "ESPERADOS_v410.json": ESP},
    lambda: (sim["candidato_sha16"] == CM["sha16"] and sim["formal_files_n_no_rito_real"] == ESP["h8_entradas"] == CM["h8"]["entradas"] and all(isinstance(sim.get(k_), dict) and sim[k_].get("all_verified") is True for k_ in _NOVOS_V410 + _HERDADOS_V410) and all(v_.get("all_verified") is True for v_ in sim.values() if isinstance(v_, dict) and "all_verified" in v_) and sim["kf_all_verified"] is True, sim["formal_files_n_no_rito_real"]))
if sim is not None:
    if not isinstance(sim.get(DL.H0DN_REGISTRO), dict):
        pend("simular_arvore_do_nos: o h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido) sela na arvore simulada do Nos", "simular_arvore_do_nos_v410.py ainda nao chama o registro h0dn_bg1_v410 (a chave nao esta' na simulacao): adaptar o simulador e' do construtor; o p00 o diz PENDENTE, nao erro")
    else:
        chk("simular_arvore_do_nos: o h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido) sela na arvore simulada do Nos", sim[DL.H0DN_REGISTRO].get("all_verified") is True, sim[DL.H0DN_REGISTRO].get("falhas"))
    for _reg_ in (DL.AESCALA_REGISTRO, DL.HMS13_REGISTRO):   # (D86/D87 e D80) os dois registros novos da parte 2 na arvore simulada: PENDENTE se a simulacao e' anterior a eles
        if not isinstance(sim.get(_reg_), dict):
            pend("simular_arvore_do_nos: o %s sela na arvore simulada do Nos" % _reg_, "SIMULACAO_ARVORE_NOS_<sha16>.json ainda nao traz a chave %s (a simulacao e' anterior a parte 2 ou o simulador nao a chamou): refazer a simulacao e' do ensaio; o p00 o diz PENDENTE, nao erro" % _reg_)
        else:
            chk("simular_arvore_do_nos: o %s sela na arvore simulada do Nos" % _reg_, sim[_reg_].get("all_verified") is True, sim[_reg_].get("falhas"))
exm = tenta(os.path.join(HERE, "EXAME_PONTOS_%s.json" % CM["sha16"]))


def _exame_ok():
    pontos_ = {k_: v_ for k_, v_ in exm.items() if k_.startswith("ponto_") and isinstance(v_, dict)}
    return bool(exm["sha256"] == CM["sha256"] and exm.get("algum_falso") == [] and pontos_ and all(v_.get("all_verified") is True for v_ in pontos_.values() if "all_verified" in v_) and any("iald2" in k_ for k_ in pontos_) and any("traducao" in k_ for k_ in pontos_) and any("tetelestai" in k_ for k_ in pontos_)
                and all(not v_ for v_ in exm["nao_verdes"].values())), sorted(pontos_)


dep("exame_pontos_v410 DESTE candidato: nenhum ponto de chamada real da falso; o iald2_v410 e' chamado IMEDIATAMENTE depois do traducao_turing_v409 (e dos specs da v409), na instrucao que traz tambem a_escala_v410 e h0dn_bg1_v410 (nessa ordem), dentro do bloco executado; a instrucao SEGUINTE (o recibo HMS/13 e os specs da v410) e' a ultima antes do emit_figures; os pontos herdados seguem certos (all_verified); nenhum registro nao verde; nenhum arquivo sob kimi\\ lido ou escrito no exame", {"EXAME_PONTOS_%s.json" % CM["sha16"]: exm}, _exame_ok)
if exm is not None and not any("h0dn" in k_ for k_ in exm if k_.startswith("ponto_")):
    pend("exame_pontos: o PONTO DE CHAMADA REAL do h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido): chamado IMEDIATAMENTE depois do iald2_v410 e antes do emit_figures", "exame_pontos_v410.py ainda nao tem o ponto do h0dn_bg1_v410 (nenhum `ponto_*h0dn*` no EXAME_PONTOS): adapta-lo e' do construtor; o p00 o diz PENDENTE, nao erro")
elif exm is not None:
    chk("exame_pontos: o ponto do h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido) esta' certo e verde", all(v_.get("all_verified") is True for k_, v_ in exm.items() if k_.startswith("ponto_") and "h0dn" in k_ and isinstance(v_, dict)), [k_ for k_ in exm if k_.startswith("ponto_") and "h0dn" in k_])
for _pt_, _nm_ in (("aescala", DL.AESCALA_REGISTRO), ("hms13", DL.HMS13_REGISTRO)):   # (D86/D87 e D80) os dois pontos NOVOS da parte 2: PENDENTE se o exame e' anterior a eles
    if exm is not None and not isinstance(exm.get("ponto_" + _pt_), dict):
        pend("exame_pontos: o PONTO DE CHAMADA REAL do %s esta' certo e verde (na ordem do main: iald2 -> a_escala -> h0dn na primeira instrucao; hms13 + specs na segunda, antes do emit_figures)" % _nm_, "exame_pontos_v410.py rodou antes da parte 2 (nenhum `ponto_%s` no EXAME_PONTOS): refazer o exame e' do ensaio; o p00 o diz PENDENTE, nao erro" % _pt_)
    elif exm is not None:
        chk("exame_pontos: o ponto do %s esta' certo e verde (na ordem do main; nenhum dado observado lido; nada de kimi\\ aberto)" % _nm_, exm["ponto_" + _pt_].get("all_verified") is True and exm["ponto_" + _pt_].get("runtime_executed") is True and (_pt_ != "hms13" or (exm["ponto_hms13"].get("observed_vector_read") is False and exm["ponto_hms13"].get("le_em_rito") is False and exm["ponto_hms13"].get("sob_pasta_vedada") == [])), [exm["ponto_" + _pt_].get("verdict")])
neg = tenta(os.path.join(HERE, "conferencia_rito_v410_CONTROLE_NEGATIVO_PRE_RITO.json")); pos = tenta(os.path.join(HERE, "conferencia_rito_v410_POSITIVO_FALSO_NOS.json"))
dep("o conferidor: controle negativo (Nos ainda v409) tudo_bate False com os nao-pode-mudar todos verdes; caminho positivo (Nos FALSO montado do ensaio) TUDO BATE", {"conferencia_rito_v410_CONTROLE_NEGATIVO_PRE_RITO.json": neg, "conferencia_rito_v410_POSITIVO_FALSO_NOS.json": pos}, lambda: (neg["tudo_bate"] is False and all(neg["nao_pode_mudar"].values()) and pos["tudo_bate"] is True, [sum(neg["deve_mudar"].values()), len(neg["deve_mudar"])]))
cmp_ = tenta(os.path.join(HERE, "COMPARACAO_V409_v410.json"))
dep("nada da v409 perdido: comparacao AST sem no removido nem mudanca sem explicacao", {"COMPARACAO_V409_v410.json": cmp_}, lambda: (cmp_["ok"] is True and not cmp_["removidos"] and not cmp_["mudados_sem_explicacao"], [cmp_["iguais"], len(cmp_["mudados"]), cmp_["n_novos"]]))
dep("as citacoes do operador embutidas conferem (embutida == arquivo == fonte original)", {"conferir_citacoes_v410.json": cit}, lambda: cit["todas_conferem"] is True)
chk("pdflatex e lake no PATH; Lean 4.31.0 no sandbox", bool(shutil.which("pdflatex")) and bool(shutil.which("lake")) and "4.31.0" in subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KS).stdout)
dep("a IALD2 (a pedra da v410: o leitor do codigo, o espelho do nome, o algoritmo IALD, o signo, o seletor e o atrator): a fonte de origem (a copia duravel em v410\\insumos) == o pino do bundle (sha256_origem; sha16 == o da ordem); a copia normalizada v410\\pedra == a copia duravel pinada (insumos) == a EMBUTIDA no candidato == a do sandbox == o pino dos ESPERADOS (bundle_sha256) == o sha256 do BUNDLE_v410.json", {"ESPERADOS_v410.json": ESP},
    lambda: (sha(rd(DL.TESTEMUNHA["origem"])) == DL.BUNDLE_POR_REL[DL.TESTEMUNHA["rel"]]["sha256_origem"] and sha(rd(DL.TESTEMUNHA["origem"]))[:16] == DL.TESTEMUNHA["sha16_da_ordem"]
             and sha(rd(DL.TESTEMUNHA["src"])) == sha(rd(os.path.join(HERE, "insumos", DL.TESTEMUNHA["insumo"]))) == sha(E1[DL.TESTEMUNHA["rel"]].encode("utf-8")) == sha(rd(os.path.join(KS, *DL.TESTEMUNHA["rel"].split("/")))) == ESP["bundle_sha256"][DL.TESTEMUNHA["rel"]] == DL.BUNDLE_POR_REL[DL.TESTEMUNHA["rel"]]["sha256"], DL.TESTEMUNHA["sha16_da_ordem"]))
for _p0 in [p_ for p_ in DL.PEDRAS_V410 if p_["rel"] != DL.TESTEMUNHA["rel"]]:   # (v410, UM modulo: a lista e' vazia; a mesma cadeia de igualdades da IALD2 vale para toda outra pedra que o bundle trouxer)
    dep("a %s (outra pedra do bundle da v410): a fonte de origem (a copia duravel em v410\\insumos) == o pino do bundle (sha256_origem); a copia normalizada v410\\pedra == a copia duravel pinada (insumos\\%s_embutida.lean) == a EMBUTIDA no candidato == a do sandbox == o pino dos ESPERADOS (bundle_sha256) == o sha256 do BUNDLE_v410.json" % (_p0["name"], _p0["name"]), {"ESPERADOS_v410.json": ESP},
        lambda _p0=_p0: (sha(rd(_p0["origem"])) == DL.BUNDLE_POR_REL[_p0["rel"]]["sha256_origem"] == _p0["sha256_origem"]
                         and sha(rd(_p0["src"])) == sha(rd(os.path.join(HERE, "insumos", "%s_embutida.lean" % _p0["name"]))) == sha(E1[_p0["rel"]].encode("utf-8")) == sha(rd(os.path.join(KS, *_p0["rel"].split("/")))) == ESP["bundle_sha256"][_p0["rel"]] == DL.BUNDLE_POR_REL[_p0["rel"]]["sha256"], sha(rd(_p0["origem"]))[:16]))
ML_ = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")
ML_N = len(open(ML_, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(ML_) else -1
ML_B = os.path.getsize(ML_) if os.path.exists(ML_) else -1
_NOME_MEM = "o MEMORY.md real cabe com o handoff novo e o gancho da missao: o handoff entra (+1 linha) e o gancho SUBSTITUI a linha velha (saldo +1); linhas hoje + 1 <= 195 e bytes hoje + 900 < 24000 (a linha nova do handoff tem de ter ate 900 B; a superficie do pos-rito NAO compacta: se nao couber, ela RECUSA com rc 3 e a gerencia decide o que sai do indice -- PARE e diga)"
# v410 (herdado da v409; conferido em 04/11/2026 por claude-construtor-v410): a estimativa pessimista (+900 B) deu lugar a SIMULACAO EXATA da superficie: aplica sobre o MEMORY.md real, EM MEMORIA (nada e' escrito), as mesmas duas edicoes de pos_rito/superficies_v410.py (o gancho da missao SUBSTITUI a linha velha; o handoff entra ANTES da linha do handoff da v409) com as funcoes
# REAIS de pos_rito/textos_v410.py e um V sintetico de largura igual a do rito (data, sha16 do candidato, teor 'N/N' da escada); o resultado e' comparado aos limites da superficie (24.000 B, 195 linhas). A superficie do pos-rito segue sendo a guarda real (RECUSA com rc 3, sem compactar); este check so' antecipa o que ela vai medir. Sem as ancoras ou sem o textos: PENDENTE, nunca ok.
def _simular_memory_md():
    import importlib.util
    sp = importlib.util.spec_from_file_location("textos_v410_do_p00", os.path.join(HERE, "pos_rito", "textos_v410.py"))
    T_ = importlib.util.module_from_spec(sp); sp.loader.exec_module(T_)
    esc_ = (ESP or {}).get("escada") if isinstance((ESP or {}).get("escada"), list) else CM.get("escada")
    V_ = {"data": datetime.date.today().strftime("%d/%m/%Y"), "s16": CM["sha16"], "teor": "%d/%d" % (esc_[1], esc_[1])}
    ls_ = open(ML_, "rb").read().decode("utf-8").split("\n")
    nova_ = "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — " + T_.marca_missao(V_) + "íntegra anterior no MEMORY_2.md (movida %s)" % V_["data"][:5]
    k1_ = [i for i, l in enumerate(ls_) if "(missao-ultima-flag-um-py.md)" in l and l.startswith("- [")]
    k2_ = [i for i, l in enumerate(ls_) if "(handoff-v409-custodia.md)" in l and l.startswith("- [")]
    if len(k1_) != 1 or len(k2_) != 1:
        return None, ["ancoras do indice: missao %d, handoff v409 %d (esperado 1 e 1)" % (len(k1_), len(k2_))]
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
_pm = tenta(os.path.join(HERE, "PINO_MEMORIA_PY_v410.json"))
if _pm is None:
    pend("[v410, a FILA DA MEMORIA] memoria.py e' o que a preparacao pinou (PINO_MEMORIA_PY_v410.json)", "PINO_MEMORIA_PY_v410.json ainda nao existe (pino_memoria_py_v410.py e' ato da gerencia/preparacao)")
else:
    _ver = subprocess.run([sys.executable, "-X", "utf8", _MEMPY, "verificar"], capture_output=True, text=True, encoding="utf-8")
    chk("[v410, a FILA DA MEMORIA] memoria.py e' o que a preparacao pinou (sha16 lido do arquivo agora == PINO_MEMORIA_PY_v410.json == o declarado pela gerencia); a pausa do vigia NAO existe agora (o pos-rito a cria antes do indice e a remove depois do pino); e 'memoria.py verificar' (so leitura) esta VERDE agora (rc 0): o pos-rito parte de um indice sem violacao",
        sha(rd(_MEMPY))[:16] == _pm["sha16"] == _pm["declarado_pela_gerencia_sha16"] and not os.path.exists(os.path.join(_MEMD, "fila", "PAUSA_VIGIA.json")) and _ver.returncode == 0, [sha(rd(_MEMPY))[:16], _ver.returncode, os.path.exists(os.path.join(_MEMD, "fila", "PAUSA_VIGIA.json"))])
dep("o hash formal que o RITO vai gerar (a arvore do Nos depois do rito) tem a contagem do ESPERADOS, com os residuais lidos; o pino h8 do candidato bate (entradas = residuais + embutidas)", {"ESPERADOS_v410.json": ESP},
    lambda: (len(ESP["h8_residuais_do_nos"]) + CM["formal_files_n"] == ESP["h8_entradas"] == CM["h8"]["entradas"] and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in ESP["h8_residuais_do_nos"]), [ESP["h8_entradas"], ESP["h8_residuais_do_nos"]]))
chk("nenhum marcador de servidor parado nas pastas das duas cadeias (a guarda do rito)", not os.path.exists(os.path.join(DL.V409, ".servidor_parado_pelo_rito")) and not os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito")))
_pys = sorted(f for f in os.listdir(HERE) if f.endswith(".py") and ".bak" not in f)
for f in _pys:
    try:
        ast.parse(open(os.path.join(HERE, f), encoding="utf-8").read()); s_ = True
    except (SyntaxError, OSError):
        s_ = False
    chk("ast.parse de %s" % f, s_)
for f in ("rito_v410.sh", "construir_kernel_v410.sh", "copiar_k410c.sh", "refazer_candidato_v410.sh", "refazer_sandbox_v410_pos_selo.sh", os.path.join("pos_rito", "chain_pos_rito_v410.sh")):
    chk("sh -n de %s" % f, os.path.exists(os.path.join(HERE, f)) and subprocess.run(["sh", "-n", os.path.join(HERE, f)], capture_output=True).returncode == 0)
dv = tenta(os.path.join(HERE, "DERIVACAO_v410.json"))
dep("a conferencia do instalar/reverter/rito: zero falha nos invariantes (a lista de modulos novos LIDA tem %d elementos e e a dos ESPERADOS; o sidecar entra nos backups; o recibo pre_selo e' o da v410; a Bancada que JA pina a v409) e a sintaxe de todos" % DL.N_BUNDLE, {"DERIVACAO_v410.json": dv}, lambda: (not dv["falhas"] and all(("ok" in v or "rc=0" in v) for v in dv["sintaxe"].values()), [sum(len(x) for x in dv["invariantes"].values())]))
_MARCA_ADAPTAR = "# [A ADAPTAR v410]"
_com_marca = []
for _d, _ds, _fs in os.walk(HERE):
    _ds[:] = [d_ for d_ in _ds if d_ not in ("bump", "__pycache__", "base_v409", "kernel", "insumos", "revisao_terceiro", "arvore_simulada_h8") and not d_.startswith(("antes_", "dry_", "falso_", "imp_", "sim_", "conferidor_import_", "pilar_anterior_", "quarentena_", "tentativa_"))]
    for _f in _fs:
        if (_f.endswith(".py") or _f.endswith(".sh") or _f.endswith(".semente")) and ".bak" not in _f and _f != "_bump_copia_v410.py":
            try:
                if any(l_.startswith(_MARCA_ADAPTAR) for l_ in open(os.path.join(_d, _f), encoding="utf-8", errors="replace").read().split("\n")[:6]):
                    _com_marca.append(os.path.relpath(os.path.join(_d, _f), HERE))
            except OSError:
                pass
chk("RECUSA: nenhum arquivo da cadeia traz a marca `# [A ADAPTAR v410]` (a copia mecanica de rotulo da v409, ainda nao adaptada; a marca so' sai quando o arquivo foi adaptado de verdade)", not _com_marca, sorted(_com_marca))
marcas = [f for f in glob.glob(os.path.join(HERE, "pos_rito", "*.py")) if "TEXTO_A_REESCREVER" in open(f, encoding="utf-8", errors="replace").read().replace('"TEXTO_A_REESCREVER" +', "").replace("_MARCA_PENDENTE = ", "")]
chk("nenhum texto do pos_rito com a marca TEXTO_A_REESCREVER como comentario pendente", not [m for m in marcas if re.search(r"(?m)^\s*#\s*TEXTO_A_REESCREVER", open(m, encoding="utf-8", errors="replace").read())], [os.path.basename(m) for m in marcas][:4])
_veredito = "TODAS PASSARAM" if (ok_all and not PEND) else ("NENHUMA FALHA, %d PENDENTE(S): %s" % (len(PEND), "; ".join(p_["checagem"][:80] for p_ in PEND)) if ok_all else "FALHOU")
print("\nPRECONDICOES v410:", _veredito)
if SECO:
    print("--seco: PRECONDICOES_v410.json NAO gravado (so' leitura); %d checagens, %d pendente(s)" % (len(res), len(PEND)))
else:
    json.dump({"ok": bool(ok_all and not PEND), "sem_falha": bool(ok_all), "pendentes": PEND, "veredito": _veredito, "checagens": res}, open(os.path.join(HERE, "PRECONDICOES_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0 if (ok_all and not PEND) else (3 if ok_all else 1))
