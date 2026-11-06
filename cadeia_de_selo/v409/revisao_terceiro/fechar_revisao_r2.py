# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R2): monta REVISAO_TERCEIRO_v409.json / .md e PEDIDO_CORRECAO_R2_v409.md (R1 fica ao lado em .R1.json/.R1.md/r1_saidas). sha16 de TUDO lido agora do arquivo. So escreve nesta pasta."""
import datetime, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
RV = R + "revisao_terceiro/"
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda p: json.load(open(p, encoding="utf-8"))
cand_fim = sha16(R + "um_v409_candidato.py"); cand_ini = "de2244483b35f5a3"   # lido ao abrir a R2 (e igual ao da PRONTA)
r1 = J(RV + "REVISAO_TERCEIRO_v409.R1.json")
rev_files = ["um_v409_candidato.py", "CANDIDATO_v409.json", "COMPARACAO_V408_v409.json", "ESPERADOS_v409.json", "BUNDLE_v409.json", "kernel_modulos_novos_v409.json", "VERBATIM_CONGELADO_v409.json", "GUARDA_FRASES_v409.json",
             "delta_v409.py", "registros_v409.py", "runtime_v409.py", "guarda_frases_v409.py", "guarda_p18_v409.py", "artigo_pt_v409.pysnip", "artigo_en_v409.pysnip",
             "pedra/TraducaoTuring.lean", "pedra/ParNaFaceDeFock.lean", "kernel/KERNEL_RECIBO_v409.json", "kernel/FLAGS_v409.json", "kernel/KH_N1_v409.json", "kernel/POS_BUILD_v409.json",
             "pos_rito/textos_v409_novo.pysnip", "pos_rito/textos_v409.py", "pos_rito/textos_custodia_handoff_v409.py", "pos_rito/CUSTODIA_v409_RASCUNHO.txt",
             "orquestrador/pos_treino_v409.py", "PREPARACAO_v409_PRONTA.json", "dry_v409/core_ensaio.json"]
arq = {k: sha16(R + k) for k in rev_files}
pronta = J(R + "PREPARACAO_v409_PRONTA.json")
mud_pronta = {}
for k, v in arq.items():
    pv = (pronta.get("hashes") or {}).get(k) or (pronta.get("hashes") or {}).get(k.replace("/", "\\"))
    if pv and pv.get("sha16") != v: mud_pronta[k] = (pv.get("sha16"), v)
mud_r1 = {k: (r1["arquivos_revisados"][k], v) for k, v in arq.items() if k in r1["arquivos_revisados"] and r1["arquivos_revisados"][k] != v}
agora = datetime.datetime.now().isoformat(timespec="seconds")
print("arquivos:", len(arq), "| mudaram desde a PRONTA:", mud_pronta, "| mudaram desde a R1:", len(mud_r1))

