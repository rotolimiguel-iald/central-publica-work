# -*- coding: utf-8 -*-
"""gerar_relatorio_v407.py -- escreve PLANO_v407.md, RELATORIO_PREPARACAO_v407.md e PREPARACAO_v407_PRONTA.json. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta no momento da geracao (nada digitado); a prosa e' da preparacao.
`pronta` e' CALCULADA: true so' se TODOS os portoes passaram (kernel, candidato, AST, ensaio a seco, conferidor, citacoes, guarda das frases, p00, B(n) pre-selo, harnesses); um arquivo que falta ou nao le reprova o portao (fail-closed), nunca o contrario.
Rodar DEPOIS de refazer_candidato_v407.sh e dos dois harnesses (sem --nao-exigir-refazer). Backup de bytes do que ja' existe; temporario -> conferir -> substituir. Molde: gerar_relatorio_v406.py (os mesmos 17 portoes, com `ast_v406_v407` no lugar de `ast_v405_v406`), adaptado em 03/11/2026 a v407 (o psion, o canto e o par: bundle de 9 modulos em TGLExt/, registro psion_canto_v407, a chave linked_to_the_corner_by_a_lemma lida do kernel; a prosa das erratas E14 a E17 e do bundle de 301 modulos saiu).
O revisor distinto da v407 e' o Sonnet (D47): a trava do orquestrador (S1b: revisao_terceiro/REVISAO_TERCEIRO_v407.json) fica FECHADA ate' a revisao aprovar este candidato; este script nao a abre.
uso: python -I -B -X utf8 gerar_relatorio_v407.py"""
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
import delta_v407 as _DL   # (para ler a Bancada que o delta le do manifesto dela, as frases e as ressalvas: nada digitado)
import guarda_frases_v407 as _GFM
DL_B_N = _DL.B_N_SEGUINTE; DL_BANCADA = _DL.BANCADA_PINA_HOJE["deployment_id"]
CM = tenta("CANDIDATO_v407.json") or {}; ES = tenta("ESPERADOS_v407.json") or {}; EN = tenta("ensaio_a_seco_v407.json") or {}; PC = tenta("PRECONDICOES_v407.json") or {"ok": False, "checagens": []}
PR = tenta("PINO_RECIBO_PRE_SELO_v407.json") or {}; PROV = tenta("PROVA_PRODUCAO_INTACTA_v407_pre_selo.json") or {}; CMP = tenta("COMPARACAO_V406_v407.json") or {}; KR = tenta("kernel/KERNEL_RECIBO_v407.json") or {}; PB = tenta("kernel/POS_BUILD_v407.json") or {}; FJ = tenta("kernel/FLAGS_v407.json") or {}; KH = tenta("kernel/KH_N1_v407.json") or {}
CN = tenta("conferencia_rito_v407_CONTROLE_NEGATIVO_PRE_RITO.json") or {}; CP = tenta("conferencia_rito_v407_POSITIVO_FALSO_NOS.json") or {}; CIT = tenta("conferir_citacoes_v407.json") or {}; GF = tenta("GUARDA_FRASES_v407.json") or {}; DRV = tenta("DERIVACAO_v407.json") or {"falhas": ["DERIVACAO_v407.json ausente"]}
SERV = tenta("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v407.json") or {}; CTRL = tenta("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v407.json") or {}; PN = tenta("PINOS_BN_v407.json") or {}
H_T = tenta("pos_rito/HARNESS_TEXTOS_ENSAIO_v407.json"); H_F = tenta("pos_rito/HARNESS_FECHAR_SANDBOX_v407.json")
ABERTA = (tenta("registro_mapa_prep_v407_ABERTA.json") or [{}])[0]
refazer = open(P("refazer_out_v407.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("refazer_out_v407.txt")) else ""
fim_ok = "== FIM" in refazer and refazer.rstrip().endswith("RC_REFAZER=0")
falhas_p00 = [c["checagem"] for c in PC["checagens"] if not c["ok"] and not c.get("pendente")]
pendentes_p00 = [c["checagem"] for c in PC["checagens"] if c.get("pendente")]
ok_p00 = sum(1 for c in PC["checagens"] if c["ok"]); n_p00 = len(PC["checagens"])
_bn = open(P("bateria_pre_selo/bn_pre_selo_out_v407.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("bateria_pre_selo/bn_pre_selo_out_v407.txt")) else ""
_m = re.search(r'veredito_bateria": "(\w+)"', _bn); bat = _m.group(1) if _m else "NAO LIDO"


def passou(H):
    return bool(H and H.get("tudo_passou") is True and not H.get("nao_exigiu_refazer"))


def _arquivo_e(p, sha):
    return bool(sha) and os.path.exists(P(p)) and fh(p) == sha


cand_ok = bool(CM.get("sha16") and ES.get("candidato_sha16") == CM["sha16"] and h16("um_v407_candidato.py") == CM["sha16"] and sz("um_v407_candidato.py") == CM.get("bytes") and EN.get("sha16") == CM["sha16"])
N_MOD = _DL.N_BUNDLE   # 9 (o bundle da v407); o recibo do kernel, os ESPERADOS e o candidato concordam com ele, ou o portao reprova
PORTOES = {
    "kernel": bool(KR.get("rc") == 0 and KR.get("sorry") in (0, [], None) and PB.get("ok") is True and len(KR.get("pedras") or []) == N_MOD == (CM.get("kernel") or {}).get("modulos_novos") and FJ.get("n_flags") == ES.get("n_bandeiras_novas") == CM.get("n_bandeiras")),
    "candidato": cand_ok,
    "ast_v406_v407": bool(CMP.get("ok") is True and CMP.get("removidos") in (0, []) and CMP.get("mudados_sem_explicacao") in (0, []) and CMP.get("o_gate_nao_se_move_e_a_v386_nao_e_reescrita") is True),
    "ensaio_a_seco": bool(EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == CM.get("sha16")),
    "conferidor_controle_negativo": bool(CN.get("tudo_bate") is False and CN.get("nao_pode_mudar") and all(CN["nao_pode_mudar"].values()) and CN.get("um_py_sha16") != CM.get("sha16")),
    "conferidor_caminho_positivo": bool(CP.get("tudo_bate") is True and CP.get("um_py_sha16") == CM.get("sha16")),
    "citacoes": bool(CIT.get("todas_conferem") is True),
    "guarda_das_frases": bool(GF.get("ok") is True and GF.get("pedras_limpas") is True and len(GF.get("pedras") or {}) == N_MOD),   # (v407: as nove pedras, todas da gerencia)
    "instalar_reverter_rito_estatico": bool(not DRV.get("falhas")),
    "p00": bool(PC.get("ok") is True and n_p00 > 0 and not falhas_p00 and not PC.get("pendentes")),
    "bn_pre_selo": bool(PR.get("veredito") == "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA" and PR.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and PROV.get("producao_intacta") is True and bat == "BATERIA_PASSA" and (PN.get("candidato") or {}).get("sha256") == CM.get("sha256")),
    "servico_estatico": bool(SERV.get("n_condicoes") and SERV.get("n_condicoes_ok") == SERV.get("n_condicoes") and CTRL.get("toda_mutacao_foi_pega") is True),
    "harness_textos": passou(H_T),
    "harness_fechar": passou(H_F),
    "refazer_limpo": fim_ok,
    "purga_da_fala_reservada": bool((tenta("purga_v407.json") or {}).get("total_com_ocorrencia") == 0),
    "fala_excluida_fora_dos_artefatos": bool((tenta("purga_v407.json") or {}).get("fala_excluida_total_com_ocorrencia") == 0),
}
falta = [k for k, v in PORTOES.items() if not v]
pronta = not falta
n_neg_leit = len((H_T or {}).get("etapas", {}).get("leitura_negativos", {}).get("controles", []))
n_neg_fech = len((H_F or {}).get("etapas", {}).get("fechar_negativos", []))
n_neg_par = len((H_T or {}).get("etapas", {}).get("paragrafo_v407_e_citacoes", {}).get("negativos", []))
ROTA = ABERTA.get("rota_id") or "NAO LIDA (registro_mapa_prep_v407_ABERTA.json)"   # a rota da preparacao da v407 no Mapa de Rotas (aberta pela gerencia; lida do registro dela)
_nome_op = dict(getattr(_DL, "NOME_DO_OPERADOR", {}) or {})
_anc_mod = {rel_: len(nomes_) for rel_, nomes_ in _DL.ANCORAS_POR_MODULO.items()}
_flags_mod = dict(FJ.get("n_por_modulo") or {})
_bun = ((CM.get("kernel") or {}).get("bundle")) or {}
tab_pedras = "\n".join("| `%s` | %s (antes: `%s`) | %s | %s | `%s` |" % (rel_.split("/")[-1], _DL.BUNDLE_POR_REL[rel_].get("tipo_do_nome"), _DL.BUNDLE_POR_REL[rel_].get("nome_antigo"), _anc_mod.get(rel_), _flags_mod.get(rel_), (_bun.get(rel_) or {}).get("sha16")) for rel_ in _DL.BUNDLE_RELS)
tab_chave = "\n".join("| `%s` | `%s` | `%s` |" % (n_, (_DL.ANCORAS.get(n_) or {}).get("rel"), (FJ.get("bandeira_da_testemunha") or {}).get(n_)) for n_ in (_DL.ANCORA_LEMA, _DL.ANCORA_PAR))
try:
    prep_seq = [json.loads(l) for l in open(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", encoding="utf-8") if l.strip() and ('"' + ROTA + '"') in l]
    seqs = ", ".join("%s (%s)" % (r["seq"], r["tipo"]) for r in prep_seq if r.get("rota_id") == ROTA)
except Exception as e:   # noqa: BLE001
    seqs = "nao lido: %r" % (e,)
ARQ = ["um_v407_candidato.py", "CANDIDATO_v407.json", "ESPERADOS_v407.json", "ensaio_a_seco_v407.json", "COMPARACAO_V406_v407.json", "PINOS_BN_v407.json", "PINO_RECIBO_PRE_SELO_v407.json", "PROVA_PRODUCAO_INTACTA_v407_pre_selo.json", "PRECONDICOES_v407.json", "GUARDA_FRASES_v407.json", "VERBATIM_CONGELADO_v407.json", "BUNDLE_v407.json", "kernel_modulos_novos_v407.json", "CONTRATO_DA_CADEIA_v407.md", "DESENHO_v407.md", "PLANO_v407_GERENCIA.md",
       "delta_v407.py", "registros_v407.py", "runtime_v407.py", "guarda_frases_v407.py", "guarda_ordem_de_chamada_v407.py", "gerar_candidato_v407.py", "gerar_esperados_v407.py", "artigo_pt_v407.pysnip", "artigo_en_v407.pysnip", "comparar_v406_v407.py", "instalar_v407.py", "reverter_v407.py", "rito_v407.sh", "conferir_rito_v407.py", "conferir_citacoes_v407.py", "p00_precondicoes_v407.py",
       "pos_rito/textos_v407.semente", "pos_rito/montar_textos_v407.py", "pos_rito/leitura_v407.py", "pos_rito/fechar_v407.py", "pos_rito/registrar_mapa_v407.py", "pos_rito/superficies_v407.py", "pos_rito/harness_textos_ensaio_v407.py", "pos_rito/harness_fechar_sandbox_v407.py", "pos_rito/chain_pos_rito_v407.sh", "pos_rito/gerar_x_custodia_v407.py"] \
      + ["pedra/" + r_.split("/")[-1] for r_ in _DL.BUNDLE_RELS] + ["kernel/KERNEL_RECIBO_v407.json", "kernel/FLAGS_v407.json", "kernel/KH_N1_v407.json", "kernel/POS_BUILD_v407.json"]
HASHES = {p: {"sha16": h16(p), "bytes": sz(p)} for p in ARQ if os.path.exists(P(p))}
tab_arq = "\n".join("| `%s` | %s | `%s` |" % (p, format(v["bytes"], ","), v["sha16"]) for p, v in HASHES.items())
_apont = (CIT.get("apontadas_a_gerencia_aspas") or [])
_apont_gf = list(getattr(_GFM, "APONTADAS_A_GERENCIA", ()) or ())
_esc = ES.get("escada_v406_e_v407") or CM.get("escada") or ["?", "?"]
_cob = ES.get("cobertura_kh_n1") or {}; _dkh = KH.get("delta_vs_v406") or {}
AVISOS = [
    "os nomes das nove pedras sao do operador (PsionCanto aceito, Par dado, as sete de 02/11 ratificados em 03/11/2026); o sufixo R1 dos arquivos de origem era marca de revisao e saiu (BUNDLE_v407.json guarda nome_antigo, sha256 da origem e o numero de linhas #print axioms removidas na normalizacao)",
    "a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma passa de literal False (v396 a v406) a LEITURA do kernel do rito (errata E18 AO LADO; o texto selado das versoes anteriores nao e' reescrito); as quatro chaves da v406 seguem True; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos de rede_fock_v394, psibit_v395, testemunha_estatica_v396 e fechamento_v406 NAO mudam (nenhuma troca dita de texto: os que carregam a escada mudam so' em numeros)",
    "ressalvas ditas em todo texto: o elo das duas faces e' de ESTRUTURA (Omega e Phi+ nao sao identificados: espacos distintos); a face de Fock do par segue [OPEN] (o FockCertificate nao tem operadores de criacao como termo); a ponte entre o espaco de Bell e o setor TT do spin 2 nao e' termo; K(O) != bot so' na cunha; o teste (d) so' consta por CITACAO do pre-registro V1.1 (D44); o motor continuo fica fora (D45)",
    "tres das sete pedras de 02/11 foram revistas pelo Sonnet (KEhATangente, APonteDoAtrito, OUmInscrito); AChaveDaGuarda, OGuarda, LeituraPreservada e OIgual NAO foram; PsionCanto e Par (03/11) tambem nao: a revisao de terceiro desta versao ainda nao aconteceu",
    "o revisor distinto da v407 e' o Sonnet (D47, ordem do operador); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar",
    "APONTADO a gerencia, NAO corrigido (o agente nao edita pedra revista): %d trecho(s) de pedra que a regra lexical F16 da guarda das frases reprova (o trecho de OUmInscrito sobre o setor de uma particula; o enunciado esta em guarda_frases_v407.APONTADAS_A_GERENCIA e nao e' repetido aqui para nao reprovar este relatorio na mesma guarda); a gerencia decide se reescreve (BAIXO)" % len(_apont_gf),
    "a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache",
    "o B(n) pre-selo da v407 (passo simples %s; a Bancada de producao pina %s) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes" % (DL_B_N, DL_BANCADA),
    "conferir_citacoes_v407.json aponta %d citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): %s; o agente nao corrige texto da gerencia" % (len(_apont), "; ".join("%s: %s" % (a_["arquivo"], a_["trecho"]) for a_ in _apont) or "nenhuma"),
    "build a frio dos %d modulos no sandbox k407c: %s s, Audit %s s (kernel/POS_BUILD_v407.json, medidos); %s declaracoes no axiom_report (+%s decl, +%s teoremas sobre a v406), nenhuma fora do trio; escada %s -> %s" % (N_MOD, PB.get("duracao_build_s"), PB.get("duracao_audit_s"), KH.get("axiom_report_efetivo_n"), _dkh.get("decl"), _dkh.get("thm"), _esc[0], _esc[1]),
]
NAO_REVISADO = "este candidato (o psion, o canto e o par, v407) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D47, ordem do operador) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova"
_REV = tenta("revisao_terceiro/REVISAO_TERCEIRO_v407.json") or {}
REVISAO_OK = bool(_REV.get("aprovada") is True and _REV.get("candidato_sha16") == CM.get("sha16") and not _REV.get("n_alto") and not _REV.get("n_medio"))
if REVISAO_OK:   # a revisao de terceiro existe e aprova ESTE candidato: o texto «NAO foi revisado» deixa de valer; o aviso novo diz o que foi e o que NAO foi examinado (nada e' inventado: tudo lido do JSON da revisao)
    NAO_REVISADO = ("este candidato (o psion, o canto e o par, v407) FOI revisado por terceiro: %s, rodada %s, aprovada, %s ALTO, %s MEDIO, %s BAIXO (revisao_terceiro/REVISAO_TERCEIRO_v407.md, sha16 %s); quem constroi nao aprova: a aprovacao e' do revisor, nao desta preparacao; "
                    "as ressalvas BAIXAS estao escritas no caderno e valem como ditas (sem terceira rodada para BAIXO); a trava do orquestrador (S1b) confere aprovada e o sha16 do candidato" % (_REV.get("revisor"), _REV.get("rodada"), _REV.get("n_alto"), _REV.get("n_medio"), _REV.get("n_baixo"), h16("revisao_terceiro/REVISAO_TERCEIRO_v407.json")))
    AVISOS = [a_ for a_ in AVISOS if "ainda nao acontece" not in a_ and "esta preparacao NAO foi revisada por terceiro" not in a_]
    AVISOS.append("revisao de terceiro (Sonnet D47): " + NAO_REVISADO)
    AVISOS.append("ressalvas BAIXAS da revisao (nenhuma trava; ver o caderno): " + " | ".join("%s" % (a_.get("onde") or "")[:70] for a_ in (_REV.get("achados") or []) if a_.get("sev") == "BAIXO"))
_vp = (CIT.get("varredura_das_pedras") or {})
_cong407 = tenta("VERBATIM_CONGELADO_v407.json") or {}
ERRATAS_V407_RES = {"erratas": ["E18", "E19", "E20"], "E18": _DL.ERRATAS_V407[0].split(";")[0][:300], "E19": _DL.ERRATAS_V407[1].split(";")[0][:300], "E20": _DL.ERRATAS_V407[2].split(";")[0][:300],
                    "falas_embutidas": len(_cong407.get("arquivos") or []), "citacoes_da_candidata": {"conferidas": _vp.get("citacoes_conferidas"), "reprovadas": len(_vp.get("reprovadas") or []), "so_sem_acento": _vp.get("so_sem_acento")}}
PRONTA = {"contrato": "PREPARACAO_v407_PRONTA", "agente": "claude-prep-v407", "quando": AGORA.strftime("%Y-%m-%d %H:%M:%S"), "pronta": pronta, "falta": falta, "portoes": PORTOES,
          "candidato_sha16": CM.get("sha16"), "candidato_sha256": CM.get("sha256"), "candidato_bytes": CM.get("bytes"), "origem_sha16": CM.get("base_v406_sha16"), "escada": ES.get("escada_v406_e_v407") or CM.get("escada"), "n_bandeiras_novas": ES.get("n_bandeiras_novas"), "n_modulos_novos": (CM.get("kernel") or {}).get("modulos_novos"),
          "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v407.json", "sha16": h16("kernel/KERNEL_RECIBO_v407.json") if os.path.exists(P("kernel/KERNEL_RECIBO_v407.json")) else None, "rc": KR.get("rc")},
          "esperados_sha16": h16("ESPERADOS_v407.json") if os.path.exists(P("ESPERADOS_v407.json")) else None, "p00": {"ok": PC.get("ok"), "passaram": ok_p00, "n": n_p00, "pendentes": pendentes_p00, "sha16": h16("PRECONDICOES_v407.json") if os.path.exists(P("PRECONDICOES_v407.json")) else None},
          "ensaio_a_seco": {"veredito": EN.get("veredito"), "sha16_do_candidato": EN.get("sha16"), "json_sha16": h16("ensaio_a_seco_v407.json") if os.path.exists(P("ensaio_a_seco_v407.json")) else None},
          "comandos": {"instalar": "python -B -X utf8 instalar_v407.py", "rito": "sh rito_v407.sh", "cadeia": "CHAIN_DE=<rotulo> CHAIN_ATE=<rotulo> sh pos_rito/chain_pos_rito_v407.sh (rotulos 0..10 10a 10b 10c 11..14; 10b com B3_AUTORIZADO=sim, EVENTO e EVENTO_HASH)", "cwd": HERE,
                       "reverter": "python -B -X utf8 reverter_v407.py (so' por decisao da gerencia)"},
          "hashes": HASHES, "nao_revisado_por_terceiro": NAO_REVISADO, "trava_do_orquestrador": ("S1b (pos_treino_v407): ABERTA pela revisao_terceiro/REVISAO_TERCEIRO_v407.json (aprovada, mesmo sha16 do candidato); a preparacao nao a abriu: o revisor abriu" if REVISAO_OK else "S1b (pos_treino_v407): fechada ate' revisao_terceiro/REVISAO_TERCEIRO_v407.json aprovar ESTE candidato (revisor: Sonnet); esta preparacao nao a abre"), "revisao_de_terceiro": ({"aprovada": _REV.get("aprovada"), "rodada": _REV.get("rodada"), "n_alto": _REV.get("n_alto"), "n_medio": _REV.get("n_medio"), "n_baixo": _REV.get("n_baixo"), "candidato_sha16": _REV.get("candidato_sha16"), "sha16_do_json": h16("revisao_terceiro/REVISAO_TERCEIRO_v407.json"), "revisor": _REV.get("revisor"), "quando": _REV.get("quando")} if REVISAO_OK else None), "erratas_E18_E20": ERRATAS_V407_RES, "avisos": AVISOS, "rota_no_mapa": "%s (seq %s)" % (ROTA, seqs)}


def grava(nome, b):
    p = P(nome)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + ST; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p)


fr = _DL.FRASE_DA_MOLDURA_V407_PT
_ressalvas_txt = "\n".join("  %d. %s" % (i_ + 1, r_) for i_, r_ in enumerate(_DL.RESSALVAS_V407))
PLANO = f"""# PLANO da v407 — O psíon, o canto e o par (preparação)

Agente de preparação `claude-prep-v407`, {AGORA.strftime('%Y-%m-%d %H:%M')}. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v406 selada `{CM.get('base_v406_sha16')}`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: {fr}.

## 0. A ordem

- [INPUT, operador, 03/11/2026] «{_DL.FRASE_LEMA_PSION}»; e: «{_DL.FRASE_PROSSIGAMOS}»; os nomes: «{_DL.FRASE_NOMES_RATIFICADOS}». As {len(ES.get('cunhagens') or CM.get('cunhagens') or {})} falas de 03/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v407.json`; as 23 de 02/11 já estão no um.py v406 e não entram de novo).
- (A) O BUNDLE: {N_MOD} módulos de kernel em `TGLExt/` (PsionCanto, Par e as sete pedras de 02/11 de nome ratificado), compilados no sandbox `{(CM.get('kernel') or {}).get('sandbox')}`, a raiz com {N_MOD} imports. (B) O registro com função `psion_canto_v407` ({_DL.N_CHECKS_FECHO} checagens) e os registros por spec `cunhagens_v407` e `kh_n1_cobertura_v407`. (C) A chave `linked_to_the_corner_by_a_lemma`, de literal False a leitura do kernel; os specs da v406 que a cobravam falsa são versionados (E20). (D) A seção «O psíon e o canto: a passagem sob compressão e o par» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v406 por script.

## 1. Os módulos e as âncoras [REAL, sandbox; nada tocado no Nós]

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
{tab_pedras}

As duas âncoras que carregam a chave e o par:

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
{tab_chave}

Pós-build: {PB.get('n_axiomas_lidos_no_audit')} axiomas lidos no Audit, {PB.get('n_flags')} bandeiras novas (só declaração nomeada), escada {_esc[0]} → {_esc[1]}; build a frio {PB.get('duracao_build_s')} s, Audit {PB.get('duracao_audit_s')} s.

## 2. O que a v407 afirma e o que não afirma

- [REAL] `TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces`: nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor sobre ele; escalariza; pesa 1; o motor comprimido devolve o canto. O elo é de ESTRUTURA, não de vetores. A chave é lida do kernel do próprio rito, só com o trio de axiomas.
- [ONTO sob a leitura do operador, composição de termos que já existiam] o par é ligado, nunca se cancela, e a leitura se faz pelo gráviton (pedra `Par`).
- [REAL] O que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`); as quatro chaves da v406 seguem lidas do kernel.
- Ressalvas ditas ({len(_DL.RESSALVAS_V407)}):
{_ressalvas_txt}
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é confirmação; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v407_candidato.py` `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; +{format(CM.get('delta_bytes') or 0, ',')} B); {CM.get('n_patches')} patches; AST: {CMP.get('nos_nomeados_v406')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (todos explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos. Ensaio a seco: **{EN.get('veredito')}**. Pós-rito: `pos_rito/chain_pos_rito_v407.sh`, rótulos 0…10 10a 10b 10c 11…14.

## 4. Gates

Ver `PREPARACAO_v407_PRONTA.json`: `pronta` = {str(pronta).lower()}. {NAO_REVISADO}.
"""
RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v407 — O psíon, o canto e o par

Agente de preparação `claude-prep-v407` · {AGORA.strftime('%Y-%m-%d %H:%M')} · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: {NAO_REVISADO}.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; base v406 `{CM.get('base_v406_sha16')}`): `pronta` = **{str(pronta).lower()}**{'' if pronta else '; falta: ' + ', '.join(falta)}.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `{(CM.get('kernel') or {}).get('sandbox')}`) | {PORTOES['kernel']}: build + Audit rc {KR.get('rc')}, {PB.get('n_flags')} bandeiras novas, escada {_esc[0]} → {_esc[1]}, {len(KR.get('pedras') or [])} módulos no recibo; `KERNEL_RECIBO_v407.json` |
| candidato | {PORTOES['candidato']}: {CM.get('n_patches')} patches; refazer limpo = {fim_ok} |
| AST v406 × v407 | {PORTOES['ast_v406_v407']}: {CMP.get('nos_nomeados_v406')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos; {len(CMP.get('funcoes_intactas') or {})} funções e constantes intactas, todas verdadeiras = {all((CMP.get('funcoes_intactas') or {'x': False}).values())} |
| ensaio a seco | {PORTOES['ensaio_a_seco']}: {EN.get('veredito')} |
| conferidor | negativo {PORTOES['conferidor_controle_negativo']} (`tudo_bate` = {CN.get('tudo_bate')}); positivo {PORTOES['conferidor_caminho_positivo']} (`tudo_bate` = {CP.get('tudo_bate')}) |
| citações | {PORTOES['citacoes']}: {len(CIT.get('apontadas_a_gerencia_aspas') or [])} apontada(s) à gerência (ver §4) |
| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo e as {len(GF.get('pedras') or {})} pedras) |
| instalar / reverter / rito (estático) | {PORTOES['instalar_reverter_rito_estatico']} |
| p00 | {PORTOES['p00']}: {ok_p00}/{n_p00} checagens OK; pendentes: {len(pendentes_p00)} |
| B(n) pré-selo | {PORTOES['bn_pre_selo']}: {PR.get('veredito')}; bateria {bat}; produção intacta = {PROV.get('producao_intacta')}; recibo `{h16('PINO_RECIBO_PRE_SELO_v407.json') if os.path.exists(P('PINO_RECIBO_PRE_SELO_v407.json')) else None}` |
| serviço da Bancada (estático) | {PORTOES['servico_estatico']}: {SERV.get('n_condicoes_ok')}/{SERV.get('n_condicoes')} condições; toda mutação pega = {CTRL.get('toda_mutacao_foi_pega')} |
| harness dos textos | {PORTOES['harness_textos']}: {n_neg_leit} controles da leitura, {n_neg_par} do parágrafo novo |
| harness do fechar | {PORTOES['harness_fechar']}: {n_neg_fech} controles do fechar |
| regeneração limpa | {PORTOES['refazer_limpo']}: `refazer_out_v407.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v407.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | {PORTOES['fala_excluida_fora_dos_artefatos']}: `purga_v407.json`, zero ocorrências |

## 3. O que NÃO passou ou fica para depois

- p00 reprova {len(falhas_p00)} checagem(ns): {'; '.join(f[:200] for f in falhas_p00) if falhas_p00 else 'nenhuma'}; pendentes ({len(pendentes_p00)}): {'; '.join(f[:160] for f in pendentes_p00) if pendentes_p00 else 'nenhum'}.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo e o fechar; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `{ROTA}`, seq {seqs}.

## 4. Avisos e desvios ditos

{chr(10).join('- ' + a for a in AVISOS)}

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D47), nesta ordem, antes de qualquer publicação: `delta_v407.py` (moldura, erratas E18 a E20, decisões D41 a D47), `registros_v407.py`, `runtime_v407.py` (as {_DL.N_CHECKS_FECHO} checagens de `psion_canto_v407`), `pedra/PsionCanto.lean` e `pedra/Par.lean` (as outras sete foram revistas em parte em 02/11), as seções do artigo (`artigo_pt_v407.pysnip`, `artigo_en_v407.pysnip`) e `pos_rito/textos_v407.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v407 NÃO entrega: validade no kernel não é creditação; o lema liga as duas faces do psíon por ESTRUTURA (Omega e Phi+ não são identificados); a face de Fock do par segue aberta e a ponte entre o espaço de Bell e o setor TT não é termo; K(O) ≠ ⊥ só vale na cunha; as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; o teste com a natureza segue da natureza e nenhum teste novo entra nesta versão.
3. O orquestrador lê `PREPARACAO_v407_PRONTA.json` e segue: `instalar_v407.py`, `rito_v407.sh`, `pos_rito/chain_pos_rito_v407.sh` (0 → 10, 10a, 10b, 10c → 14), com a trava S1b aberta só pela revisão aprovada.
4. Se o rito cair: `reverter_v407.py` é decisão da gerência; `refazer_candidato_v407.sh --regerar` refaz o candidato.

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
grava("PLANO_v407.md", PLANO.encode("utf-8")); grava("RELATORIO_PREPARACAO_v407.md", RELATORIO.encode("utf-8"))
HASHES["PLANO_v407.md"] = {"sha16": h16("PLANO_v407.md"), "bytes": sz("PLANO_v407.md")}; HASHES["RELATORIO_PREPARACAO_v407.md"] = {"sha16": h16("RELATORIO_PREPARACAO_v407.md"), "bytes": sz("RELATORIO_PREPARACAO_v407.md")}
grava("PREPARACAO_v407_PRONTA.json", json.dumps(PRONTA, ensure_ascii=False, indent=1).encode("utf-8"))
print("pronta =", pronta, "| falta:", falta)
print("candidato", CM.get("sha16"), "| kernel recibo", PRONTA["kernel_recibo"]["sha16"], "| ESPERADOS", PRONTA["esperados_sha16"], "| p00", PRONTA["p00"]["sha16"], "(%d/%d)" % (ok_p00, n_p00))
print(P("PREPARACAO_v407_PRONTA.json"))
