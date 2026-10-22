# -*- coding: utf-8 -*-
"""O RESULTADO da v385 para o MAPA DE ROTAS (molde: registrar_resultado_v384.py), tudo LIDO da rodada (leitura_v385.ler). Por padrao NAO registra: monta o
JSON (registro_mapa_v385.json), PRE-VALIDA cada registro pela propria regua do mapa (rotas._valida, so leitura: estatuto da casa, guarda da palavra
proibida, artefatos existentes com o sha256 calculado pela ferramenta) e imprime o comando que a GERENCIA roda:
    python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py registrar <json> --quem "<IA / sessao>"
Com --registrar (so com o Nos REAL; ato da gerencia), chama rotas.registrar. Com o Nos SINTETICO: o JSON vai a ensaio_saidas, marcado SINTETICO, e --registrar e' recusado.
Registros (v385): (1) ROTA kernel.v385_axioma_e_testemunha_falsa (a pedra + o TheDarkSplit auditado + o nome do degrau final); (2) ROTA
quantica.pilar_v385_reprodutibilidade (o pilar de novo sob o mesmo V1 e o que a comparacao deu); (3) ANOTACAO na quantica.pilar_v384_rodada_completa (a
segunda rodada); (4) ANOTACAO na kernel.livro_de_cobrancas.otica (o nome do degrau final: Axioma); (5) ANOTACAO na quantica.pilar_v384_rascunhos_b_reduzido_e_a
(o V1 lido de novo, por hash)."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import ambiente_v385 as A
import leitura_v385, textos_v385 as T
import rotas
AMB = A.ambiente()
V, PROB = leitura_v385.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
X = T._x(V)
ROTA_ID = "kernel.v385_axioma_e_testemunha_falsa"
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
            nota=(V.get("intervencao_txt") or "sem intervencao de ambiente registrada durante o rito"),   # a prioridade do trabalhador (11:47), dita ao lado da reprodutibilidade
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
if AMB["sint"]:
    for r in res:
        r["nota"] = (r.get("nota", "") + " | SINTETICO: ensaio da cadeia com o Nos sintetico; NAO registrar").strip(" |")
# pre-validacao pela regua do mapa (so leitura)
regs = rotas._le(); ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}; seqs = {r["seq"] for r in regs}
ok = []
for r in res:
    vv = rotas._valida(dict(r), set(ids), seqs)
    ok.append((r["tipo"], r["rota_id"], len(vv.get("artefatos") or [])))
    if r["tipo"] == "ROTA":
        ids.add(r["rota_id"])
out_dir = AMB["saidas"]; os.makedirs(out_dir, exist_ok=True)
out = A.pode_escrever(os.path.join(out_dir, "registro_mapa_v385.json"), AMB)
open(out + ".tmp", "wb").write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8")); os.replace(out + ".tmp", out)
print("pre-validado pela regua do mapa:", ok)
print("JSON para o mapa%s: %s" % (S, out))
if "--registrar" in sys.argv:
    if AMB["sint"]:
        print("RECUSO --registrar com o Nos SINTETICO"); sys.exit(2)
    o = rotas.registrar(res, "claude-code/central-de-patentes (gerencia) sessao 6da8f00d")
    print(json.dumps({k: o[k] for k in o if k != "registros"}, ensure_ascii=False)[:500])
else:
    print('a gerencia registra: python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py registrar "%s" --quem "claude-code/central-de-patentes (gerencia) sessao 6da8f00d"%s' % (out, "   <- NAO (SINTETICO)" if AMB["sint"] else ""))
