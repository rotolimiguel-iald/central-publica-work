# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] ESCRITO DE NOVO (varrido, nao remendado) a partir do molde gerar_relatorio_v410.py: a v411 NAO tem modulo novo de kernel; UM registro com funcao (h0dn_bg1_v411, 16 checagens: o resultado da abertura RECALCULADO dos bytes embutidos) e dois por spec (cunhagens_v411, kh_n1_cobertura_v411); os portoes sem bundle; o topo ratificado como portao; o modo de ensaio do topo proposto (nunca pronta); a prosa montada do DESENHO_v411 e do core, com a guarda das frases da v411 (F67) e a P18 pela excecao unica da cabeca
"""gerar_relatorio_v411.py -- o RELATORIO da preparacao da v411 (claude-construtor-v411, a servico da gerencia c1, 12/11/2026). Grava PLANO_v411.md, RELATORIO_PREPARACAO_v411.md e PREPARACAO_v411_PRONTA.json
(na pasta da cadeia; no modo de ensaio do topo proposto, V411_ENSAIO_TOPO_PROPOSTO=1, na pasta de ensaio fora de work, marcados com DL.MARCA_ENSAIO e NUNCA com pronta = true). TUDO e' LIDO dos artefatos por script
(nada digitado; o arquivo manda): o manifesto do candidato, os ESPERADOS, o ensaio a seco, a comparacao v410/v411, os conferidores (controle negativo e caminho positivo), as citacoes, a derivacao do instalar/rito,
o p00, o B(n) pre-selo pinado, o servico estatico e o controle negativo dele, as guardas estaticas da Bancada, os harnesses do pos-rito, a purga, a varredura do Fock/Omega e, da preparacao, o recibo do kernel,
os ensaios offline (o registro 16/16, o quadro), a guarda das frases e o pre-voo do gerador. Os numeros do teste saem do core do ensaio a seco (o registro h0dn_bg1_v411 RECALCULADO); sem ele, do registro do ensaio
offline, dito. A prosa passa pela guarda das frases da v411 (inclusive a F67: o primario nunca sem a linha das Cefeidas livres, o modelo publicado, a retrodicao nao cega e validade, nao creditacao) e pela P18 com a
UNICA excecao (_v411_p18_sem_cabeca); a guarda da prosa e' um portao. Validade no kernel nao e' creditacao; o gate nao se move.
uso: python -B -X utf8 gerar_relatorio_v411.py [--seco [--imprimir]]   (--seco: monta e mede, nao grava)"""
import datetime, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
AGORA = datetime.datetime.now(); ST = AGORA.strftime("%Y%m%d_%H%M%S")
ENSAIO = DL.ENSAIO_TOPO_PROPOSTO
S = lambda rel_: os.path.join(DL.SAIDA, *rel_.split("/"))    # um artefato da RODADA (a pasta da cadeia, ou a de ensaio)
H = lambda rel_: os.path.join(HERE, *rel_.split("/"))         # um artefato da PREPARACAO (o kernel do sandbox, os ensaios offline, a guarda, o pre-voo)
sha = lambda p_: hashlib.sha256(open(p_, "rb").read()).hexdigest()
h16 = lambda p_: sha(p_)[:16] if os.path.isfile(p_) else None
sz = lambda p_: os.path.getsize(p_) if os.path.isfile(p_) else None


