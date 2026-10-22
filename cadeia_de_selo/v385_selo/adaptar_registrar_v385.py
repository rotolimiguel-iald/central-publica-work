# -*- coding: utf-8 -*-
"""Reescreve os registros do registrar_resultado_v385.py (gerado pelo conversor): duas ROTAS novas (o Axioma; a reprodutibilidade do pilar) e tres
ANOTACOES (na rota do pilar da v384: a segunda rodada; na do livro de cobrancas: o nome do degrau final; e o V1 lido de novo). Backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "registrar_resultado_v385.py")
s0 = open(P, encoding="utf-8", newline="").read()
i = s0.index('ROTA_ID = "quantica.pilar_v384_rodada_completa"')
j = s0.index('if AMB["sint"]:\n    for r in res:')
NOVO = r'''ROTA_ID = "kernel.v385_axioma_e_testemunha_falsa"
# a guarda de idempotencia do molde: a rota ja existe -> nada gravado, rc 0
if any(r.get("rota_id") == ROTA_ID and r.get("tipo") == "ROTA" for r in rotas._le()):
    print("mapa: a rota %s ja existe; nada gravado (os registros desta rodada ja entraram)" % ROTA_ID); sys.exit(0)
NOS = V["nos"]; S = " [SINTETICO -- ENSAIO DA CADEIA; NAO REGISTRAR]" if AMB["sint"] else ""
RD = os.path.join(NOS, V["qp_run_dir"]) if not os.path.isabs(V["qp_run_dir"]) else V["qp_run_dir"]
art_k = [os.path.join(NOS, f) for f in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "rodada_v385_stdout.txt")]
art_k += [os.path.join(NOS, "tgl_kernel", "TGLExt", "TheAxiomAndTheFalseWitness.lean"), os.path.join(NOS, "tgl_kernel", "TGLExt", "TheDarkSplit.lean"),
          os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"), os.path.join(AMB["conf_dir"], "conferencia_rito_v385.json")]
art_p = [os.path.join(NOS, f) for f in ("um_absoluto_pilar_quantico.json", "um_absoluto_selo.json", "um_absoluto.json", "rodada_v385_stdout.txt")]
art_p += [os.path.join(RD, f) for f in ("result.json", "result_partial.json", "details.jsonl", "cpuref.json") if os.path.exists(os.path.join(RD, f))]
if V["qp_classe"] != "RAMO_9" and os.path.exists(os.path.join(RD, "worker_stdout.txt")):
    art_p.append(os.path.join(RD, "worker_stdout.txt"))   # fora do ramo 9, o registro do trabalhador e' a prova do que houve
_op = lambda n: "%s (%s)" % (((V.get("op") or {}).get(n) or {}).get("texto", "AUSENTE"), ((V.get("op") or {}).get(n) or {}).get("quando", "n/d"))
res = [dict(tipo="ROTA", rota_id=ROTA_ID, dominio="KERNEL_FORMAL", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo=("v385 SELADA%s: o Axioma e a testemunha falsa [KERNEL: a pedra TheAxiomAndTheFalseWitness + o TheDarkSplit auditado; as leituras do operador "
                    "INPUT/ONTO] -- o Um posto ([POSTO]); a leitura radical tem dois pontos fixos (0 e 1); o 1 e' o Axioma (o modo zero de peso 1); o 0 e' a "
                    "testemunha falsa (a estatica, o zero absoluto, proibida por beta > 0); o degrau final do gate chama-se Axioma, ao lado do gate; gate intocado" % S),
            pergunta="o que o operador cunhou em 05/10 (posto, Axioma, testemunha falsa, observador conjugado) tem termo no kernel que o sustente, e o gate fica onde esta?",
            dados=["nenhum dado da natureza: kernel Lean 4 desta rodada (%s; %s declaracoes da v385 no trio)" % (V["teor"], V["ax_decl"]),
                   "as palavras do operador de 05/10, lidas do transcrito por script: posto = %s; axioma = %s; testemunha = %s" % (_op("posto"), _op("axioma"), _op("testemunha"))],
            metodo=("pedra nova TGLExt/TheAxiomAndTheFalseWitness.lean (%s declaracoes; sha16 %s) + #print axioms das 7 do TheDarkSplit; sandbox antes do rito; "
                    "rito completo; conferidor do pacote (copia byte a byte); o nome do degrau final lido do .lean pelo runtime" % (V["ax_n_pedra"], V["ax_pedra16"])),
            resultado=("um.py %s (%s B) sobre a v384 %s; %s; escada %s -> %s; o Axioma %s; nome do degrau final (do kernel): %s; etiqueta de omega(I)=1: %s; "
                       "conferidor %s (%s / %s); gate %s (%s/18) inalterado; por termo %s"
                       % (V["s16"], X["umb_fmt"], V["base16"], V["teor"], V["esc_v384"], V["esc"], V["ax_ok"], V["ax_nome"], V["ax_tag"], X["conf_res"], V["conf_dm"],
                          V["conf_np"], V["qg"], V["n18"], V["hvals"])),
            veredito=V["ax_v"],
            nao_refazer=("os dois pontos fixos, o peso 1 do modo zero, a proibicao da testemunha estatica e o fluxo do posto estao no kernel; que F(t) = e^(-tH_min) e' "
                         "[KNOWN], nao termo; o nome do degrau final fica AO LADO do gate (o gate nao muda); as leituras sao do operador [INPUT/ONTO]; provado nao e' confirmado"),
            proximo_passo="custodia conjunta v383 + v384 + v385 pela sessao do site (decisao do operador de 05/10); commit/push do operador",
            onde="Nos\\um.py v385: the_axiom_v385; Nos\\tgl_kernel\\TGLExt\\TheAxiomAndTheFalseWitness.lean; selo the_axiom_v385 / final_step_name_v385 / the_axiom_reading_v385",
            artefatos=art_k, refs=["kernel.livro_de_cobrancas.otica", "quantica.pilar_v384_rodada_completa", "memory um-posto-jamais-pressuposto-e-h2-17set"]),
       dict(tipo="ROTA", rota_id="quantica.pilar_v385_reprodutibilidade", dominio="DEPHASING", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo=("v385 SELADA%s: o pilar quantico de NOVO, inteiro, sob o MESMO V1 %s (especificacao %s), e a reprodutibilidade contra a v384 [COMPUTED: calculo, "
                    "nao medicao] -- %s; gate intocado" % (S, V["pr_id"], V["pr_spec16"], X["rp_curta"])),
            pergunta="o mesmo sistema, sob a mesma especificacao, o mesmo trabalhador e o mesmo beta, devolve o mesmo resumo na segunda rodada completa?",
            dados=["nenhum dado da natureza: calculo do sistema da teoria na GPU (%s), duas rodadas completas (v384 e v385)" % V["qp_gpu"],
                   "o resultado da v384 lido do cache ANTES do calculo (sha16 %s, pinado nos esperados)" % V["rp_prev16"]],
            metodo=("quantum_pillar_previous_v385 (le o resultado guardado pela rodada anterior com a mesma chave) + quantum_pillar_reproducibility_v385 (os dois "
                    "resumos da _qp_summary, campo a campo, fora os de tempo e de ambiente; bit a bit, ou arredondamento <= 1e-9, ou diferente)"),
            resultado=("o pilar: %s (%s; o mesmo veredito da v384: %s); a reprodutibilidade: %s; %s campos (%s numericos), %s diferem, max rel %s; resultado %s"
                       % (V["qp_v"], X["qp_classe_curta"], V["qp_igual_v384"], V["rp_v"], V["rp_n_fields"], V["rp_n_num"], V["rp_n_differ"], V["rp_maxrel"], V["qp_res16"])),
            veredito=V["rp_v"],
            nao_refazer=("reprodutibilidade de calculo nao e' medicao da natureza; o V1 congelado nao muda; uma diferenca, se houver, e' resultado e fica dita; "
                         "negativos honestos do pilar nesta rodada: %s" % V["qp_negativos"]),
            proximo_passo="custodia conjunta pela sessao do site (o V1 e as evidencias numa subpasta da Um, com PORTA por script)",
            onde="Nos\\um.py v385: quantum_pillar_previous_v385 / quantum_pillar_reproducibility_v385; pasta da rodada: %s" % V["qp_run_dir"],
            artefatos=art_p + [A.PR_JSON, A.PR_MD], refs=["quantica.pilar_v384_rodada_completa", "kernel.v385_axioma_e_testemunha_falsa"]),
       dict(tipo="ANOTACAO", rota_id="quantica.pilar_v384_rodada_completa", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="o pilar rodou de NOVO na v385%s, sob o mesmo V1: %s (%s); a reprodutibilidade contra esta rodada: %s" % (S, V["qp_v"][:120], X["qp_classe_curta"], V["rp_v"]),
            nota="ver quantica.pilar_v385_reprodutibilidade; servidor do modelo nativo depois do rito: %s; o marcador do pacote v385: %s" % (V["servidor"], V["marcador_txt"]),
            artefatos=[os.path.join(NOS, "rodada_v385_stdout.txt")], refs=["quantica.pilar_v385_reprodutibilidade"]),
       dict(tipo="ANOTACAO", rota_id="kernel.livro_de_cobrancas.otica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="o degrau final do gate tem NOME na v385%s: Axioma (decisao do operador, 05/10; lido do kernel: %s); a proposta da v383 fica ao lado (the_proposal_beside_is_kept); o gate nao muda" % (S, V["ax_nome"][:60]),
            nota="o operador: %s" % _op("nome_axioma"),
            artefatos=[os.path.join(NOS, "tgl_kernel", "TGLExt", "TheAxiomAndTheFalseWitness.lean")], refs=["kernel.v385_axioma_e_testemunha_falsa"]),
       dict(tipo="ANOTACAO", rota_id="quantica.pilar_v384_rascunhos_b_reduzido_e_a", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="o V1 ratificado (%s) foi lido de novo pelo rito v385%s: JSON %s e MD %s em disco = os pinados, especificacao %s embutida e conferida pelo hash" % (V["pr_escolha"], S, V["pr_json16"], V["pr_md16"], V["pr_spec16"]),
            artefatos=[A.PR_JSON, A.PR_MD], refs=["quantica.pilar_v385_reprodutibilidade"])]
'''
s = s0[:i] + NOVO + s0[j:]
s = s.replace('''Registros: (1) ROTA quantica.pilar_v384_rodada_completa (o pilar calculado na rodada completa: veredito, numeros, negativos honestos, custodia);
(2) ANOTACAO na quantica.pilar_v384_cadeia_ate_o_rito (a cadeia ate o selo fechou: conferidor, superficies); (3) ANOTACAO na
quantica.pilar_v384_rascunhos_b_reduzido_e_a (o V1 ratificado foi o lido pelo rito, por hash).''',
'''Registros (v385): (1) ROTA kernel.v385_axioma_e_testemunha_falsa (a pedra + o TheDarkSplit auditado + o nome do degrau final); (2) ROTA
quantica.pilar_v385_reprodutibilidade (o pilar de novo sob o mesmo V1 e o que a comparacao deu); (3) ANOTACAO na quantica.pilar_v384_rodada_completa (a
segunda rodada); (4) ANOTACAO na kernel.livro_de_cobrancas.otica (o nome do degrau final: Axioma); (5) ANOTACAO na quantica.pilar_v384_rascunhos_b_reduzido_e_a
(o V1 lido de novo, por hash).''')
assert "kernel.v385_axioma_e_testemunha_falsa" in s and "Registros (v385)" in s
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_adapt", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("OK registrar_resultado_v385.py:", len(s0), "->", len(s))