M1 = {
    "sev": "MEDIO",
    "onde": "pos_rito/textos_v409_novo.pysnip:625 (funcao _paragrafo_v409_de, 1a linha do bloco) e o montado pos_rito/textos_v409.py:819; rendido em harness textos/paragrafo_v409.txt e handoff.txt (bloco INICIO_PARAGRAFO_TRADUCAO_TURING_v409)",
    "achado": "R1-MEDIO 1 ficou ATENDIDO em tres dos quatro lugares (estatuto do registro, `_respostas`, bloco [OPEN] do core memory: conferidos nos fontes, no candidato, no core do ensaio e nos textos rendidos) mas NAO no quarto: o CABECALHO de estatuto do paragrafo PRONTO PARA O README DO ESPELHO E O SITE (o texto que a custodia cola em publico) segue dizendo «[REAL: … · KNOWN: … · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]». "
              "Na R1 eu atribui esse cabecalho ao estatuto do registro; na verdade e' uma linha escrita a mao em `_paragrafo_v409_de` (nao vem do registro), por isso a correcao do estatuto nao a atingiu. Contradiz o proprio paragrafo (ressalva 6 do registro, no mesmo bloco: «o par na face de Fock esta' ligado nesta versao») e o item (d): estatuto errado em texto publico. "
              "A guarda reforcada (F41b) nao pega esta forma: ela casa «[OPEN]» entre colchetes e «em aberto/segue aberto», mas aqui a palavra e' «OPEN:» dentro de um grupo de colchetes de estatuto («OPEN:» sem colchetes proprios). Medido: a varredura ampla (t1b_fock_open_amplo.py) sobre fontes e 52 textos rendidos acha SO' este segmento (4 arquivos: os 2 fontes e os 2 rendidos); o resto sao E21 historico, a E21 em `registros`, e a documentacao da propria guarda.",
    "evidencia": "revisao_terceiro/t1b_fock_open_amplo.py + t1b_fock_open_amplo_out.json; grep em C:/t/h409/harness_saida_v409/textos/paragrafo_v409.txt e handoff.txt; pos_rito/textos_v409_novo.pysnip:625.",
    "correcao": "Ver PEDIDO_CORRECAO_R2_v409.md. Trocar o cabecalho por «[REAL: … o par na face de Fock LIGADO (ParNaFaceDeFock) · INPUT: … · KNOWN: … · PODADA: a identidade de vetores Omega = uniforme (a ponte e' a inscricao) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]»; "
                "estender a F41b para a palavra «OPEN» com ou sem colchetes (\\bOPEN\\b) e acrescentar ao controle negativo esta sonda; regenerar o texto do pos-rito (nao muda o candidato: `textos_v409*.py` nao estao embutidos no um.py), rerodar o harness dos textos e a PRONTA.",
}
# BAIXOS da R1: estado na R2
B = []
for a in r1["achados"][1:]:
    b = dict(a)
    o = a["onde"]
    if o.startswith("artigo_pt_v409"):
        b["estado_na_R2"] = "PARCIAL: a frase agora diz «vale só para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay; E28)» (PT, EN, delta, registros, textos): o leitor fica nomeado e BGS citado; o «só» ainda pode sugerir que a igualdade é falsa para o leitor que só conta (o que se sabe é que NÃO está provada). Fica BAIXO, não trava."
    elif o.startswith("registros_v409.py (cunhagens_v409 u1"):
        b["estado_na_R2"] = "ATENDIDO nos fontes que vão ao candidato: u1 = «as 82 ancoras, o sha256 dos dois modulos, as 20 checagens, o gate» (valores lidos de DL.N_CHECKS_FECHO); docstring da mecanica e do delta = 82 e 20; grep «17 checagens|62 ancoras» nos textos novos: 0. RELATORIO/PLANO (preparação, não público) não conferidos."
    elif o.startswith("pos_rito/textos_v409_novo.pysnip:617-633"):
        b["estado_na_R2"] = "ABERTO (índices fixos de `diz`); fica BAIXO. Corrigir junto com o MÉDIO, que já mexe nessa função."
    elif o.startswith("runtime_v409.py _v409_guarda_frases (F43)"):
        b["estado_na_R2"] = "PARCIAL: a F41b/F40b entraram (as 4 sondas de Fock/Ω passam a reprovar); a F43 e o EN curto «Clay resolved» seguem como estavam; a F41b não casa «OPEN:» sem colchetes próprios nem paráfrases («ainda não foi ligado», «fica para a v411», «continua por fazer», «é pendência»): ver o MÉDIO e o BAIXO novo."
    else:
        b["estado_na_R2"] = "ABERTO, inalterado (BAIXO, não trava)"
    B.append(b)
