# -*- coding: utf-8 -*-
"""Grava AFERIDOR_v385.txt (os relatorios VERBATIM das afericoes, concatenados, cada um com o seu sha256 lido do arquivo) e disposicoes_afericoes_v385.json
(o que a gerencia fez com cada achado/nota: CORRIGIDO onde, ou NAO CORRIGIDO e por que). Uso: python gravar_afericoes_v385.py (idempotente: regrava os dois
a partir dos relatorios em disco; backup de bytes do anterior)."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
RELS = [("passada1_codigo", os.path.join(HERE, "afericao_codigo", "RELATORIO_AFERIDOR_CODIGO_v385.txt")),
        ("passada1_texto", os.path.join(HERE, "afericao_texto", "RELATORIO_AFERIDOR_TEXTO_v385.txt"))]
for extra in ("passada2", "passada3"):
    p = os.path.join(HERE, "afericao_%s" % extra, "RELATORIO_AFERIDOR_%s_v385.txt" % extra.upper())
    if os.path.exists(p):
        RELS.append((extra, p))
partes = []
for nome, p in RELS:
    partes.append("=" * 100 + "\n%s — %s (sha256 %s)\n" % (nome, os.path.basename(p), sha(p)) + "=" * 100 + "\n" + open(p, encoding="utf-8").read().rstrip() + "\n")
txt = "AFERIDOR_v385 — os relatorios VERBATIM das afericoes da v385 (gravado por gravar_afericoes_v385.py em %s)\n\n" % time.strftime("%Y-%m-%d %H:%M:%S") + "\n".join(partes)
D = {"o_que_e": "as disposicoes da gerencia sobre cada achado/nota das afericoes da v385 (verbatim em AFERIDOR_v385.txt)",
     "relatorios": {n: {"arquivo": p, "sha256": sha(p)} for n, p in RELS},
     "passada1": {
         "codigo": {
             "1_CORRIGIR_nan": "CORRIGIDO: campo nao finito que difere conta como diferenca (v385_runtime.py, quantum_pillar_reproducibility_v385; corrigir_comparador_v385.py); teste de unidade nan_e_diferenca no ensaio a seco",
             "2_CORRIGIR_escala": "CORRIGIDO: escala max(1,|a|,|b|) da bancada v361; o veredito diz MAX_SCALED; a relativa pura dos finitos fica ao lado (informativa); teste residuo_de_maquina_e_arredondamento",
             "N3_pulo_por_chave": "CORRIGIDO: os de tempo pulam por chave de tempo e so se nao forem booleanos; phase_seconds/env so no topo; teste started_booleano_comparado (o resumo passou de 227 a 228 campos)",
             "N4_D128_pulado": "CORRIGIDO: D128 que nao rodou nesta rodada (e rodou na anterior) sai da comparacao, dito no veredito (D128_EXCLUDED_NOT_RUN_THIS_RUN) e no artigo; teste d128_excluido_dito",
             "N5_entradas": "CORRIGIDO: a leitura anterior guarda spec/trabalhador/beta/ambiente do resultado; entradas diferentes -> NOT_COMPARED_DIFFERENT_INPUTS; o ambiente e' gravado e comparado (informativo); teste entradas_diferentes_nao_compara",
             "N6_frases_do_artigo": "CORRIGIDO: «logo depois de lancar o trabalhador, antes que o calculo novo pudesse substitui-lo»; o nome impresso e' o lido do kernel (final_step_name_from_kernel)",
             "N7_exp": "CORRIGIDO NO KERNEL: axiomFlow_eq_exp ligado a exp_complement_idempotent (ver texto 4)",
             "N8_segunda_tentativa": "CORRIGIDO: restaurar_cache_anterior_v385.py (fail-closed; nao apaga; so com ordem da gerencia)",
             "N9_ordem_no_candidato": "CORRIGIDO: CANDIDATO_v385.json.ordem_do_operador (lida do transcrito pelo gerador)",
             "N10_try_except_W04": "CORRIGIDO: W04 em try/except; excecao vira registro NAO comparado / Axioma NAO selado, dito; o rito segue",
             "N11_marcador_na_memoria": "NA CADEIA: a superficies_v385 poe ao lado, na linha do pilar do MEMORY.md, o marcador do pacote v385; a memoria-topico do pilar diz a regra nova"},
         "texto": {
             "1_BLOQUEIA_citacao": "CORRIGIDO: «testemunha falsa é a testemunha estática é o zero absoluto» verbatim; e TODA citacao do operador nos trechos PT/EN conferida contra o transcrito por script (conferir_citacoes_v385.py; o ensaio a seco a exige)",
             "2_BLOQUEIA_v183": "CORRIGIDO: «desde a v183» no artigo PT/EN, no runtime e no comentario do Audit.lean (sandbox reconstruido e reauditado); o ensaio a seco recusa «v181» na secao",
             "3_medida_e_dois_zeros": "CORRIGIDO: «analogia de forma, calculada [COMPUTED]»; V_tP_F = P_F e' do dephasing; rho_ss nao e' Pi; os dois zeros nao se identificam (artigo e docstring da pedra)",
             "4_exp_fiacao": "CORRIGIDO NO KERNEL: theorem axiomFlow_eq_exp (import TGLExt.O16.IdempotentDephasing_v2; a prova do aferidor); 22 + 7 = 29 bandeiras; escada 6027; NAO entrou na conjuncao mestra (lema proprio, dito na docstring)",
             "5_dois_Verbos": "CORRIGIDO: dois termos distintos com o seu objeto (verb_not_identity; verb_word_fixes_the_name: age como o escalar q(0)); a frase do operador entre aspas e [INPUT/ONTO]; «Verbo vivo» na lista das leituras",
             "6_conjuncao": "CORRIGIDO: «duas faces lado a lado (uma conjuncao), sem termo que identifique o perfil ¼sech² com o atomo» (artigo e docstring)",
             "7_errata": "CORRIGIDO: PT «um único postulado», «o único postulado», «o postulado do Um»; EN «a single postulate», «the single postulate», «the One postulate»; .md «o postulado `ω(I)=1`»; conferido por script que as formas existem no texto",
             "N1_traco": "CORRIGIDO: a errata diz que «$1=1$ deixa de ser postulado e vira o teorema do traço» fica como esta (estatuto anterior de 1=1)",
             "N2_axioma_unico": "CORRIGIDO COMO LEITURA: o «axioma único (ω(I)=1)» e' o Um posto no comeco; «Axioma» nomeia o 1 que volta como ponto fixo; que sejam o mesmo Um e' a leitura do nome do degrau final [INPUT/ONTO]; a distincao de nomes fica como pendencia do operador no handoff",
             "N3_leituras_sem_aspas": "CORRIGIDO: as leituras do operador do paragrafo «Do posto ao gradiente» entre aspas, verbatim e [INPUT/ONTO]",
             "N4_tudo_num_so_termo": "CORRIGIDO: «os itens centrais num so termo; os demais ficam como lemas proprios» (docstring da pedra)",
             "N5_alcance": "CORRIGIDO: beta > 0 E g > 0 no fluxo escalar; o zero absoluto inalcancavel vem de exp != 0; o token do veredito diz THE_STATIC_ONE_FORBIDDEN_BY_BETA_THE_ABSOLUTE_ZERO_UNREACHABLE_IN_FINITE_TIME",
             "N6_confirmada": "CORRIGIDO: «RATIFICADA» na docstring da pedra",
             "N7_leitura_do_selo": "CORRIGIDO: OPERATOR_COINAGES_AND_RATIFIED_READINGS_...; os fatos da rodada sairam da string fixa (THE_RUN_FACTS_ARE_IN_THE_COMPUTED_RECORDS_NOT_IN_THIS_STRING)",
             "N8_EN": "CORRIGIDO: «status»; «posited» (como na errata da v365); as citacoes em portugues, verbatim, com a traducao marcada; o PT atribui «não existe...» ao operador",
             "N9_corte": "CORRIGIDO: a primeira citacao vai ate «inscrito, distinto.»",
             "N10_resumos": "CORRIGIDO: «comparou os dois resumos (os numeros que o artigo e o selo leem)»",
             "N11_v365_tornou_se_posto": "NAO CORRIGIDO (pergunta ao operador, no handoff): a errata da v365 diz «tornou-se Posto»; 05/10 diz «não se ascende ao posto»"}},
     "passada2": {
         "1_CORRIGIR_chaves_do_selo": "CORRIGIDO: a W07 e o conferidor leem max_scaled_diff, max_rel_diff_finite, n_nonfinite_differ, d128_excluded, inputs, env (corrigir_passada2_v385.py); conferido por script que cada chave do selo existe no registro calculado (so `why` falta quando houve comparacao, como deve)",
         "2_CORRIGIR_conferidor_de_citacoes": "CORRIGIDO: pula isCompactSummary/isMeta; corta <pasted_content>; confere tambem os «…» da pedra e do comentario do Audit.lean contra os transcritos de 05/10 e 20/08 (reticencias = lacuna na ordem); teste negativo: as tres frases da brecha sao recusadas",
         "N1_docstring_Verbo": "CORRIGIDO na pedra: «no núcleo, a palavra do Verbo age como o escalar q(0)»; dois termos distintos (sandbox reconstruido e reauditado: 10129, 29/29, 0 sorry)",
         "N2_hipoteses": "CORRIGIDO: verb_not_identity com t > 0, beta > 0 e algum d_i > 0 (artigo PT/EN, pedra); «proibida no fluxo escalar com beta > 0 e g > 0» na docstring do termo",
         "N3_token": "CORRIGIDO: THE_FULL_STATIC_WITNESS_FORBIDDEN_BY_BETA (sem «STATIC_ONE»)",
         "N4_contagens": "CORRIGIDO: (21)/(28)/10128 nos comentarios e strings -> lidos das listas ou 29/10129",
         "N5_antes_do_calculo": "CORRIGIDO: «logo depois de lancar o trabalhador» no comentario do runtime e no da W03",
         "N6_max_no_TXT": "CORRIGIDO: \\mathrm{max} (sobrevive no TXT, como \\mathrm{min})",
         "N7_token_sem_calculo": "CORRIGIDO: com a rodada sem calculo (REUSE / recusa), NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT (not_compute na leitura anterior)",
         "N8_restaurador": "CORRIGIDO: ver restaurar_cache_anterior_v385.py (volta se a segunda troca falhar; stderr do vigia conferido)",
         "N9_grep_cego": "REGISTRADO: a ferramenta Grep nao ve TGLExt/O16 (o .gitignore do Nos); a frase «0 arquivos» da 1a passada de codigo (nota 7) e' AUSENCIA FALSA -- exp_complement_idempotent EXISTE E ESTA LIGADO (axiom_report do core v384) desde antes da v385; errata ao lado aqui",
         "N10_menores": "CORRIGIDO: «conjugado» la e' a leitura do modulo para «invariante sob todos os operadores» (totally_invariant_is_all_or_nothing); as traducoes do EN marcadas «condensed»; int contra booleano conta como diferenca no comparador"},
     "passada3": {
         "CORRIGIR_conferidor_de_citacoes": "CORRIGIDO: a promessa reduzida ao que o script garante (mensagem de entrada do operador, sem bloco colado MARCADO); por citacao, o carimbo e o tamanho da mensagem (leitura humana: as mensagens achadas sao curtas, 58 a 1.555 caracteres, lidas pela 3a passada como texto do operador)",
         "N1_numeros_do_selo": "CORRIGIDO: o conferidor do rito compara compared/n_fields/n_differ/max_scaled_diff/d128_excluded do selo com os do core",
         "N2_contraste": "CORRIGIDO: o token diz THE_FULL_STATIC_WITNESS_FORBIDDEN_BY_BETA_AND_CONTRAST (o g do kernel e' o contraste, NoFullWitness.lean:88)",
         "N3_ker_T": "CORRIGIDO: no EN, «on $\\ker T$»",
         "N4_bit_a_bit_literal": "CORRIGIDO: mesmo tipo e mesmo float.hex; valor igual com representacao diferente vai a arredondamento (diferenca 0); teste valor_igual_tipo_diferente_nao_e_bit_a_bit",
         "N5_teste_do_token": "CORRIGIDO: teste sem_calculo_nesta_rodada_token (NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT)"}}
for nome, obj in (("AFERIDOR_v385.txt", txt), ("disposicoes_afericoes_v385.json", D)):
    p = os.path.join(HERE, nome)
    if os.path.exists(p):
        open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "wb").write(open(p, "rb").read())
    b = (obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=1)).encode("utf-8")
    open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    print("OK", nome, len(b), "B; sha16", hashlib.sha256(b).hexdigest()[:16])