def tenta(p_):
    """O JSON lido, ou None (o portao que depende dele reprova, visivel)."""
    try:
        return json.load(open(p_, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def txt(p_):
    return open(p_, encoding="utf-8", errors="replace").read() if os.path.isfile(p_) else ""


def zero(x_):
    return str(x_) in ("0", "[]", "None") or x_ in (0, [], None)


# ---------------- o que a rodada produziu (pasta da cadeia, ou a de ensaio)
CM = tenta(DL.MANIFESTO_ARQ) or {}; ES = tenta(S("ESPERADOS_v411.json")) or {}; EN = tenta(S("ensaio_a_seco_v411.json")) or {}; PC = tenta(S("PRECONDICOES_v411.json")) or {}
CMP = tenta(S("COMPARACAO_V410_v411.json")) or {}; CN = tenta(S("conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json")) or {}; CP = tenta(S("conferencia_rito_v411_POSITIVO_FALSO_NOS.json")) or {}
CIT = tenta(S("conferir_citacoes_v411.json")) or {}; DRV = tenta(S("DERIVACAO_v411.json")) or {}; PN = tenta(S("PINOS_BN_v411.json")) or {}
PR = tenta(S("PINO_RECIBO_PRE_SELO_v411.json")) or {}; PROV = tenta(S("PROVA_PRODUCAO_INTACTA_v411_pre_selo.json")) or {}
SERV = tenta(S("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v411.json")) or {}; CTRL = tenta(S("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v411.json")) or {}
H_T = tenta(S("pos_rito/HARNESS_TEXTOS_ENSAIO_v411.json")); H_F = tenta(S("pos_rito/HARNESS_FECHAR_SANDBOX_v411.json"))
PUR = tenta(S("purga_v411.json")) or {}; GE = tenta(S("GUARDAS_ESTATICAS_BANCADA_v411.json")) or {}; VF = tenta(S("VARREDURA_FOCK_OMEGA_v411.json"))
BN_OUT = txt(S("bateria_pre_selo/bn_pre_selo_out_v411.txt")); _m_bat = re.search(r'veredito_bateria": "(\w+)"', BN_OUT); BAT = _m_bat.group(1) if _m_bat else "NAO LIDO"
CAD_OUT = txt(S("cadeia_v411_out.txt"))
# ---------------- o que a preparacao mediu (a pasta da cadeia)
KR = tenta(H("kernel/KERNEL_RECIBO_v411.json")) or {}; PB = tenta(H("kernel/POS_BUILD_v411.json")) or {}; FJ = tenta(H("kernel/FLAGS_v411.json")) or {}; KH = tenta(H(DL.KERNEL_DIR + "/" + DL.KH_N1_INSUMO)) or {}
TO = tenta(H("TESTE_H0DN_OFFLINE_v411.json")) or {}; TQ = tenta(H("TESTE_QUADRO_v411.json")) or {}; GFJ = tenta(H("GUARDA_FRASES_v411.json")) or {}; GCV = tenta(H("GUARDA_CONVERSA_v411.json")) or {}; PV = tenta(H("PREVOO_GERADOR_v411.json")) or {}
_AB = tenta(H("registro_mapa_prep_v411_ABERTA.json")) or tenta(H("registro_mapa_construtor_v411.json")) or {}
ABERTA = (_AB[0] if _AB else {}) if isinstance(_AB, list) else _AB
ROTA = ABERTA.get("rota_id") or "NAO LIDA (registro_mapa_prep_v411_ABERTA.json / registro_mapa_construtor_v411.json)"
_REV = tenta(H("revisao_terceiro/REVISAO_TERCEIRO_v411.json")) or {}

# ---------------- os numeros do teste: o registro h0dn_bg1_v411 RECALCULADO no core do ensaio a seco (deste artefato); sem ele, o do ensaio offline (dito)
_core_dry = (tenta(os.path.join(DL.DRY_DIR, "core_ensaio.json")) or {}).get("core") or {}
_dry_e_deste = bool(CM.get("sha16")) and h16(os.path.join(DL.DRY_DIR, "um.py")) == CM.get("sha16")
if _dry_e_deste and isinstance(_core_dry.get(DL.FECHO_REGISTRO), dict):
    REG = _core_dry[DL.FECHO_REGISTRO]; ORIGEM_NUM = "o core do ensaio a seco deste %s (o registro %s recalculado no ponto de chamada real)" % (DL.ROTULO_DO_ARTEFATO, DL.FECHO_REGISTRO)
else:
    REG = tenta(H("TESTE_H0DN_OFFLINE_v411_registro.json")) or {}; ORIGEM_NUM = "o registro do ensaio OFFLINE (o mesmo recalculo, os mesmos insumos; o ensaio a seco deste artefato ainda nao gravou o core)"
_v = REG.get("values") or {}; PRI = _v.get("primario") or {}; CEF = _v.get("cefeidas_livres") or {}
_mch = (REG.get("mechanics") or {}).get("checks") or []


def fpt(x_, k_=2):
    return ("%.*f" % (k_, x_)).replace(".", ",").replace("-", "−") if isinstance(x_, (int, float)) and not isinstance(x_, bool) else "n/d"


H0DN_RES = {"registro": DL.FECHO_REGISTRO, "origem_dos_numeros": ORIGEM_NUM, "all_verified": REG.get("all_verified"), "n_checks_ok": sum(1 for c_ in _mch if c_.get("ok")), "n_checks": len(_mch), "n_checks_esperadas": DL.N_CHECKS_FECHO,
            "verdict": REG.get("verdict"), "primario": {k_: PRI.get(k_) for k_ in ("z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome", "modelo")},
            "cefeidas_livres": {k_: CEF.get(k_) for k_ in ("z_null", "z_tgl", "D", "ramo", "outcome", "modelo")}, "cabeca_do_teste_no_core": bool(PRI.get("cabeca_do_teste")), "tolerancia_do_recalculo": DL.TOL_RECALCULO}
MOLDURA_PT = DL.FRASE_MOLDURA_V411_PT % (fpt(PRI.get("z_null")), fpt(PRI.get("z_tgl")), PRI.get("ramo", "n/d"), fpt(CEF.get("z_null")), CEF.get("ramo", "n/d"))

# ---------------- a ordem do operador (D169) e o topo (5.1 b)
ORDEM = DL.FALA_ORDEM_V411; ORDEM16 = h16(ORDEM["arquivo"])   # (D181) a ordem e' CITADA (arquivo, sha16, papel); o relatorio nao a transcreve
_topo_cm = CM.get("topo") or {}
TOPO_OK = bool((not ENSAIO) and os.path.isfile(DL.TOPO_RATIFICADO_ARQ) and _topo_cm.get("ratificado") is True and _topo_cm.get("sha256") == sha(DL.TOPO_RATIFICADO_ARQ))

# ---------------- D135: nenhum .tmp na pasta; nenhuma copia do kernel por rodada dentro de work; a contagem de arquivos da pasta
_tmps = [p_ for p_ in glob.glob(os.path.join(HERE, "**", "*.tmp"), recursive=True)]
_copias_em_work = [d_ for d_ in os.listdir(HERE) if re.match(r"^(imp_|dry_|falso_nos|arvore_simulada_|sim_)", d_) and os.path.isdir(os.path.join(HERE, d_))]
_arqs = [os.path.join(dp_, f_) for dp_, dn_, fn_ in os.walk(HERE) for f_ in fn_ if not f_.endswith(".tmp")]
_novos_deste = [n_ for n_ in ("PLANO_v411.md", "RELATORIO_PREPARACAO_v411.md", "PREPARACAO_v411_PRONTA.json") if not ENSAIO and not os.path.exists(H(n_))]
CONTAGEM = {"quando": AGORA.strftime("%Y-%m-%d %H:%M:%S"), "n_arquivos_na_pasta_da_cadeia": len(_arqs) + len(_novos_deste), "n_sem_backups": sum(1 for p_ in _arqs if ".bak_" not in os.path.basename(p_)) + len(_novos_deste),
            "n_backups": sum(1 for p_ in _arqs if ".bak_" in os.path.basename(p_)), "inclui_os_que_este_relatorio_grava": _novos_deste,
            "nota": "a contagem e' da pasta da cadeia no momento deste relatorio (os .tmp fora); o fechar_preparacao, a inscricao ACOM, a revisao de terceiro e o rito acrescentam arquivos depois: a contagem final vai no handoff"}
COPIAS = sorted(p_ for p_ in [DL.SANDBOX, os.path.join(DL.SANDBOX_PAI, "arvore_simulada_h8"), DL.DRY_DIR, DL.FALSO_NOS_DIR, DL.ENSAIO_DIR] + glob.glob(os.path.join(DL.SANDBOX_PAI, "imp_*")) + glob.glob(os.path.join(DL.SANDBOX_PAI, "arvore_simulada_*")) if os.path.isdir(p_))


def passou(H_):
    return bool(H_ and H_.get("tudo_passou") is True and not H_.get("nao_exigiu_refazer"))


def _chk_p00(prefixo_):
    cs_ = [c_ for c_ in (PC.get("checagens") or []) if str(c_.get("checagem", "")).startswith(prefixo_)]
    return bool(cs_) and all(c_.get("ok") is True for c_ in cs_)


_rcs = re.findall(r"^   rc=(\d+)$", CAD_OUT, re.M)
_passos_cad = re.findall(r"^== (\d\d_[a-z0-9_]+) ", CAD_OUT, re.M)
_orq = txt(H("orquestrador/pos_treino_v411.py")); _laco = re.search(r"for passo in \(([^)]*)\)", _orq)
SEM_S7_S10 = bool(_laco and "s7_" not in _laco.group(1) and "s10_" not in _laco.group(1))
_cand16 = CM.get("sha16")
PORTOES = {
    "topo_ratificado": TOPO_OK,   # (DESENHO 5.1 b e secao 8: sem a palavra do operador sobre o topo nao ha' candidato; o ensaio do topo proposto nunca passa aqui)
    "kernel": bool(all(k_ in KR for k_ in ("rc", "sorry", "erros")) and zero(KR.get("rc")) and zero(KR.get("sorry")) and zero(KR.get("erros")) and KR.get("pedras") == [] and PB.get("ok") is True and all((PB.get("criterios") or {"x": False}).values()) and PB.get("n_modulos_compilados") == 0
                   and FJ.get("n_flags") == 0 and not FJ.get("flags") and (CM.get("kernel") or {}).get("modulos_novos") == 0 and CM.get("n_bandeiras") == 0 and (PB.get("escada") or [0, 1])[0] == (PB.get("escada") or [0, 1])[1] == (CM.get("escada") or [None])[-1]),   # (C-10 da revisao de terceiro: a PRESENCA das chaves, alem do valor) [CU-1 da conferencia unica, 12/11/2026, gerencia c1: este comentario estava no MEIO da expressao, na linha de cima, e desligava PB.ok, os criterios do POS_BUILD e n_modulos_compilados; foi movido para o fim, sem mudar condicao]
    "candidato": bool(_cand16 and h16(DL.CANDIDATO_ARQ) == _cand16 and sz(DL.CANDIDATO_ARQ) == CM.get("bytes") and ES.get("candidato_sha16") == _cand16 and EN.get("sha16") == _cand16),
    "previoo_do_gerador": bool(PV.get("ok") is True and not (PV.get("guarda_frases") or {}).get("violacoes_no_texto_renderizado")),
    "registro_h0dn_offline_16": bool(TO.get("TUDO_PASSOU") is True and TO.get("n_ok") == DL.N_CHECKS_FECHO),
    "quadro_e_secao_renderizados": bool(TQ.get("TUDO_PASSOU") is True),
    "guarda_das_frases": bool((GFJ.get("controle_negativo") or {}).get("ok") is True),
    "ast_v410_v411": bool(CMP.get("ok") is True and CMP.get("removidos") == [] and CMP.get("mudados_sem_explicacao") == [] and CMP.get("o_gate_nao_se_move_e_o_kernel_nao_muda") is True),
    "ensaio_a_seco": bool(EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == _cand16),
    "registro_h0dn_no_ensaio_16": bool(_dry_e_deste and REG.get("all_verified") is True and H0DN_RES["n_checks_ok"] == H0DN_RES["n_checks"] == DL.N_CHECKS_FECHO),
    "guarda_da_conversa_d181": bool(GCV.get("ok") is True and GCV.get("candidato_sha16") == _cand16 and (GCV.get("controle_negativo") or {}).get("ok") is True and _chk_p00("(D181) a GUARDA DA CONVERSA") and (EN.get("guarda_conversa") or {}).get("ok") is True
                                    and (EN.get("guarda_conversa") or {}).get("n_alvos", 0) >= 6),   # (R1, D181: as 11 falas da casa tem 0 ocorrencias no fonte do candidato e nos rendidos do ensaio a seco, com os controles negativos dos dois lados)
    "conferidor_controle_negativo": bool(CN.get("tudo_bate") is False and CN.get("nao_pode_mudar") and all(CN["nao_pode_mudar"].values()) and CN.get("um_py_sha16") != _cand16),
    "conferidor_caminho_positivo": bool(CP.get("tudo_bate") is True and CP.get("um_py_sha16") == _cand16),
    "citacoes": bool(CIT.get("ok") is True and not CIT.get("nao_verbatim") and not CIT.get("nao_conferidos_corpo_da_v410_a_adaptar")),
    "instalar_reverter_rito_estatico": bool(DRV and not DRV.get("falhas")),
    "p00": bool(PC.get("veredito") == "TODAS PASSARAM"),
    "veto_kimi": _chk_p00("VETO"),
    "material_privado": bool(_chk_p00("GUARDA DE MATERIAL PRIVADO") and _chk_p00("a mesma guarda sobre")),
    "bn_pre_selo": bool(PR.get("veredito") == "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA" and PR.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and PROV.get("producao_intacta") is True and BAT == "BATERIA_PASSA"
                        and (PN.get("candidato") or {}).get("sha256") == CM.get("sha256")),
    "servico_estatico": bool(SERV.get("n_condicoes") and SERV.get("n_condicoes_ok") == SERV.get("n_condicoes") and CTRL.get("toda_mutacao_foi_pega") is True),
    "guardas_estaticas_bancada": bool(str(GE.get("veredito")).startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and (GE.get("candidato") or {}).get("sha16") == _cand16),
    "harness_textos": passou(H_T),
    "harness_fechar": bool(passou(H_F) and not (H_F or {}).get("pino_emulado") and (((H_F or {}).get("etapas") or {}).get("fila_da_memoria") or {}).get("tudo_passou") is True),
    "cadeia_limpa_ate_o_relatorio": bool(CAD_OUT and "PARADO" not in CAD_OUT and "Traceback" not in CAD_OUT and _rcs and all(r_ == "0" for r_ in _rcs) and any(p_.startswith("15_") for p_ in _passos_cad)),
    "purga_da_fala_reservada": bool(PUR.get("total_com_ocorrencia") == 0),
    "fala_excluida_fora_dos_artefatos": bool(PUR.get("fala_excluida_total_com_ocorrencia") == 0),
    "varredura_fock_omega": bool(VF is not None and VF.get("n_novos") == 0 and VF.get("arquivos", 0) > 0),
    "d135_sem_tmp_e_sem_copias_do_kernel_em_work": bool(not _tmps and not _copias_em_work),
    "orquestrador_sem_S7_e_sem_S10": SEM_S7_S10,
}
if ENSAIO:
    PORTOES["nao_e_ensaio_do_topo_proposto"] = False   # (o ensaio do topo proposto depura a cadeia: NUNCA vale como preparacao pronta)

# ---------------- avisos (montados dos arquivos e do DESENHO)
_excecao = GFJ.get("excecao_p18_da_cabeca") or {}
AVISOS = ([("ENSAIO DO TOPO PROPOSTO: o artefato %s (sha16 %s) NAO e' candidato: o texto do topo e' a PROPOSTA da gerencia (DESENHO 5.1 b), pendente da palavra do operador; nada aqui se instala; o hash nao entra na pasta da cadeia; "
             "a preparacao real comeca quando a gerencia gravar TOPO_RATIFICADO_v411.json" % (os.path.basename(DL.CANDIDATO_ARQ), _cand16))] if ENSAIO else [])
AVISOS += [
    "a excecao ESTREITA da P18 (decisao (c) da gerencia, 12/11): uma funcao so', _v411_p18_sem_cabeca (a mesma no um.py e na cadeia: guarda_frases_v411.p18_sem_cabeca), retira APENAS a cabeca exata que a c7 monta do literal pre-registrado; "
    "controles: a exata sai = %s; um caractere trocado e' recusado = %s; a crua e' recusada = %s; o portao de textos da G1 nao tem a R1 (medido pela custodia): a excecao fica so' na cadeia, e a NOTA do handoff diz isso em uma linha"
    % (_excecao.get("exata_retirada"), _excecao.get("um_caractere_trocado_recusado"), _excecao.get("crua_recusada")),
    "contratos de registro novos, FORA da escada de teoremas (D135; dizer no handoff): " + ", ".join(DL.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA),
    "as erratas AO LADO, em nome proprio da gerencia c1: " + "; ".join("%s: %s" % (e_["id"], e_["texto"]) for e_ in DL.ERRATAS_V411),
    "as traducoes EN (o titulo do quadro do topo e a frase EN ao lado do estatuto da prova) sao do construtor e ficam marcadas para a revisao de terceiro (decisao (e) da gerencia)",
    "a tolerancia do recalculo segue %g; o medido no ensaio offline foi %s (decisao (g) da gerencia)" % (DL.TOL_RECALCULO, json.dumps(TO.get("c6_max_dif"), ensure_ascii=False)),
    "a contagem de arquivos da pasta da cadeia, para o handoff: %d (%d sem os backups; %d backups), no momento deste relatorio" % (CONTAGEM["n_arquivos_na_pasta_da_cadeia"], CONTAGEM["n_sem_backups"], CONTAGEM["n_backups"]),
    "as copias do kernel por rodada ficam FORA de work (D135): " + ", ".join(COPIAS),
    "o orquestrador (orquestrador/pos_treino_v411.py) sem S7 e sem S10, MEDIDO no laco de passos = %s; o fim da cadeia desta versao e' o HANDOFF; a custodia, o site e o X sao da sessao de custodia" % SEM_S7_S10,
]
NAO_REVISADO = ("este %s (o teste H0DN x BG1 aberto, v411) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D109: uma rodada de conserto e uma conferencia unica), ato da gerencia; quem constroi nao aprova" % DL.ROTULO_DO_ARTEFATO)
REVISAO_OK = bool((not ENSAIO) and _REV.get("aprovada") is True and _REV.get("candidato_sha16") == _cand16 and not _REV.get("n_alto") and not _REV.get("n_medio"))
if REVISAO_OK:
    NAO_REVISADO = "a revisao de terceiro (revisao_terceiro/REVISAO_TERCEIRO_v411.json, rodada %s, revisor %s) APROVOU este candidato (%s): %s ALTO, %s MEDIO, %s BAIXO; quem constroi nao aprovou: o revisor aprovou" % (
        _REV.get("rodada"), _REV.get("revisor"), _cand16, _REV.get("n_alto"), _REV.get("n_medio"), _REV.get("n_baixo"))


def _tab(linhas_):
    return "\n".join(linhas_)


def _prosa(pronta_, falta_):
    rot_ = DL.ROTULO_DO_ARTEFATO
    cab_ = "ENSAIO DO TOPO PROPOSTO (nao e' candidato; nao vale como preparacao)" if ENSAIO else ("PRONTA" if pronta_ else "NAO PRONTA")
    dec_ = _tab("- **%s** %s" % (k_, v_) for k_, v_ in DL.DECISOES_V411.items())
    err_ = _tab("- **%s** (%s) %s" % (e_["id"], e_["assinatura"], e_["texto"]) for e_ in DL.ERRATAS_V411)
    t7_ = _tab("| %s | %s |" % (r_["item"], r_["nesta_versao"] + (" (%s; na secao 7: “%s”)" % (r_["ao_lado"], r_["na_secao_7"]) if r_.get("ao_lado") else "")) for r_ in DL.TABELA_SECAO7)
    nd_ = _tab("%d. %s" % (i_ + 1, x_) for i_, x_ in enumerate(DL.NAO_DECIDE_RESUMO_PT))
    rs_ = _tab("%d. %s" % (i_ + 1, x_) for i_, x_ in enumerate(DL.RESSALVAS_ROTULOS_PT))
    port_ = _tab("| `%s` | %s |" % (k_, "passa" if v_ else "NAO passa") for k_, v_ in PORTOES.items())
    arq_ = _tab("| `%s` | %s | `%s` |" % (os.path.relpath(p_, DL.SAIDA) if p_.startswith(DL.SAIDA) else p_, format(sz(p_) or 0, ","), h16(p_)) for p_ in HASH_ARQS if os.path.isfile(p_))
    plano_ = f"""# PLANO DA v411 — o teste H0DN × BG1 aberto, a emenda e o resultado recalculado no rito ({cab_})

> Gerado por `gerar_relatorio_v411.py` (claude-construtor-v411, a serviço da gerência c1) em {AGORA.strftime('%d/%m/%Y %H:%M')}; tudo lido dos artefatos. Molde: `PLANO_v410.md`. Base: a v410 selada `{CM.get('base_v410_sha16')}`; {rot_} `{_cand16}` ({format(CM.get('bytes') or 0, ',')} B).

## A ordem

A ordem desta versão (D169), citada do arquivo `{ORDEM['nome']}` (sha16 `{ORDEM16}`; papel: {ORDEM['papel']}; o texto fica no arquivo da casa, D181). O topo do resumo segue o texto {'PROPOSTO pela gerência (DESENHO 5.1 b), pendente da palavra do operador' if not TOPO_OK else 'RATIFICADO (TOPO_RATIFICADO_v411.json, sha16 `%s`)' % h16(DL.TOPO_RATIFICADO_ARQ)}.

## O que entra

- Kernel: NENHUM módulo novo; o da v410, byte a byte (escada {(CM.get('escada') or ['?'])[-1]}, {FJ.get('n_flags')} bandeiras novas; o Audit do sandbox `{DL.SANDBOX}` com o log da v410).
- UM registro com função, `{DL.FECHO_REGISTRO}` ({DL.N_CHECKS_FECHO} checagens): a cada rito ele decodifica os insumos embutidos, confere-os contra os pinos de produção, executa dos bytes a rotina pinada da abertura e compara o recálculo com o resultado gravado (tolerância {DL.TOL_RECALCULO:g}); dois por spec, `{DL.CUNHAGENS_REGISTRO}` e `{DL.KH_REGISTRO}`. Os quatro registros com função da v410 seguem selados, como herança.
- O resultado, com os números do registro ({ORIGEM_NUM}): {MOLDURA_PT}.
- O que o teste não decide:

{nd_}

- As sete ressalvas (em toda superfície em que o resultado aparecer; o texto é o da seção 8 do pré-registro embutido):

{rs_}

- P = nP {DL.D10.FRASE_QUALIFICADOR_PT} (D64 e D84 da v410).

## Decisões e erratas (lidas do DESENHO_v411)

{dec_}

{err_}

## A lista herdada da v410 (a seção 7, com a linha AO LADO da E43)

| item | nesta versão |
|---|---|
{t7_}

## O que é da gerência, na ordem

1. a revisão de terceiro (Sonnet, D109); 2. `fechar_preparacao_v411.py` e `acom_inscrever_prep_v411.py`; 3. `pino_memoria_py_v411.py` e a folga do `MEMORY.md`; 4. a tarefa agendada `IALD_pos_treino_v411` (Enable, Start, Disable); 5. o orquestrador: S0 a S9, sem S7 e sem S10, o fim é o HANDOFF; 6. o rito, o B{DL.B_N_SEGUINTE[1:]} da Bancada (a produção pina `{DL.BANCADA_PINA_HOJE['deployment_id']}`) e a custódia, que não é desta cadeia.
"""
    rel_ = f"""# RELATÓRIO DA PREPARAÇÃO DA v411 ({cab_})

> Gerado por `gerar_relatorio_v411.py` em {AGORA.strftime('%d/%m/%Y %H:%M')}; tudo lido dos artefatos; o que não foi lido aparece como portão que não passa. {rot_.capitalize()}: `{_cand16}`; base v410 `{CM.get('base_v410_sha16')}`; escada {CM.get('escada')}; bandeiras novas: {FJ.get('n_flags')}; módulos novos: {(CM.get('kernel') or {}).get('modulos_novos')}.

## Portões ({sum(1 for v_ in PORTOES.values() if v_)} de {len(PORTOES)} passam; falta: {', '.join(falta_) or 'nada'})

| portão | estado |
|---|---|
{port_}

## O teste, do registro

{MOLDURA_PT}. Checagens do registro: {H0DN_RES['n_checks_ok']} de {H0DN_RES['n_checks']} ({DL.N_CHECKS_FECHO} esperadas); origem dos números: {ORIGEM_NUM}.

## Avisos

{_tab('- ' + a_ for a_ in AVISOS)}

## Revisão

{NAO_REVISADO}.

## Arquivos (sha16 lidos)

| arquivo | bytes | sha16 |
|---|---|---|
{arq_}

## Pendências do p00 (atos da gerência, quando houver)

{_tab('- ' + str(p_.get('checagem'))[:200] for p_ in (PC.get('pendentes') or [])) or '- nenhuma lida'}
"""
    return plano_, rel_


HASH_ARQS = [DL.CANDIDATO_ARQ, DL.MANIFESTO_ARQ, S("ESPERADOS_v411.json"), S("ensaio_a_seco_v411.json"), S("COMPARACAO_V410_v411.json"), S("conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json"),
             S("conferencia_rito_v411_POSITIVO_FALSO_NOS.json"), S("conferir_citacoes_v411.json"), S("DERIVACAO_v411.json"), S("PINOS_BN_v411.json"), S("PINO_RECIBO_PRE_SELO_v411.json"), S("PROVA_PRODUCAO_INTACTA_v411_pre_selo.json"),
             S("PRECONDICOES_v411.json"), S("GUARDAS_ESTATICAS_BANCADA_v411.json"), S("VARREDURA_FOCK_OMEGA_v411.json"), S("purga_v411.json"), S("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v411.json"),
             S("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v411.json"), S("pos_rito/HARNESS_TEXTOS_ENSAIO_v411.json"), S("pos_rito/HARNESS_FECHAR_SANDBOX_v411.json"),
             H("kernel/KERNEL_RECIBO_v411.json"), H("kernel/POS_BUILD_v411.json"), H("TESTE_H0DN_OFFLINE_v411.json"), H("TESTE_QUADRO_v411.json"), H("GUARDA_FRASES_v411.json"), H("PREVOO_GERADOR_v411.json"), H("DESENHO_v411.md")]


def _guarda(txt_):
    """a guarda das frases da v411 (F60 a F67 e as herdadas) e a P18 com a UNICA excecao da cabeca; lista de (regra, trecho)"""
    return [tuple(v_[:2]) for v_ in list(GF.violacoes(txt_)) + list(GF.p18_sem_cabeca(txt_, GF.RAMOS_V411, GF.N_DA_CABECA))]


falta = [k_ for k_, v_ in PORTOES.items() if not v_]
pronta = not falta
for _volta in range(3):   # a guarda da prosa e' um portao: renderiza, mede, renderiza de novo com o portao dentro do quadro (converge em duas voltas)
    PLANO, RELATORIO = _prosa(pronta, falta)
    _viol = _guarda(PLANO + "\n" + RELATORIO)
    PORTOES["guarda_da_prosa"] = not _viol
    _falta2 = [k_ for k_, v_ in PORTOES.items() if not v_]
    if _falta2 == falta and pronta == (not falta):
        break
    falta, pronta = _falta2, not _falta2
PLANO, RELATORIO = _prosa(pronta, falta)
assert not (ENSAIO and pronta), "o ensaio do topo proposto nunca vale como preparacao pronta"
PRONTA = {"contrato": "PREPARACAO_v411_PRONTA", "agente": "claude-construtor-v411", "quando": AGORA.strftime("%Y-%m-%d %H:%M:%S"), **DL.MARCA_ENSAIO, "pronta": pronta, "falta": falta, "portoes": PORTOES,
          "candidato_sha16": _cand16, "candidato_sha256": CM.get("sha256"), "candidato_bytes": CM.get("bytes"), "rotulo_do_artefato": DL.ROTULO_DO_ARTEFATO, "origem_sha16": CM.get("base_v410_sha16"), "escada": CM.get("escada"),
          "n_bandeiras_novas": FJ.get("n_flags"), "n_modulos_novos": (CM.get("kernel") or {}).get("modulos_novos"),
          "ordem_do_operador": {"arquivo": ORDEM["nome"], "sha16_lido_do_arquivo": ORDEM16, "papel": ORDEM["papel"], "quando": DL._quando_da_fala(ORDEM["nome"])},
          "topo": {"ratificado": TOPO_OK, "arquivo": DL.TOPO_RATIFICADO_ARQ if os.path.isfile(DL.TOPO_RATIFICADO_ARQ) else None, "sha16": h16(DL.TOPO_RATIFICADO_ARQ), "no_manifesto": _topo_cm},
          "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v411.json", "sha16": h16(H("kernel/KERNEL_RECIBO_v411.json")), "rc": KR.get("rc")},
          "esperados_sha16": h16(S("ESPERADOS_v411.json")), "p00": {"veredito": PC.get("veredito"), "passaram": PC.get("n_ok"), "n": PC.get("n_checagens"), "pendentes": [p_.get("checagem") for p_ in (PC.get("pendentes") or [])], "sha16": h16(S("PRECONDICOES_v411.json"))},
          "ensaio_a_seco": {"veredito": EN.get("veredito"), "sha16_do_candidato": EN.get("sha16"), "json_sha16": h16(S("ensaio_a_seco_v411.json"))},
          "previoo_do_gerador": {"ok": PV.get("ok"), "sha16": h16(H("PREVOO_GERADOR_v411.json"))}, "h0dn": H0DN_RES,
          "erratas": [dict(e_) for e_ in DL.ERRATAS_V411], "tabela_secao7": [dict(r_) for r_ in DL.TABELA_SECAO7], "decisoes": dict(DL.DECISOES_V411),
          "excecao_p18": {"funcao": "_v411_p18_sem_cabeca", "controles": _excecao, "g1": "o portao de textos da G1 nao tem a R1: a excecao fica so' na cadeia (NOTA do handoff)"},
          "contratos_de_registro_fora_da_escada": list(DL.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA), "contagem_de_arquivos": CONTAGEM, "copias_do_kernel_fora_de_work": COPIAS,
          "veto_kimi": {"pasta_vedada": DL.H0DN_PASTA_VEDADA_V410, "p00": PORTOES["veto_kimi"]},
          "orquestrador": {"sem_S7_e_sem_S10_medido_no_laco": SEM_S7_S10, "fim_da_cadeia": "HANDOFF"},
          "comandos": ({} if ENSAIO else {"instalar": "python -B -X utf8 instalar_v411.py", "rito": "sh rito_v411.sh", "cadeia": "CHAIN_DE=<rotulo> CHAIN_ATE=<rotulo> sh pos_rito/chain_pos_rito_v411.sh (o orquestrador pos_treino_v411 os chama)",
                                    "reverter": "python -B -X utf8 reverter_v411.py (so' por decisao da gerencia)", "cwd": HERE}),
          "hashes": {(os.path.relpath(p_, DL.SAIDA) if p_.startswith(DL.SAIDA) else p_): {"sha16": h16(p_), "bytes": sz(p_)} for p_ in HASH_ARQS if os.path.isfile(p_)},
          "nao_revisado_por_terceiro": NAO_REVISADO, "revisao_de_terceiro": ({k_: _REV.get(k_) for k_ in ("aprovada", "rodada", "n_alto", "n_medio", "n_baixo", "candidato_sha16", "revisor", "quando")} if _REV else None),
          "avisos": AVISOS, "violacoes_da_guarda_da_prosa": [list(v_) for v_ in _viol[:8]], "rota_no_mapa": ROTA, "desenho_sha16": DL.DESENHO_SHA16}


def grava(p_, b_):
    if os.path.exists(p_):
        raw_ = open(p_, "rb").read()
        if raw_ == b_:
            return
        bk_ = p_ + ".bak_" + ST; open(bk_, "wb").write(raw_); assert open(bk_, "rb").read() == raw_
    tmp_ = p_ + ".tmp"; open(tmp_, "wb").write(b_); assert os.path.getsize(tmp_) == len(b_); os.replace(tmp_, p_)


if SECO:
    print("gerar_relatorio --seco: PLANO %d B, RELATORIO %d B, PRONTA %d B | a guarda (frases + P18) sobre a prosa: %s | portoes ok %d/%d; falta: %s" % (len(PLANO.encode("utf-8")), len(RELATORIO.encode("utf-8")), len(json.dumps(PRONTA, ensure_ascii=False).encode("utf-8")),
          "LIMPA" if not _viol else _viol[:6], sum(1 for v_ in PORTOES.values() if v_), len(PORTOES), ", ".join(falta)))
    if "--imprimir" in sys.argv:
        print(PLANO); print("=" * 100); print(RELATORIO)
    sys.exit(0 if not _viol else 1)
grava(DL.saida("PLANO_v411.md"), PLANO.encode("utf-8")); grava(DL.saida("RELATORIO_PREPARACAO_v411.md"), RELATORIO.encode("utf-8"))
PRONTA["hashes"]["PLANO_v411.md"] = {"sha16": h16(DL.saida("PLANO_v411.md")), "bytes": sz(DL.saida("PLANO_v411.md"))}
PRONTA["hashes"]["RELATORIO_PREPARACAO_v411.md"] = {"sha16": h16(DL.saida("RELATORIO_PREPARACAO_v411.md")), "bytes": sz(DL.saida("RELATORIO_PREPARACAO_v411.md"))}
grava(DL.saida("PREPARACAO_v411_PRONTA.json"), json.dumps(PRONTA, ensure_ascii=False, indent=1).encode("utf-8"))
print("pronta =", pronta, "| falta:", falta)
print(DL.ROTULO_DO_ARTEFATO, _cand16, "| kernel recibo", PRONTA["kernel_recibo"]["sha16"], "| ESPERADOS", PRONTA["esperados_sha16"], "| p00", PRONTA["p00"]["sha16"], "| guarda da prosa:", "LIMPA" if not _viol else _viol[:3])
print(DL.saida("PREPARACAO_v411_PRONTA.json"))
sys.exit(0)
