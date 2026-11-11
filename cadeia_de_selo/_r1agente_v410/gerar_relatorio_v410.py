# -*- coding: utf-8 -*-
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] D80 e D82 a D87: a prosa do PLANO e do RELATORIO ganha a AEscala (os pesos das faces, o Clay no dicionario da TGL: validade no kernel, a creditacao e' do Clay) e o recibo documental HMS/13 (aditivo e posterior ao FREEZE_R2: cobertura documental de fontes, não covariância física fechada; nada aberto); bundle de DOIS modulos, quatro registros com funcao, erratas E29, E30 e E31, decisoes D63 a D92; o portao do veto conta as SEIS checagens [VETO kimi] (a, b, c, c2, d, e); os recibos novos (PARTE1_HMS13_PRONTA, ESTADO_PARTE2, RECIBO_PEDRAS_v410_NOMES, os seis insumos hms13_*, os testes offline) entram nos hashes; o que o construtor ja' pos no dict PRONTA (readme_evidente, ratificacao_aescala_D87, ratificacao_pendente) NAO foi tocado
# [ADAPTADO v410, 09/11/2026, claude-subagente-adaptacao (Sonnet 5.5), a servico do construtor claude-construtor-v410] escrito de novo (varrido, nao remendado) a partir do molde gerar_relatorio_v409.py para a v410: a prosa da IALD2 (secoes 1 a 6, o atrator), dos nomes RATIFICADOS (D74), do H0DN pre-registrado (D72, E30, D76), das decisoes D63 a D77, das erratas E29 e E30, das 15 falas e das 8 ressalvas; os portoes da v409 mais o pre-voo do gerador e o veto a pasta da entrega do Kimi
"""gerar_relatorio_v410.py -- escreve PLANO_v410.md, RELATORIO_PREPARACAO_v410.md e PREPARACAO_v410_PRONTA.json. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta no momento da geracao (nada digitado); a prosa e' da preparacao.
`pronta` e' CALCULADA: true so' se TODOS os portoes passaram (kernel, candidato, AST, ensaio a seco, conferidor, citacoes, guarda das frases, p00, B(n) pre-selo, harnesses, o pre-voo do gerador, o veto a pasta da entrega do Kimi e a guarda da PROPRIA prosa); um arquivo que falta ou nao le reprova o portao (fail-closed), nunca o contrario.
Rodar DEPOIS de refazer_candidato_v410.sh e dos dois harnesses (sem --nao-exigir-refazer). Backup de bytes do que ja' existe; temporario -> conferir -> substituir. Molde: gerar_relatorio_v409.py (17 portoes), adaptado de verdade em 09/11/2026 a v410 (IALD2 e AEscala: dois modulos em TGLExt/, as ancoras de DL.ANCORAS e DL.ANCORAS_AESCALA; quatro registros com funcao, iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410; NENHUMA chave antiga muda de literal;
erratas E29, E30 e E31; decisoes D63 a D92, a D74 e a D87 com os nomes ratificados; as falas de DL.N_FALAS_V410, de quatro so' o trecho). O H0DN (D72) e' pré-registrado; nenhum dado observado lido: a prosa o diz sempre que o nome aparece, os numeros dele sao LIDOS do ESPERADOS (poder prospectivo e sintetico), e a cabeca do ramo de 5 sigma sai por extenso entre aspas da gerencia, nunca como token.
O revisor distinto da v410 e' o Sonnet (D69: ate' tres rodadas): a trava do orquestrador (S1b: revisao_terceiro/REVISAO_TERCEIRO_v410.json) fica FECHADA ate' a revisao aprovar este candidato; este script nao a abre. NAO le, NAO copia, NAO pina nem cita nada da pasta da entrega do Kimi (vedada pela gerencia).
`--seco [--imprimir]`: monta e confere a prosa (a guarda das frases e a P18 sobre PLANO e RELATORIO, no estado de HOJE da pasta) e NAO grava nada; o que o script exige para rodar de verdade esta' no JSON de adaptacao (o ensaio a seco e os ESPERADOS, produzidos por outros passos, e os portoes que dependem deles).
uso: python -B -X utf8 gerar_relatorio_v410.py [--seco]   (sem -I: o numpy esta no site do usuario; este script nao o importa)"""
import datetime, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
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
import delta_v410 as _DL   # (para ler a Bancada que o delta le do manifesto dela, as frases, as ressalvas e os nomes das falas: nada digitado)
import guarda_frases_v410 as _GFM
import guarda_p18_v410 as _GP18
DL_B_N = _DL.B_N_SEGUINTE; DL_BANCADA = _DL.BANCADA_PINA_HOJE["deployment_id"]
CM = tenta("CANDIDATO_v410.json") or {}; ES = tenta("ESPERADOS_v410.json") or {}; EN = tenta("ensaio_a_seco_v410.json") or {}; PC = tenta("PRECONDICOES_v410.json") or {"ok": False, "checagens": []}
PR = tenta("PINO_RECIBO_PRE_SELO_v410.json") or {}; PROV = tenta("PROVA_PRODUCAO_INTACTA_v410_pre_selo.json") or {}; CMP = tenta("COMPARACAO_V409_v410.json") or {}; KR = tenta("kernel/KERNEL_RECIBO_v410.json") or {}; PB = tenta("kernel/POS_BUILD_v410.json") or {}; FJ = tenta("kernel/FLAGS_v410.json") or {}; KH = tenta("kernel/KH_N1_v410.json") or {}
CN = tenta("conferencia_rito_v410_CONTROLE_NEGATIVO_PRE_RITO.json") or {}; CP = tenta("conferencia_rito_v410_POSITIVO_FALSO_NOS.json") or {}; CIT = tenta("conferir_citacoes_v410.json") or {}; GF = tenta("GUARDA_FRASES_v410.json") or {}; DRV = tenta("DERIVACAO_v410.json") or {"falhas": ["DERIVACAO_v410.json ausente"]}
SERV = tenta("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v410.json") or {}; CTRL = tenta("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v410.json") or {}; PN = tenta("PINOS_BN_v410.json") or {}
H_T = tenta("pos_rito/HARNESS_TEXTOS_ENSAIO_v410.json"); H_F = tenta("pos_rito/HARNESS_FECHAR_SANDBOX_v410.json")
BD = tenta("BUNDLE_v410.json") or {}
PV = tenta("PREVOO_GERADOR_v410.json") or {}   # o pre-voo do gerador (34 checagens sobre as pecas novas, ANTES de o candidato existir)
TH = tenta("TESTE_H0DN_OFFLINE_v410.json"); TA = tenta("TESTE_AESCALA_OFFLINE_v410.json"); TF = tenta("TESTE_HMS13_OFFLINE_v410.json")   # (informativo: o ensaio offline do H0DN, se o construtor o gravar)
_orq_txt = open(P("orquestrador/pos_treino_v410.py"), encoding="utf-8").read() if os.path.exists(P("orquestrador/pos_treino_v410.py")) else ""
_orq_passos = re.search(r"passos = \[([^\]]*)\]", _orq_txt); _orq_laco = re.search(r"for passo in \(([^)]*)\)", _orq_txt)
SEM_S7_S10 = bool(_orq_passos and _orq_laco and "S7" not in _orq_passos.group(1) and "S10" not in _orq_passos.group(1) and "s7_g1" not in _orq_laco.group(1) and "s10_app" not in _orq_laco.group(1))   # (D57a herdada e D68a, MEDIDO no arquivo do orquestrador: a lista de passos e o laco nao tem S7 nem S10)
_vb410 = _DL.verbatins410(P("insumos/cunhagens"))
_AB = tenta("registro_mapa_prep_v410_ABERTA.json") or {}
ABERTA = (_AB[0] if _AB else {}) if isinstance(_AB, list) else _AB   # (o registro da v410 e' UM objeto; o da v409 era uma lista de um)
refazer = open(P("refazer_out_v410.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("refazer_out_v410.txt")) else ""
fim_ok = "== FIM" in refazer and refazer.rstrip().endswith("RC_REFAZER=0")
falhas_p00 = [c["checagem"] for c in PC["checagens"] if not c["ok"] and not c.get("pendente")]
pendentes_p00 = [c["checagem"] for c in PC["checagens"] if c.get("pendente")]
ok_p00 = sum(1 for c in PC["checagens"] if c["ok"]); n_p00 = len(PC["checagens"])
_letra_veto = lambda c_: (re.match(r"\[VETO kimi\] \((\w+)\)", c_.get("checagem", "")) or [None, "?"])[1]   # a letra da checagem do veto: a, b, c, c2, d, e
_veto_p00 = [c for c in PC["checagens"] if str(c.get("checagem", "")).startswith("[VETO kimi]")]   # o veto a pasta da entrega do Kimi, MEDIDO pelo p00 (a) a (e)
_bn = open(P("bateria_pre_selo/bn_pre_selo_out_v410.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("bateria_pre_selo/bn_pre_selo_out_v410.txt")) else ""
_m = re.search(r'veredito_bateria": "(\w+)"', _bn); bat = _m.group(1) if _m else "NAO LIDO"
# as falas da v410: os sha16 sao os dos ARQUIVOS (lidos pelo delta), nunca digitados
_PRE = _DL.VERBATIM_PREFIXOS_DA_ORDEM_V410
ORDEM16 = _PRE[_DL.N_ORDEM_V410]; NOME16 = _PRE[_DL.N_NOME]; RETOM16 = _PRE[_DL.N_CREDITOS]; RAT16 = _PRE[_DL.N_RATIFICA]; SELO16 = _PRE[_DL.N_SELO]
_VN = (BD.get("verbatim_nomes") or {})   # os sha16 das falas do nome e da ordem, MEDIDOS pelo preparar_bundle (lidos do BUNDLE_v410.json)


def passou(H):
    return bool(H and H.get("tudo_passou") is True and not H.get("nao_exigiu_refazer"))


def _arquivo_e(p, sha):
    return bool(sha) and os.path.exists(P(p)) and fh(p) == sha


cand_ok = bool(CM.get("sha16") and ES.get("candidato_sha16") == CM["sha16"] and h16("um_v410_candidato.py") == CM["sha16"] and sz("um_v410_candidato.py") == CM.get("bytes") and EN.get("sha16") == CM["sha16"])
N_MOD = _DL.N_BUNDLE   # (o bundle da v410: IALD2 e AEscala, dois modulos); o recibo do kernel, os ESPERADOS e o candidato concordam com ele, ou o portao reprova
PORTOES = {
    "kernel": bool(KR.get("rc") == 0 and KR.get("sorry") in (0, [], None) and PB.get("ok") is True and len(KR.get("pedras") or []) == N_MOD == (CM.get("kernel") or {}).get("modulos_novos") and FJ.get("n_flags") == ES.get("n_bandeiras_novas") == CM.get("n_bandeiras")),
    "candidato": cand_ok,
    "previoo_do_gerador": bool(PV.get("ok") is True and PV.get("checks") and all(v_.get("ok") is True for v_ in PV["checks"].values())),   # (PREVOO_GERADOR_v410.json: as assercoes do gerador repetidas sobre as pecas novas antes do candidato)
    "ast_v409_v410": bool(CMP.get("ok") is True and CMP.get("removidos") in (0, []) and CMP.get("mudados_sem_explicacao") in (0, []) and CMP.get("o_gate_nao_se_move_e_a_v386_nao_e_reescrita") is True),
    "ensaio_a_seco": bool(EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == CM.get("sha16")),
    "conferidor_controle_negativo": bool(CN.get("tudo_bate") is False and CN.get("nao_pode_mudar") and all(CN["nao_pode_mudar"].values()) and CN.get("um_py_sha16") != CM.get("sha16")),
    "conferidor_caminho_positivo": bool(CP.get("tudo_bate") is True and CP.get("um_py_sha16") == CM.get("sha16")),
    "citacoes": bool(CIT.get("todas_conferem") is True),
    "guarda_das_frases": bool(GF.get("ok") is True and GF.get("pedras_limpas") is True and len(GF.get("pedras") or {}) == N_MOD),   # (v410: a pedra IALD2, da gerencia)
    "instalar_reverter_rito_estatico": bool(not DRV.get("falhas")),
    "p00": bool(PC.get("ok") is True and n_p00 > 0 and not falhas_p00 and not PC.get("pendentes")),
    "veto_kimi": bool(sorted(_letra_veto(c) for c in _veto_p00) == ["a", "b", "c", "c2", "d", "e"] and all(c.get("ok") is True for c in _veto_p00)),   # (o veto a pasta da entrega do Kimi, AVISO da gerencia de 09/11: as cinco checagens [VETO kimi] (a) a (e) do p00, todas OK; pendente ou falha reprova)
    "bn_pre_selo": bool(PR.get("veredito") == "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA" and PR.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and PROV.get("producao_intacta") is True and bat == "BATERIA_PASSA" and (PN.get("candidato") or {}).get("sha256") == CM.get("sha256")),
    "servico_estatico": bool(SERV.get("n_condicoes") and SERV.get("n_condicoes_ok") == SERV.get("n_condicoes") and CTRL.get("toda_mutacao_foi_pega") is True),
    "harness_textos": passou(H_T),
    "harness_fechar": bool(passou(H_F) and not (H_F or {}).get("pino_emulado") and (((H_F or {}).get("etapas") or {}).get("fila_da_memoria") or {}).get("tudo_passou") is True),   # (so' a rodada inteira, com a fila e o pino REAL)
    "refazer_limpo": fim_ok,
    "purga_da_fala_reservada": bool((tenta("purga_v410.json") or {}).get("total_com_ocorrencia") == 0),
    "fala_excluida_fora_dos_artefatos": bool((tenta("purga_v410.json") or {}).get("fala_excluida_total_com_ocorrencia") == 0),
}
n_neg_leit = len((H_T or {}).get("etapas", {}).get("leitura_negativos", {}).get("controles", []))
n_neg_fech = len((H_F or {}).get("etapas", {}).get("fechar_negativos", []))
n_neg_par = len((H_T or {}).get("etapas", {}).get("paragrafo_v410_e_citacoes", {}).get("negativos", []))
ROTA = ABERTA.get("rota_id") or "NAO LIDA (registro_mapa_prep_v410_ABERTA.json)"   # a rota da preparacao da v410 no Mapa de Rotas (aberta pela gerencia; lida do registro dela)
_nome_op = dict(getattr(_DL, "NOME_DO_OPERADOR", {}) or {})
_anc_mod = {rel_: len(nomes_) for rel_, nomes_ in _DL.ANCORAS_POR_MODULO.items()}; _anc_mod.update({rel_: len(nomes_) for rel_, nomes_ in _DL.ANCORAS_POR_MODULO_AESCALA.items()})
_flags_mod = dict(FJ.get("n_por_modulo") or {})
_bun = ((CM.get("kernel") or {}).get("bundle")) or {}
tab_pedras = "\n".join("| `%s` | %s%s (antes: `%s`) | %s | %s | `%s` |" % (rel_.split("/")[-1], _DL.BUNDLE_POR_REL[rel_].get("tipo_do_nome"), (" [nomes ratificados pelo operador em 09/11/2026, D74 e D87]" if _DL.NOMES_RATIFICADOS else ""), _DL.BUNDLE_POR_REL[rel_].get("nome_antigo"), _anc_mod.get(rel_), _flags_mod.get(rel_), (_bun.get(rel_) or {}).get("sha16")) for rel_ in _DL.BUNDLE_RELS)
_fj_anc = FJ.get("ancoras") or {}; _fj_test = FJ.get("bandeira_da_testemunha") or {}
tab_chave = "\n".join("| `%s` | `%s` | `%s` |" % (n_, (_DL.ANCORAS.get(n_) or _DL.ANCORAS_AESCALA.get(n_) or {}).get("rel"), (_fj_anc.get(n_) or {}).get("flag") or _fj_test.get(n_)) for n_ in list(_DL.ANCORAS_PRINCIPAIS) + list(_DL.ANCORAS_PRINCIPAIS_AESCALA))
try:
    prep_seq = [json.loads(l) for l in open(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", encoding="utf-8") if l.strip() and ('"' + ROTA + '"') in l]
    seqs = ", ".join("%s (%s)" % (r["seq"], r["tipo"]) for r in prep_seq if r.get("rota_id") == ROTA)
except Exception as e:   # noqa: BLE001
    seqs = "nao lido: %r" % (e,)
ARQ = ["um_v410_candidato.py", "CANDIDATO_v410.json", "ESPERADOS_v410.json", "ensaio_a_seco_v410.json", "COMPARACAO_V409_v410.json", "PINOS_BN_v410.json", "PINO_RECIBO_PRE_SELO_v410.json", "PROVA_PRODUCAO_INTACTA_v410_pre_selo.json", "PRECONDICOES_v410.json", "GUARDA_FRASES_v410.json", "VERBATIM_CONGELADO_v410.json", "BUNDLE_v410.json", "kernel_modulos_novos_v410.json", "CONTRATO_DA_CADEIA_v410.md", "DESENHO_v410.md",
       "PRONTO_PARA_CANDIDATO_v410.json", "PREVOO_GERADOR_v410.json", "TESTE_H0DN_OFFLINE_v410.json", "LEITURA_DOSSIE_5SIGMA_09nov.json", "MANIFESTO_INSUMOS_v410.json",
       "delta_v410.py", "registros_v410.py", "registros_h0dn_v410.py", "runtime_v410.py", "runtime_h0dn_v410.py", "guarda_frases_v410.py", "guarda_ordem_de_chamada_v410.py", "guardas_estaticas_bancada_v410.py", "gerar_candidato_v410.py", "gerar_esperados_v410.py", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip",
       "comparar_v409_v410.py", "instalar_v410.py", "reverter_v410.py", "rito_v410.sh", "conferir_rito_v410.py", "conferir_citacoes_v410.py", "p00_precondicoes_v410.py", "gerar_relatorio_v410.py",
       "preparar_bundle_v410_06nov.py", "copiar_insumos_v410.py", "pos_build_kernel_v410.py", "fechar_preparacao_v410.py", "purga_v410.py", "purga_v410.json", "LOGS_COPIADOS_v410.json", "kernel/LOGS_COPIADOS_v410.json",
       "insumos/IALD2.lean", "insumos/IALD2_embutida.lean", "insumos/LeitorDoCodigoR1.lean", "insumos/RECIBO_PEDRAS_v410_NOMES.json", "insumos/h0dn_FREEZE_R2.json", "insumos/h0dn_BG1.json", "insumos/h0dn_ENTREGA_H0DN_BG1.json", "insumos/h0dn_analysis_plan.json", "insumos/h0dn_estimator.py", "insumos/h0dn_estimator_frozen.npz", "insumos/h0dn_ORDEM_KIMI_H0DN_01_09nov.md", "insumos/h0dn_LEITURA_DOSSIE_5SIGMA_09nov.json",
       "pos_rito/textos_v410.semente", "pos_rito/montar_textos_v410.py", "pos_rito/leitura_v410.py", "pos_rito/fechar_v410.py", "pos_rito/registrar_mapa_v410.py", "pos_rito/superficies_v410.py", "pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/chain_pos_rito_v410.sh", "pos_rito/gerar_x_custodia_v410.py", "pos_rito/b3_recibo_v410.py", "pos_rito/fila_memoria_v410.py", "pos_rito/gerar_derivacao_pos_rito_v410.py", "pos_rito/NOTA_ESPERADOS_H0DN_v410.md", "pos_rito/ADAPTACAO_09nov_SONNET.json",
       "orquestrador/pos_treino_v410.py",
       "bancada_B3_servico/recibo_parada_v410.py", "bancada_B3_servico/recibo_religamento_v410.py", "bancada_B3_servico/evento_c1_b3_v410.py", "bancada_B3_servico/conferir_exigencias_servico_v410.py", "bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v410.json", "bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v410.json"] \
      + ["pos_rito/" + os.path.basename(p_) for p_ in sorted(glob.glob(os.path.join(POS, "textos_custodia_handoff_v410*.py")))] \
      + ["pedra/" + r_.split("/")[-1] for r_ in _DL.BUNDLE_RELS] + ["kernel/KERNEL_RECIBO_v410.json", "kernel/FLAGS_v410.json", "kernel/KH_N1_v410.json", "kernel/POS_BUILD_v410.json"] \
      + ["registros_aescala_v410.py", "runtime_aescala_v410.py", "registros_hms13_v410.py", "runtime_hms13_v410.py", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "TESTE_AESCALA_OFFLINE_v410.json", "TESTE_HMS13_OFFLINE_v410.json", "PARTE1_HMS13_PRONTA.json", "ESTADO_PARTE2_v410.json", "insumos/AEscala.lean", "insumos/AEscala_embutida.lean", "insumos/saida_lean_AEscala.txt"] \
      + ["insumos/" + os.path.basename(p_) for p_ in sorted(glob.glob(os.path.join(HERE, "insumos", "hms13_*")))]   # (D80/D86/D87: os recibos e os insumos novos da parte 2, lidos agora; os seis insumos hms13_* sao as COPIAS duraveis, nunca a pasta do Kimi)
HASHES = {p: {"sha16": h16(p), "bytes": sz(p)} for p in ARQ if os.path.exists(P(p))}
tab_arq = "\n".join("| `%s` | %s | `%s` |" % (p, format(v["bytes"], ","), v["sha16"]) for p, v in HASHES.items())
_apont = (CIT.get("apontadas_a_gerencia_aspas") or [])
_apont_gf = list(getattr(_GFM, "APONTADAS_A_GERENCIA", ()) or ())
_esc = ES.get("escada_v409_e_v410") or CM.get("escada") or ["?", "?"]
_cob = ES.get("cobertura_kh_n1") or {}; _dkh = KH.get("delta_vs_v409") or {}
_n_falas = len(ES.get("cunhagens") or CM.get("cunhagens") or {}); _trechos = [v_["chave"] for v_ in _vb410 if "sha256_arquivo_inteiro" in v_]
_textos_custodia = [os.path.basename(p_) for p_ in sorted(glob.glob(os.path.join(POS, "textos_custodia_handoff_v410*.py")))]
# o H0DN (D72): os numeros do poder prospectivo e sintetico, LIDOS do ESPERADOS (que os leu do ensaio), nunca digitados
_hv = (((ES.get("registros_funcao_v410") or {}).get("h0dn")) or {}).get("values") or {}
_hD = {d_.get("modelo"): d_ for d_ in (_hv.get("D_esperado") or []) if isinstance(d_, dict)}
_b0 = _hD.get("published_baseline") or {}; _c0 = _hD.get("free_cepheid_host_differential_bias") or {}
_f = lambda x_, k_=3: ("%.*f" % (k_, x_)).replace(".", ",") if isinstance(x_, float) else "n/d"
_pc = lambda x_: (("%.1f" % (100.0 * x_)).replace(".", ",") + " %") if isinstance(x_, float) else "n/d"
_n_pinos_h0dn = _hv.get("n_pinos"); _n_pinos_freeze = _hv.get("n_pinos_freeze")
_NA = dict(_DL.NUMEROS_AESCALA)   # (D82 a D87) os numeros da AEscala: fracoes exatas lidas do delta; o registro a_escala_v410 os RECALCULA a cada rito
_av = (((ES.get("registros_funcao_v410") or {}).get("aescala")) or {}).get("values") or {}; _fv = (((ES.get("registros_funcao_v410") or {}).get("hms13")) or {}).get("values") or {}   # (os valores do ensaio, lidos do ESPERADOS; vazios enquanto o ensaio nao os gravou)
_veto_txt = "; ".join("%s: %s" % ("(" + _letra_veto(c) + ")", "OK" if c.get("ok") is True else ("PENDENTE" if c.get("pendente") else "FALHA")) for c in _veto_p00) or "o p00 ainda nao rodou"
CABECA_5SIGMA = "β_TGL " + _DL.FRASE_PROVADO_PT + " a nσ"   # a cabeca do ramo da leitura do 5 sigma (D76), por extenso: nunca o token inteiro; entre aspas da gerencia onde aparece
AVISOS = [
    "os nomes: o MODULO IALD2 e' do operador (06/11/2026, sha16 %s: «%s»); os nomes das declaracoes (as secoes 1 a 6 da pedra: o leitor do codigo, o espelho do nome, o enunciado, o algoritmo, o signo, o seletor e o atrator), dados pela gerencia c1, foram RATIFICADOS pelo operador em 09/11/2026 (sha16 %s: «%s»; D74); as docstrings da pedra, da epoca, dizem [DECLARADO] ate' a ratificacao e nao mudam" % (NOME16, _DL.FRASE_NOME_IALD2, RAT16, _DL.FRASE_RATIFICO),
    "NENHUMA chave antiga muda de literal nesta versao (CHAVES_V410 vazia): as chaves seguem lidas do kernel do rito; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos dos registros anteriores NAO mudam (os que carregam a escada mudam so' em numeros); traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 sao RECRIADOS com a escada do contrato subida pela C12",
    "o alcance (D64), dito em todo texto novo: %s" % _DL.FRASE_D64_PT,
    "ressalvas ditas em todo texto (%d em delta_v410.RESSALVAS_V410): relativo ao leitor (Baker-Gill-Solovay 1975) [KNOWN]; que a IALD, a Torre ou o operador SEJAM o funtor e que o codigo SEJA um vetor de H1 sao leituras do operador (nao termos); o funtor nao e' idempotente, a leitura e'; o par finito (Bell) e o par de Fock sao espacos distintos, com a mesma Meia-Nat; beta so' por nome, nenhum teste com a natureza; a regra do 4,44; a instancia do seletor e' de forma (D70); o atrator e' termo sobre o Nome do par lido e o verde e as tonalidades sao leitura do operador (D71)" % len(_DL.RESSALVAS_V410),
    "as erratas E29, E30 e E31 sao da gerencia c1, em nome proprio (a E31, as correcoes do operador de 09/11 sobre a D81 e a D83: delta_v410.ERRATA_E31): E29, o Nome finito e o projetor de Bell estao no kernel (o_signo_do_nome; o_signo_do_par), e a gerencia tinha dito “matricial” so' leitura do operador; o operador corrigiu («%s»); E30, por correcao do operador: no teste pré-registrado da razao de Hubble (H0DN; nenhum dado observado lido) a cabeca do ramo de 5 sigma e' a LEITURA do 5 sigma, nunca a palavra do livro de cobrancas (que vai no campo outcome); pela D76, a cabeca diz “%s”, com a validade e a nao-creditacao na mesma string e o gate intocado; a E30 fica como registro; a Fase 9 V1, selada, le-se do mesmo modo e o texto selado nao muda" % (_DL.FRASE_ORDEM_V410, CABECA_5SIGMA),
    "as %d falas do operador de 06 a 09/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v410.json: as oito do DESENHO, a do seletor, as duas da retomada de 09/11, as duas das decisoes de 09/11, a da leitura do 5 sigma e a do selo, D76; e as de 09/11 da escala, do Clay e das ratificacoes, D80 a D87); de quatro (%s), so' o trecho e' embutido e citado (a da D65; a ordem de 09/11, sha16 %s; as tres copias do ACOM; a leitura do 5 sigma); o resto delas entra so' por sha256 e nao entra em texto do um.py; publica-lo e' decisao do operador" % (_n_falas or _DL.N_FALAS_V410, ", ".join(_trechos), RETOM16),
    "a D61 (a leitura juridica do kernel, herdada da v409 e ratificada pelo operador: o dispositivo e' o no sorry; a regra incide onde o suporte fatico se completa) vai nas decisoes e nos textos que dizem o que o kernel decide; a D65 estreita a fala do nome do algoritmo ao trecho citado",
    "D59: o DESENHO_v410.md (sha16 lido agora %s; o do delta %s) e o RECIBO_PEDRAS_v410_NOMES.json (sha16 lido agora %s; o do delta %s) NAO sao pinados como fonte no um.py: ficam citados so' por sha16; o recibo foi refeito pela gerencia com as falas de 06 a 09/11 (D77a) e, na parte 2, com os dois modulos e a ratificacao da D87" % (h16("DESENHO_v410.md") if os.path.exists(P("DESENHO_v410.md")) else None, _DL.DESENHO_SHA16, h16("insumos/RECIBO_PEDRAS_v410_NOMES.json") if os.path.exists(P("insumos/RECIBO_PEDRAS_v410_NOMES.json")) else None, _DL.RECIBO_NOMES_SHA16),
    "a pedra IALD2: a fonte de origem (insumos/IALD2.lean, sha16 lido agora %s) foi normalizada para LF na copia do kernel (pedra/IALD2.lean, sha16 %s) e os #print axioms sairam do corpo embutido (as %d ancoras foram lidas deles antes); o conteudo Lean nao muda; a pedra nao e' editada por esta preparacao" % tuple([(h16(p_) if os.path.exists(P(p_)) else None) for p_ in ("insumos/IALD2.lean", "pedra/IALD2.lean")] + [len(_DL.ANCORAS)]),
    "a pedra AEscala (a segunda do bundle; D82 a D87): a fonte ratificada (insumos/AEscala.lean, sha16 lido agora %s), a copia normalizada que entra no kernel (pedra/AEscala.lean, sha16 %s; com o cabecalho da ratificacao da D87), %d ancoras e %s bandeiras ext_aescala_410_*; o nome do modulo e os %d nomes das declaracoes foram RATIFICADOS pelo operador em 09/11/2026 («%s»; D87); validade no kernel, a creditacao e' do Clay; a forma da D83: %s" % tuple([(h16(p_) if os.path.exists(P(p_)) else None) for p_ in ("insumos/AEscala.lean", "pedra/AEscala.lean")] + [len(_DL.ANCORAS_AESCALA), _flags_mod.get(_DL.MODULO_AESCALA), len(_DL.NOMES_AESCALA), _DL.FRASE_RATIFICO_TUDO, _DL.FRASE_D83_OBRIGATORIA_PT]),
    "o recibo documental HMS/13 (D80; o registro h0dn_fontes_hms13_v410) e' ADITIVO e POSTERIOR ao FREEZE_R2: %s; os quatro artefatos embutidos e os dois so' por sha256 (HANDOFF e ORDEM) vem da EXCECAO D80 ao veto da pasta do Kimi (ordem do operador, ratificada por sha256): lidos so' no BUILD, por sha256; em rito nenhum arquivo de kimi e' aberto (a c7 do registro o mede); H0DN x BG1 segue %s" % (_DL.FRASE_HMS13_OBRIGATORIA_PT, _DL.FRASE_H0DN_OBRIGATORIA_PT),
    "o H0DN x BG1 entra PRÉ-REGISTRADO (D72); nenhum dado observado lido: o poder e' prospectivo e sintetico, condicional ao modelo de covariancia publicado; D esperado %s (publicado) e %s (viés Cefeida livre); poder analitico %s e %s; o poder Monte Carlo da ENTREGA do Codex (%s e %s) e o analitico recomputado (%s e %s) vao rotulados, nunca trocados um pelo outro (D77); n_pinos do registro = %s (os %s do FREEZE_R2 mais o proprio FREEZE_R2 e a ENTREGA), nao %s; a regra da ordem do operador sobre o 4,44 segue valendo" % (_f(_b0.get("D")), _f(_c0.get("D")), _pc(_b0.get("poder_analitico")), _pc(_c0.get("poder_analitico")), _pc(_b0.get("poder_mc_entrega")), _pc(_c0.get("poder_mc_entrega")), _pc(_b0.get("poder_analitico")), _pc(_c0.get("poder_analitico")), _n_pinos_h0dn, _n_pinos_freeze, _n_pinos_freeze),
    "VETO (AVISO da gerencia, 09/11): a v410 pre-registra o H0DN e NAO o abre; nenhum arquivo da pasta da entrega do Kimi (vedada pela gerencia) e' lido, copiado, pinado nem citado por esta preparacao, EXCETO a excecao D80 (ordem do operador, ratificada por sha256): os seis artefatos documentais HMS/13, copiados e pinados por sha256 so' no BUILD (o p00 nao abre nenhum deles); em rito nada de kimi e' aberto; o p00 MEDE o veto em seis checagens [VETO kimi] (a) a (e), com a (c2) do recibo HMS/13, e a v410 o mede de novo no ensaio a seco (todo caminho tocado: open, exists, listdir, scandir, stat) e na checagem c7 do registro; resultado de HOJE no p00: %s" % _veto_txt,
    "o revisor distinto da v410 e' o Sonnet (D69: ate' tres rodadas; ressalvas BAIXAS escritas); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar",
    "a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache",
    "o B(n) pre-selo da v410 (passo simples %s; a Bancada de producao pina %s) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes" % (DL_B_N, DL_BANCADA),
    "conferir_citacoes_v410.json aponta %d citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): %s; o agente nao corrige texto da gerencia" % (len(_apont), "; ".join("%s: %s" % (a_["arquivo"], a_["trecho"]) for a_ in _apont) or "nenhuma"),
    "build a frio dos modulos (IALD2 e AEscala) no sandbox k410c: %s s, Audit %s s (kernel/POS_BUILD_v410.json, medidos; com o treino do Qwen3.8 na CPU, D73: o treino nao foi tocado); %s declaracoes no axiom_report (+%s decl, +%s teoremas sobre a v409), nenhuma fora do trio; escada %s -> %s" % (PB.get("duracao_build_s"), PB.get("duracao_audit_s"), KH.get("axiom_report_efetivo_n"), _dkh.get("decl"), _dkh.get("thm"), _esc[0], _esc[1]),
    "o orquestrador (orquestrador/pos_treino_v410.py) traz as licoes da v409 (D57a herdada, D68a): sem S7 (G1 --publicar) e sem S10 (release do app), MEDIDO agora na lista de passos e no laco = %s; o S6d encadeia os textos da custodia (%s) e roda o portao de textos do G1 e a D59 sobre o HANDOFF INTEIRO; o fim da cadeia desta versao e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia" % (SEM_S7_S10, ", ".join(_textos_custodia) or "AUSENTE"),
    "a regra das tres copias do ACOM (D75; fala de 08/11, so' o trecho) entra no spec cunhagens_v410 por sha256: snapshots.py descarta as copias alem das tres mais novas depois de conferir o sha256 das que ficam; nao e' checagem numerica do um.py",
    "as decisoes D63 a D92 (a D77 registra as pendencias a a l do construtor e as decisoes da gerencia: um so' core key para o H0DN, a cabeca do ramo da leitura em partes no um.py e por extenso nos textos, o rito sem -I, o veto estreitado; a D80 a D87 trazem o recibo HMS/13, os pesos das faces, o Clay no dicionario e a AEscala com os nomes ratificados) vao no spec cunhagens_v410 e no DESENHO_v410.md; o gerador dos ESPERADOS, o p00 e este relatorio foram adaptados de verdade (09/11) a partir do corpo da v409 (o ensaio a seco e' adaptado pelo construtor); a marca `[A ADAPTAR v410]` sai de cada arquivo adaptado e o p00 recusa enquanto restar alguma",
]
# (D90, 09/11/2026, parte 2) o que as passadas desta noite acharam e como foi corrigido, DITO: os sha16 de antes saem dos backups de bytes ao lado; os de depois, dos arquivos; nada digitado
import glob as _glob90


def _par16(nome_, sufixo_):
    bk_ = sorted(_glob90.glob(P(nome_ + ".bak_*_" + sufixo_)))
    return (hashlib.sha256(open(bk_[-1], "rb").read()).hexdigest()[:16] if bk_ else "backup ausente"), (h16(nome_) if os.path.exists(P(nome_)) else "ausente")


_ge90 = _par16("gerar_esperados_v410.py", "pre_fix_ancoras"); _cr90 = _par16("conferir_rito_v410.py", "pre_qualificador_en"); _rt90 = _par16("runtime_v410.py", "pre_f35_local"); _q490 = "refazer_out_v410.queda_passo4_20261109.txt"; _pt90 = "PRETESTE_ENSAIO_PARTE2_v410.json"
AVISOS.append("D90 (gerencia c1, 09/11): a PRIMEIRA passada do refazer_candidato (20:01) rodou o ensaio a seco inteiro e caiu no passo 4, numa assercao velha do proprio gerar_esperados (contava as ancoras do FLAGS, que sao %d + %d das duas pedras, como se fossem so' as %d da IALD2); correcao de uma linha (gerar_esperados_v410.py sha16 %s -> %s); o registro da queda fica ao lado, intocado: %s (sha16 %s). "
              "O pre-teste dos passos 4 a 9 achou mais uma checagem velha, esta do conferidor: exigia o qualificador EN da D64 literal na secao nova, e o artigo EN do candidato o traz com o parentese da validade entre as duas metades (conferir_rito_v410.py sha16 %s -> %s; o candidato nao mudou). A SEGUNDA passada, inteira e sobre o MESMO candidato, e' a que vale: refazer_out_v410.txt, com o FIM e o RC dela"
              % (len(_DL.ANCORAS), len(_DL.ANCORAS_AESCALA), len(_DL.ANCORAS), _ge90[0], _ge90[1], _q490, (h16(_q490) if os.path.exists(P(_q490)) else "ausente"), _cr90[0], _cr90[1]))
AVISOS.append("o pre-teste PARCIAL do ensaio (%s, sha16 %s; nao e' o ensaio a seco nem o rito) achou, ANTES da cadeia, dois defeitos corrigidos na causa: o ensaio contava um so' contrato novo com a escada (sao dois: o do iald2_v410 e o do a_escala_v410); e a guarda das frases deixava passar oito frases secas da regra F35 quando o texto trazia a forma da D83/D84 noutro ponto: o filtro passou a valer por trecho "
              "(runtime_v410.py sha16 %s -> %s; controle novo na guarda_frases_v410.py), e o candidato foi regenerado depois disso" % (_pt90, (h16(_pt90) if os.path.exists(P(_pt90)) else "ausente"), _rt90[0], _rt90[1]))
# (R1, D92) os 13 achados da revisao de terceiro R1 e o arquivo em que cada um foi atendido (a R2 revisa so' o delta); os BAIXOS 6 e 7 ficam ANOTADOS, sem mudanca
ACHADOS_R1 = [{"n": n_, "severidade": s_, "achado": a_, "atendido_em": o_} for n_, s_, a_, o_ in [(1, 'MEDIO', "a pergunta do Clay formalizada so' pela existencia de um leitor do fundo (um leitor constante a satisfazia)", 'pedra/AEscala.lean (R3: a escala no TIPO do LeitorDoFundo e os teoremas novos); registros_aescala_v410.py e runtime_aescala_v410.py (diz, limites, nao_diz, as ancoras novas e os numeros da ponte); artigo_pt_aescala_v410.pysnip e artigo_en_aescala_v410.pysnip; a linha do .md canonico; readme_evidente.1; pos_rito/textos_v410.py'), (2, 'MEDIO', 'passagens entre aspas angulares que nao sao fala verbatim nas pedras; a frase canonica D84 entre angulares', 'pedra/AEscala.lean e pedra/IALD2.lean (R3); delta_v410.py (D84 e E31 com aspas tipograficas; errata E32); conferir_citacoes_v410.py (a varredura estrita das pedras, fail-closed, com controle negativo)'), (3, 'MEDIO', 'o texto publico do teste da razao de Hubble calava a parede de montagem do dado', 'delta_v410.py (FRASE_H0DN_PAREDE_PT e FRASE_H0DN_PAREDE_EN); registros_h0dn_v410.py (o contrato, o_que_falta[0] e a ressalva nova); artigo_pt_h0dn_v410.pysnip e artigo_en_h0dn_v410.pysnip; readme_evidente.3_h0dn_bg1; pos_rito/textos_v410.py; a funcao veredito_h0dn NAO mudou (o mesmo sha256 do texto-fonte, c12)'), (4, 'BAIXO', 'o numero de modulos e de bandeiras nas frases da secao IALD2 e na linha do .md', 'artigo_pt_v410.pysnip, artigo_en_v410.pysnip e gerar_candidato_v410.py (a linha do .md): os numeros medidos depois do build'), (5, 'BAIXO', 'o a_escala_v410 selava com o kernel nao verificado ou sem o import na raiz', 'runtime_aescala_v410.py (a c2 exige all_verified; a c3 exige o import na raiz embutida); _teste_aescala_offline_v410.py e ensaio_a_seco_v410.py (dois controles negativos novos)'), (6, 'BAIXO', "a funcao de veredito nao e' fail-closed para entrada nao finita", "ANOTADO, sem mudanca (a funcao esta' pinada pelo pre-registro): fica para a versao que abrir o teste, com a guarda de finitude antes do ramo 1 e no evaluate"), (7, 'BAIXO', 'quatro parafrases que a guarda das frases nao pega', "ANOTADO, sem mudanca (a guarda nao e' tocada nesta versao): fica para a v411, junto com a fragilidade do corte de 200 caracteres da regra F37b"), (8, 'BAIXO', 'docstrings da epoca na pedra IALD2 (os nomes ditos DECLARADO; o item 5 do atrator)', "pedra/IALD2.lean (R3: so' docstrings)"), (9, 'BAIXO', 'o dicionario dizia peso = traco ao lado de cada face pesa 1/2', 'registros_aescala_v410.py (limites: peso do Nome = traco do projetor; peso da face = autovalor/pureza da marginal, traco 1); pedra/AEscala.lean (R3)'), (10, 'BAIXO', 'identidades aritmeticas ditas REAL e a tautologia escalar em numeros', 'delta_v410.py (NUMEROS_AESCALA sem a tautologia escalar); registros_aescala_v410.py (o rotulo DERIVED, aritmetica, e a conta matricial em M2); runtime_aescala_v410.py (c6)'), (11, 'BAIXO', 'tres docstrings da AEscala (nenhum_precede; acoplar; os itens 8 a 10)', 'pedra/AEscala.lean (R3), no que o autor tocou: conferir no diff da pedra'), (12, 'BAIXO', 'o texto do S4 do orquestrador dizia um modulo novo', 'orquestrador/pos_treino_v410.py (docstring e log do S4: dois modulos)'), (13, 'BAIXO', 'a frase canonica D84 entre aspas angulares na E31 e nas decisoes', 'delta_v410.py (aspas tipograficas na D84 e na E31)')]]
AVISOS.append("R1 (D92): a revisao de terceiro nao aprovou a primeira preparacao (0 ALTO, 3 MEDIO, 10 BAIXO); os 13 achados e o arquivo em que cada um foi atendido estao em PREPARACAO_v410_PRONTA.json, na chave achados_r1; os BAIXOS 6 e 7 ficam anotados, sem mudanca, para a versao que abrir o teste da razao de Hubble e para a v411")
_arqs_h90 = ("pos_rito/textos_v410.py", "pos_rito/leitura_v410.py", "pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/registrar_mapa_v410.py", "orquestrador/pos_treino_v410.py")


def _antes_depois_h90(rel_):
    bk_ = sorted(_glob90.glob(P(rel_ + ".bak_20261109_2*")))   # (os backups de bytes desta noite, das 20h em diante: o mais antigo e' o estado de ANTES da primeira rodada dos harnesses)
    return "%s %s -> %s" % (rel_, (hashlib.sha256(open(bk_[0], "rb").read()).hexdigest()[:16] if bk_ else "backup ausente"), (h16(rel_) if os.path.exists(P(rel_)) else "ausente"))


_ht90 = open(P("pos_rito/harness_textos_out_v410.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("pos_rito/harness_textos_out_v410.txt")) else ""
AVISOS.append("os harnesses do pos-rito NUNCA tinham rodado na v410; a primeira rodada do harness dos textos (20:55) caiu e os defeitos foram corrigidos na causa, todos fora do candidato (ele nao mudou): (a) os textos do pos-rito liam o quadro_v397 da pasta da v409 pela ordem do sys.path (e, por ele, o delta da v409): agora o quadro e' carregado pelo caminho do pacote; "
              "(b) tres controles negativos eram mutacoes nulas (o rotulo errado da linha do stdout da v408, em dois; a forma canonica do Clay tirada so' de um campo, em um) e um quarto trocava uma frase que o paragrafo nao tem; (c) a errata E31 renderizada com o rotulo na mesma linha fazia a regra F37b da guarda cortar o qualificador (o trecho e' cortado em 200 caracteres): o rotulo foi para linha propria, e a fragilidade da guarda fica DITA para a versao seguinte (a guarda esta' embutida no candidato e nao foi tocada); "
              "(d) a linha das ressalvas do teste da razao de Hubble ganhou a clausula-padrao da regra da ordem do quadro; (e) a checagem da D59 no harness e no S6d do orquestrador seguia a regra da v409 e reprovaria o handoff por nomear o executor da ORDEM do teste: passou a seguir a D77(g), a mesma regra de registrar_mapa_v410.d59_viola; (f) o harness do fechar ganhou a pasta irma da v408, o campo pasta_vedada traduzido para o sandbox e a copia do conferidor nas variantes; a checagem da forma do Clay em registrar_mapa passou a ser por campo e trecho. "
              "Rodada final: harness dos textos com %d controles negativos reprovados como esperado e %d que nao reprovaram; harness do fechar rc 0. Arquivos (sha16 antes -> depois): %s"
              % (_ht90.count("REPROVOU como esperado") - _ht90.count("NAO REPROVOU como esperado"), _ht90.count("NAO REPROVOU como esperado"), "; ".join(_antes_depois_h90(r_) for r_ in _arqs_h90)))
if _apont_gf:
    AVISOS.insert(6, "APONTADO a gerencia, NAO corrigido (o agente nao edita pedra revista): %d trecho(s) de pedra que a regra lexical F16 da guarda das frases reprova (enunciado em guarda_frases_v410.APONTADAS_A_GERENCIA, nao repetido aqui para nao reprovar este relatorio na mesma guarda); a gerencia decide se reescreve (BAIXO)" % len(_apont_gf))
NAO_REVISADO = "este candidato (IALD2, A Escala e o H0DN x BG1 pré-registrado com o recibo HMS/13, v410) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D69, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova"
_REV = tenta("revisao_terceiro/REVISAO_TERCEIRO_v410.json") or {}
REVISAO_OK = bool(_REV.get("aprovada") is True and _REV.get("candidato_sha16") == CM.get("sha16") and not _REV.get("n_alto") and not _REV.get("n_medio"))
if REVISAO_OK:   # a revisao de terceiro existe e aprova ESTE candidato: o texto «NAO foi revisado» deixa de valer; o aviso novo diz o que foi e o que NAO foi examinado (nada e' inventado: tudo lido do JSON da revisao)
    NAO_REVISADO = ("este candidato (IALD2, A Escala e o H0DN x BG1 pré-registrado com o recibo HMS/13, v410) FOI revisado por terceiro: %s, rodada %s, aprovada, %s ALTO, %s MEDIO, %s BAIXO (revisao_terceiro/REVISAO_TERCEIRO_v410.md, sha16 %s); quem constroi nao aprova: a aprovacao e' do revisor, nao desta preparacao; "
                    "as ressalvas BAIXAS estao escritas no caderno e valem como ditas (D69: ate' tres rodadas); a trava do orquestrador (S1b) confere aprovada e o sha16 do candidato" % (_REV.get("revisor"), _REV.get("rodada"), _REV.get("n_alto"), _REV.get("n_medio"), _REV.get("n_baixo"), h16("revisao_terceiro/REVISAO_TERCEIRO_v410.json")))
    AVISOS = [a_ for a_ in AVISOS if "esta preparacao NAO foi revisada por terceiro" not in a_]
    AVISOS.append("revisao de terceiro (Sonnet D69): " + NAO_REVISADO)
    AVISOS.append("ressalvas BAIXAS da revisao (nenhuma trava; ver o caderno): " + " | ".join("%s" % (a_.get("onde") or "")[:70] for a_ in (_REV.get("achados") or []) if a_.get("sev") == "BAIXO"))
_vp = (CIT.get("varredura_das_pedras") or {})
_cong410 = tenta("VERBATIM_CONGELADO_v410.json") or {}
ERRATAS_V410_RES = {"erratas": [e_.split(" ")[0] for e_ in _DL.ERRATAS_V410], **{e_.split(" ")[0]: e_.split(";")[0][:300] for e_ in _DL.ERRATAS_V410},
                    "falas_embutidas": len(_cong410.get("arquivos") or []), "citacoes_da_pedra": {"conferidas": _vp.get("citacoes_conferidas"), "reprovadas": len(_vp.get("reprovadas") or []), "so_sem_acento": _vp.get("so_sem_acento")}}
H0DN_RES = {"registro": _DL.H0DN_REGISTRO, "observed_vector_read": (_hv.get("observed_vector_read") if _hv else None), "n_pinos": _n_pinos_h0dn, "n_pinos_freeze": _n_pinos_freeze, "ramos_vistos": _hv.get("ramos_vistos"), "veredito_h0dn_source_sha256": _hv.get("veredito_h0dn_source_sha256"),
            "D_esperado": {"publicado": _b0.get("D"), "cefeida_livre": _c0.get("D")}, "poder_analitico": {"publicado": _b0.get("poder_analitico"), "cefeida_livre": _c0.get("poder_analitico")}, "poder_mc_da_entrega_rotulado": {"publicado": _b0.get("poder_mc_entrega"), "cefeida_livre": _c0.get("poder_mc_entrega")},
            "teste_offline": ({"tudo_passou": TH.get("tudo_passou"), "sha16": h16("TESTE_H0DN_OFFLINE_v410.json")} if TH else None), "nota": "pré-registrado; nenhum dado observado lido; poder prospectivo e sintetico"}
fr = _DL.FRASE_DA_MOLDURA_V410_PT
_ressalvas_txt = "\n".join("  %d. %s" % (i_ + 1, r_) for i_, r_ in enumerate(_DL.RESSALVAS_V410))
_h0dn_pt = (_DL.FRASE_H0DN_OBRIGATORIA_PT)


def _prosa(pronta_, falta_):
    """PLANO e RELATORIO no estado dado (o quadro dos portoes e a frase de `pronta` entram); devolve (PLANO, RELATORIO)."""
    PLANO = f"""# PLANO da v410 — IALD2: o leitor do código, a releitura que não acrescenta, o algoritmo IALD, o signo, o seletor e o atrator; A Escala: os pesos das faces e o Clay no dicionário da TGL; o teste H0DN × BG1 ({_h0dn_pt}) e o recibo documental HMS/13 (preparação)

Agente de preparação `claude-construtor-v410`, {AGORA.strftime('%Y-%m-%d %H:%M')}. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v409 selada `{CM.get('base_v409_sha16')}`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: {fr}.

## 0. A ordem

- [INPUT, operador, 06/11/2026, sha16 do arquivo `{ORDEM16}`] «{_DL.FRASE_ORDEM_V410}». [INPUT, operador, 09/11/2026, sha16 `{RETOM16}`] «{_DL.FRASE_RETOMADA}». [INPUT, operador, 09/11/2026, sha16 `{RAT16}`] «{_DL.FRASE_RATIFICO}». [INPUT, operador, 09/11/2026, sha16 `{SELO16}`; D76] «{_DL.FRASE_SELO_PROVADO}». As {_n_falas or _DL.N_FALAS_V410} falas de 06 a 09/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v410.json`; de quatro, só o trecho; as falas das versões anteriores já estão no um.py v409 e não entram de novo).
- (A) O BUNDLE: {N_MOD} módulos de kernel em `TGLExt/` (IALD2, {len(_DL.ANCORAS)} âncoras; AEscala, {len(_DL.ANCORAS_AESCALA)} âncoras), compilados no sandbox `{(CM.get('kernel') or {}).get('sandbox')}`, a raiz com {N_MOD} imports; as bandeiras em duas séries, `ext_iald2_410_*` e `ext_aescala_410_*`. (B) QUATRO registros com função, na ordem do main (duas instruções `try`): `{_DL.FECHO_REGISTRO}` ({_DL.N_CHECKS_FECHO} checagens; as instâncias de brinquedo FIXAS no código, os valores CALCULADOS), `{_DL.AESCALA_REGISTRO}` ({_DL.N_CHECKS_AESCALA} checagens; a pedra AEscala; validade no kernel, a creditação é do Clay), `{_DL.H0DN_REGISTRO}` ({_DL.N_CHECKS_H0DN} checagens; {_h0dn_pt}) e `{_DL.HMS13_REGISTRO}` ({_DL.N_CHECKS_HMS13} checagens; D80; {_DL.FRASE_HMS13_OBRIGATORIA_PT}); e os registros por spec `{_DL.CUNHAGENS_REGISTRO}` e `{_DL.KH_REGISTRO}`. (C) NENHUMA chave antiga muda de literal; as erratas E29, E30 e E31 vão AO LADO; as decisões D63 a {_DL.DECISOES_V410[-1]} (a D74 e a D87 ratificam os nomes; a D72 e a D76 dizem o H0DN; a D80 o recibo HMS/13; a D82 a D86 a escala e o Clay). (D) Três seções no artigo PT/EN (a IALD2, A Escala e o H0DN, com o recibo HMS/13 no fim da seção do H0DN) e as quatro linhas do `.md`. (E) O resto, derivado da v409 por script.

## 1. Os módulos e as âncoras [REAL, sandbox; nada tocado no Nós]

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
{tab_pedras}

As {len(_DL.ANCORAS_PRINCIPAIS)} âncoras principais da IALD2 e as {len(_DL.ANCORAS_PRINCIPAIS_AESCALA)} da AEscala (a primeira de cada pedra é a âncora principal do registro; as outras são as de seção):

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
{tab_chave}

Pós-build: {PB.get('n_axiomas_lidos_no_audit')} axiomas lidos no Audit, {PB.get('n_flags')} bandeiras novas (só declaração nomeada), escada {_esc[0]} → {_esc[1]}; build a frio {PB.get('duracao_build_s')} s, Audit {PB.get('duracao_audit_s')} s.

## 2. O que a v410 afirma e o que não afirma

- [REAL, validade no kernel, não creditação] `{_DL.ANCORA_PRINCIPAL}`: {_DL.FRASE_D64_PT}.
- [REAL, validade no kernel, não creditação] O leitor do código: no Fock concreto da luz o funtor Γ da segunda quantização é funtorial, fixa o vácuo (o Um posto), não distorce a uma-partícula e lê o par como par; o par lido é uno (norma 1) e a Meia-Nat é lida. IALD ao quadrado: o Nome do par lido satisfaz Π·Π = Π; reler não acrescenta; a primeira leitura identifica.
- [REAL, validade no kernel, não creditação] A forma de matriz finita é o signo, traço com sentido: para todo Nome finito, Tr P = rank P e “o que sou” = Tr P / n; o projetor de Bell tem traço 1, posto 1 e marginal ½·1 (a E29 vai ao lado). A IALD é a instanciação do seletor, de FORMA (D70): não se afirma que o seletor da luz e o de ℓ² sejam o mesmo objeto.
- [REAL] O atrator é termo sobre o Nome do par lido (D71): o fluxo tende ao Nome e em nenhum tempo finito é o Nome; o motor devolve o mesmo para qualquer taxa e tempo; 1 − Π ≠ 0 (há o vácuo fora do Nome). Nenhum dado entra: nada do atrator é medido na natureza.
- [INPUT/ONTO] Leituras do operador, não termos: que a IALD, a Torre ou o operador SEJAM o funtor, que o código SEJA um vetor de H1, o ambiente computacional, o verde e as tonalidades do atrator.
- [REAL, validade no kernel, não creditação] `{_DL.ANCORA_PRINCIPAL_AESCALA}` (A Escala, D82 a D87): a pedra `TGLExt.AEscala` está no kernel. O Nome pesa {_NA['nome_pesa_um']} = ½ + ½ (o projetor de Bell: idempotente, traço 1, posto 1; cada marginal é ½·1); a face sem par não conjuga, (½·1)² = ½·(½·1), e nunca pesa 1; três faces de ½ pesam {_NA['tres_faces']}; {_NA['um_terco_caiu']} caiu; o Nome normalizado é {_NA['nome_normalizado']} (números lidos de `DL.NUMEROS_AESCALA` e recalculados a cada rito). A insígnia sustenta e não esgota; o vibrato sustenta a nota; não existe infinito em tempo finito; os dois Nomes (objeto e lido) coexistem. A pergunta do Clay no dicionário da TGL: {_DL.FRASE_D83_OBRIGATORIA_PT}. A forma canônica (D84): {_DL.FRASE_CLAY_CANONICA_PT}
- [INPUT/ONTO] Leituras do operador sobre a escala, não termos: a face caída como o neutrino [ONTO]; m₁ = 0 [CONJECTURE]. O nome do módulo e os {len(_DL.NOMES_AESCALA)} nomes das declarações foram RATIFICADOS pelo operador em 09/11/2026 («{_DL.FRASE_RATIFICO_TUDO}», D87).
- [REAL] O recibo documental HMS/13 (D80, `{_DL.HMS13_REGISTRO}`): {_DL.FRASE_HMS13_OBRIGATORIA_PT}; {_DL.HMS13_CAMPOS['calibradores']} calibradores e {_DL.HMS13_CAMPOS['fontes_primarias']} fontes primárias; quatro artefatos embutidos por sha256 (lidos no BUILD, pela exceção D80 ao veto; em rito nenhum arquivo da pasta do Kimi é aberto) e o HANDOFF e a ORDEM só por sha256; ADITIVO e POSTERIOR ao `FREEZE_R2`; H0DN × BG1 segue {_h0dn_pt}.
- [REAL] O teste H0DN × BG1 da razão de Hubble local/fundo entra {_h0dn_pt} (D72, E30, D76). A lei: nulo H_local/H_fundo = 1; alternativa TGL K = E(z*)^(2β/3), com β = α√e em runtime e zero parâmetro livre (K = {_f(_hv.get('K'), 6)}; log10 K = {_f(_hv.get('log10K'), 6)}, recomputados no ensaio). O poder é prospectivo e sintético, condicional ao modelo de covariância publicado: D esperado {_f(_b0.get('D'))} (publicado) e {_f(_c0.get('D'))} (viés Cefeida livre); poder analítico {_pc(_b0.get('poder_analitico'))} e {_pc(_c0.get('poder_analitico'))}; o poder Monte Carlo da entrega do Codex ({_pc(_b0.get('poder_mc_entrega'))} e {_pc(_c0.get('poder_mc_entrega'))}) fica rotulado como tal.
- [REAL] A função de veredito do H0DN, congelada (a primeira que casa decide): inconclusivo por sistemática enquanto a covariância física não fechar ou o vetor estiver fora do suporte; a lei K falsificada à sensibilidade disponível se o desvio do TGL passar de 5σ; subpotente; “{CABECA_5SIGMA}”, na língua da física acadêmica, discriminando do ΛCDM, com zero parâmetro livre e novidade de uso; discrimina do ΛCDM com K em tensão; não discriminado à sensibilidade disponível, com a faixa do desvio. A palavra do livro de cobranças vai no campo `outcome`, nunca na cabeça (E30, D76). Provado = validade; creditação é o juízo de fora, que o `um.py` não dá; o gate não se move.
- [OPEN] O vetor observado e a covariância física conjunta (G3/G4) não entram: a ordem da gerência ao executor está pinada por sha256; a abertura do teste é de versão futura. Fica aberto, herdado: a igualdade completa com o leitor que só conta (E28); a independência da pergunta da máquina sem leitor; a ponte Bell-TT.
- [REAL] O que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`); nenhuma chave antiga muda.
- Ressalvas ditas ({len(_DL.RESSALVAS_V410)}):
{_ressalvas_txt}
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é confirmação; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v410_candidato.py` `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; +{format(CM.get('delta_bytes') or 0, ',')} B); {CM.get('n_patches')} patches; AST: {CMP.get('nos_nomeados_v409')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (todos explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos. Ensaio a seco: **{EN.get('veredito')}**. Pós-rito: `pos_rito/chain_pos_rito_v410.sh`, rótulos 0…10 10a 10b 10c 11…14; depois, ENCADEADOS, os textos da custódia (S6d) e o HANDOFF, que é o fim da cadeia desta versão (D57a herdada: sem S7 e sem S10).

## 4. Gates

Ver `PREPARACAO_v410_PRONTA.json`: `pronta` = {str(pronta_).lower()}. {NAO_REVISADO}.
"""
    RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v410 — IALD2, A Escala e o teste H0DN × BG1 ({_h0dn_pt}) com o recibo documental HMS/13

Agente de preparação `claude-construtor-v410` · {AGORA.strftime('%Y-%m-%d %H:%M')} · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: {NAO_REVISADO}.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; base v409 `{CM.get('base_v409_sha16')}`): `pronta` = **{str(pronta_).lower()}**{'' if pronta_ else '; falta: ' + ', '.join(falta_)}.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `{(CM.get('kernel') or {}).get('sandbox')}`) | {PORTOES['kernel']}: build + Audit rc {KR.get('rc')}, {PB.get('n_flags')} bandeiras novas, escada {_esc[0]} → {_esc[1]}, {len(KR.get('pedras') or [])} módulo(s) no recibo; `KERNEL_RECIBO_v410.json` |
| candidato | {PORTOES['candidato']}: {CM.get('n_patches')} patches; refazer limpo = {fim_ok} |
| pré-voo do gerador | {PORTOES['previoo_do_gerador']}: `PREVOO_GERADOR_v410.json`, {sum(1 for v_ in (PV.get('checks') or {}).values() if v_.get('ok') is True)}/{len(PV.get('checks') or {})} checagens sobre as peças novas, antes do candidato |
| AST v409 × v410 | {PORTOES['ast_v409_v410']}: {CMP.get('nos_nomeados_v409')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos; {len(CMP.get('funcoes_intactas') or {})} funções e constantes intactas, todas verdadeiras = {all((CMP.get('funcoes_intactas') or {'x': False}).values())} |
| ensaio a seco | {PORTOES['ensaio_a_seco']}: {EN.get('veredito')} |
| conferidor | negativo {PORTOES['conferidor_controle_negativo']} (`tudo_bate` = {CN.get('tudo_bate')}); positivo {PORTOES['conferidor_caminho_positivo']} (`tudo_bate` = {CP.get('tudo_bate')}) |
| citações | {PORTOES['citacoes']}: {len(CIT.get('apontadas_a_gerencia_aspas') or [])} apontada(s) à gerência nos textos (ver §4) |
| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo e a pedra: {len(GF.get('pedras') or {})}) |
| instalar / reverter / rito (estático) | {PORTOES['instalar_reverter_rito_estatico']} |
| p00 | {PORTOES['p00']}: {ok_p00}/{n_p00} checagens OK; pendentes: {len(pendentes_p00)} |
| veto à pasta da entrega do Kimi | {PORTOES['veto_kimi']}: as seis checagens [VETO kimi] do p00 ({_veto_txt}) |
| B(n) pré-selo | {PORTOES['bn_pre_selo']}: {PR.get('veredito')}; bateria {bat}; produção intacta = {PROV.get('producao_intacta')}; recibo `{h16('PINO_RECIBO_PRE_SELO_v410.json') if os.path.exists(P('PINO_RECIBO_PRE_SELO_v410.json')) else None}` |
| serviço da Bancada (estático) | {PORTOES['servico_estatico']}: {SERV.get('n_condicoes_ok')}/{SERV.get('n_condicoes')} condições; toda mutação pega = {CTRL.get('toda_mutacao_foi_pega')} |
| harness dos textos | {PORTOES['harness_textos']}: {n_neg_leit} controles da leitura, {n_neg_par} do parágrafo novo |
| harness do fechar | {PORTOES['harness_fechar']}: {n_neg_fech} controles do fechar |
| regeneração limpa | {PORTOES['refazer_limpo']}: `refazer_out_v410.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v410.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | {PORTOES['fala_excluida_fora_dos_artefatos']}: `purga_v410.json`, zero ocorrências |
| guarda da própria prosa | {PORTOES.get('guarda_da_prosa')}: a guarda das frases e a P18 sobre este relatório e o plano |

Fora dos portões, informativo: o orquestrador sem S7 e sem S10 (D57a herdada), medido na lista de passos e no laço de `orquestrador/pos_treino_v410.py` = {SEM_S7_S10}; os textos da custódia encadeados no S6d: {', '.join(_textos_custodia) or 'AUSENTE'}; o ensaio offline do H0DN ({_h0dn_pt}): {('tudo_passou = %s' % TH.get('tudo_passou')) if TH else 'o construtor não gravou TESTE_H0DN_OFFLINE_v410.json'}; o da AEscala: {('tudo_passou = %s' % TA.get('tudo_passou')) if TA else 'o construtor não gravou TESTE_AESCALA_OFFLINE_v410.json'}; o do recibo HMS/13: {('tudo_passou = %s' % TF.get('tudo_passou')) if TF else 'o construtor não gravou TESTE_HMS13_OFFLINE_v410.json'}.

## 3. O que NÃO passou ou fica para depois

- p00 reprova {len(falhas_p00)} checagem(ns): {'; '.join(f[:200] for f in falhas_p00) if falhas_p00 else 'nenhuma'}; pendentes ({len(pendentes_p00)}): {'; '.join(f[:160] for f in pendentes_p00) if pendentes_p00 else 'nenhum'}.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo, os textos da custódia e o HANDOFF; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `{ROTA}`, seq {seqs}.

## 4. Avisos e desvios ditos

{chr(10).join('- ' + a for a in AVISOS)}

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D69: até três rodadas), nesta ordem, antes de qualquer publicação: `delta_v410.py` (moldura, erratas E29, E30 e E31, decisões D63 a {_DL.DECISOES_V410[-1]}, as leituras, as ressalvas), `registros_v410.py`, `registros_h0dn_v410.py`, `registros_aescala_v410.py` e `registros_hms13_v410.py`, `runtime_v410.py` (as {_DL.N_CHECKS_FECHO} checagens de `{_DL.FECHO_REGISTRO}` e a guarda das frases), `runtime_h0dn_v410.py` (as {_DL.N_CHECKS_H0DN} checagens de `{_DL.H0DN_REGISTRO}`, a função de veredito congelada e a vigia de arquivos), `runtime_aescala_v410.py` (as {_DL.N_CHECKS_AESCALA} de `{_DL.AESCALA_REGISTRO}`) e `runtime_hms13_v410.py` (as {_DL.N_CHECKS_HMS13} de `{_DL.HMS13_REGISTRO}`), as pedras em `pedra/IALD2.lean` e `pedra/AEscala.lean`, as seções do artigo (`artigo_pt_v410.pysnip`, `artigo_en_v410.pysnip`, as duas da AEscala e as duas do H0DN, com o parágrafo do HMS/13 no fim) e `pos_rito/textos_v410.semente`.
2. Dizer ao operador, na língua dele (regra do posto, antes de qualquer teste que possa dar negativo), o que a v410 NÃO entrega e o que o teste H0DN ({_h0dn_pt}) decide, não decide e significaria: validade no kernel não é creditação; P = nP aqui é relativo ao leitor (a máquina com o leitor) e a máquina de Turing padrão sem o leitor fica fora; a forma de matriz finita é o signo; o atrator é termo sobre o Nome do par lido e nada foi medido na natureza; o teste H0DN decide, quando for aberto, se a razão de Hubble local/fundo discrimina β_TGL do ΛCDM à sensibilidade disponível; NÃO decide a TGL inteira nem a creditação; um desfecho inconclusivo por sistemática é parede de montagem do dado, não falsificação, e “a lei K falsificada” falsifica a lei K àquela sensibilidade, não a teoria; as escolhas do desenho (os dois modelos, a covariância publicada, o limiar de 5σ, a função de veredito congelada) estão ditas aqui e no `DESENHO_v410.md`; o 4,44 continua abaixo do degrau de 5σ; nenhum teste com a natureza entra nesta versão.
3. O orquestrador lê `PREPARACAO_v410_PRONTA.json` e segue: `instalar_v410.py`, `rito_v410.sh`, `pos_rito/chain_pos_rito_v410.sh` (0 → 10, 10a, 10b, 10c → 14), os textos da custódia encadeados (S6d) e o HANDOFF (fim da cadeia, D57a herdada), com a trava S1b aberta só pela revisão aprovada; a custódia completa e o release do app são da sessão de custódia.
4. Se o rito cair: `reverter_v410.py` é decisão da gerência; `refazer_candidato_v410.sh --regerar` refaz o candidato.

## 6. Os módulos e as âncoras

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
    return PLANO, RELATORIO


def _guarda(txt_):
    """a guarda das frases (v410) e a P18 sobre o texto; lista de (regra, trecho)"""
    return [tuple(v_[:2]) for v_ in list(_GFM.violacoes(txt_)) + list(_GP18.violacoes(txt_))]


falta = [k for k, v in PORTOES.items() if not v]
pronta = not falta
for _volta in range(3):   # a guarda da prosa e' um portao: renderiza, mede, renderiza de novo com o portao dentro do quadro (converge em duas voltas)
    PLANO, RELATORIO = _prosa(pronta, falta)
    _viol = _guarda(PLANO + "\n" + RELATORIO)
    PORTOES["guarda_da_prosa"] = not _viol
    _falta2 = [k for k, v in PORTOES.items() if not v]
    if _falta2 == falta and pronta == (not falta):
        break
    falta, pronta = _falta2, not _falta2
PLANO, RELATORIO = _prosa(pronta, falta)
PRONTA = {"contrato": "PREPARACAO_v410_PRONTA", "agente": "claude-construtor-v410", "quando": AGORA.strftime("%Y-%m-%d %H:%M:%S"), "pronta": pronta, "falta": falta, "portoes": PORTOES,
          "candidato_sha16": CM.get("sha16"), "candidato_sha256": CM.get("sha256"), "candidato_bytes": CM.get("bytes"), "origem_sha16": CM.get("base_v409_sha16"), "escada": ES.get("escada_v409_e_v410") or CM.get("escada"), "n_bandeiras_novas": ES.get("n_bandeiras_novas"), "n_modulos_novos": (CM.get("kernel") or {}).get("modulos_novos"),
          "ordem_do_operador": {"arquivo": _DL.N_ORDEM_V410, "sha16_lido_do_arquivo": ORDEM16, "frase": _DL.FRASE_ORDEM_V410, "retomada_09nov_sha16": RETOM16, "ratificacao_dos_nomes_09nov_sha16": RAT16, "selo_D76_sha16": SELO16},
          "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v410.json", "sha16": h16("kernel/KERNEL_RECIBO_v410.json") if os.path.exists(P("kernel/KERNEL_RECIBO_v410.json")) else None, "rc": KR.get("rc")},
          "esperados_sha16": h16("ESPERADOS_v410.json") if os.path.exists(P("ESPERADOS_v410.json")) else None, "p00": {"ok": PC.get("ok"), "passaram": ok_p00, "n": n_p00, "pendentes": pendentes_p00, "sha16": h16("PRECONDICOES_v410.json") if os.path.exists(P("PRECONDICOES_v410.json")) else None},
          "ensaio_a_seco": {"veredito": EN.get("veredito"), "sha16_do_candidato": EN.get("sha16"), "json_sha16": h16("ensaio_a_seco_v410.json") if os.path.exists(P("ensaio_a_seco_v410.json")) else None},
          "previoo_do_gerador": {"ok": PV.get("ok"), "checagens_ok": sum(1 for v_ in (PV.get("checks") or {}).values() if v_.get("ok") is True), "n": len(PV.get("checks") or {}), "sha16": h16("PREVOO_GERADOR_v410.json") if os.path.exists(P("PREVOO_GERADOR_v410.json")) else None},
          "h0dn": H0DN_RES, "veto_kimi": {"pasta_vedada": _DL.H0DN_PASTA_VEDADA, "checagens_p00": [{"checagem": c.get("checagem", "")[:60], "ok": c.get("ok"), "pendente": bool(c.get("pendente"))} for c in _veto_p00], "nada_da_pasta_foi_lido_copiado_pinado_ou_citado": True},
          "orquestrador": {"sem_S7_e_sem_S10_D57a_medido": SEM_S7_S10, "textos_custodia_encadeados_S6d": _textos_custodia, "fim_da_cadeia": "HANDOFF (D57a)"},
          "comandos": {"instalar": "python -B -X utf8 instalar_v410.py", "rito": "sh rito_v410.sh", "cadeia": "CHAIN_DE=<rotulo> CHAIN_ATE=<rotulo> sh pos_rito/chain_pos_rito_v410.sh (rotulos 0..10 10a 10b 10c 11..14; 10b com B3_AUTORIZADO=sim, EVENTO e EVENTO_HASH); depois os textos da custodia (S6d, D52, D57c) e o HANDOFF (fim da cadeia, D57a)", "cwd": HERE,
                       "reverter": "python -B -X utf8 reverter_v410.py (so' por decisao da gerencia)"},
          "hashes": HASHES, "nao_revisado_por_terceiro": NAO_REVISADO, "trava_do_orquestrador": ("S1b (pos_treino_v410): ABERTA pela revisao_terceiro/REVISAO_TERCEIRO_v410.json (aprovada, mesmo sha16 do candidato); a preparacao nao a abriu: o revisor abriu" if REVISAO_OK else "S1b (pos_treino_v410): fechada ate' revisao_terceiro/REVISAO_TERCEIRO_v410.json aprovar ESTE candidato (revisor: Sonnet, D69); esta preparacao nao a abre"), "revisao_de_terceiro": ({"aprovada": _REV.get("aprovada"), "rodada": _REV.get("rodada"), "n_alto": _REV.get("n_alto"), "n_medio": _REV.get("n_medio"), "n_baixo": _REV.get("n_baixo"), "candidato_sha16": _REV.get("candidato_sha16"), "sha16_do_json": h16("revisao_terceiro/REVISAO_TERCEIRO_v410.json"), "revisor": _REV.get("revisor"), "quando": _REV.get("quando")} if REVISAO_OK else None),
          "readme_evidente": {"ordem": "D85 (operador, 09/11/2026): tudo isso fica evidente no README, junto com o resultado do novo teste, quando ficar pronto; a custodia NAO adivinha: os tres itens estao aqui",
                              "1_clay_forma_canonica": {"pt": _DL.FRASE_CLAY_CANONICA_PT, "en": _DL.FRASE_CLAY_CANONICA_EN, "forma_da_D83_pt": _DL.FRASE_D83_OBRIGATORIA_PT, "forma_da_D83_en": _DL.FRASE_D83_OBRIGATORIA_EN, "p_igual_np_D81_pt": _DL.FRASE_D81_PT, "p_igual_np_D81_en": _DL.FRASE_D81_EN,
                                                        "termos_do_kernel": ["TGLExt.TraducaoTuring (v409): opDaInstancia, nomeDasSolucoes, a_maquina_com_o_leitor, uma_leitura_decide_SAT, p_igual_np_no_modo_selecao", "TGLExt.AEscala (v410): LeitorDoFundo, aPerguntaDoClay, iald, a_pergunta_do_clay_tem_resposta, a_iald_le_a_face_sem_leitura, le_como_dissipacao_termica, a_face_caida_e_o_fundo, sem_leitor_a_face_e_ruido, existe_o_algoritmo_e_e_a_iald, a_escala; os nomes novos da R3, a ratificar: " + ", ".join(_DL.NOMES_NOVOS_AESCALA)],
                                                        "estatuto": "[REAL] validade no kernel; [INPUT] a definicao da pergunta no dicionario e' do operador; a creditacao e' do Clay (de quem tem autoridade para falar em nome dele)"},
                              "2_aescala_e_os_seus_numeros": {"pedra": "TGLExt.AEscala", "aescala": {k_: (CM.get("aescala") or {}).get(k_) for k_ in ("source_sha256", "n_ancoras", "ancora_principal", "ancoras_de_secao", "n_flags", "flag_prefix", "n_nomes", "n_nomes_novos", "nomes_novos_a_ratificar", "campos_novos_da_estrutura", "estatuto_dos_nomes_novos", "ponte", "n_falas", "numeros", "bandeiras_de_constantes_geradas_pela_structure")}, "numeros": dict(_DL.NUMEROS_AESCALA),
                                                              "leitura": "o Nome pesa {nome_pesa_um} = {meio} + {meio}; a face sem par nao conjuga, ({meio} . 1)^2 = {meio} . ({meio} . 1); tres faces = {tres_faces}; {um_terco_caiu} caiu; o Nome normalizado = {nome_normalizado}".format(**_DL.NUMEROS_AESCALA), "estatuto": "[REAL] termos no trio; [DERIVED, aritmetica] os numeros e a ponte da escala; [DECLARADO] os nomes novos da pedra, a ratificar; [ONTO] a face caida como o neutrino; [CONJECTURE] m1 = 0", "nomes": _DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT},
                              "3_h0dn_bg1": {"parede_de_montagem_pt": _DL.FRASE_H0DN_PAREDE_PT, "parede_de_montagem_en": _DL.FRASE_H0DN_PAREDE_EN, "agora": "o teste H0DN x BG1 entra " + _DL.FRASE_H0DN_OBRIGATORIA_PT + " (registro h0dn_bg1_v410); o recibo documental HMS/13 (h0dn_fontes_hms13_v410): " + _DL.FRASE_HMS13_OBRIGATORIA_PT,
                                             "depois": "o RESULTADO exato quando a abertura acontecer (versao futura), pela funcao de veredito ja' congelada, com o campo outcome", "estatuto": "[REAL] o pre-registro e o recibo documental; [OPEN] a covariancia fisica conjunta (G3/G4); nenhum dado observado lido"},
                              "regras": "estatutos em cada item; a regra da porta e a da linhagem"},
          "ratificacao_aescala_D87": dict((CM.get("aescala") or {}).get("ratificacao_D87") or {}, nome_do_modulo="TGLExt.AEscala", n_nomes=(CM.get("aescala") or {}).get("n_nomes"), nomes=(CM.get("aescala") or {}).get("nomes")),
          "ratificacao_pendente": dict(_DL.RATIFICACAO_PENDENTE_AESCALA),   # (R1/D92: os nomes e os campos novos da pedra R3, [DECLARADO], a ratificar pelo operador; os nomes anteriores foram ratificados na D87 («ratifico tudo»))
          "erratas_E29_E30": ERRATAS_V410_RES, "avisos": AVISOS, "achados_r1": ACHADOS_R1, "violacoes_da_guarda_da_prosa": [list(v_) for v_ in _viol[:8]], "rota_no_mapa": "%s (seq %s)" % (ROTA, seqs)}


def grava(nome, b):
    p = P(nome)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + ST; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p)


if SECO:
    print("gerar_relatorio --seco: PLANO %d B, RELATORIO %d B, PRONTA %d B | a guarda (frases + P18) sobre a prosa: %s | portoes ok %d/%d; falta: %s" % (len(PLANO.encode("utf-8")), len(RELATORIO.encode("utf-8")), len(json.dumps(PRONTA, ensure_ascii=False).encode("utf-8")),
          "LIMPA" if not _viol else _viol[:6], sum(1 for v_ in PORTOES.values() if v_), len(PORTOES), ", ".join(falta)))
    if "--imprimir" in sys.argv:   # (so' com --seco: mostra a prosa montada, sem gravar)
        print(PLANO); print("=" * 100); print(RELATORIO)
    sys.exit(0 if not _viol else 1)
grava("PLANO_v410.md", PLANO.encode("utf-8")); grava("RELATORIO_PREPARACAO_v410.md", RELATORIO.encode("utf-8"))
HASHES["PLANO_v410.md"] = {"sha16": h16("PLANO_v410.md"), "bytes": sz("PLANO_v410.md")}; HASHES["RELATORIO_PREPARACAO_v410.md"] = {"sha16": h16("RELATORIO_PREPARACAO_v410.md"), "bytes": sz("RELATORIO_PREPARACAO_v410.md")}
grava("PREPARACAO_v410_PRONTA.json", json.dumps(PRONTA, ensure_ascii=False, indent=1).encode("utf-8"))
print("pronta =", pronta, "| falta:", falta)
print("candidato", CM.get("sha16"), "| kernel recibo", PRONTA["kernel_recibo"]["sha16"], "| ESPERADOS", PRONTA["esperados_sha16"], "| p00", PRONTA["p00"]["sha16"], "(%d/%d)" % (ok_p00, n_p00))
print(P("PREPARACAO_v410_PRONTA.json"))
