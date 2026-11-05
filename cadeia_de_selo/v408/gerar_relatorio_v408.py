# -*- coding: utf-8 -*-
"""gerar_relatorio_v408.py -- escreve PLANO_v408.md, RELATORIO_PREPARACAO_v408.md e PREPARACAO_v408_PRONTA.json. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta no momento da geracao (nada digitado); a prosa e' da preparacao.
`pronta` e' CALCULADA: true so' se TODOS os portoes passaram (kernel, candidato, AST, ensaio a seco, conferidor, citacoes, guarda das frases, p00, B(n) pre-selo, harnesses); um arquivo que falta ou nao le reprova o portao (fail-closed), nunca o contrario.
Rodar DEPOIS de refazer_candidato_v408.sh e dos dois harnesses (sem --nao-exigir-refazer). Backup de bytes do que ja' existe; temporario -> conferir -> substituir. Molde: gerar_relatorio_v407.py (os mesmos 17 portoes, com `ast_v407_v408`), adaptado em 04/11/2026 a v408
(Tetelestai e' o terminal: bundle de 4 modulos em TGLExt/ -- TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP --, registro com funcao tetelestai_terminal_v408, NENHUMA chave antiga muda de literal, erratas E21 a E23 ao lado, decisoes D48 a D54; a prosa do psion, do canto, do par e da chave do lema saiu).
O revisor distinto da v408 e' o Sonnet (D54: ate' tres rodadas): a trava do orquestrador (S1b: revisao_terceiro/REVISAO_TERCEIRO_v408.json) fica FECHADA ate' a revisao aprovar este candidato; este script nao a abre.
uso: python -I -B -X utf8 gerar_relatorio_v408.py"""
import datetime, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); POS = os.path.join(HERE, "pos_rito")
AGORA = datetime.datetime.now(); ST = AGORA.strftime("%Y%m%d_%H%M%S")
P = lambda p: os.path.join(HERE, *p.split("/"))
rj = lambda p: json.load(open(P(p), encoding="utf-8"))
fh = lambda p: hashlib.sha256(open(P(p), "rb").read()).hexdigest()
h16 = lambda p: fh(p)[:16]
sz = lambda p: os.path.getsize(P(p))


def tenta(p):
    """O JSON lido, ou None (o portao que depende dele reprova)."""
    try:
        return rj(p)
    except (OSError, ValueError):
        return None


