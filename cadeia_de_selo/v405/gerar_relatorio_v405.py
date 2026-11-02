# -*- coding: utf-8 -*-
"""gerar_relatorio_v405.py -- escreve PLANO_v405.md, RELATORIO_PREPARACAO_v405.md e PREPARACAO_v405_PRONTA.json. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta no momento da geracao (nada digitado); a prosa e' da preparacao.
`pronta` e' CALCULADA: true so' se TODOS os portoes passaram (kernel, candidato, AST, ensaio a seco, conferidor, citacoes, guarda das frases, p00, B(n) pre-selo, harnesses); um arquivo que falta ou nao le reprova o portao (fail-closed), nunca o contrario.
Rodar DEPOIS de refazer_candidato_v405.sh e dos dois harnesses (sem --nao-exigir-refazer). Backup de bytes do que ja' existe; temporario -> conferir -> substituir. uso: python -I -B -X utf8 gerar_relatorio_v405.py"""
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


CM = tenta("CANDIDATO_v405.json") or {}; ES = tenta("ESPERADOS_v405.json") or {}; EN = tenta("ensaio_a_seco_v405.json") or {}; PC = tenta("PRECONDICOES_v405.json") or {"ok": False, "checagens": []}
PR = tenta("PINO_RECIBO_PRE_SELO_v405.json") or {}; PROV = tenta("PROVA_PRODUCAO_INTACTA_v405_pre_selo.json") or {}; CMP = tenta("COMPARACAO_V404_v405.json") or {}; KR = tenta("kernel/KERNEL_RECIBO_v405.json") or {}; PB = tenta("kernel/POS_BUILD_v405.json") or {}; FJ = tenta("kernel/FLAGS_v405.json") or {}
CN = tenta("conferencia_rito_v405_CONTROLE_NEGATIVO_PRE_RITO.json") or {}; CP = tenta("conferencia_rito_v405_POSITIVO_FALSO_NOS.json") or {}; CIT = tenta("conferir_citacoes_v405.json") or {}; GF = tenta("GUARDA_FRASES_v405.json") or {}; DRV = tenta("DERIVACAO_v405.json") or {"falhas": ["DERIVACAO_v405.json ausente"]}
SERV = tenta("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v405.json") or {}; CTRL = tenta("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v405.json") or {}; PN = tenta("PINOS_BN_v405.json") or {}
H_T = tenta("pos_rito/HARNESS_TEXTOS_ENSAIO_v405.json"); H_F = tenta("pos_rito/HARNESS_FECHAR_SANDBOX_v405.json")
refazer = open(P("refazer_out_v405.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("refazer_out_v405.txt")) else ""
fim_ok = "== FIM" in refazer and refazer.rstrip().endswith("RC_REFAZER=0")
falhas_p00 = [c["checagem"] for c in PC["checagens"] if not c["ok"]]
ok_p00 = sum(1 for c in PC["checagens"] if c["ok"]); n_p00 = len(PC["checagens"])
_bn = open(P("bateria_pre_selo/bn_pre_selo_out_v405.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("bateria_pre_selo/bn_pre_selo_out_v405.txt")) else ""
_m = re.search(r'veredito_bateria": "(\w+)"', _bn); bat = _m.group(1) if _m else "NAO LIDO"


def passou(H):
    return bool(H and H.get("tudo_passou") is True and not H.get("nao_exigiu_refazer"))


def _arquivo_e(p, sha):
    return bool(sha) and os.path.exists(P(p)) and fh(p) == sha


cand_ok = bool(CM.get("sha16") and ES.get("candidato_sha16") == CM["sha16"] and h16("um_v405_candidato.py") == CM["sha16"] and sz("um_v405_candidato.py") == CM.get("bytes") and EN.get("sha16") == CM["sha16"])
PORTOES = {
    "kernel": bool(KR.get("rc") == 0 and KR.get("sorry") in (0, [], None) and PB.get("ok") is True and len(KR.get("pedras") or []) == 8 and FJ.get("n_flags") == ES.get("n_bandeiras_novas")),
    "candidato": cand_ok,
    "ast_v404_v405": bool(CMP.get("ok") is True and CMP.get("removidos") in (0, []) and CMP.get("mudados_sem_explicacao") in (0, []) and CMP.get("o_gate_nao_se_move_e_a_v386_nao_e_reescrita") is True),
    "ensaio_a_seco": bool(EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == CM.get("sha16")),
    "conferidor_controle_negativo": bool(CN.get("tudo_bate") is False and CN.get("nao_pode_mudar") and all(CN["nao_pode_mudar"].values()) and CN.get("um_py_sha16") != CM.get("sha16")),
    "conferidor_caminho_positivo": bool(CP.get("tudo_bate") is True and CP.get("um_py_sha16") == CM.get("sha16")),
    "citacoes": bool(CIT.get("todas_conferem") is True),
    "guarda_das_frases": bool(GF.get("ok") is True and GF.get("pedras_limpas") is True and len(GF.get("pedras") or {}) == 8),
    "instalar_reverter_rito_estatico": bool(not DRV.get("falhas")),
    "p00": bool(PC.get("ok") is True and n_p00 > 0 and not falhas_p00),
    "bn_pre_selo": bool(PR.get("veredito") == "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA" and PR.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and PROV.get("producao_intacta") is True and bat == "BATERIA_PASSA" and (PN.get("candidato") or {}).get("sha256") == CM.get("sha256")),
    "servico_estatico": bool(SERV.get("n_condicoes") and SERV.get("n_condicoes_ok") == SERV.get("n_condicoes") and CTRL.get("toda_mutacao_foi_pega") is True),
    "harness_textos": passou(H_T),
    "harness_fechar": passou(H_F),
    "refazer_limpo": fim_ok,
    "purga_da_fala_reservada": bool((tenta("purga_v405.json") or {}).get("total_com_ocorrencia") == 0),
    "fala_excluida_fora_dos_artefatos": bool((tenta("purga_v405.json") or {}).get("fala_excluida_total_com_ocorrencia") == 0),
}
falta = [k for k, v in PORTOES.items() if not v]
pronta = not falta
n_neg_leit = len((H_T or {}).get("etapas", {}).get("leitura_negativos", {}).get("controles", []))
n_neg_fech = len((H_F or {}).get("etapas", {}).get("fechar_negativos", []))
n_neg_par = len((H_T or {}).get("etapas", {}).get("paragrafo_v405_e_citacoes", {}).get("negativos", []))
pedras_es = (ES.get("kernel") or {}).get("pedras") or {}
tab_pedras = "\n".join("| `%s` | %s | `%s` | %s |" % (k, v.get("nome_do_operador"), v["sha16"], v["bandeiras"]) for k, v in pedras_es.items())
try:
    prep_seq = [json.loads(l) for l in open(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", encoding="utf-8") if l.strip() and '"kernel.v405.preparacao_01nov"' in l]
    seqs = ", ".join("%s (%s)" % (r["seq"], r["tipo"]) for r in prep_seq if r.get("rota_id") == "kernel.v405.preparacao_01nov")
except Exception as e:   # noqa: BLE001
    seqs = "nao lido: %r" % (e,)
ARQ = ["um_v405_candidato.py", "CANDIDATO_v405.json", "ESPERADOS_v405.json", "ensaio_a_seco_v405.json", "COMPARACAO_V404_v405.json", "PINOS_BN_v405.json", "PINO_RECIBO_PRE_SELO_v405.json", "PROVA_PRODUCAO_INTACTA_v405_pre_selo.json", "PRECONDICOES_v405.json", "GUARDA_FRASES_v405.json", "VERBATIM_CONGELADO_v405.json", "pedras_sha16_da_ordem.json",
       "delta_v405.py", "registros_v405.py", "runtime_v405.py", "guarda_frases_v405.py", "guarda_ordem_de_chamada_v405.py", "gerar_candidato_v405.py", "gerar_esperados_v405.py", "artigo_pt_v405.pysnip", "artigo_en_v405.pysnip", "comparar_v404_v405.py", "instalar_v405.py", "reverter_v405.py", "rito_v405.sh", "conferir_rito_v405.py", "p00_precondicoes_v405.py",
       "pos_rito/textos_v405_novo.pysnip", "pos_rito/montar_textos_v405.py", "pos_rito/textos_v405.py", "pos_rito/leitura_v405.py", "pos_rito/fechar_v405.py", "pos_rito/registrar_mapa_v405.py", "pos_rito/superficies_v405.py", "pos_rito/harness_textos_ensaio_v405.py", "pos_rito/harness_fechar_sandbox_v405.py", "pos_rito/chain_pos_rito_v405.sh", "pos_rito/gerar_x_custodia_v405.py",
       "kernel/KERNEL_RECIBO_v405.json", "kernel/FLAGS_v405.json", "kernel/KH_N1_v405.json"]
HASHES = {p: {"sha16": h16(p), "bytes": sz(p)} for p in ARQ if os.path.exists(P(p))}
tab_arq = "\n".join("| `%s` | %s | `%s` |" % (p, format(v["bytes"], ","), v["sha16"]) for p, v in HASHES.items())
AVISOS = [
    "o titulo da secao fica «A massa derivada e a identidade definida», porque vem da fala dele; a moldura diz que a derivacao e' da forma, dadas as entradas, e que a leitura fisica segue leitura (decisao da gerencia, errata R2)",
    "a ordem do operador pedia «tudo derivado»; isso nao foi alcancado e tem de ser dito a ele na lingua dele (regra do posto): os campos fecharam, as leituras da cadeia da massa entram como definicao ou identificacao; a fala dele de 01/11 14:19 diz «massa totalmente derivada» e «muito mais preciso», e os textos nao repetem nenhuma das duas",
    "a guarda das frases passou a varrer as oito pedras, com as falas como excecao, e a conferencia de citacoes passou a conferir as docstrings delas (conferir_citacoes_v405.json, varredura_das_pedras); as frases apontadas a gerencia estao la: o agente nao corrige pedra",
    "checks tautologicos: ficam, por decisao da gerencia, descritos como tal (g1, p6, d6, x7 e x10); so' o du_ do g1 saiu, porque comparava forma(57) com forma(57)",
    "os nomes de declaracao com derivad- (transicaoDerivada, leiDerivada, emprestimoDerivado, angulo_derivado_do_absoluto) ficam, por decisao da gerencia: as docstrings avisam",
    "tempoDoRetido como o tau* do sistema segue sem ratificacao do operador; a leitura 15 (o angulo de Miguel como o sistema do gap com unidade) tambem e' dele, nao teorema",
    "achado 5 da segunda revisao: a origem de stealth e' derivacao propria e condicional (prove_ga_mass_audit, v98); RECLASSIFICACAO_GA_01nov.md nao usa [KNOWN]: diz stealth sem etiqueta e sem a condicao, e ficou intacto",
    "BAIXO do instalar_v405.py (a janela minima: o recibo APLICADO so' e' gravado depois do os.replace) nao foi tocado: a revisao o deu por aceitavel e a ordem nao o pediu",
    "escolha do agente, dita: a composicao do registro da Lei do Diminuto passou a ser the_diminished_law_closes e a estrela modular_nao_e_transposicao; leiDerivada_no_um_posto e Lei.the_mass_formula seguem no contrato e nos checks",
    "os nomes de teorema the_scale_is_free, the_scale_is_the_invariant e no_positive_scale_invariant ficam, nomes assentados; no texto se diz valor absoluto",
    "o acorde do calculo tem notas de TESTE, numeros neutros de proposito; nenhuma nota da teoria e' nomeada; o unico intervalo escolhido e' o da terca, e^(3/2), o que o teorema diz",
    "m1 = 0 entra na lista das leituras sem termo no kernel (definicao_lean = None); os consumidores tratam esse caso",
    "a pasta revisao_terceiro cita a fala excluida em tres arquivos do revisor: nao foi tocada; a purga a deixa de fora e diz por que; a fala original segue no acervo (work), decisao da gerencia",
    "as falas embutidas estao congeladas em VERBATIM_CONGELADO_v405.json: fala nova do operador entra na proxima versao, salvo se a gerencia apagar o arquivo e regenerar",
    "o MD da reclassificacao do Grande Atrator cita «podemos reclassificá-lo...» com um acento que a fala nao tem e omite a quarta frase da errata do parecer; o registro traz as quatro frases lidas do parecer (terceira fonte pinada) e a citacao exata do operador",
    "o piso de definicao do Grande Atrator e' lido de core.mode_A/mode_B, os mesmos numeros que verdict.masses_Msun publica, porque _v405_rodar_specs recebe so' o core",
    "desvio do molde, dito: o passo 12 da cadeia REGISTRA no Mapa (uma vez, com marcador idempotente), porque o orquestrador roda 10c -> 14 de uma vez e 13 e 14 leem o mapa; na v404 esse registro era ato a mao",
    "desvio do molde, dito: o passo 14-bis da cadeia escreve o rascunho pos_rito/CUSTODIA_v405_RASCUNHO.txt (nao publica; falha ali nao para a cadeia); CUSTODIA_v405.txt no tunel segue ato da gerencia",
    "desvio do molde, dito: reverter_v405.py e instalar_v405.py passam a guardar tambem tgl_kernel_proof_manifest.json (licao 2 da v404)",
    "a saida dos harnesses mora em C:\\t\\h405 (caminho curto): os nomes longos das falas passavam do MAX_PATH do Windows na arvore emulada",
    "o contexto ACOM orfao cac35ffd-2ad4-51f0-bfbb-b893b9c7741a ficou da inscricao anterior; a referencia desta preparacao e' SESSION_REFERENCE_prep_v405.json",
    "o recibo R6 repete as entradas do R5 (com o sha256_antes do R5): o pino e o p00 leem a pedra mudada na R6 por depois diferente do R5, e a cadeia R6 -> R5 -> R4 -> R3 -> R2 fecha assim",
    "a reclassificacao do Grande Atrator diz a escala do setor; nos textos novos desta preparacao se le o valor absoluto do setor, pela regra da mensagem da gerencia de 19:03; o documento dela fica como esta",
    "nenhum nome do contrato com o orquestrador divergiu",
]
NAO_REVISADO = "este candidato (erratas R2 a R7) NAO foi revisado por terceiro: a primeira revisao de 01/11 reprovou a30f9f0ebf90c277, a segunda reprovou eaefcd095abbaee7, e a trava do orquestrador fica fechada ate uma nova revisao aprovar; a segunda revisao nao examinou leitura_v405, fechar, superficies, chain, registrar_mapa, harnesses nem o B(n) (quem constroi nao aprova)"
_vp = (CIT.get("varredura_das_pedras") or {})
_cong_r2 = tenta("VERBATIM_CONGELADO_v405.json") or {}
_falas_01nov = sorted(os.path.basename(p_) for p_ in (_cong_r2.get("arquivos") or []) if "OPERADOR_01nov_" in os.path.basename(p_) and "A_IDENTIDADE" not in os.path.basename(p_))
ERRATA_R2 = {"revisao_anterior": {"candidato": "eaefcd095abbaee7", "veredito": "NAO APROVADA (1 ALTO, 4 MEDIO, 11 BAIXO)", "caderno": "revisao_terceiro/REVISAO_TERCEIRO_v405.md"}, "revisao_primeira": {"candidato": "a30f9f0ebf90c277", "veredito": "NAO APROVADA (2 ALTO, 11 MEDIO, 10 BAIXO)", "caderno": "revisao_terceiro/REVISAO_TERCEIRO_v405_R1.md"},
             "recibo_vigente_das_pedras": "RECIBO_ERRATA_PEDRAS_R7_01nov.json", "falas_embutidas": len(_cong_r2.get("arquivos") or []), "falas_de_01nov_no_glob": _falas_01nov, "falas_novas_desde_o_congelamento_anterior": _cong_r2.get("novas_em_relacao_ao_anterior") or [], "falas_excluidas_sha16": ["25c09b91c2a226c7"],
             "citacoes_das_pedras": {"conferidas": _vp.get("citacoes_conferidas"), "rotulos": len(_vp.get("rotulos") or []), "reprovadas": len(_vp.get("reprovadas") or []), "apontadas_a_gerencia": _vp.get("apontadas_a_gerencia") or []},
             "guarda_das_frases_nas_pedras": {"limpas": GF.get("pedras_limpas"), "falas_retiradas": sum(v_.get("falas_retiradas", 0) for v_ in (GF.get("pedras") or {}).values())}}
PRONTA = {"contrato": "PREPARACAO_v405_PRONTA", "agente": "claude-prep-v405", "quando": AGORA.strftime("%Y-%m-%d %H:%M:%S"), "pronta": pronta, "falta": falta, "portoes": PORTOES,
          "candidato_sha16": CM.get("sha16"), "candidato_sha256": CM.get("sha256"), "candidato_bytes": CM.get("bytes"), "origem_sha16": CM.get("base_v404_sha16"), "escada": ES.get("escada_v404_e_v405"), "n_bandeiras_novas": ES.get("n_bandeiras_novas"),
          "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v405.json", "sha16": h16("kernel/KERNEL_RECIBO_v405.json") if os.path.exists(P("kernel/KERNEL_RECIBO_v405.json")) else None, "rc": KR.get("rc")},
          "esperados_sha16": h16("ESPERADOS_v405.json") if os.path.exists(P("ESPERADOS_v405.json")) else None, "p00": {"ok": PC.get("ok"), "passaram": ok_p00, "n": n_p00, "sha16": h16("PRECONDICOES_v405.json") if os.path.exists(P("PRECONDICOES_v405.json")) else None},
          "ensaio_a_seco": {"veredito": EN.get("veredito"), "sha16_do_candidato": EN.get("sha16"), "json_sha16": h16("ensaio_a_seco_v405.json") if os.path.exists(P("ensaio_a_seco_v405.json")) else None},
          "comandos": {"instalar": "python -B -X utf8 instalar_v405.py", "rito": "sh rito_v405.sh", "cadeia": "CHAIN_DE=<rotulo> CHAIN_ATE=<rotulo> sh pos_rito/chain_pos_rito_v405.sh (rotulos 0..10 10a 10b 10c 11..14; 10b com B3_AUTORIZADO=sim, EVENTO e EVENTO_HASH)", "cwd": HERE,
                       "reverter": "python -B -X utf8 reverter_v405.py (so' por decisao da gerencia)"},
          "hashes": HASHES, "nao_revisado_por_terceiro": NAO_REVISADO, "errata_r2": ERRATA_R2, "avisos": AVISOS, "rota_no_mapa": "kernel.v405.preparacao_01nov (seq %s)" % seqs}


def grava(nome, b):
    p = P(nome)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + ST; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p)


fr = "um Um posto, uma α medida e as leituras do operador; dadas essas entradas, a FORMA é teorema"
PLANO = f"""# PLANO da v405 — A MASSA DERIVADA E A IDENTIDADE DEFINIDA (preparação)

Agente de preparação `claude-prep-v405`, {AGORA.strftime('%Y-%m-%d %H:%M')}. Estatutos: [REAL] lido aqui por script · [POSTO] · [MEDIDA] · [INPUT/ONTO] leitura do operador, que entra como definição · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v404 selada `{CM.get('base_v404_sha16')}`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura (errata da gerência c1, 01/11/2026): os campos das estruturas fecharam, as leituras do operador passaram do campo para a definição, a leitura física não virou teorema: {fr}.

## 0. A ordem

- [INPUT, operador, 01/11/2026] «é isso , perfeito, concordo com tudo, deixe tudo pronto para assim que o treinamento acabar, automaticamente rodar a nova versão do um.py e atualizar tudo». As {len(ES.get('cunhagens') or {})} falas de 30/10 a 01/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v405.json`).
- (A) Oito módulos de kernel com os nomes do operador. (B) Oito registros com função e cinco por spec (`cunhagens_v405`, `campos_fechados_e_leituras_v405`, `ga_reclassificacao_v405`, `gap_v405`, `kh_n1_cobertura_v405`). (C) As seções «A massa derivada e a identidade definida» e «A identidade» (o ensaio do operador, verbatim, r2 ratificada) no artigo PT/EN e a linha do `.md`. (D) Todo o resto derivado da v404 por script.

## 1. As oito pedras [REAL, sandbox `{(CM.get('kernel') or {}).get('sandbox')}`; nada tocado no Nós]

| módulo | nome do operador | sha16 | bandeiras |
|---|---|---|---|
{tab_pedras}

Sha256 lidos do recibo vigente das pedras (`insumos\\RECIBO_ERRATA_PEDRAS_R7_01nov.json`, cadeia de custódia R7 → R6 → R5 → R4 → R3 → R2 → primeira errata): nenhuma prova antiga caiu; seis nomes de teorema mudaram ao longo das erratas; o disco ganhou `the_flow_is_the_canonical_law`, o fecho do observador ganhou a leitura binária, a Lei do Diminuto ganhou o acorde e a modulação, a Tônica ganhou `the_ratio_survives_the_rescaling`, o Ponto Zero ganhou a seção O GAP. Pós-build: {PB.get('n_axiomas_lidos_no_audit')} axiomas lidos no Audit, {PB.get('n_flags')} bandeiras novas, escada {(ES.get('escada_v404_e_v405') or ['?', '?'])[0]} → {(ES.get('escada_v404_e_v405') or ['?', '?'])[1]}.

## 2. O que a v405 afirma e o que não afirma

- [REAL] a forma: dadas as entradas, `m₂ = β·sen45°·u`; o ½ da face absoluta; a unicidade de π/4; ½·√2 = sen45° é aritmética.
- [POSTO] o 1 / u = 1 eV. [MEDIDA] α, por dentro.
- [INPUT/ONTO, definição, não teorema] `massaDerivada`; o estado inscrito lido em θ = π/4 (`transicaoDerivada`: o ângulo é ESCRITO); a tônica (β/α)·u; R = β·u² (`pagamentoComoCurvatura`).
- O no-go de E₀ não cai: localiza-se no Um posto. A `Identidade` prova um fato sobre projeções no estado traço; que isso seja a identidade é leitura, tipada como modelo.
- O número da massa não muda; o veredito do canal do neutrino não muda; o gate não se move: as funções `evaluate_quantum_gravity_closure`, `prove_qg_closure_gate`, `prove_neutrino_mass_gravitational`, `ramo_b_preregistration_v386`, `ledger_errata_v386`, `prove_ga_mass_audit`, `prove_joint_coincidence_result_v3` e a constante `GA_WINDOW_STATUS` ficam idênticas (AST).
- O Grande Atrator, ao lado: de `A3_APOSENTADO` para `A13_FORMA_CONDICIONAL_SEM_INCERTEZA` (saída iii da ENTREGA 005); veto mantido; não é evidência; não discrimina da RG.

## 3. A cadeia

Candidato `um_v405_candidato.py` `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; +{format(CM.get('delta_bytes') or 0, ',')} B); {CM.get('n_patches')} patches; AST: {CMP.get('nos_nomeados_v404')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (todos explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos. Ensaio a seco: **{EN.get('veredito')}**. Pós-rito: `pos_rito\\chain_pos_rito_v405.sh`, rótulos 0…10 10a 10b 10c 11…14.

## 4. Gates

Ver `PREPARACAO_v405_PRONTA.json`: `pronta` = {str(pronta).lower()}. {NAO_REVISADO}.
"""
RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v405 — A massa derivada e a identidade definida

Agente de preparação `claude-prep-v405` · {AGORA.strftime('%Y-%m-%d %H:%M')} · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: {NAO_REVISADO}.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; base v404 `{CM.get('base_v404_sha16')}`): `pronta` = **{str(pronta).lower()}**{'' if pronta else '; falta: ' + ', '.join(falta)}.

## 1b. As erratas R2 a R7 (a primeira revisão de terceiro não aprovou `a30f9f0ebf90c277`; a segunda não aprovou `eaefcd095abbaee7`)

A revisão achou 2 ALTO, 11 MÉDIO e 10 BAIXO, todos de texto, nome ou docstring: nenhuma prova caiu e nenhum número físico estava errado. A gerência corrigiu as oito pedras nas origens (`RECIBO_ERRATA_PEDRAS_R2_01nov.json`); a revisita da Lei do Diminuto ordenada pelo operador mudou seis delas (`..._R3_01nov.json`); a resposta dele mudou três (`..._R4_01nov.json`: o diminuto é modulação, e a seção O GAP); um achado desta preparação mudou quatro (`..._R5_01nov.json`: a escala é o que fica parado); a guarda desta preparação pegou uma docstring da Tônica (`..._R6_01nov.json`); e a segunda revisão, 1 ALTO, 4 MÉDIO e 11 BAIXO, mudou três (`..._R7_01nov.json`, a referência vigente: `gap` virou `retidoNoAngulo`); o resto foi refeito aqui, pela cadeia existente.

| achado | o que foi feito |
|---|---|
| 1, 5, 6, 12 (pedras) | resolvidos pela gerência nas pedras; a E12 cita a pedra; D29 usa `FRASE_ALFA_CAUDA` com a grafia dele |
| 2 (homônimo) | token e check antigos fora; «o terminal lê 1» cita `the_fixed_points_read_one_and_zero`; o polo ω aparece como polo, homônimo dito, ligação [ONTO] do operador; checks o6 e o7 |
| 3, 4 (disco) | `E(t)` e `Ω²` são [DEF]; o fluxo é `the_flow_is_the_canonical_law` (check k7 novo); a taxa de dephasing lida como perda de energia é [INPUT/ONTO]; `Ω²` sem cota é [REAL]; a inscrição do zero no infinito e a terceira lei são [ONTO] |
| 7 (lista que não fecha) | «as leituras da cadeia da massa», catorze itens hoje, lista declarada não fechada (`lista_de_leituras_fechada = false`), com `meioTom`, `omegaSq`, `½ω = massa`, a hipótese de `area_por_volta_da_massa_inscrita`, `b = 0`, a taxa do disco; `g` e `κ` na moldura do artigo; token e chave novos |
| 8 (dispersão) | [INPUT, Tratado §3], entra como definição (`omegaSq`); só o ponto zero é [KNOWN] |
| 9 (fóton) | `foton_sem_massa` é álgebra de forma genérica; `b = 0` lido como o fóton é [ONTO]; o veredito do registro acompanha |
| 10 (observador) | ressalva dos rótulos e de `medido` no artigo PT/EN |
| 11 (ponto zero) | o que permanece no limite é [ONTO]: nenhum teorema liga os dois |
| 13 | «quatro níveis e cinco posições» |
| BAIXOS de texto e runtime | comentário e `Q_` em `v405_ponte_mechanics`, «a única massa», etiquetas de E12 e Tetelestai, «[DECISÃO da gerência c1…]», «not as a calculation» |
| título da seção | o título fica, porque vem da fala dele; a glosa saiu; a derivação é da forma, dadas as entradas |
| guardas novas | `guarda_frases` varre as oito pedras, com as falas como exceção, e tem controle negativo próprio; `conferir_citacoes` confere as docstrings das pedras, com as pedras FORA do corpus |
| a fala pessoal | lista de exclusão em `delta_v405.py`, por sha16 (o nome do arquivo não viaja); congelado regenerado; portão próprio na purga |
| R3 e R4: a Lei do Diminuto | o diminuto é modulação, não transposição: composição `the_diminished_law_closes`, estrela `modular_nao_e_transposicao`; `transpor` é só a liberdade do no-go; o `AcordeE0.lean` do Kimi é fonte pinada por sha256; `E0_relativo_pinado` é a definição dita como razão; as terças são a aritmética 1 nat + ½ nat; a espera é [ONTO] |
| R4: `gap_v405` | registro novo, ao lado, com onze checagens em runtime: Δ, τ, Γ_B, Q, a medida negativa do fluxo, τ ≠ t_P, κ como hipótese, K sem inclinação; `tempoDoRetido` como τ★ é [ONTO], a ratificar |
| R3: a frase do no-go | o valor absoluto segue livre e o no-go não cai; o valor relativo à tônica está pinado; sobra a transposição do acorde inteiro; as frases antigas viraram regra F6 da guarda, com controle negativo |
| R3: meio-tom e tônica | igualdades de valor; `CollapseCostLaw` [INPUT]; a calibração de 1 nat de 24/06 citada por sha256 como normalização definicional; `U_E_NOT_DERIVED` fica; `m₂` não muda |
| R3: as cinco notas | [OPEN] em todo texto; o acorde do cálculo é de teste; a pêntada são cinco componentes, não cinco autovalores |
| R3 e R4: a lista das leituras | `modular` (11), `m₁ = 0` (12, sem termo no kernel), `tempoDoGap` (13), α como inscrição elétrica (14) |
| R5 e R6: a escala | a escala é a musical, o que fica parado; onde o texto fala do acorde ou da Lei do Diminuto, e nos textos novos, o que era escala de energia é valor absoluto e valor relativo à tônica; fora disso «escala» como escala de energia é permitida, e a guarda só pega a colisão (F10, F11, F12); os dois teoremas rebatizados entram nos textos; `the_scale_is_free` fica como nome |
| R7, achado 1 (ALTO, o homônimo do gap) | o gap espectral do lock é 1, na unidade posta `u`, o `E₀` da Lei do Diminuto, e a tônica fica meio-tom acima dele; `Δ = β · u` é o valor esperado do lock no ângulo de Miguel, a energia retida, e não é gap (1/β vezes menor). Registro, artigos PT/EN, moldura e parágrafo público corrigidos; o nome do registro e o título O GAP ficam; que o ângulo de Miguel seja o sistema do gap com unidade é leitura [ONTO] dele (leitura 15, nova); check x11 novo, `x_h` e `x_i` no registro |
| R7, achado 2 (o lock em Hilbert) | os lemas do lock saem [REAL] em qualquer espaço de Hilbert; `HminMic` é instância (`HminMic_e_o_lock`), condicional a um `FockCertificate` que o kernel não habita: o registro lê `psibit_v395.conditional_psion_face.inhabitant_exhibited` = falso (check `x_i`) |
| R7, achado 3 (a inscrição e a medida) | [REAL] os dois teoremas existem; [ONTO, da gerência] lê-los como a forma da fala do operador; homônimo dito: `alphaKappa` não é a α de estrutura fina, e κ ali não é o relógio; gradiente negativo em κ > 0; a palavra cauda não está no teorema |
| R7, achado 4 (o tom) | [REAL] as notas sustentadas e as razões entre elas ficam; [INPUT] o tom fica, na fala dele: o kernel não tem termo para o tom |
| R7, achado 5 (stealth) | origem conferida: é derivação da própria teoria, condicional (`prove_ga_mass_audit`, v98: «[CONDICIONAL linear] M_TGL = M_RG», (P1)-(P4) + T1, Face C na ordem linear). A etiqueta passou de [KNOWN] a [DERIVED, condicional] no registro e nos textos. `RECLASSIFICACAO_GA_01nov.md` não tem o vício: não usa [KNOWN]; diz stealth sem etiqueta e sem a condição, e fica intacto |
| R7, BAIXOS | E10 e parágrafo público: «mais uma leitura do mesmo sen 45°»; x7 sem o número no `valor`, «como antecedente»; `gap_v405` no `__HEADER__`, em `topico_missao`, no remissivo e no cabeçalho de `rito_v405.sh`; `reverter_v405.py` com a guarda de -O e dizendo o que não restaura; «O que segue do operador» sem a revisão; a reescala «corresponde à» transposição; nomes `derivad-` ficam por decisão da gerência; checks tautológicos ficam, descritos como tal (g1, p6, d6, x7, x10) |
| R7, guarda | F13 recusa `Δ`, a energia retida ou 12,03 meV chamados de gap, em PT, EN e token; F14 recusa «a escala e o tom ficam»; as duas com controle negativo |
| guarda | F6 (a frase do no-go), F7 (τ★ e κ derivados), F8 (a escala ligada à transposição), F9 (κ = F como objetivo, sem a palavra proibido), F10 (a razão chamada de escala), F11 (o diminuto muda a escala), F12 (escala absoluta ou relativa), todas com controle negativo |
| R3 e R4: runtime | d7 a d12 na Lei do Diminuto, com controle negativo (o acorde modulado não é transposição) e `e^(3/2)`, e h7 na Tônica; `N_CHECKS` atualizado |

Citações das pedras: {_vp.get('citacoes_conferidas')} conferidas, {len(_vp.get('rotulos') or [])} rótulos listados, {len(_vp.get('reprovadas') or [])} reprovadas. **Apontadas à gerência, sem corrigir:** {'; '.join('%s: «%s» (%s)' % (a_['pedra'], a_['trecho'], a_['por_que']) for a_ in (_vp.get('apontadas_a_gerencia') or [])) or 'nenhuma'}.

Falas: {ERRATA_R2['falas_embutidas']} embutidas; novas em relação ao congelado anterior: {', '.join(ERRATA_R2['falas_novas_desde_o_congelamento_anterior']) or 'nenhuma'}; uma fala saiu pela lista de exclusão. Nenhum nome próprio de terceiro nas demais falas (varredura por capitalizadas, lista de prenomes e termos de parentesco; só aparecem o sobrenome do operador em «ângulo de Miguel», nomes da teoria e IAs).

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `{(CM.get('kernel') or {}).get('sandbox')}`) | {PORTOES['kernel']}: build + Audit rc {KR.get('rc')}, {PB.get('n_flags')} bandeiras novas, escada {(ES.get('escada_v404_e_v405') or ['?', '?'])[0]} → {(ES.get('escada_v404_e_v405') or ['?', '?'])[1]}; `KERNEL_RECIBO_v405.json` |
| candidato | {PORTOES['candidato']}: {CM.get('n_patches')} patches; refazer limpo = {fim_ok} |
| AST v404 × v405 | {PORTOES['ast_v404_v405']}: {CMP.get('nos_nomeados_v404')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos; {len(CMP.get('funcoes_intactas') or {})} funções e constantes intactas, todas verdadeiras = {all((CMP.get('funcoes_intactas') or {'x': False}).values())} |
| ensaio a seco | {PORTOES['ensaio_a_seco']}: {EN.get('veredito')} |
| conferidor | negativo {PORTOES['conferidor_controle_negativo']} (`tudo_bate` = {CN.get('tudo_bate')}); positivo {PORTOES['conferidor_caminho_positivo']} (`tudo_bate` = {CP.get('tudo_bate')}) |
| citações | {PORTOES['citacoes']} |
| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo e as oito pedras, com as falas como exceção) |
| instalar / reverter / rito (estático) | {PORTOES['instalar_reverter_rito_estatico']} |
| p00 | {PORTOES['p00']}: {ok_p00}/{n_p00} checagens OK |
| B(n) pré-selo | {PORTOES['bn_pre_selo']}: {PR.get('veredito')}; bateria {bat}; produção intacta = {PROV.get('producao_intacta')}; recibo `{h16('PINO_RECIBO_PRE_SELO_v405.json') if os.path.exists(P('PINO_RECIBO_PRE_SELO_v405.json')) else None}` |
| serviço da Bancada (estático) | {PORTOES['servico_estatico']}: {SERV.get('n_condicoes_ok')}/{SERV.get('n_condicoes')} condições; toda mutação pega = {CTRL.get('toda_mutacao_foi_pega')} |
| harness dos textos | {PORTOES['harness_textos']}: {n_neg_leit} controles da leitura, {n_neg_par} do parágrafo novo |
| harness do fechar | {PORTOES['harness_fechar']}: {n_neg_fech} controles do fechar |
| regeneração limpa | {PORTOES['refazer_limpo']}: `refazer_out_v405.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v405.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | {PORTOES['fala_excluida_fora_dos_artefatos']}: `purga_v405.json`, zero ocorrências |

## 3. O que NÃO passou ou fica para depois

- p00 reprova {len(falhas_p00)} checagem(ns): {'; '.join(f[:200] for f in falhas_p00) if falhas_p00 else 'nenhuma'}.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo e o fechar; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: seq {seqs}.

## 4. Avisos e desvios ditos

{chr(10).join('- ' + a for a in AVISOS)}

## 5. Lições desta subida

1. Regra de texto que entra no candidato mexe em tudo: juntar as mudanças antes de regenerar.
2. Heredoc do Bash colapsa barra invertida e quebra em apóstrofo desbalanceado: regra com barra vai por arquivo ou por `chr(92)`.
3. Nome longo de fala passa do MAX_PATH numa árvore emulada: a saída dos harnesses mora em caminho curto.
4. O JSON do rito real tem chaves no topo que o ensaio não guarda: a emulação lê a constante do próprio candidato, nunca de ESPERADOS.
5. A subida de versão funde os rótulos 403→404: as pastas irmãs (v403) e os registros da v404 recriados precisam de regra própria.
6. O G1 lê o cabeçalho do bloco da linhagem por regex: uma cláusula só antes de «N módulos novos». O harness dos textos agora confere com as MESMAS regex de `tools/custodia_g1/nos.py`.
7. A linha do handoff do índice saiu da âncora antiga (as linhas v392–v404 foram consolidadas): a superfície ancora na linha de 30/10 da v405.
8. O corpus de uma conferência de citações não pode conter o texto conferido: as pedras eram corpus da varredura, por isso as citações delas nunca reprovavam.
9. Guarda que não varre a origem deixa o resíduo onde ninguém olha: a moldura estava certa nos textos e errada nas docstrings.
10. Lista de leituras com tamanho fixo no código convida a fechá-la: a chave e as asserções passaram a dizer que a lista não é fechada.

## 6. Para a gerência — ordem sugerida

1. Revisão de terceiro, nesta ordem, antes de qualquer publicação: as oito pedras (`pedra/`), `delta_v405.py` (moldura, erratas, decisões), `registros_v405.py`, `runtime_v405.py` (as oito mecânicas e as medidas do Grande Atrator), as seções do artigo (`artigo_pt_v405.pysnip`, `artigo_en_v405.pysnip`) e `pos_rito/textos_v405_novo.pysnip`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v405 NÃO entrega: a ordem pedia que nenhuma hipótese restasse; os campos fecharam, as leituras da cadeia da massa entram como definição ou identificação e a leitura física não virou teorema. O teste do Grande Atrator muda de classe, ao lado, sem abrir dado e sem precisão nova: as escolhas da partitura são dele.
3. O orquestrador lê `PREPARACAO_v405_PRONTA.json` e segue: `instalar_v405.py`, `rito_v405.sh`, `pos_rito/chain_pos_rito_v405.sh` (0 → 10, 10a, 10b, 10c → 14). O passo 12 registra no Mapa; o 14-bis escreve o rascunho do post do X (não publica; `CUSTODIA_v405.txt` segue da gerência).
4. Se o rito cair: `reverter_v405.py` é decisão da gerência; `refazer_candidato_v405.sh --regerar` refaz o candidato; `pos_rito/adaptar_pos_rito_v405.py` e `montar_textos_v405.py` refazem o pós-rito a partir das sementes.

## 7. Pedras

| módulo | nome do operador | sha16 | bandeiras |
|---|---|---|---|
{tab_pedras}

## 8. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
{tab_arq}
"""
grava("PLANO_v405.md", PLANO.encode("utf-8")); grava("RELATORIO_PREPARACAO_v405.md", RELATORIO.encode("utf-8"))
HASHES["PLANO_v405.md"] = {"sha16": h16("PLANO_v405.md"), "bytes": sz("PLANO_v405.md")}; HASHES["RELATORIO_PREPARACAO_v405.md"] = {"sha16": h16("RELATORIO_PREPARACAO_v405.md"), "bytes": sz("RELATORIO_PREPARACAO_v405.md")}
grava("PREPARACAO_v405_PRONTA.json", json.dumps(PRONTA, ensure_ascii=False, indent=1).encode("utf-8"))
print("pronta =", pronta, "| falta:", falta)
print("candidato", CM.get("sha16"), "| kernel recibo", PRONTA["kernel_recibo"]["sha16"], "| ESPERADOS", PRONTA["esperados_sha16"], "| p00", PRONTA["p00"]["sha16"], "(%d/%d)" % (ok_p00, n_p00))
print(P("PREPARACAO_v405_PRONTA.json"))
