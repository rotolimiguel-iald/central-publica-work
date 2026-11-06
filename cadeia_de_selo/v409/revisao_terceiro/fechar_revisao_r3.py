# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R3, ULTIMA): monta REVISAO_TERCEIRO_v409.json / .md. R1 e R2 ficam ao lado (.R1/.R2.json/.md, r1_saidas/, r2_saidas/, PEDIDOs). sha16 de TUDO lido agora do arquivo. So escreve nesta pasta.
`aprovada` = 0 ALTO, 0 MEDIO, candidato integro do inicio ao fim e as conferencias que dependem do candidato sem falha inesperada (calculado aqui, nao digitado)."""
import datetime, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
RV = R + "revisao_terceiro/"
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda p: json.load(open(p, encoding="utf-8"))
cand_fim = sha16(R + "um_v409_candidato.py"); cand_ini = "53284ba461ecd940"   # lido ao abrir a R3 (= o da PRONTA)
r2 = J(RV + "REVISAO_TERCEIRO_v409.R2.json"); r1 = J(RV + "REVISAO_TERCEIRO_v409.R1.json")
rev_files = list(r2["arquivos_revisados"].keys())
arq = {k: sha16(R + k) for k in rev_files}
pronta = J(R + "PREPARACAO_v409_PRONTA.json")
mud_pronta = {}
for k, v in arq.items():
    pv = (pronta.get("hashes") or {}).get(k) or (pronta.get("hashes") or {}).get(k.replace("/", "\\"))
    if pv and pv.get("sha16") != v: mud_pronta[k] = (pv.get("sha16"), v)
mud_r2 = {k: (r2["arquivos_revisados"][k], v) for k, v in arq.items() if r2["arquivos_revisados"][k] != v}
agora = datetime.datetime.now().isoformat(timespec="seconds")

lean = J(RV + "lean_r1_out.json"); fontes_lean = J(RV + "b4_fontes_out.json")
cfc = J(RV + "c_fail_closed_out.json"); kv = J(RV + "k_funcoes_vivas_out.json"); c2 = J(RV + "c2_mecanica_direta_out.json"); a1 = J(RV + "a_intocados_out.json"); fh = J(RV + "f_hashes_out.json"); hg = J(RV + "h_guardas_out.json")
t6 = J(RV + "t6_varredura_independente_r3_out.json"); t5 = J(RV + "t5_guarda_probes_out.json"); t1b = J(RV + "t1b_fock_open_amplo_out.json")
n_cfc_ok = sum(1 for v in cfc.values() if v.get("ok") is True); n_cfc_f = [k for k, v in cfc.items() if v.get("ok") is False]
n_k_ok = sum(1 for v in kv.values() if v.get("ok") is True); n_k_f = [k for k, v in kv.items() if v.get("ok") is False]
n_c2_ok = sum(1 for v in c2.values() if v.get("ok") is True)
N_IGUAIS = sum(1 for v in a1["nomes"].values() if v.get("ast_igual") and v.get("fonte_igual")); N_HASH = sum(1 for v in fh["ok"].values() if v)
falhas_esperadas_cfc = {"guarda: Clay resolved", "guarda: a máquina sem leitor fica fora; P = nP não é o P = NP de Turing"}   # expectativas MINHAS de sondagem (R1/R2), nao defeito
falhas_hash_esperadas = {"varredura geral: todo {path, sha256} existente == disco"}
sondas_ok = all(s["ok"] is not False for s in t5)
t6_zero = all(len(t6[k]) == 0 for k in ("A", "B", "C"))
conds = {
    "candidato_integro": cand_fim == cand_ini, "mudados_27_novos_14": bool(a1["mud_igual_declarado"] and a1["nov_igual_declarado"] and not a1["removidos"]), "intocadas_38": N_IGUAIS == 38,
    "fail_closed_sem_falha_inesperada": set(n_cfc_f) <= falhas_esperadas_cfc, "k_funcoes_vivas": not n_k_f and n_k_ok >= 34, "c2": n_c2_ok == len(c2),
    "hashes_sem_falha_inesperada": {f[0] for f in fh["falhas"]} <= falhas_hash_esperadas, "controle_negativo_das_guardas": hg.get("controle_negativo_ok") is True,
    "sondas_da_guarda": sondas_ok and sum(1 for s in t5 if s["esperado_pegar"] is True and s["pega"]) >= 22, "minha_varredura_independente_zero": t6_zero,
    "nenhuma_pedra_mudou": all(arq[k] == r2["arquivos_revisados"][k] for k in arq if k.startswith("pedra/") or k.startswith("kernel/") or k.startswith("orquestrador/")),
}
aprovada_calculada = all(conds.values())
print("conds:", conds, "| mudaram desde a R2:", len(mud_r2), "| desde a PRONTA:", mud_pronta)

# ---- achados: os BAIXOS herdados (R1+R2) com o estado na R3
est = {
    "pos_rito/textos_v409_novo.pysnip:617-633": "ATENDIDO: `_paragrafo_v409_de` acha cada item do `diz` pelo CONTEUDO (`_diz(prefixo)`, recusa se nao achar UMA vez); o README/site rendido traz os marcadores certos («O dicionario de Turing» = o dicionario; «A trava no Nome» = a trava; «A maquina com o leitor», «A inscricao no psion», «O par na face de Fock» e «O que nao muda» proprios).",
    "artigo_pt_v409": "ATENDIDO nas frases-chave: «a igualdade completa esta' provada para o leitor que le tambem as maquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, nao creditacao); para o leitor que so' conta, nao esta' provada (E28, validade nao afirmada)» em artigo PT/EN, delta, registros e textos. Resto: formas antigas, corretas e com [KNOWN]/BGS na mesma ressalva (limites[0]: «vale para o leitor que se le (… BGS 1975 …) [KNOWN]»), mas `diz[3]` («ela vale para o leitor que se le») e `nao_diz[8]` seguem sem o selo; BAIXO, nao trava.",
    "o enunciado de uma_leitura_decide_SAT": "ABERTO (BAIXO): inalterado; o texto separa [REAL] de [KNOWN].",
    "runtime_v409.py v409_traducao_mechanics (c3": "ABERTO (BAIXO): inalterado; o texto ja' diz «aritmetica da instancia de brinquedo … quem prova e' o kernel».",
    "registros_v409.py (cunhagens_v409 u1": "ATENDIDO nos fontes que vao ao candidato (82, dois modulos, 20; sem «17 checagens|62 ancoras» em texto novo). O RELATORIO §6 e o PLANO §1 ainda rotulam o tipo do nome «…DECLARADO / DECLARADO_ate_a_ratificacao» (preparacao, nao publico): PARCIAL, BAIXO.",
    "pedra/TraducaoTuring.lean:15-17": "ABERTO (BAIXO, decisao D62): as docstrings embutidas seguem «[DECLARADO] ate a ratificacao».",
    "pedra/TraducaoTuring.lean:49-50": "ABERTO (BAIXO): citacoes ja' apontadas; nenhuma nova.",
    "runtime_v409.py _v409_guarda_frases (F43)": "PARCIAL: F41b/F40b/F42 estendidas e eficazes (22 de 22 sondas reprovam, 8 frases certas passam); a F43 so' exige a presenca da E28 e o EN curto «Clay resolved» segue sem F35 (BAIXO).",
    "kernel/FLAGS_v409.json": "ABERTO (BAIXO): 136 + 22 = 158, inalterado.",
    "pedra/TraducaoTuring.lean (p_igual_np_no_modo_selecao)": "ABERTO (BAIXO): partitura para o operador, nao defeito.",
    "runtime_v409.py _v409_guarda_frases (F41b/F40b, novas na R2)": "ATENDIDO: a F41b agora casa «OPEN» (case-sensitive, com ou sem colchetes), «em aberto/aberta», «segue/fica/continua/permanece/esta' aberto|pendente», «pendente», «por fazer», «ainda nao (foi) ligad…», «v41x», «stays/remains/is/still open|pending», «not yet linked», com o ponto mediano como separador; a F42 cobre qualquer v41x («fica para a v411», «deixado para a v413»). Residuo: a isencao por «e21/v407/deixou/dizia/ficava» e' contornavel por quem escrever essas palavras no mesmo trecho; BAIXO.",
    "RELATORIO_PREPARACAO_v409.md linha 65": "ATENDIDO: §5 item 2 agora diz «o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista); a identidade Omega = uniforme esta' podada (a ponte e' a inscricao); com o leitor que so' conta, a igualdade completa nao esta' provada (E28, validade nao afirmada)».",
}
B = []
for a in r2["achados"][1:]:
    b = dict(a); b.pop("estado_na_R2", None)
    chave = next((k for k in est if a["onde"].startswith(k)), None)
    b["estado_na_R3"] = est.get(chave, "ABERTO, inalterado (BAIXO, nao trava)") if chave else "ABERTO, inalterado (BAIXO, nao trava)"
    B.append(b)
# o MEDIO da R1/R2: situacao
situacao = {
    "R1-MEDIO 1 (par na face de Fock [OPEN] em texto novo) / R2-MEDIO (cabecalho do paragrafo README/site)": "ATENDIDO nos quatro lugares + o cabecalho: estatuto do registro («[REAL] o par na face de Fock LIGADO … PODADA a identidade … [OPEN] a independencia …»), `_respostas`, bloco [OPEN] do core memory, e o CABECALHO do paragrafo README/site (rendido em paragrafo_v409.txt e handoff.txt: «[REAL: … o par na face de Fock LIGADO (`ParNaFaceDeFock`) · INPUT … · KNOWN … · PODADA: a identidade de vetores Ω = uniforme (a ponte é a inscrição) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]»). Minha varredura independente (t6): 0 segmentos «Fock/Ω–uniforme + OPEN/aberto/pendente/ainda nao/por fazer/fica para/v41x» fora do historico declarado, em fontes novos, 52 textos rendidos, secao v409 do artigo PT/EN, linha do .md, registros v409 do core e RELATORIO/PLANO; sensibilidade provada (t6_sensibilidade.py: 6 de 6 formas ruins pegas, 2 de 2 boas e historicas passam).",
}
for i, b in enumerate(B): situacao["BAIXO %d (R1/R2) %s" % (i + 1, b["onde"][:60])] = b["estado_na_R3"]
achados = B
n_alto = sum(1 for a in achados if a["sev"] == "ALTO"); n_medio = sum(1 for a in achados if a["sev"] == "MEDIO"); n_baixo = sum(1 for a in achados if a["sev"] == "BAIXO")
aprovada = bool(aprovada_calculada and n_alto == 0 and n_medio == 0)
res = {
    "aprovada": aprovada, "rodada": "R3 (ultima, D58)", "quando": agora,
    "candidato_sha16": cand_fim, "candidato_sha16_no_inicio": cand_ini, "candidato_mudou_durante_a_revisao": cand_fim != cand_ini,
    "candidato_bytes": os.path.getsize(R + "um_v409_candidato.py"), "candidato_da_R2": {"sha16": r2["candidato_sha16"], "bytes": r2["candidato_bytes"]}, "candidato_da_R1": {"sha16": r1["candidato_sha16"], "bytes": r1["candidato_bytes"]},
    "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R3, a ultima; nao construi a v409; mesma instancia de trabalho da R1 e da R2)",
    "n_alto": n_alto, "n_medio": n_medio, "n_baixo": n_baixo, "achados": achados,
    "condicoes_da_aprovacao_calculadas": conds,
    "situacao_dos_achados_da_R1_e_R2": situacao,
    "lean": {**lean, "nota": "nenhuma pedra mudou desde a R1 (pedra/*.lean, KERNEL_RECIBO, FLAGS, KH_N1, POS_BUILD, orquestrador: mesmos sha16 da R2); o `lake env lean` e a compilacao independente das duas fontes da R1 valem; d_kernel.py reconferido sobre o candidato novo: embutido == sandbox == pedra == BUNDLE (2 de 2), raiz = raiz v408 + 2 imports, 1761 embutidos == sandbox", "compilacao_independente_das_fontes": fontes_lean},
    "conferencias": {
        "a_intocados": {"nomes_iguais_por_AST_e_fonte": N_IGUAIS, "mudados_igual_declarado_27": a1["mud_igual_declarado"], "novos_igual_declarado_14": a1["nov_igual_declarado"], "removidos": a1["removidos"], "blocos_fora": a1["blocos_fora"], "obs": "o unico bloco fora dos nos declarados e' o comentario-cabecalho da secao v409; a_intocados_b: 31 linhas fora = comentarios/brancos, 0 linhas da base removidas fora dos nos mudados; _c: 0 segmentos nao declarados diferentes"},
        "a2_mudados": "27 mudados: contratos antigos SO' expected_ladder 12029 -> 12187 (28 ocorrencias, 0 restantes); _V407_FONTES SO' a chave psion_no_acervo (copia purgada); specs +errata e pisos declarados; _LEAN_THEOREM_FLAGS +158 (sub-dict da base igual); build_pt/build_en/emit_canonical_md/main/prove_external_ladder so' acrescimos (0 linhas removidas); resultado igual ao da R2 exceto o texto das frases (R3)",
        "c_fail_closed": {"ok": n_cfc_ok, "falha": n_cfc_f, "nota": "as 2 'falhas' sao expectativas MINHAS de sondagem (EN curto «Clay resolved»; uma frase de teste sem o qualificador, que a guarda acerta em reprovar); 82/82 ancoras, 158/158 bandeiras, 14/14 falas, fontes, raiz, escada, gate, beta, contrato recusam; casos R3 acrescentados (forma «OPEN:», paraphrases, v41x, frase nova do leitor)"},
        "c2_mecanica_direta": {"ok": n_c2_ok, "de": len(c2)}, "k_funcoes_vivas": {"ok": n_k_ok, "falha": n_k_f},
        "f_hashes": {"checagens_ok": N_HASH, "falhas": [f[0] for f in fh["falhas"]], "divergentes_historicos": [x[0] for x in fh.get("divergentes", [])], "nota": "a unica falha e' a varredura geral e so' por 3 pares historicos esperados: adendo T12 «antes» (o Nos antes da v408) e 2 referencias de sessao ao DESENHO no momento do init (o DESENHO e' append-only); CANDIDATO.sha16/sha256/bytes/delta, ESPERADOS, PINOS_BN, BUNDLE, KERNEL_RECIBO e FORMAL_MAP conferem com o candidato NOVO"},
        "e_citacoes": "14 falas do VERBATIM_CONGELADO existem em cunhagens_13out com o sha256 declarado; nenhuma citacao nova em « » fora do corpus (mesmas nao casadas da R2)",
        "l_orquestrador": "plano rc True; main SEM s7_g1 e SEM s10_app; pos_treino_v409.py inalterado desde a R1 (mesmo sha16)",
        "h_guardas": {"controle_negativo_ok": hg.get("controle_negativo_ok"), "varredura_propria": {k: len(v) for k, v in hg["varredura_propria"].items()}},
        "guarda_reforcada": {"sondas_que_deviam_reprovar": sum(1 for s in t5 if s["esperado_pegar"] is True), "reprovam": sum(1 for s in t5 if s["esperado_pegar"] is True and s["pega"]), "frases_certas": sum(1 for s in t5 if s["esperado_pegar"] is False), "passam": sum(1 for s in t5 if s["esperado_pegar"] is False and not s["pega"]), "falhas": [s["frase"][:70] for s in t5 if s["ok"] is False]},
        "varredura_independente_t6": {"A_fontes_e_textos_rendidos": len(t6["A"]), "B_artigo_md_core": len(t6["B"]), "C_relatorio_plano": len(t6["C"])},
        "frase_do_leitor": "«esta' provada para o leitor que le tambem as maquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, nao creditacao); para o leitor que so' conta, nao esta' provada (E28, validade nao afirmada)» em registros (ressalva 1), delta, artigo PT/EN, textos do pos-rito e docstring da F43; nenhum texto novo afirma a igualdade para o leitor que so' conta (varredura (b): 0)",
    },
    "ressalvas": [
        "R3 = ultima rodada (D58). R1 e R2 guardadas em bytes ao lado (REVISAO_TERCEIRO_v409.R1/.R2.json/.md, PEDIDO_CORRECAO_R1/R2_v409.md, r1_saidas/, r2_saidas/). Fora de revisao_terceiro/ nao escrevi nada; nao rodei `lake build`, o instalar, o rito nem o orquestrador (so' _plano(), com ORQ redirecionado a esta pasta).",
        "Nenhuma pedra mudou entre a R1 e a R3; o Lean da R1 (82 #print axioms; varredura MetaM de 223 constantes; compilacao independente das duas fontes) continua valendo. Nao li as provas Lean linha a linha.",
        "Nao revisei instalar_v409.py, reverter_v409.py, rito_v409.sh, conferir_rito_v409.py, o p00, o harness do fechar, a Bancada B3 nem os scripts de superficie (fora da lista do pedido). Os textos do pos-rito foram lidos nos rendidos pelo harness (23:21, depois dos fontes das 23:00), nao regerados por mim.",
        "arquivos_revisados: sha16 lidos agora, na R3. Se qualquer arquivo listado mudar, esta revisao nao vale para ele (o S1b do orquestrador confere). O Mapa de Rotas nao foi consultado nem alimentado por mim.",
        "BAIXOS abertos ficam escritos e nao travam: ate duas rodadas por achado BAIXO ja' foram usadas.",
    ],
    "rotas_examinadas": r2["rotas_examinadas"] + [
        "R3-A: reconferencia sobre o candidato 53284ba461ecd940: a_intocados*.py, a2_mudados.py, d_kernel.py, f_hashes.py, e_citacoes.py, c_fail_closed.py (casos R3), c2, k_funcoes_vivas.py, l_orquestrador.py, m_flags_audit.py, h_guardas.py.",
        "R3-B: t6_varredura_independente_r3.py (a minha varredura: Fock e Ω–uniforme perto de OPEN/aberto/pendente/ainda nao/por fazer/fica para/v41x) em fontes novos, 52 textos rendidos, secao v409 do artigo PT/EN, linha v409 do .md, registros v409 do core e RELATORIO/PLANO: 0 achados; t6_sensibilidade.py; t5_guarda_probes.py (22 sondas que devem reprovar, 8 frases certas).",
        "R3-C: r3_diffs.py (diff R2 x R3 dos fontes): registros (frase do leitor), runtime (F41b com OPEN case-sensitive, ponto mediano, pendente/por fazer/ainda nao ligad/v41x; F42 v41x), guarda_frases (casos), delta, artigos PT/EN, textos_v409_novo.pysnip (`_diz`, cabecalho, frase, core memory), RELATORIO §5.",
    ],
    "arquivos_revisados": arq, "candidato_da_R2_arquivos": r2["arquivos_revisados"],
    "nota": "aprovada=%s: 0 ALTO, 0 MEDIO; os BAIXOS ficam escritos." % aprovada,
}
json.dump(res, open(RV + "REVISAO_TERCEIRO_v409.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("JSON R3 gravado: aprovada", aprovada, "|", n_alto, n_medio, n_baixo, "| candidato", cand_ini, "->", cand_fim)