B.append({"sev": "BAIXO", "onde": "runtime_v409.py _v409_guarda_frases (F41b/F40b, novas na R2)", "achado": "As guardas novas casam «[OPEN]», «em aberto», «segue/fica/continua/está aberto», «stays/remains/is open» no MESMO trecho que «face de Fock»/«par de Fock»/«ParNaFaceDeFock» (e «Ω … uniforme» em lista aberta), com isenção por «E21», «v407», «deixou», «dizia» e «podad…». Sondadas (t5_guarda_probes.py): as 4 sondas da R1 e 3 variantes reprovam; as 7 frases certas passam; ESCAPAM: a forma «OPEN:» sem colchetes próprios (a do MÉDIO) e paráfrases «ainda não foi ligado», «fica para a v411», «continua por fazer», «é pendência». A isenção por «e21/v407/deixou/dizia» é contornável por quem escrever essas palavras no mesmo trecho. Limite de regex, não defeito de texto novo (varredura ampla: 0 outras ocorrências).", "evidencia": "revisao_terceiro/t5_guarda_probes_out.json; t1b_fock_open_amplo_out.json.", "correcao": "Estender a F41b com \\bOPEN\\b e, se quiser, com «ainda não», «por fazer», «pendente», «fica para». Não trava além do MÉDIO.", "estado_na_R2": "NOVO"})
B.append({"sev": "BAIXO", "onde": "RELATORIO_PREPARACAO_v409.md linha 65 (§5, item 2, «Dizer ao operador, na lingua dele (regra do posto), o que a v409 NAO entrega»)", "achado": "O relatorio de preparacao (nao publico, mas e' o roteiro do que a gerencia le ao operador) ainda lista entre o que a v409 «NAO entrega»: «o par na face de Fock segue aberto (D60); o Omega do psion e o uniforme da instancia tem a mesma forma, e que sejam o mesmo segue aberto». O par esta' LIGADO (kernel, registro, artigo) e a identidade esta' PODADA. Se a gerencia ler o roteiro como esta', repete ao operador o [OPEN] errado (regra do posto: a partitura tem de dizer o que o teste decide e nao decide). O texto e' gerado por gerar_relatorio_v409.py e nao foi regenerado com a D60 revista.", "evidencia": "RELATORIO_PREPARACAO_v409.md:65 (mtime 22:37, depois da correcao); h_guardas_out.txt «GUARDA ACHOU em RELATORIO_PREPARACAO_v409.md ... F41».", "correcao": "Corrigir a linha no gerar_relatorio_v409.py («o par na face de Fock esta' ligado nesta versao; a identidade Omega = uniforme esta' podada, a ponte e' a inscricao») e regenerar; nao muda o candidato.", "estado_na_R2": "NOVO (ja' presente na R1, nao anotado por mim)"})
achados = [M1] + B
n_alto = sum(1 for a in achados if a["sev"] == "ALTO"); n_medio = sum(1 for a in achados if a["sev"] == "MEDIO"); n_baixo = sum(1 for a in achados if a["sev"] == "BAIXO")