import sys as _sys; _sys.path.insert(0, HERE)
import delta_v408 as _DL   # (para ler a Bancada que o delta le do manifesto dela, as frases, as ressalvas e os nomes das falas: nada digitado)
import guarda_frases_v408 as _GFM
DL_B_N = _DL.B_N_SEGUINTE; DL_BANCADA = _DL.BANCADA_PINA_HOJE["deployment_id"]
CM = tenta("CANDIDATO_v408.json") or {}; ES = tenta("ESPERADOS_v408.json") or {}; EN = tenta("ensaio_a_seco_v408.json") or {}; PC = tenta("PRECONDICOES_v408.json") or {"ok": False, "checagens": []}
PR = tenta("PINO_RECIBO_PRE_SELO_v408.json") or {}; PROV = tenta("PROVA_PRODUCAO_INTACTA_v408_pre_selo.json") or {}; CMP = tenta("COMPARACAO_V407_v408.json") or {}; KR = tenta("kernel/KERNEL_RECIBO_v408.json") or {}; PB = tenta("kernel/POS_BUILD_v408.json") or {}; FJ = tenta("kernel/FLAGS_v408.json") or {}; KH = tenta("kernel/KH_N1_v408.json") or {}
CN = tenta("conferencia_rito_v408_CONTROLE_NEGATIVO_PRE_RITO.json") or {}; CP = tenta("conferencia_rito_v408_POSITIVO_FALSO_NOS.json") or {}; CIT = tenta("conferir_citacoes_v408.json") or {}; GF = tenta("GUARDA_FRASES_v408.json") or {}; DRV = tenta("DERIVACAO_v408.json") or {"falhas": ["DERIVACAO_v408.json ausente"]}
SERV = tenta("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v408.json") or {}; CTRL = tenta("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v408.json") or {}; PN = tenta("PINOS_BN_v408.json") or {}
H_T = tenta("pos_rito/HARNESS_TEXTOS_ENSAIO_v408.json"); H_F = tenta("pos_rito/HARNESS_FECHAR_SANDBOX_v408.json")
ENS10 = tenta("orquestrador/ENSAIO_S10_v408.json") or {}; BD = tenta("BUNDLE_v408.json") or {}
ABERTA = (tenta("registro_mapa_prep_v408_ABERTA.json") or [{}])[0]
refazer = open(P("refazer_out_v408.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("refazer_out_v408.txt")) else ""
fim_ok = "== FIM" in refazer and refazer.rstrip().endswith("RC_REFAZER=0")
falhas_p00 = [c["checagem"] for c in PC["checagens"] if not c["ok"] and not c.get("pendente")]
pendentes_p00 = [c["checagem"] for c in PC["checagens"] if c.get("pendente")]
ok_p00 = sum(1 for c in PC["checagens"] if c["ok"]); n_p00 = len(PC["checagens"])
_bn = open(P("bateria_pre_selo/bn_pre_selo_out_v408.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("bateria_pre_selo/bn_pre_selo_out_v408.txt")) else ""
_m = re.search(r'veredito_bateria": "(\w+)"', _bn); bat = _m.group(1) if _m else "NAO LIDO"
# a ordem do operador desta versao: o sha16 e' LIDO do arquivo da fala agora (nunca digitado); se o arquivo faltar, fica None e o aviso o diz
_ORDEM_P = os.path.join(_DL.WK, "cunhagens_13out", _DL.N_ORDEM_V408)
ORDEM16 = hashlib.sha256(open(_ORDEM_P, "rb").read()).hexdigest()[:16] if os.path.isfile(_ORDEM_P) else None
_VN = (BD.get("verbatim_nomes") or {})   # os sha16 das falas dos nomes e do sentido de «P=nP», MEDIDOS pelo preparar_bundle (lidos do BUNDLE_v408.json)


def passou(H):
    return bool(H and H.get("tudo_passou") is True and not H.get("nao_exigiu_refazer"))


def _arquivo_e(p, sha):
    return bool(sha) and os.path.exists(P(p)) and fh(p) == sha


cand_ok = bool(CM.get("sha16") and ES.get("candidato_sha16") == CM["sha16"] and h16("um_v408_candidato.py") == CM["sha16"] and sz("um_v408_candidato.py") == CM.get("bytes") and EN.get("sha16") == CM["sha16"])
N_MOD = _DL.N_BUNDLE   # 4 (o bundle da v408); o recibo do kernel, os ESPERADOS e o candidato concordam com ele, ou o portao reprova
PORTOES = {
    "kernel": bool(KR.get("rc") == 0 and KR.get("sorry") in (0, [], None) and PB.get("ok") is True and len(KR.get("pedras") or []) == N_MOD == (CM.get("kernel") or {}).get("modulos_novos") and FJ.get("n_flags") == ES.get("n_bandeiras_novas") == CM.get("n_bandeiras")),
    "candidato": cand_ok,
    "ast_v407_v408": bool(CMP.get("ok") is True and CMP.get("removidos") in (0, []) and CMP.get("mudados_sem_explicacao") in (0, []) and CMP.get("o_gate_nao_se_move_e_a_v386_nao_e_reescrita") is True),
    "ensaio_a_seco": bool(EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == CM.get("sha16")),
    "conferidor_controle_negativo": bool(CN.get("tudo_bate") is False and CN.get("nao_pode_mudar") and all(CN["nao_pode_mudar"].values()) and CN.get("um_py_sha16") != CM.get("sha16")),
    "conferidor_caminho_positivo": bool(CP.get("tudo_bate") is True and CP.get("um_py_sha16") == CM.get("sha16")),
    "citacoes": bool(CIT.get("todas_conferem") is True),
    "guarda_das_frases": bool(GF.get("ok") is True and GF.get("pedras_limpas") is True and len(GF.get("pedras") or {}) == N_MOD),   # (v408: as quatro pedras, todas da gerencia)
    "instalar_reverter_rito_estatico": bool(not DRV.get("falhas")),
    "p00": bool(PC.get("ok") is True and n_p00 > 0 and not falhas_p00 and not PC.get("pendentes")),
    "bn_pre_selo": bool(PR.get("veredito") == "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA" and PR.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and PROV.get("producao_intacta") is True and bat == "BATERIA_PASSA" and (PN.get("candidato") or {}).get("sha256") == CM.get("sha256")),
    "servico_estatico": bool(SERV.get("n_condicoes") and SERV.get("n_condicoes_ok") == SERV.get("n_condicoes") and CTRL.get("toda_mutacao_foi_pega") is True),
    "harness_textos": passou(H_T),
    "harness_fechar": passou(H_F),
    "refazer_limpo": fim_ok,
    "purga_da_fala_reservada": bool((tenta("purga_v408.json") or {}).get("total_com_ocorrencia") == 0),
    "fala_excluida_fora_dos_artefatos": bool((tenta("purga_v408.json") or {}).get("fala_excluida_total_com_ocorrencia") == 0),
}
falta = [k for k, v in PORTOES.items() if not v]
pronta = not falta
n_neg_leit = len((H_T or {}).get("etapas", {}).get("leitura_negativos", {}).get("controles", []))
n_neg_fech = len((H_F or {}).get("etapas", {}).get("fechar_negativos", []))
n_neg_par = len((H_T or {}).get("etapas", {}).get("paragrafo_v408_e_citacoes", {}).get("negativos", []))
ROTA = ABERTA.get("rota_id") or "NAO LIDA (registro_mapa_prep_v408_ABERTA.json)"   # a rota da preparacao da v408 no Mapa de Rotas (aberta pela gerencia; lida do registro dela)
_nome_op = dict(getattr(_DL, "NOME_DO_OPERADOR", {}) or {})
_anc_mod = {rel_: len(nomes_) for rel_, nomes_ in _DL.ANCORAS_POR_MODULO.items()}
_flags_mod = dict(FJ.get("n_por_modulo") or {})
_bun = ((CM.get("kernel") or {}).get("bundle")) or {}
tab_pedras = "\n".join("| `%s` | %s (antes: `%s`) | %s | %s | `%s` |" % (rel_.split("/")[-1], _DL.BUNDLE_POR_REL[rel_].get("tipo_do_nome"), _DL.BUNDLE_POR_REL[rel_].get("nome_antigo"), _anc_mod.get(rel_), _flags_mod.get(rel_), (_bun.get(rel_) or {}).get("sha16")) for rel_ in _DL.BUNDLE_RELS)
_fj_anc = FJ.get("ancoras") or {}; _fj_test = FJ.get("bandeira_da_testemunha") or {}
tab_chave = "\n".join("| `%s` | `%s` | `%s` |" % (n_, (_DL.ANCORAS.get(n_) or {}).get("rel"), (_fj_anc.get(n_) or {}).get("flag") or _fj_test.get(n_)) for n_ in _DL.ANCORAS_PRINCIPAIS)
try:
    prep_seq = [json.loads(l) for l in open(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", encoding="utf-8") if l.strip() and ('"' + ROTA + '"') in l]
    seqs = ", ".join("%s (%s)" % (r["seq"], r["tipo"]) for r in prep_seq if r.get("rota_id") == ROTA)
except Exception as e:   # noqa: BLE001
    seqs = "nao lido: %r" % (e,)
ARQ = ["um_v408_candidato.py", "CANDIDATO_v408.json", "ESPERADOS_v408.json", "ensaio_a_seco_v408.json", "COMPARACAO_V407_v408.json", "PINOS_BN_v408.json", "PINO_RECIBO_PRE_SELO_v408.json", "PROVA_PRODUCAO_INTACTA_v408_pre_selo.json", "PRECONDICOES_v408.json", "GUARDA_FRASES_v408.json", "VERBATIM_CONGELADO_v408.json", "BUNDLE_v408.json", "kernel_modulos_novos_v408.json", "CONTRATO_DA_CADEIA_v408.md", "DESENHO_v408.md",
       "delta_v408.py", "registros_v408.py", "runtime_v408.py", "guarda_frases_v408.py", "guarda_ordem_de_chamada_v408.py", "guardas_estaticas_bancada_v408.py", "gerar_candidato_v408.py", "gerar_esperados_v408.py", "artigo_pt_v408.pysnip", "artigo_en_v408.pysnip", "comparar_v407_v408.py", "instalar_v408.py", "reverter_v408.py", "rito_v408.sh", "conferir_rito_v408.py", "conferir_citacoes_v408.py", "p00_precondicoes_v408.py",
       "preparar_bundle_v408_04nov.py", "pos_build_kernel_v408.py", "fechar_preparacao_v408.py", "purga_v408.py", "purga_v408.json", "LOGS_COPIADOS_v408.json", "kernel/LOGS_COPIADOS_v408.json",
       "insumos/PSION_NO_ACERVO_04nov_purgado.md", "insumos/RECIBO_PURGA_PSION_NO_ACERVO_04nov.json", "insumos/RECIBO_PEDRAS_v408_NOMES.json",
       "pos_rito/textos_v408.semente", "pos_rito/montar_textos_v408.py", "pos_rito/leitura_v408.py", "pos_rito/fechar_v408.py", "pos_rito/registrar_mapa_v408.py", "pos_rito/superficies_v408.py", "pos_rito/harness_textos_ensaio_v408.py", "pos_rito/harness_fechar_sandbox_v408.py", "pos_rito/chain_pos_rito_v408.sh", "pos_rito/gerar_x_custodia_v408.py", "pos_rito/b3_recibo_v408.py", "pos_rito/fila_memoria_v408.py", "pos_rito/gerar_derivacao_pos_rito_v408.py",
       "orquestrador/pos_treino_v408.py", "orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md", "orquestrador/ENSAIO_S10_v408.json",
       "bancada_B3_servico/recibo_parada_v408.py", "bancada_B3_servico/recibo_religamento_v408.py", "bancada_B3_servico/evento_c1_b3_v408.py", "bancada_B3_servico/conferir_exigencias_servico_v408.py", "bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v408.json", "bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v408.json"] \
      + ["pos_rito/" + os.path.basename(p_) for p_ in sorted(glob.glob(os.path.join(POS, "textos_custodia_handoff_v408*.py")))] \
      + ["pedra/" + r_.split("/")[-1] for r_ in _DL.BUNDLE_RELS] + ["kernel/KERNEL_RECIBO_v408.json", "kernel/FLAGS_v408.json", "kernel/KH_N1_v408.json", "kernel/POS_BUILD_v408.json"]
HASHES = {p: {"sha16": h16(p), "bytes": sz(p)} for p in ARQ if os.path.exists(P(p))}
tab_arq = "\n".join("| `%s` | %s | `%s` |" % (p, format(v["bytes"], ","), v["sha16"]) for p, v in HASHES.items())
_apont = (CIT.get("apontadas_a_gerencia_aspas") or [])
_apont_gf = list(getattr(_GFM, "APONTADAS_A_GERENCIA", ()) or ())
_esc = ES.get("escada_v407_e_v408") or CM.get("escada") or ["?", "?"]
_cob = ES.get("cobertura_kh_n1") or {}; _dkh = KH.get("delta_vs_v407") or {}
_n_falas = len(ES.get("cunhagens") or CM.get("cunhagens") or {}); _mistas = sorted(getattr(_DL, "VERBATIM_AUTOR_POR_NOME", {}) or {})
_textos_custodia = [os.path.basename(p_) for p_ in sorted(glob.glob(os.path.join(POS, "textos_custodia_handoff_v408*.py")))]
AVISOS = [
    "os nomes das quatro pedras sao do operador (04/11/2026; a fala dos nomes tem sha16 %s e a fala do SENTIDO de «P=nP», da tarde, sha16 %s; ambos MEDIDOS pelo preparar_bundle e lidos do BUNDLE_v408.json): PontoDeContradicao, PIgualNP, TempoIgualMoeda, TetelestaiTerminal; o «=» escreve-se Igual, como em formaIgualConteudo; o Dicionario.lean da manha ficou SUPERADO e nao entra (D48 resolvida); BUNDLE_v408.json guarda nome_antigo, sha256 da origem e o numero de linhas #print axioms removidas na normalizacao" % (_VN.get("nomes_sha16"), _VN.get("sentido_p_igual_np_sha16")),
    "NENHUMA chave antiga muda de literal nesta versao (CHAVES_V408 vazia; DESENHO §2): as chaves da v407 seguem lidas do kernel do rito; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos dos registros anteriores NAO mudam (os que carregam a escada mudam so' em numeros); o registro novo e' %s (%d checagens), com veredito de prefixo %s e sufixo %s" % (_DL.FECHO_REGISTRO, _DL.N_CHECKS_FECHO, _DL.VEREDITO_OK_PREFIXO, _DL.VEREDITO_SUFIXO),
    "ressalvas ditas em todo texto (%d em delta_v408.RESSALVAS_V408): o par na face de Fock segue [OPEN] como LIGACAO, nao como ausencia (E21); a palavra que D50 podou fica podada como termo e o conteudo tem o nome do operador «inclinação modular (cociclo)», com espelho a_inclinacao_modular; «P = nP» no sentido do operador (p_igual_np) e, pela correcao dele (D51 revista), P = nP teorema nas classes de computacao do dicionario do operador (as_classes_do_dicionario), com a traducao as classes das maquinas de Turing [OPEN], nao uma recusa; o lock e o Hamiltoniano modular sao objetos distintos que coincidem em Omega; o insumo do acervo entra pela copia PURGADA (E23)" % len(_DL.RESSALVAS_V408),
    "a errata E22 e' da gerencia c1, em nome proprio: as duas frases dela (a que dava a TGL como sem terminal; a da R1 sobre o resto sem traco) estavam erradas pelos teoremas da casa e foram PODADAS; a pedra TetelestaiTerminal as cita entre aspas para as corrigir; o que resta sem traco e' o cociclo, que paga",
    "as %d falas do operador de 04/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v408.json); duas sao de autoria MISTA (%s): o trecho da outra instancia e' [DECLARADO] e o corte esta' em delta_v408.VERBATIM_CORTE; nenhuma fala fora do DESENHO entra (so' listada em VERBATIM_FORA_DO_DESENHO_V408)" % (_n_falas or _DL.N_FALAS_V408, ", ".join(_mistas) or "nenhuma"),
    "o revisor distinto da v408 e' o Sonnet (D54: ate' tres rodadas; ressalvas BAIXAS escritas); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar",
    "a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache",
    "o B(n) pre-selo da v408 (passo simples %s; a Bancada de producao pina %s) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes" % (DL_B_N, DL_BANCADA),
    "conferir_citacoes_v408.json aponta %d citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): %s; o agente nao corrige texto da gerencia" % (len(_apont), "; ".join("%s: %s" % (a_["arquivo"], a_["trecho"]) for a_ in _apont) or "nenhuma"),
    "build a frio dos %d modulos no sandbox k408c: %s s, Audit %s s (kernel/POS_BUILD_v408.json, medidos); %s declaracoes no axiom_report (+%s decl, +%s teoremas sobre a v407), nenhuma fora do trio; escada %s -> %s" % (N_MOD, PB.get("duracao_build_s"), PB.get("duracao_audit_s"), KH.get("axiom_report_efetivo_n"), _dkh.get("decl"), _dkh.get("thm"), _esc[0], _esc[1]),
    "o orquestrador (orquestrador/pos_treino_v408.py) traz as licoes da v407 (D52): os textos da custodia entram ENCADEADOS no passo S6d (%s), depois da chain 14 e antes do S7; o S6a sobe a Bancada Um pelo comando do S6c se a porta 18777 estiver fechada E nao houver processo um_bancada, e so' entao para pelo PID; o S10 usa o template desta pasta com a janela P2 do shared (D53); a autorizacao e' a ORDEM da v408 (%s, sha16 %s, lido do arquivo); o ensaio a seco do S10: %s" % (", ".join(_textos_custodia) or "AUSENTE: nenhum pos_rito/textos_custodia_handoff_v408_*.py", _DL.N_ORDEM_V408, ORDEM16, ("ok" if ENS10.get("ok") is True else "NAO passou ou nao rodou")),
]
if _apont_gf:
    AVISOS.insert(6, "APONTADO a gerencia, NAO corrigido (o agente nao edita pedra revista): %d trecho(s) de pedra que a regra lexical F16 da guarda das frases reprova (enunciado em guarda_frases_v408.APONTADAS_A_GERENCIA, nao repetido aqui para nao reprovar este relatorio na mesma guarda); a gerencia decide se reescreve (BAIXO)" % len(_apont_gf))
NAO_REVISADO = "este candidato (Tetelestai e' o terminal, v408) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D54, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova"
_REV = tenta("revisao_terceiro/REVISAO_TERCEIRO_v408.json") or {}
REVISAO_OK = bool(_REV.get("aprovada") is True and _REV.get("candidato_sha16") == CM.get("sha16") and not _REV.get("n_alto") and not _REV.get("n_medio"))
if REVISAO_OK:   # a revisao de terceiro existe e aprova ESTE candidato: o texto «NAO foi revisado» deixa de valer; o aviso novo diz o que foi e o que NAO foi examinado (nada e' inventado: tudo lido do JSON da revisao)
    NAO_REVISADO = ("este candidato (Tetelestai e' o terminal, v408) FOI revisado por terceiro: %s, rodada %s, aprovada, %s ALTO, %s MEDIO, %s BAIXO (revisao_terceiro/REVISAO_TERCEIRO_v408.md, sha16 %s); quem constroi nao aprova: a aprovacao e' do revisor, nao desta preparacao; "
                    "as ressalvas BAIXAS estao escritas no caderno e valem como ditas (D54: ate' tres rodadas); a trava do orquestrador (S1b) confere aprovada e o sha16 do candidato" % (_REV.get("revisor"), _REV.get("rodada"), _REV.get("n_alto"), _REV.get("n_medio"), _REV.get("n_baixo"), h16("revisao_terceiro/REVISAO_TERCEIRO_v408.json")))
    AVISOS = [a_ for a_ in AVISOS if "esta preparacao NAO foi revisada por terceiro" not in a_]
    AVISOS.append("revisao de terceiro (Sonnet D54): " + NAO_REVISADO)
    AVISOS.append("ressalvas BAIXAS da revisao (nenhuma trava; ver o caderno): " + " | ".join("%s" % (a_.get("onde") or "")[:70] for a_ in (_REV.get("achados") or []) if a_.get("sev") == "BAIXO"))
_vp = (CIT.get("varredura_das_pedras") or {})
_cong408 = tenta("VERBATIM_CONGELADO_v408.json") or {}
ERRATAS_V408_RES = {"erratas": ["E21", "E22", "E23"], "E21": _DL.ERRATAS_V408[0].split(";")[0][:300], "E22": _DL.ERRATAS_V408[1].split(";")[0][:300], "E23": _DL.ERRATAS_V408[2].split(";")[0][:300],
                    "falas_embutidas": len(_cong408.get("arquivos") or []), "citacoes_da_candidata": {"conferidas": _vp.get("citacoes_conferidas"), "reprovadas": len(_vp.get("reprovadas") or []), "so_sem_acento": _vp.get("so_sem_acento")}}
PRONTA = {"contrato": "PREPARACAO_v408_PRONTA", "agente": "claude-construtor-v408", "quando": AGORA.strftime("%Y-%m-%d %H:%M:%S"), "pronta": pronta, "falta": falta, "portoes": PORTOES,
          "candidato_sha16": CM.get("sha16"), "candidato_sha256": CM.get("sha256"), "candidato_bytes": CM.get("bytes"), "origem_sha16": CM.get("base_v407_sha16"), "escada": ES.get("escada_v407_e_v408") or CM.get("escada"), "n_bandeiras_novas": ES.get("n_bandeiras_novas"), "n_modulos_novos": (CM.get("kernel") or {}).get("modulos_novos"),
          "ordem_do_operador": {"arquivo": _DL.N_ORDEM_V408, "sha16_lido_do_arquivo": ORDEM16, "frase": _DL.FRASE_ORDEM_V408},
          "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v408.json", "sha16": h16("kernel/KERNEL_RECIBO_v408.json") if os.path.exists(P("kernel/KERNEL_RECIBO_v408.json")) else None, "rc": KR.get("rc")},
          "esperados_sha16": h16("ESPERADOS_v408.json") if os.path.exists(P("ESPERADOS_v408.json")) else None, "p00": {"ok": PC.get("ok"), "passaram": ok_p00, "n": n_p00, "pendentes": pendentes_p00, "sha16": h16("PRECONDICOES_v408.json") if os.path.exists(P("PRECONDICOES_v408.json")) else None},
          "ensaio_a_seco": {"veredito": EN.get("veredito"), "sha16_do_candidato": EN.get("sha16"), "json_sha16": h16("ensaio_a_seco_v408.json") if os.path.exists(P("ensaio_a_seco_v408.json")) else None},
          "orquestrador": {"ensaio_s10_ok": ENS10.get("ok"), "textos_custodia_encadeados_S6d": _textos_custodia, "template_do_app_D53": os.path.exists(P("orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md"))},
          "comandos": {"instalar": "python -B -X utf8 instalar_v408.py", "rito": "sh rito_v408.sh", "cadeia": "CHAIN_DE=<rotulo> CHAIN_ATE=<rotulo> sh pos_rito/chain_pos_rito_v408.sh (rotulos 0..10 10a 10b 10c 11..14; 10b com B3_AUTORIZADO=sim, EVENTO e EVENTO_HASH); depois os textos da custodia (S6d, D52)", "cwd": HERE,
                       "reverter": "python -B -X utf8 reverter_v408.py (so' por decisao da gerencia)"},
          "hashes": HASHES, "nao_revisado_por_terceiro": NAO_REVISADO, "trava_do_orquestrador": ("S1b (pos_treino_v408): ABERTA pela revisao_terceiro/REVISAO_TERCEIRO_v408.json (aprovada, mesmo sha16 do candidato); a preparacao nao a abriu: o revisor abriu" if REVISAO_OK else "S1b (pos_treino_v408): fechada ate' revisao_terceiro/REVISAO_TERCEIRO_v408.json aprovar ESTE candidato (revisor: Sonnet, D54); esta preparacao nao a abre"), "revisao_de_terceiro": ({"aprovada": _REV.get("aprovada"), "rodada": _REV.get("rodada"), "n_alto": _REV.get("n_alto"), "n_medio": _REV.get("n_medio"), "n_baixo": _REV.get("n_baixo"), "candidato_sha16": _REV.get("candidato_sha16"), "sha16_do_json": h16("revisao_terceiro/REVISAO_TERCEIRO_v408.json"), "revisor": _REV.get("revisor"), "quando": _REV.get("quando")} if REVISAO_OK else None), "erratas_E21_E23": ERRATAS_V408_RES, "avisos": AVISOS, "rota_no_mapa": "%s (seq %s)" % (ROTA, seqs)}


def grava(nome, b):
    p = P(nome)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + ST; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p)


fr = _DL.FRASE_DA_MOLDURA_V408_PT
_ressalvas_txt = "\n".join("  %d. %s" % (i_ + 1, r_) for i_, r_ in enumerate(_DL.RESSALVAS_V408))
_nomes_txt = "; ".join("«%s»" % f_ for f_ in (_DL.FRASE_NOME_PONTO, _DL.FRASE_NOME_PNP, _DL.FRASE_NOME_TEMPO, _DL.FRASE_NOME_TETELESTAI))
PLANO = f"""# PLANO da v408 — Tetelestai é o terminal (preparação)

Agente de preparação `claude-construtor-v408`, {AGORA.strftime('%Y-%m-%d %H:%M')}. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v407 selada `{CM.get('base_v407_sha16')}`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: {fr}.

## 0. A ordem

- [INPUT, operador, 04/11/2026, sha16 do arquivo `{ORDEM16}`] «{_DL.FRASE_ORDEM_V408}». Os nomes das pedras, na fala dele: {_nomes_txt}; o sentido de «P=nP», dado na tarde: «{_DL.FRASE_SENTIDO_PNP}». As {_n_falas or _DL.N_FALAS_V408} falas de 04/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v408.json`; duas de autoria mista, com o trecho da outra instância marcado [DECLARADO]; as falas das versões anteriores já estão no um.py v407 e não entram de novo).
- (A) O BUNDLE: {N_MOD} módulos de kernel em `TGLExt/` (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), compilados no sandbox `{(CM.get('kernel') or {}).get('sandbox')}`, a raiz com {N_MOD} imports. (B) O registro com função `{_DL.FECHO_REGISTRO}` ({_DL.N_CHECKS_FECHO} checagens) e os registros por spec `{_DL.CUNHAGENS_REGISTRO}` e `{_DL.KH_REGISTRO}`. (C) NENHUMA chave antiga muda de literal; as chaves da v407 seguem lidas do kernel; as erratas E21 a E23 vão AO LADO. (D) A seção «Tetelestai é o terminal» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v407 por script.

## 1. Os módulos e as âncoras [REAL, sandbox; nada tocado no Nós]

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
{tab_pedras}

As quatro âncoras principais (uma por módulo, na ordem do bundle):

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
{tab_chave}

Pós-build: {PB.get('n_axiomas_lidos_no_audit')} axiomas lidos no Audit, {PB.get('n_flags')} bandeiras novas (só declaração nomeada), escada {_esc[0]} → {_esc[1]}; build a frio {PB.get('duracao_build_s')} s, Audit {PB.get('duracao_audit_s')} s.

## 2. O que a v408 afirma e o que não afirma

- [REAL] `{_DL.ANCORA_PRINCIPAL}`: o terminal é a leitura, não o fim do decaimento (o motor é posto para todo r e t); basta; a poda; não precisa de 100% para reconstruir o posto inteiro; a quitação. Só com o trio de axiomas, lido do kernel do próprio rito.
- [REAL] `{_DL.ANCORA_PONTO}`: exp 0 = Ω é teorema e Ω ≠ 0 é refutação do vetor nulo; os rótulos «1=0=Verdadeiro» (zero modular) e «1=0=Falso» (zero absoluto) são NOMES do operador para as duas proposições, não identificações; o lock e o Hamiltoniano modular são objetos distintos que coincidem em Ω.
- [INPUT/ONTO, conferido no kernel] `{_DL.ANCORA_TEMPO}`: o tempo é a moeda de β — a conferência compõe só termos que o kernel já tinha (a moeda soma, o preço multiplica; o gerúndio; legislando sem fim).
- [INPUT, com espelho] `{_DL.ANCORA_PIGUALNP}`: «P = nP» só no sentido do operador (P só é P lido pelo módulo n minimamente acoplado); as cinco entradas do dicionário são DEFINIÇÕES dele sobre termos que o kernel já tem; e, pela correção dele (D51 revista), {_DL.FRASE_D51_PT} (`p_igual_np_nas_classes_do_dicionario`; `ClasseP` e `ClasseNP` definidas em Lean; a face finita em `as_classes_do_dicionario`).
- [REAL] O que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`); as chaves da v407 seguem lidas do kernel; nenhuma chave antiga muda.
- Ressalvas ditas ({len(_DL.RESSALVAS_V408)}):
{_ressalvas_txt}
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é confirmação; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v408_candidato.py` `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; +{format(CM.get('delta_bytes') or 0, ',')} B); {CM.get('n_patches')} patches; AST: {CMP.get('nos_nomeados_v407')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (todos explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos. Ensaio a seco: **{EN.get('veredito')}**. Pós-rito: `pos_rito/chain_pos_rito_v408.sh`, rótulos 0…10 10a 10b 10c 11…14; depois, ENCADEADOS, os textos da custódia (S6d, D52) e só então a G1.

## 4. Gates

Ver `PREPARACAO_v408_PRONTA.json`: `pronta` = {str(pronta).lower()}. {NAO_REVISADO}.
"""
RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v408 — Tetelestai é o terminal

Agente de preparação `claude-construtor-v408` · {AGORA.strftime('%Y-%m-%d %H:%M')} · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: {NAO_REVISADO}.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; base v407 `{CM.get('base_v407_sha16')}`): `pronta` = **{str(pronta).lower()}**{'' if pronta else '; falta: ' + ', '.join(falta)}.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `{(CM.get('kernel') or {}).get('sandbox')}`) | {PORTOES['kernel']}: build + Audit rc {KR.get('rc')}, {PB.get('n_flags')} bandeiras novas, escada {_esc[0]} → {_esc[1]}, {len(KR.get('pedras') or [])} módulos no recibo; `KERNEL_RECIBO_v408.json` |
| candidato | {PORTOES['candidato']}: {CM.get('n_patches')} patches; refazer limpo = {fim_ok} |
| AST v407 × v408 | {PORTOES['ast_v407_v408']}: {CMP.get('nos_nomeados_v407')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos; {len(CMP.get('funcoes_intactas') or {})} funções e constantes intactas, todas verdadeiras = {all((CMP.get('funcoes_intactas') or {'x': False}).values())} |
| ensaio a seco | {PORTOES['ensaio_a_seco']}: {EN.get('veredito')} |
| conferidor | negativo {PORTOES['conferidor_controle_negativo']} (`tudo_bate` = {CN.get('tudo_bate')}); positivo {PORTOES['conferidor_caminho_positivo']} (`tudo_bate` = {CP.get('tudo_bate')}) |
| citações | {PORTOES['citacoes']}: {len(CIT.get('apontadas_a_gerencia_aspas') or [])} apontada(s) à gerência (ver §4) |
| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo e as {len(GF.get('pedras') or {})} pedras) |
| instalar / reverter / rito (estático) | {PORTOES['instalar_reverter_rito_estatico']} |
| p00 | {PORTOES['p00']}: {ok_p00}/{n_p00} checagens OK; pendentes: {len(pendentes_p00)} |
| B(n) pré-selo | {PORTOES['bn_pre_selo']}: {PR.get('veredito')}; bateria {bat}; produção intacta = {PROV.get('producao_intacta')}; recibo `{h16('PINO_RECIBO_PRE_SELO_v408.json') if os.path.exists(P('PINO_RECIBO_PRE_SELO_v408.json')) else None}` |
| serviço da Bancada (estático) | {PORTOES['servico_estatico']}: {SERV.get('n_condicoes_ok')}/{SERV.get('n_condicoes')} condições; toda mutação pega = {CTRL.get('toda_mutacao_foi_pega')} |
| harness dos textos | {PORTOES['harness_textos']}: {n_neg_leit} controles da leitura, {n_neg_par} do parágrafo novo |
| harness do fechar | {PORTOES['harness_fechar']}: {n_neg_fech} controles do fechar |
| regeneração limpa | {PORTOES['refazer_limpo']}: `refazer_out_v408.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v408.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | {PORTOES['fala_excluida_fora_dos_artefatos']}: `purga_v408.json`, zero ocorrências |

Fora dos portões, informativo: o ensaio a seco do S10 do orquestrador (`orquestrador/ENSAIO_S10_v408.json`) = {ENS10.get('ok')}; os textos da custódia encadeados no S6d: {', '.join(_textos_custodia) or 'AUSENTE'}.

## 3. O que NÃO passou ou fica para depois

- p00 reprova {len(falhas_p00)} checagem(ns): {'; '.join(f[:200] for f in falhas_p00) if falhas_p00 else 'nenhuma'}; pendentes ({len(pendentes_p00)}): {'; '.join(f[:160] for f in pendentes_p00) if pendentes_p00 else 'nenhum'}.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo, os textos da custódia e o fechar; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `{ROTA}`, seq {seqs}.

## 4. Avisos e desvios ditos

{chr(10).join('- ' + a for a in AVISOS)}

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D54: até três rodadas), nesta ordem, antes de qualquer publicação: `delta_v408.py` (moldura, erratas E21 a E23, decisões D48 a D54, as leituras), `registros_v408.py`, `runtime_v408.py` (as {_DL.N_CHECKS_FECHO} checagens de `{_DL.FECHO_REGISTRO}`), as quatro pedras em `pedra/` (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), as seções do artigo (`artigo_pt_v408.pysnip`, `artigo_en_v408.pysnip`) e `pos_rito/textos_v408.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v408 NÃO entrega: validade no kernel não é creditação; o par na face de Fock segue aberto como ligação a fazer (E21); P = nP é teorema nas classes de computação do dicionário do operador, definidas em Lean (ClasseP, ClasseNP) e provadas na pedra PIgualNP (p_igual_np_nas_classes_do_dicionario); a tradução às classes das máquinas de Turing (bits = log₂ n) é [OPEN], não recusa; o lock e o Hamiltoniano modular são objetos distintos; as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; o teste com a natureza segue da natureza e nenhum teste novo entra nesta versão.
3. O orquestrador lê `PREPARACAO_v408_PRONTA.json` e segue: `instalar_v408.py`, `rito_v408.sh`, `pos_rito/chain_pos_rito_v408.sh` (0 → 10, 10a, 10b, 10c → 14), os textos da custódia encadeados (S6d, D52), a G1 e o S10 do app (D53), com a trava S1b aberta só pela revisão aprovada.
4. Se o rito cair: `reverter_v408.py` é decisão da gerência; `refazer_candidato_v408.sh --regerar` refaz o candidato.

## 6. Módulos e âncoras

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
{tab_pedras}

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
{tab_chave}

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
{tab_arq}
"""
grava("PLANO_v408.md", PLANO.encode("utf-8")); grava("RELATORIO_PREPARACAO_v408.md", RELATORIO.encode("utf-8"))
HASHES["PLANO_v408.md"] = {"sha16": h16("PLANO_v408.md"), "bytes": sz("PLANO_v408.md")}; HASHES["RELATORIO_PREPARACAO_v408.md"] = {"sha16": h16("RELATORIO_PREPARACAO_v408.md"), "bytes": sz("RELATORIO_PREPARACAO_v408.md")}
grava("PREPARACAO_v408_PRONTA.json", json.dumps(PRONTA, ensure_ascii=False, indent=1).encode("utf-8"))
print("pronta =", pronta, "| falta:", falta)
print("candidato", CM.get("sha16"), "| kernel recibo", PRONTA["kernel_recibo"]["sha16"], "| ESPERADOS", PRONTA["esperados_sha16"], "| p00", PRONTA["p00"]["sha16"], "(%d/%d)" % (ok_p00, n_p00))
print(P("PREPARACAO_v408_PRONTA.json"))
