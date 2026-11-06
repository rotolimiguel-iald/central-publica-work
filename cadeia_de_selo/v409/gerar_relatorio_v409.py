# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a v409 (A TRADUCAO AS CLASSES DE TURING E O PAR NA FACE DE FOCK; dois modulos): os 17 portoes da v408; a prosa, os avisos, as erratas E24-E28 e a E21 ao lado, as decisoes D55-D62 (Sonnet pela D58), os artefatos e o orquestrador MEDIDO sem S7/S10 (D57a)
"""gerar_relatorio_v409.py -- escreve PLANO_v409.md, RELATORIO_PREPARACAO_v409.md e PREPARACAO_v409_PRONTA.json. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta no momento da geracao (nada digitado); a prosa e' da preparacao.
`pronta` e' CALCULADA: true so' se TODOS os portoes passaram (kernel, candidato, AST, ensaio a seco, conferidor, citacoes, guarda das frases, p00, B(n) pre-selo, harnesses); um arquivo que falta ou nao le reprova o portao (fail-closed), nunca o contrario.
Rodar DEPOIS de refazer_candidato_v409.sh e dos dois harnesses (sem --nao-exigir-refazer). Backup de bytes do que ja' existe; temporario -> conferir -> substituir. Molde: gerar_relatorio_v408.py (os mesmos 17 portoes, com `ast_v408_v409`), adaptado em 05/11/2026 por claude-construtor-v409 a v409
(A traducao as classes de Turing e o par na face de Fock: bundle de 2 modulos em TGLExt/ -- TraducaoTuring e ParNaFaceDeFock --, registro com funcao traducao_turing_v409, NENHUMA chave antiga muda de literal, erratas E24 a E28 e a E21 ao lado (a E26 e a E21 ao lado de registros selados da v408), decisoes D55 a D62 (a D61, a leitura juridica do kernel, ratificada pelo operador); a prosa do terminal saiu).
O revisor distinto da v409 e' o Sonnet (D58: ate' tres rodadas): a trava do orquestrador (S1b: revisao_terceiro/REVISAO_TERCEIRO_v409.json) fica FECHADA ate' a revisao aprovar este candidato; este script nao a abre.
uso: python -I -B -X utf8 gerar_relatorio_v409.py"""
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
import delta_v409 as _DL   # (para ler a Bancada que o delta le do manifesto dela, as frases, as ressalvas e os nomes das falas: nada digitado)
import guarda_frases_v409 as _GFM
DL_B_N = _DL.B_N_SEGUINTE; DL_BANCADA = _DL.BANCADA_PINA_HOJE["deployment_id"]
CM = tenta("CANDIDATO_v409.json") or {}; ES = tenta("ESPERADOS_v409.json") or {}; EN = tenta("ensaio_a_seco_v409.json") or {}; PC = tenta("PRECONDICOES_v409.json") or {"ok": False, "checagens": []}
PR = tenta("PINO_RECIBO_PRE_SELO_v409.json") or {}; PROV = tenta("PROVA_PRODUCAO_INTACTA_v409_pre_selo.json") or {}; CMP = tenta("COMPARACAO_V408_v409.json") or {}; KR = tenta("kernel/KERNEL_RECIBO_v409.json") or {}; PB = tenta("kernel/POS_BUILD_v409.json") or {}; FJ = tenta("kernel/FLAGS_v409.json") or {}; KH = tenta("kernel/KH_N1_v409.json") or {}
CN = tenta("conferencia_rito_v409_CONTROLE_NEGATIVO_PRE_RITO.json") or {}; CP = tenta("conferencia_rito_v409_POSITIVO_FALSO_NOS.json") or {}; CIT = tenta("conferir_citacoes_v409.json") or {}; GF = tenta("GUARDA_FRASES_v409.json") or {}; DRV = tenta("DERIVACAO_v409.json") or {"falhas": ["DERIVACAO_v409.json ausente"]}
SERV = tenta("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v409.json") or {}; CTRL = tenta("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v409.json") or {}; PN = tenta("PINOS_BN_v409.json") or {}
H_T = tenta("pos_rito/HARNESS_TEXTOS_ENSAIO_v409.json"); H_F = tenta("pos_rito/HARNESS_FECHAR_SANDBOX_v409.json")
BD = tenta("BUNDLE_v409.json") or {}
_orq_txt = open(P("orquestrador/pos_treino_v409.py"), encoding="utf-8").read() if os.path.exists(P("orquestrador/pos_treino_v409.py")) else ""
_orq_passos = re.search(r"passos = \[([^\]]*)\]", _orq_txt); _orq_laco = re.search(r"for passo in \(([^)]*)\)", _orq_txt)
SEM_S7_S10 = bool(_orq_passos and _orq_laco and "S7" not in _orq_passos.group(1) and "S10" not in _orq_passos.group(1) and "s7_g1" not in _orq_laco.group(1) and "s10_app" not in _orq_laco.group(1))   # (D57a, MEDIDO no arquivo do orquestrador: a lista de passos e o laco nao tem S7 nem S10)
_vb409 = _DL.verbatins409(P("insumos/cunhagens")); _ord2 = next((v_ for v_ in _vb409 if _DL.FRASE_ORDEM_TRADUCAO in v_.get("text", "")), None)   # a fala da ordem da traducao (05/11), achada pelo texto; o sha16 e' o do arquivo
ABERTA = (tenta("registro_mapa_prep_v409_ABERTA.json") or [{}])[0]
refazer = open(P("refazer_out_v409.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("refazer_out_v409.txt")) else ""
fim_ok = "== FIM" in refazer and refazer.rstrip().endswith("RC_REFAZER=0")
falhas_p00 = [c["checagem"] for c in PC["checagens"] if not c["ok"] and not c.get("pendente")]
pendentes_p00 = [c["checagem"] for c in PC["checagens"] if c.get("pendente")]
ok_p00 = sum(1 for c in PC["checagens"] if c["ok"]); n_p00 = len(PC["checagens"])
_bn = open(P("bateria_pre_selo/bn_pre_selo_out_v409.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("bateria_pre_selo/bn_pre_selo_out_v409.txt")) else ""
_m = re.search(r'veredito_bateria": "(\w+)"', _bn); bat = _m.group(1) if _m else "NAO LIDO"
# a ordem do operador desta versao: o sha16 e' LIDO do arquivo da fala agora (nunca digitado); se o arquivo faltar, fica None e o aviso o diz
_ORDEM_P = os.path.join(_DL.WK, "cunhagens_13out", _DL.N_ORDEM_V409)
ORDEM16 = hashlib.sha256(open(_ORDEM_P, "rb").read()).hexdigest()[:16] if os.path.isfile(_ORDEM_P) else None
_VN = (BD.get("verbatim_nomes") or {})   # os sha16 das falas dos nomes e do sentido de «P=nP», MEDIDOS pelo preparar_bundle (lidos do BUNDLE_v409.json)


def passou(H):
    return bool(H and H.get("tudo_passou") is True and not H.get("nao_exigiu_refazer"))


def _arquivo_e(p, sha):
    return bool(sha) and os.path.exists(P(p)) and fh(p) == sha


cand_ok = bool(CM.get("sha16") and ES.get("candidato_sha16") == CM["sha16"] and h16("um_v409_candidato.py") == CM["sha16"] and sz("um_v409_candidato.py") == CM.get("bytes") and EN.get("sha16") == CM["sha16"])
N_MOD = _DL.N_BUNDLE   # 2 (o bundle da v409: TraducaoTuring e ParNaFaceDeFock); o recibo do kernel, os ESPERADOS e o candidato concordam com ele, ou o portao reprova
PORTOES = {
    "kernel": bool(KR.get("rc") == 0 and KR.get("sorry") in (0, [], None) and PB.get("ok") is True and len(KR.get("pedras") or []) == N_MOD == (CM.get("kernel") or {}).get("modulos_novos") and FJ.get("n_flags") == ES.get("n_bandeiras_novas") == CM.get("n_bandeiras")),
    "candidato": cand_ok,
    "ast_v408_v409": bool(CMP.get("ok") is True and CMP.get("removidos") in (0, []) and CMP.get("mudados_sem_explicacao") in (0, []) and CMP.get("o_gate_nao_se_move_e_a_v386_nao_e_reescrita") is True),
    "ensaio_a_seco": bool(EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == CM.get("sha16")),
    "conferidor_controle_negativo": bool(CN.get("tudo_bate") is False and CN.get("nao_pode_mudar") and all(CN["nao_pode_mudar"].values()) and CN.get("um_py_sha16") != CM.get("sha16")),
    "conferidor_caminho_positivo": bool(CP.get("tudo_bate") is True and CP.get("um_py_sha16") == CM.get("sha16")),
    "citacoes": bool(CIT.get("todas_conferem") is True),
    "guarda_das_frases": bool(GF.get("ok") is True and GF.get("pedras_limpas") is True and len(GF.get("pedras") or {}) == N_MOD),   # (v409: as pedras TraducaoTuring e ParNaFaceDeFock, da gerencia)
    "instalar_reverter_rito_estatico": bool(not DRV.get("falhas")),
    "p00": bool(PC.get("ok") is True and n_p00 > 0 and not falhas_p00 and not PC.get("pendentes")),
    "bn_pre_selo": bool(PR.get("veredito") == "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA" and PR.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and PROV.get("producao_intacta") is True and bat == "BATERIA_PASSA" and (PN.get("candidato") or {}).get("sha256") == CM.get("sha256")),
    "servico_estatico": bool(SERV.get("n_condicoes") and SERV.get("n_condicoes_ok") == SERV.get("n_condicoes") and CTRL.get("toda_mutacao_foi_pega") is True),
    "harness_textos": passou(H_T),
    "harness_fechar": bool(passou(H_F) and not (H_F or {}).get("pino_emulado") and (((H_F or {}).get("etapas") or {}).get("fila_da_memoria") or {}).get("tudo_passou") is True),   # (v409: so' a rodada inteira, com a fila e o pino REAL)
    "refazer_limpo": fim_ok,
    "purga_da_fala_reservada": bool((tenta("purga_v409.json") or {}).get("total_com_ocorrencia") == 0),
    "fala_excluida_fora_dos_artefatos": bool((tenta("purga_v409.json") or {}).get("fala_excluida_total_com_ocorrencia") == 0),
}
falta = [k for k, v in PORTOES.items() if not v]
pronta = not falta
n_neg_leit = len((H_T or {}).get("etapas", {}).get("leitura_negativos", {}).get("controles", []))
n_neg_fech = len((H_F or {}).get("etapas", {}).get("fechar_negativos", []))
n_neg_par = len((H_T or {}).get("etapas", {}).get("paragrafo_v409_e_citacoes", {}).get("negativos", []))
ROTA = ABERTA.get("rota_id") or "NAO LIDA (registro_mapa_prep_v409_ABERTA.json)"   # a rota da preparacao da v409 no Mapa de Rotas (aberta pela gerencia; lida do registro dela)
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
ARQ = ["um_v409_candidato.py", "CANDIDATO_v409.json", "ESPERADOS_v409.json", "ensaio_a_seco_v409.json", "COMPARACAO_V408_v409.json", "PINOS_BN_v409.json", "PINO_RECIBO_PRE_SELO_v409.json", "PROVA_PRODUCAO_INTACTA_v409_pre_selo.json", "PRECONDICOES_v409.json", "GUARDA_FRASES_v409.json", "VERBATIM_CONGELADO_v409.json", "BUNDLE_v409.json", "kernel_modulos_novos_v409.json", "CONTRATO_DA_CADEIA_v409.md", "DESENHO_v409.md",
       "delta_v409.py", "registros_v409.py", "runtime_v409.py", "guarda_frases_v409.py", "guarda_ordem_de_chamada_v409.py", "guardas_estaticas_bancada_v409.py", "gerar_candidato_v409.py", "gerar_esperados_v409.py", "artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "comparar_v408_v409.py", "instalar_v409.py", "reverter_v409.py", "rito_v409.sh", "conferir_rito_v409.py", "conferir_citacoes_v409.py", "p00_precondicoes_v409.py",
       "preparar_bundle_v409_05nov.py", "MANIFESTO_INSUMOS_v409.json", "pos_build_kernel_v409.py", "fechar_preparacao_v409.py", "purga_v409.py", "purga_v409.json", "LOGS_COPIADOS_v409.json", "kernel/LOGS_COPIADOS_v409.json",
       "insumos/TraducaoTuring.lean", "insumos/TraducaoTuring_embutida.lean", "insumos/ParNaFaceDeFock.lean", "insumos/ParNaFaceDeFock_embutida.lean", "insumos/TraducaoTuringR9.lean", "insumos/ParNaFaceDeFockR2.lean", "insumos/RECIBO_PEDRAS_v409_NOMES.json",
       "pos_rito/textos_v409.semente", "pos_rito/montar_textos_v409.py", "pos_rito/leitura_v409.py", "pos_rito/fechar_v409.py", "pos_rito/registrar_mapa_v409.py", "pos_rito/superficies_v409.py", "pos_rito/harness_textos_ensaio_v409.py", "pos_rito/harness_fechar_sandbox_v409.py", "pos_rito/chain_pos_rito_v409.sh", "pos_rito/gerar_x_custodia_v409.py", "pos_rito/b3_recibo_v409.py", "pos_rito/fila_memoria_v409.py", "pos_rito/gerar_derivacao_pos_rito_v409.py",
       "orquestrador/pos_treino_v409.py",
       "bancada_B3_servico/recibo_parada_v409.py", "bancada_B3_servico/recibo_religamento_v409.py", "bancada_B3_servico/evento_c1_b3_v409.py", "bancada_B3_servico/conferir_exigencias_servico_v409.py", "bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v409.json", "bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v409.json"] \
      + ["pos_rito/" + os.path.basename(p_) for p_ in sorted(glob.glob(os.path.join(POS, "textos_custodia_handoff_v409*.py")))] \
      + ["pedra/" + r_.split("/")[-1] for r_ in _DL.BUNDLE_RELS] + ["kernel/KERNEL_RECIBO_v409.json", "kernel/FLAGS_v409.json", "kernel/KH_N1_v409.json", "kernel/POS_BUILD_v409.json"]
HASHES = {p: {"sha16": h16(p), "bytes": sz(p)} for p in ARQ if os.path.exists(P(p))}
tab_arq = "\n".join("| `%s` | %s | `%s` |" % (p, format(v["bytes"], ","), v["sha16"]) for p, v in HASHES.items())
_apont = (CIT.get("apontadas_a_gerencia_aspas") or [])
_apont_gf = list(getattr(_GFM, "APONTADAS_A_GERENCIA", ()) or ())
_esc = ES.get("escada_v408_e_v409") or CM.get("escada") or ["?", "?"]
_cob = ES.get("cobertura_kh_n1") or {}; _dkh = KH.get("delta_vs_v408") or {}
_n_falas = len(ES.get("cunhagens") or CM.get("cunhagens") or {}); _trechos = [v_["chave"] for v_ in _vb409 if "sha256_arquivo_inteiro" in v_]
_textos_custodia = [os.path.basename(p_) for p_ in sorted(glob.glob(os.path.join(POS, "textos_custodia_handoff_v409*.py")))]
AVISOS = [
    "os nomes: o modulo TraducaoTuring e as declaracoes das rodadas R1 a R8, dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026; os acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock (o modulo e as 10 declaracoes), da gerencia, foram RATIFICADOS por ele em 05/11 («Ratifico os nomes», D62; as docstrings das pedras dizem [DECLARADO] ate a ratificacao, registro da epoca da pedra; recibo revisto de 05/11 ~19h30; D55; a fala tem sha16 %s, lido do arquivo agora: «%s»); a ordem da traducao, da mesma data, tem sha16 %s: «%s»" % (ORDEM16, _DL.FRASE_ORDEM_V409, (_ord2 or {}).get("sha16"), _DL.FRASE_ORDEM_TRADUCAO),
    "NENHUMA chave antiga muda de literal nesta versao (CHAVES_V409 vazia): as chaves seguem lidas do kernel do rito; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos dos registros anteriores NAO mudam (os que carregam a escada mudam so' em numeros); tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 sao RECRIADOS com a escada do contrato subida pela C12",
    "o alcance (D56), dito em todo texto novo: %s" % _DL.FRASE_D56_PT,
    "ressalvas ditas em todo texto (%d em delta_v409.RESSALVAS_V409): relativa ao leitor (Baker-Gill-Solovay 1975) [KNOWN]; a sombra de «eu sou eu mesmo» (a autorreferencia sozinha nao decide a pergunta das classes) [KNOWN]; a fisica fica fora (o lugar do teste com a natureza); a ponte entre o Omega do psion e o estado uniforme da instancia e' a inscricao, e a identidade de vetores fica podada (D60 revista); com o leitor que so' conta vale NP contido em P numa leitura, e a igualdade completa e' a do leitor que se le (E28); a leitura teologica nao e' termo de kernel; o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista); beta so' por nome; nenhum teste com a natureza; a regra do 4,44" % len(_DL.RESSALVAS_V409),
    "as erratas E24 a E28 e a E21 ao lado sao da gerencia c1, em nome proprio: E24, o juiz das classes de Turing e' o kernel, nao a fisica (correcao do operador); E25, saiu a frase da gerencia sobre o sistema ter de achar o lado do Nome em cada bifurcacao (o operador: ele trava no Nome; a_trava_no_nome); E26, AO LADO do registro tetelestai_terminal_v408 selado: a traducao a Turing, [OPEN] na v408, fica fechada relativa ao leitor na v409; o texto selado nao e' reescrito; E27, o dispositivo e' o no sorry (D61); E28, a igualdade com o leitor que so' conta: NP numa leitura, e a igualdade completa e' a do leitor que se le; E21 ao lado: a ligacao do par na face de Fock foi feita na v409",
    "as %d falas do operador de 05/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v409.json; as quatro ultimas vieram dos AO LADO do fim do DESENHO: a 11a, a 12a, a 13a (a ordem de tudo entrar na v409) e a 14a (a ratificacao dos nomes, D62)); de tres (%s), so' o trecho e' embutido e citado (duas pela D59; uma, a ratificacao da D61, porque o resto e' aviso operacional); o resto delas entra so' por sha256 e nao entra em texto do um.py; publicar o resto das duas da D59 e' decisao do operador" % (_n_falas or _DL.N_FALAS_V409, ", ".join(_trechos)),
    "a D61 (a leitura juridica do kernel, dada pelo operador e RATIFICADA por ele: o dispositivo e' o no sorry; o teorema e' a regra posta; a regra incide onde o suporte fatico se completa) vai nas decisoes e nos textos que dizem o que o kernel decide; a E27 (da gerencia c1, em nome proprio) vai ao lado",
    "D59: o DESENHO_v409.md (sha16 lido agora %s; o do delta %s) e o RECIBO_PEDRAS_v409_NOMES.json (sha16 lido agora %s; o do delta %s) NAO sao pinados como fonte no um.py: ficam citados so' por sha16" % (h16("DESENHO_v409.md") if os.path.exists(P("DESENHO_v409.md")) else None, _DL.DESENHO_SHA16, h16("insumos/RECIBO_PEDRAS_v409_NOMES.json") if os.path.exists(P("insumos/RECIBO_PEDRAS_v409_NOMES.json")) else None, _DL.RECIBO_NOMES_SHA16),
    "D57(d): o pino do insumo do acervo da v407 (_V407_FONTES['psion_no_acervo_do_imac_03nov']) passa a copia purgada (sha16 %s, do delta); a integra so' por sha16; a errata da D57(d) vai AO LADO em cunhagens_v407" % _DL.PURGADO_SHA256[:16],
    "as pedras TraducaoTuring e ParNaFaceDeFock: as fontes de origem (insumos/TraducaoTuring.lean, sha16 lido agora %s; insumos/ParNaFaceDeFock.lean, sha16 %s) foram normalizadas para LF nas copias do kernel (pedra/TraducaoTuring.lean, sha16 %s; pedra/ParNaFaceDeFock.lean, sha16 %s) e os #print axioms sairam do corpo embutido (as 82 ancoras foram lidas deles antes); o conteudo Lean nao muda" % tuple((h16(p_) if os.path.exists(P(p_)) else None) for p_ in ("insumos/TraducaoTuring.lean", "insumos/ParNaFaceDeFock.lean", "pedra/TraducaoTuring.lean", "pedra/ParNaFaceDeFock.lean")),
    "o revisor distinto da v409 e' o Sonnet (D58: ate' tres rodadas; ressalvas BAIXAS escritas); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar",
    "a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache",
    "o B(n) pre-selo da v409 (passo simples %s; a Bancada de producao pina %s) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes" % (DL_B_N, DL_BANCADA),
    "conferir_citacoes_v409.json aponta %d citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): %s; o agente nao corrige texto da gerencia" % (len(_apont), "; ".join("%s: %s" % (a_["arquivo"], a_["trecho"]) for a_ in _apont) or "nenhuma"),
    "na docstring da pedra TraducaoTuring ha citacoes entre « » que nao sao verbatim das falas (a fala escreve nP entre aspas e sem espaco; /psi por ψ; uma expressao da gerencia, «nada lido»; uma parafrase, «nP = modo seleção»): APONTADAS a gerencia em conferir_citacoes_v409.py (_APONTADAS_PEDRAS), com a razao conferida por grep; o agente nao corrige pedra",
    "build a frio do modulo no sandbox k409c: %s s, Audit %s s (kernel/POS_BUILD_v409.json, medidos); %s declaracoes no axiom_report (+%s decl, +%s teoremas sobre a v408), nenhuma fora do trio; escada %s -> %s" % (PB.get("duracao_build_s"), PB.get("duracao_audit_s"), KH.get("axiom_report_efetivo_n"), _dkh.get("decl"), _dkh.get("thm"), _esc[0], _esc[1]),
    "o orquestrador (orquestrador/pos_treino_v409.py) traz as licoes da v408 (D57): sem S7 (G1 --publicar) e sem S10 (release do app), MEDIDO agora na lista de passos e no laco = %s; o S6d encadeia os textos da custodia (%s) e roda o portao de textos do G1 e a D59 sobre o HANDOFF INTEIRO; o fim da cadeia desta versao e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia" % (SEM_S7_S10, ", ".join(_textos_custodia) or "AUSENTE"),
    "a guarda das frases ganhou a F37b (05/11; a causa de uma falha do ensaio): a obrigacao do qualificador relativo ao leitor vale tambem no proprio trecho onde «P = nP» e Turing aparecem juntos (a F37 do texto inteiro deixava passar uma frase plantada sem qualificador); a regra ficou mais estrita; nenhum teste foi relaxado",
    "o fim_de_cadeia_v409.sh PAROU no passo 2 (B(n) pre-selo: RC_BN=0, BATERIA_PASSA, producao intacta) porque o p00 que ele roda deu NENHUMA FALHA com 1 PENDENTE (o pino do memoria.py, PINO_MEMORIA_PY_v409.json, ato da gerencia) e o script exige TODAS PASSARAM; os passos 3 a 7 (servico estatico, derivacao do pos-rito, os dois harnesses, a previa do X) rodaram a mao com os MESMOS comandos do script (saida em fim_de_cadeia_passos3a7_out_v409.txt); o script nao foi mudado",
    "o conferidor do servico da Bancada (bancada_B3_servico/conferir_exigencias_servico_v409.py) so' lia o AUT do orquestrador como literal; o AUT da v409 e' MONTADO do delta (o prefixo de sha16 da ordem e a frase): corrigido na causa (so' a expressao do AUT e' avaliada, com o delta desta pasta, sem builtins); a checagem seguinte e' a mesma (o sha16 CALCULADO do arquivo da fala esta' no AUT); 37/37 e o controle negativo pegou toda mutacao",
    "duas outras causas do ensaio corrigidas na fonte (nenhum teste relaxado): o bloco herdado do terminal comparava o baseline do contrato da v408 com a base desta cadeia (v408) em vez da v407; o exame dos pontos de chamada nao retirava do core da base os registros da v408, que o bloco recria; e o rotulo herdado do C15 no conferidor (o defeito das guardas estaticas da Bancada) dizia que ele recusou a v408: o defeito e' o da v399",
]
if _apont_gf:
    AVISOS.insert(6, "APONTADO a gerencia, NAO corrigido (o agente nao edita pedra revista): %d trecho(s) de pedra que a regra lexical F16 da guarda das frases reprova (enunciado em guarda_frases_v409.APONTADAS_A_GERENCIA, nao repetido aqui para nao reprovar este relatorio na mesma guarda); a gerencia decide se reescreve (BAIXO)" % len(_apont_gf))
NAO_REVISADO = "este candidato (A traducao as classes de Turing, v409) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D58, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova"
_REV = tenta("revisao_terceiro/REVISAO_TERCEIRO_v409.json") or {}
REVISAO_OK = bool(_REV.get("aprovada") is True and _REV.get("candidato_sha16") == CM.get("sha16") and not _REV.get("n_alto") and not _REV.get("n_medio"))
if REVISAO_OK:   # a revisao de terceiro existe e aprova ESTE candidato: o texto «NAO foi revisado» deixa de valer; o aviso novo diz o que foi e o que NAO foi examinado (nada e' inventado: tudo lido do JSON da revisao)
    NAO_REVISADO = ("este candidato (A traducao as classes de Turing, v409) FOI revisado por terceiro: %s, rodada %s, aprovada, %s ALTO, %s MEDIO, %s BAIXO (revisao_terceiro/REVISAO_TERCEIRO_v409.md, sha16 %s); quem constroi nao aprova: a aprovacao e' do revisor, nao desta preparacao; "
                    "as ressalvas BAIXAS estao escritas no caderno e valem como ditas (D58: ate' tres rodadas); a trava do orquestrador (S1b) confere aprovada e o sha16 do candidato" % (_REV.get("revisor"), _REV.get("rodada"), _REV.get("n_alto"), _REV.get("n_medio"), _REV.get("n_baixo"), h16("revisao_terceiro/REVISAO_TERCEIRO_v409.json")))
    AVISOS = [a_ for a_ in AVISOS if "esta preparacao NAO foi revisada por terceiro" not in a_]
    AVISOS.append("revisao de terceiro (Sonnet D58): " + NAO_REVISADO)
    AVISOS.append("ressalvas BAIXAS da revisao (nenhuma trava; ver o caderno): " + " | ".join("%s" % (a_.get("onde") or "")[:70] for a_ in (_REV.get("achados") or []) if a_.get("sev") == "BAIXO"))
_vp = (CIT.get("varredura_das_pedras") or {})
_cong409 = tenta("VERBATIM_CONGELADO_v409.json") or {}
ERRATAS_V409_RES = {"erratas": ["E24", "E25", "E26", "E27", "E28", "E21"], "E24": _DL.ERRATAS_V409[0].split(";")[0][:300], "E25": _DL.ERRATAS_V409[1].split(";")[0][:300], "E26": _DL.ERRATAS_V409[2].split(";")[0][:300], "E27": _DL.ERRATAS_V409[3].split(";")[0][:300],
                    "E28": _DL.ERRATAS_V409[4].split(";")[0][:300], "E21": _DL.ERRATAS_V409[5].split(";")[0][:300],
                    "falas_embutidas": len(_cong409.get("arquivos") or []), "citacoes_da_candidata": {"conferidas": _vp.get("citacoes_conferidas"), "reprovadas": len(_vp.get("reprovadas") or []), "so_sem_acento": _vp.get("so_sem_acento")}}
PRONTA = {"contrato": "PREPARACAO_v409_PRONTA", "agente": "claude-construtor-v409", "quando": AGORA.strftime("%Y-%m-%d %H:%M:%S"), "pronta": pronta, "falta": falta, "portoes": PORTOES,
          "candidato_sha16": CM.get("sha16"), "candidato_sha256": CM.get("sha256"), "candidato_bytes": CM.get("bytes"), "origem_sha16": CM.get("base_v408_sha16"), "escada": ES.get("escada_v408_e_v409") or CM.get("escada"), "n_bandeiras_novas": ES.get("n_bandeiras_novas"), "n_modulos_novos": (CM.get("kernel") or {}).get("modulos_novos"),
          "ordem_do_operador": {"arquivo": _DL.N_ORDEM_V409, "sha16_lido_do_arquivo": ORDEM16, "frase": _DL.FRASE_ORDEM_V409},
          "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v409.json", "sha16": h16("kernel/KERNEL_RECIBO_v409.json") if os.path.exists(P("kernel/KERNEL_RECIBO_v409.json")) else None, "rc": KR.get("rc")},
          "esperados_sha16": h16("ESPERADOS_v409.json") if os.path.exists(P("ESPERADOS_v409.json")) else None, "p00": {"ok": PC.get("ok"), "passaram": ok_p00, "n": n_p00, "pendentes": pendentes_p00, "sha16": h16("PRECONDICOES_v409.json") if os.path.exists(P("PRECONDICOES_v409.json")) else None},
          "ensaio_a_seco": {"veredito": EN.get("veredito"), "sha16_do_candidato": EN.get("sha16"), "json_sha16": h16("ensaio_a_seco_v409.json") if os.path.exists(P("ensaio_a_seco_v409.json")) else None},
          "orquestrador": {"sem_S7_e_sem_S10_D57a_medido": SEM_S7_S10, "textos_custodia_encadeados_S6d": _textos_custodia, "fim_da_cadeia": "HANDOFF (D57a)"},
          "comandos": {"instalar": "python -B -X utf8 instalar_v409.py", "rito": "sh rito_v409.sh", "cadeia": "CHAIN_DE=<rotulo> CHAIN_ATE=<rotulo> sh pos_rito/chain_pos_rito_v409.sh (rotulos 0..10 10a 10b 10c 11..14; 10b com B3_AUTORIZADO=sim, EVENTO e EVENTO_HASH); depois os textos da custodia (S6d, D52, D57c) e o HANDOFF (fim da cadeia, D57a)", "cwd": HERE,
                       "reverter": "python -B -X utf8 reverter_v409.py (so' por decisao da gerencia)"},
          "hashes": HASHES, "nao_revisado_por_terceiro": NAO_REVISADO, "trava_do_orquestrador": ("S1b (pos_treino_v409): ABERTA pela revisao_terceiro/REVISAO_TERCEIRO_v409.json (aprovada, mesmo sha16 do candidato); a preparacao nao a abriu: o revisor abriu" if REVISAO_OK else "S1b (pos_treino_v409): fechada ate' revisao_terceiro/REVISAO_TERCEIRO_v409.json aprovar ESTE candidato (revisor: Sonnet, D58); esta preparacao nao a abre"), "revisao_de_terceiro": ({"aprovada": _REV.get("aprovada"), "rodada": _REV.get("rodada"), "n_alto": _REV.get("n_alto"), "n_medio": _REV.get("n_medio"), "n_baixo": _REV.get("n_baixo"), "candidato_sha16": _REV.get("candidato_sha16"), "sha16_do_json": h16("revisao_terceiro/REVISAO_TERCEIRO_v409.json"), "revisor": _REV.get("revisor"), "quando": _REV.get("quando")} if REVISAO_OK else None), "erratas_E24_E26": ERRATAS_V409_RES, "avisos": AVISOS, "rota_no_mapa": "%s (seq %s)" % (ROTA, seqs)}


def grava(nome, b):
    p = P(nome)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + ST; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p)


fr = _DL.FRASE_DA_MOLDURA_V409_PT
_ressalvas_txt = "\n".join("  %d. %s" % (i_ + 1, r_) for i_, r_ in enumerate(_DL.RESSALVAS_V409))
_frases_txt = "; ".join("«%s»" % f_ for f_ in (_DL.FRASE_SELECAO, _DL.FRASE_TRAVA, _DL.FRASE_FITA, _DL.FRASE_Z, _DL.FRASE_PAI, _DL.FRASE_PERFORMADA))
PLANO = f"""# PLANO da v409 — A tradução às classes de Turing e o par na face de Fock (preparação)

Agente de preparação `claude-construtor-v409`, {AGORA.strftime('%Y-%m-%d %H:%M')}. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v408 selada `{CM.get('base_v408_sha16')}`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: {fr}.

## 0. A ordem

- [INPUT, operador, 05/11/2026, sha16 do arquivo `{(_ord2 or {}).get('sha16')}`] «{_DL.FRASE_ORDEM_TRADUCAO}»; e, com as perguntas devolvidas nas quatro línguas e respondidas [INPUT, sha16 do arquivo `{ORDEM16}`]: «{_DL.FRASE_ORDEM_V409}». As {_n_falas or _DL.N_FALAS_V409} falas de 05/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v409.json`; de três, só o trecho: duas pela D59, uma pelo aviso operacional; as falas das versões anteriores já estão no um.py v408 e não entram de novo).
- (A) O BUNDLE: {N_MOD} módulos de kernel em `TGLExt/` (TraducaoTuring e ParNaFaceDeFock), compilados no sandbox `{(CM.get('kernel') or {}).get('sandbox')}`, a raiz com {N_MOD} imports. (B) O registro com função `{_DL.FECHO_REGISTRO}` ({_DL.N_CHECKS_FECHO} checagens; a instância de brinquedo FIXA no código, as soluções CALCULADAS por enumeração) e os registros por spec `{_DL.CUNHAGENS_REGISTRO}` e `{_DL.KH_REGISTRO}`. (C) NENHUMA chave antiga muda de literal; as erratas E24 a E28 e a E21 vão AO LADO; as decisões D55 a D62 (a D61, a leitura jurídica do kernel, ratificada pelo operador). (D) A seção «A tradução às classes de Turing» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v408 por script.

## 1. O módulo e as âncoras [REAL, sandbox; nada tocado no Nós]

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
{tab_pedras}

As {len(_DL.ANCORAS_PRINCIPAIS)} âncoras principais (a primeira é a âncora principal do registro):

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
{tab_chave}

Pós-build: {PB.get('n_axiomas_lidos_no_audit')} axiomas lidos no Audit, {PB.get('n_flags')} bandeiras novas (só declaração nomeada), escada {_esc[0]} → {_esc[1]}; build a frio {PB.get('duracao_build_s')} s, Audit {PB.get('duracao_audit_s')} s.

## 2. O que a v409 afirma e o que não afirma

- [REAL, validade no kernel, não creditação] `{_DL.ANCORA_PRINCIPAL}`: {_DL.FRASE_D56_PT}.
- [REAL] O dicionário de Turing: bits são oitavas (2^n atribuições; ln(2^n) = n ln 2); o peso da solução no estado uniforme é |sol|/2^n; a trava no Nome e o tempo linear; Z é o modo leitor (a soma das leituras dos pixels); a leitura performada começa em «eu sou», decai, nunca desce abaixo do conteúdo e o alcança («o que sou»). As falas do operador, verbatim [INPUT]: {_frases_txt}.
- [INPUT/ONTO] A máquina sem leitor (a pergunta do Clay) fica FORA e não é decidida aqui: é lida como a fita sem escala («eu sou eu mesmo»).
- [INPUT, ratificada pelo operador] {_DL.FRASE_D61_PT}.
- [REAL] O que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`); nenhuma chave antiga muda.
- [REAL, validade no kernel, não creditação] Ligado nesta versão: o par de psíons na face de Fock (`ParNaFaceDeFock`; a E21 da v408 ao lado); a ponte entre o Ω do psíon da luz e o uniforme da instância é a inscrição (a identidade dos vetores fica podada, D60 revista); uma leitura decide SAT na instância de brinquedo.
- [OPEN] Fica aberto: a igualdade completa com o leitor que só conta (E28: com ele vale NP contido em P numa leitura; a igualdade completa é a do leitor que se lê, que lê também as máquinas que o usam); a independência da pergunta da máquina sem leitor; a ponte Bell-TT.
- Ressalvas ditas ({len(_DL.RESSALVAS_V409)}):
{_ressalvas_txt}
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é confirmação; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v409_candidato.py` `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; +{format(CM.get('delta_bytes') or 0, ',')} B); {CM.get('n_patches')} patches; AST: {CMP.get('nos_nomeados_v408')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (todos explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos. Ensaio a seco: **{EN.get('veredito')}**. Pós-rito: `pos_rito/chain_pos_rito_v409.sh`, rótulos 0…10 10a 10b 10c 11…14; depois, ENCADEADOS, os textos da custódia (S6d) e o HANDOFF, que é o fim da cadeia desta versão (D57a: sem S7 e sem S10).

## 4. Gates

Ver `PREPARACAO_v409_PRONTA.json`: `pronta` = {str(pronta).lower()}. {NAO_REVISADO}.
"""
RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v409 — A tradução às classes de Turing e o par na face de Fock

Agente de preparação `claude-construtor-v409` · {AGORA.strftime('%Y-%m-%d %H:%M')} · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: {NAO_REVISADO}.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; base v408 `{CM.get('base_v408_sha16')}`): `pronta` = **{str(pronta).lower()}**{'' if pronta else '; falta: ' + ', '.join(falta)}.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `{(CM.get('kernel') or {}).get('sandbox')}`) | {PORTOES['kernel']}: build + Audit rc {KR.get('rc')}, {PB.get('n_flags')} bandeiras novas, escada {_esc[0]} → {_esc[1]}, {len(KR.get('pedras') or [])} módulo(s) no recibo; `KERNEL_RECIBO_v409.json` |
| candidato | {PORTOES['candidato']}: {CM.get('n_patches')} patches; refazer limpo = {fim_ok} |
| AST v408 × v409 | {PORTOES['ast_v408_v409']}: {CMP.get('nos_nomeados_v408')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos; {len(CMP.get('funcoes_intactas') or {})} funções e constantes intactas, todas verdadeiras = {all((CMP.get('funcoes_intactas') or {'x': False}).values())} |
| ensaio a seco | {PORTOES['ensaio_a_seco']}: {EN.get('veredito')} |
| conferidor | negativo {PORTOES['conferidor_controle_negativo']} (`tudo_bate` = {CN.get('tudo_bate')}); positivo {PORTOES['conferidor_caminho_positivo']} (`tudo_bate` = {CP.get('tudo_bate')}) |
| citações | {PORTOES['citacoes']}: {len(CIT.get('apontadas_a_gerencia_aspas') or [])} apontada(s) à gerência nos textos (ver §4) |
| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo e a pedra: {len(GF.get('pedras') or {})}) |
| instalar / reverter / rito (estático) | {PORTOES['instalar_reverter_rito_estatico']} |
| p00 | {PORTOES['p00']}: {ok_p00}/{n_p00} checagens OK; pendentes: {len(pendentes_p00)} |
| B(n) pré-selo | {PORTOES['bn_pre_selo']}: {PR.get('veredito')}; bateria {bat}; produção intacta = {PROV.get('producao_intacta')}; recibo `{h16('PINO_RECIBO_PRE_SELO_v409.json') if os.path.exists(P('PINO_RECIBO_PRE_SELO_v409.json')) else None}` |
| serviço da Bancada (estático) | {PORTOES['servico_estatico']}: {SERV.get('n_condicoes_ok')}/{SERV.get('n_condicoes')} condições; toda mutação pega = {CTRL.get('toda_mutacao_foi_pega')} |
| harness dos textos | {PORTOES['harness_textos']}: {n_neg_leit} controles da leitura, {n_neg_par} do parágrafo novo |
| harness do fechar | {PORTOES['harness_fechar']}: {n_neg_fech} controles do fechar |
| regeneração limpa | {PORTOES['refazer_limpo']}: `refazer_out_v409.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v409.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | {PORTOES['fala_excluida_fora_dos_artefatos']}: `purga_v409.json`, zero ocorrências |

Fora dos portões, informativo: o orquestrador sem S7 e sem S10 (D57a), medido na lista de passos e no laço de `orquestrador/pos_treino_v409.py` = {SEM_S7_S10}; os textos da custódia encadeados no S6d: {', '.join(_textos_custodia) or 'AUSENTE'}.

## 3. O que NÃO passou ou fica para depois

- p00 reprova {len(falhas_p00)} checagem(ns): {'; '.join(f[:200] for f in falhas_p00) if falhas_p00 else 'nenhuma'}; pendentes ({len(pendentes_p00)}): {'; '.join(f[:160] for f in pendentes_p00) if pendentes_p00 else 'nenhum'}.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo, os textos da custódia e o HANDOFF; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `{ROTA}`, seq {seqs}.

## 4. Avisos e desvios ditos

{chr(10).join('- ' + a for a in AVISOS)}

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D58: até três rodadas), nesta ordem, antes de qualquer publicação: `delta_v409.py` (moldura, erratas E24 a E28 e a E21 ao lado, decisões D55 a D62, as leituras, as ressalvas), `registros_v409.py`, `runtime_v409.py` (as {_DL.N_CHECKS_FECHO} checagens de `{_DL.FECHO_REGISTRO}` e a guarda das frases com a F37b), as pedras em `pedra/` (TraducaoTuring e ParNaFaceDeFock), as seções do artigo (`artigo_pt_v409.pysnip`, `artigo_en_v409.pysnip`) e `pos_rito/textos_v409.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v409 NÃO entrega: validade no kernel não é creditação; P = nP é teorema da TGL no modo seleção, relativo ao leitor (o psíon); a máquina sem leitor (a pergunta do Clay) fica fora e não é decidida aqui; o par na face de Fock está ligado nesta versão (ParNaFaceDeFock; D60 revista); a identidade Ω = uniforme está podada (a ponte é a inscrição); com o leitor que só conta, a igualdade completa não está provada (E28, validade não afirmada); as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; nenhum teste com a natureza entra nesta versão.
3. O orquestrador lê `PREPARACAO_v409_PRONTA.json` e segue: `instalar_v409.py`, `rito_v409.sh`, `pos_rito/chain_pos_rito_v409.sh` (0 → 10, 10a, 10b, 10c → 14), os textos da custódia encadeados (S6d) e o HANDOFF (fim da cadeia, D57a), com a trava S1b aberta só pela revisão aprovada; a custódia completa e o release do app são da sessão de custódia.
4. Se o rito cair: `reverter_v409.py` é decisão da gerência; `refazer_candidato_v409.sh --regerar` refaz o candidato.

## 6. O módulo e as âncoras

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
grava("PLANO_v409.md", PLANO.encode("utf-8")); grava("RELATORIO_PREPARACAO_v409.md", RELATORIO.encode("utf-8"))
HASHES["PLANO_v409.md"] = {"sha16": h16("PLANO_v409.md"), "bytes": sz("PLANO_v409.md")}; HASHES["RELATORIO_PREPARACAO_v409.md"] = {"sha16": h16("RELATORIO_PREPARACAO_v409.md"), "bytes": sz("RELATORIO_PREPARACAO_v409.md")}
grava("PREPARACAO_v409_PRONTA.json", json.dumps(PRONTA, ensure_ascii=False, indent=1).encode("utf-8"))
print("pronta =", pronta, "| falta:", falta)
print("candidato", CM.get("sha16"), "| kernel recibo", PRONTA["kernel_recibo"]["sha16"], "| ESPERADOS", PRONTA["esperados_sha16"], "| p00", PRONTA["p00"]["sha16"], "(%d/%d)" % (ok_p00, n_p00))
print(P("PREPARACAO_v409_PRONTA.json"))