lean = J(RV + "lean_r1_out.json"); fontes_lean = J(RV + "b4_fontes_out.json")
cfc = J(RV + "c_fail_closed_out.json"); kv = J(RV + "k_funcoes_vivas_out.json"); c2 = J(RV + "c2_mecanica_direta_out.json"); a1 = J(RV + "a_intocados_out.json"); fh = J(RV + "f_hashes_out.json"); hg = J(RV + "h_guardas_out.json")
n_cfc_ok = sum(1 for v in cfc.values() if v.get("ok") is True); n_cfc_f = [k for k, v in cfc.items() if v.get("ok") is False]
n_k_ok = sum(1 for v in kv.values() if v.get("ok") is True); n_k_f = [k for k, v in kv.items() if v.get("ok") is False]
n_c2_ok = sum(1 for v in c2.values() if v.get("ok") is True)
N_IGUAIS = sum(1 for v in a1["nomes"].values() if v.get("ast_igual") and v.get("fonte_igual")); N_HASH = sum(1 for v in fh["ok"].values() if v)
sondas = J(RV + "t5_guarda_probes_out.json")
res = {
    "aprovada": False, "rodada": "R2", "quando": agora,
    "candidato_sha16": cand_fim, "candidato_sha16_no_inicio": cand_ini, "candidato_mudou_durante_a_revisao": cand_fim != cand_ini,
    "candidato_bytes": os.path.getsize(R + "um_v409_candidato.py"), "candidato_da_R1": {"sha16": r1["candidato_sha16"], "bytes": r1["candidato_bytes"]},
    "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R2; nao construi a v409; mesma instancia de trabalho da R1)",
    "n_alto": n_alto, "n_medio": n_medio, "n_baixo": n_baixo, "achados": achados,
    "situacao_dos_achados_da_R1": {
        "MEDIO 1 (par na face de Fock [OPEN] em texto novo)": "PARCIAL: ATENDIDO no estatuto do registro (registros_v409.py; core do ensaio traz «[REAL] o par na face de Fock LIGADO … PODADA a identidade … [OPEN] a independencia …»), em `_respostas` («nem que o par finito de Bell e o par de Fock sejam o mesmo objeto … o par na face de Fock está ligado nesta versão»), no bloco [OPEN] do core memory (sem o par e sem Ω = uniforme) e na guarda (F41b/F40b: 4 de 4 sondas reprovam, 7 de 7 frases certas passam); NAO atendido no cabecalho de estatuto do paragrafo pronto do README/site (MEDIO da R2).",
        **{("BAIXO %d" % (i + 1)): b.get("estado_na_R2", "") for i, b in enumerate(B[:-1])},
    },
    "lean_r2": {**lean, "nota": "nenhuma pedra mudou desde a R1 (pedra/*.lean e KERNEL_RECIBO com os mesmos sha16); o `lake env lean` e a compilacao independente da R1 valem; d_kernel.py reconferido sobre o candidato novo: embutido == sandbox == pedra == BUNDLE (2 de 2), raiz = raiz v408 + 2 imports, 1761 embutidos == sandbox", "compilacao_independente_das_fontes": fontes_lean},
    "conferencias": {
        "a_intocados": {"nomes_iguais_por_AST_e_fonte": N_IGUAIS, "mudados_igual_declarado_27": a1["mud_igual_declarado"], "novos_igual_declarado_14": a1["nov_igual_declarado"], "removidos": a1["removidos"], "blocos_fora": a1["blocos_fora"], "obs": "o unico bloco fora dos nos declarados e' o comentario-cabecalho da secao v409; a_intocados_b/_c: 0 diferencas fora dos nos declarados"},
        "a2_mudados": "27 mudados: contratos antigos SO' expected_ladder 12029 -> 12187 (28 ocorrencias, 0 restantes); _V407_FONTES SO' a chave psion_no_acervo (copia purgada); _V408_SPECS/_V407_SPECS +errata e pisos declarados; _LEAN_THEOREM_FLAGS +158 (sub-dict da base igual); build_pt/build_en/emit_canonical_md/main/prove_external_ladder so' acrescimos (0 linhas removidas)",
        "c_fail_closed": {"ok": n_cfc_ok, "falha": n_cfc_f, "nota": "82/82 ancoras (ausente, sorryAx, ofReduceBool, lista vazia, proveniencia, bandeira), 158/158 bandeiras (False e ausente), 14/14 falas (adulterada e trecho inexistente), fontes, raiz sem import, escada, gate, beta, contrato: recusam; guardas F35–F43 e as novas F41b/F40b (casos de R2 acrescentados: 4 sondas + frases certas)"},
        "c2_mecanica_direta": {"ok": n_c2_ok, "de": len(c2)}, "k_funcoes_vivas": {"ok": n_k_ok, "falha": n_k_f},
        "f_hashes": {"checagens_ok": N_HASH, "falhas": [f[0] for f in fh["falhas"]], "nota": "a unica falha e' a mesma da R1: 2 pares {path, sha256} historicos (adendo T12 «antes» e SESSION_REFERENCE.source); CANDIDATO.sha16/sha256/bytes/delta, ESPERADOS, PINOS_BN, BUNDLE, KERNEL_RECIBO e FORMAL_MAP conferem com o candidato NOVO"},
        "e_citacoes": "14 falas do VERBATIM_CONGELADO existem em cunhagens_13out com o sha256 declarado; nenhuma citacao nova em « » de texto novo fora do corpus (as 'novas' nao casadas sao fragmentos de codigo da F41b em runtime_v409.py)",
        "l_orquestrador": "plano rc True; main SEM s7_g1 e SEM s10_app; pos_treino_v409.py inalterado desde a R1 (mesmo sha16)",
        "h_guardas": {"controle_negativo_ok": hg.get("controle_negativo_ok"), "varredura_propria": {k: len(v) for k, v in hg["varredura_propria"].items()}},
        "guarda_reforcada": {"sondas_da_R1_reprovam": [s["pega"] for s in sondas[:4]], "frases_certas_passam": [not s["pega"] for s in sondas if s["esperado_pegar"] is False], "escapam_informativo": [s["frase"] for s in sondas if s["esperado_pegar"] is None and not s["pega"]]},
        "contagens_e_frase_do_leitor": "u1 = 82 ancoras / dois modulos / 20 checagens (lido de DL.N_CHECKS_FECHO); docstrings 82 e 20; «17 checagens|62 ancoras»: 0 nos textos novos; a frase do leitor: «vale só para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay; E28)» em PT, EN, delta, registros e textos",
    },
    "ressalvas": [
        "R2 de ate tres rodadas (D58). A R1 esta' guardada em bytes: REVISAO_TERCEIRO_v409.R1.json/.R1.md, PEDIDO_CORRECAO_R1_v409.md e r1_saidas/. Fora de revisao_terceiro/ nao escrevi nada; nao rodei `lake build`, o instalar, o rito nem o orquestrador (so' _plano(), com ORQ redirecionado a esta pasta).",
        "Nenhuma pedra mudou entre a R1 e a R2 (sha16 de pedra/*.lean e do KERNEL_RECIBO identicos), entao o Lean da R1 (82 #print axioms, varredura de 223 constantes, compilacao independente das duas fontes) continua valendo; reconferi por d_kernel.py contra o candidato novo.",
        "O MEDIO da R2 e' de TEXTO do pos-rito (textos_v409*.py NAO sao embutidos no um.py): corrigi-lo nao muda o candidato (de2244483b35f5a3); muda pos_rito/textos_v409_novo.pysnip, o montado textos_v409.py, o harness e a PRONTA. Se a gerencia estender tambem a F41b em runtime_v409.py, o candidato muda e a R3 refaz as conferencias (os scripts desta pasta rodam sem edicao).",
        "arquivos_revisados: sha16 lidos agora, na R2. Se qualquer arquivo listado mudar, esta revisao nao vale para ele. O Mapa de Rotas nao foi consultado nem alimentado por mim.",
    ],
    "rotas_examinadas": r1["rotas_examinadas"] + [
        "R2-A: reconferencia sobre o candidato de2244483b35f5a3: a_intocados*.py (38 nomes iguais, 27 mudados == declarados, 14 novos == declarados), a2_mudados.py, d_kernel.py, f_hashes.py, e_citacoes.py, c_fail_closed.py, c2, k_funcoes_vivas.py, l_orquestrador.py, m_flags_audit.py, h_guardas.py.",
        "R2-B: t1b_fock_open_amplo.py (varredura ampla de «Fock/Ω uniforme» + OPEN/aberto/pendente/v41x em fontes e 52 textos rendidos): acha so' o cabecalho do paragrafo README/site; t5_guarda_probes.py (guarda reforcada).",
        "R2-C: diff R1 x R2 dos fontes (r2_diffs.py): registros (estatuto, u1, frase), runtime (F41b/F40b e docstring), guarda_frases (casos), delta (docstring, frase), artigos PT/EN (frase), textos_v409_novo.pysnip (3 linhas).",
    ],
    "arquivos_revisados": arq, "candidato_da_R1_arquivos": r1["arquivos_revisados"],
    "nota": "aprovada=false por 1 MEDIO residual (o cabecalho do paragrafo README/site). Correcao pequena e so' no pos-rito; BAIXOS ficam escritos.",
}
json.dump(res, open(RV + "REVISAO_TERCEIRO_v409.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("JSON R2 gravado:", n_alto, n_medio, n_baixo, "| candidato", cand_ini, "->", cand_fim)
