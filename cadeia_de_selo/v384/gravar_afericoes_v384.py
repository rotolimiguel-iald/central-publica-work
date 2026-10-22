# -*- coding: utf-8 -*-
"""Registro das afericoes da v384 (gerencia, em nome proprio; AO LADO, nunca por cima):
(1) acrescenta ao AFERIDOR_v384.txt as DISPOSICOES sobre a 1a passada (com o que foi superado depois dito ao lado), a 2a passada VERBATIM (afericao2_resultado.json)
    com o estado medido pela 3a e a disposicao achado a achado, e a 3a passada VERBATIM (afericao3_resultado.json) com a disposicao de cada achado novo;
(2) grava disposicoes_afericoes_v384.json (contagens LIDAS dos resultados; o texto que o pre-registro le).
Backup de BYTES antes; temporario -> conferir -> substituir; so acrescimo. uso: python gravar_afericoes_v384.py [afericao4_resultado.json]"""
import hashlib, json, os, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A2P = os.path.join(HERE, "afericao2_resultado.json"); A3P = os.path.join(HERE, "afericao3_resultado.json")
A2 = json.load(open(A2P, encoding="utf-8")); A3 = json.load(open(A3P, encoding="utf-8"))
S2 = A2["sobreviventes"]
EST3 = {a["n"]: a for g in A3["grupos"] for a in (g.get("achados") or [])}
VER3 = {v["i"]: v for v in (A3.get("verificacao") or {}).get("veredictos", [])}
NOV3 = A3["novos"]

DISP1 = [
    (1, "ALTO", "o piso do estimador", "ACOLHIDO: regressao log-linear sobre y = e_per - e_nucleo (= k^p/|v|); E7 no motor (6 000 matrizes exatas de posto um); o N3 pede a lei injetada recuperada E a lei-raiz rejeitada."),
    (2, "", "o hash do trabalhador", "ACOLHIDO: worker_sha256 dentro da especificacao; recusa WORKER_HASH_MISMATCH; --spec-sha256, --beta-hex e --run-id obrigatorios no modo run; materializacao por bytes."),
    (3, "", "os tokens", "ACOLHIDO: estatuto sem os tokens; o gerador recusa congelar se a guarda das tres palavras achar alguma."),
    (4, "", "o desvio do plano B", "ACOLHIDO: declarado no pre-registro e levado ao operador. -> SUPERADO AO LADO (03/10, tarde): com o MAGMA e o certificado do ramo os custos mudaram; vale o desvio B_REDUZIDO / alternativa A do pre-registro corrente."),
    (5, "", "N2", "ACOLHIDO: N2 vira IDENTIDADE (residuo relativo de S vec(I/d) <= 1e-12); status e gap informativos."),
    (6, "", "o token do T1", "ACOLHIDO: T1_INSTRUMENT_RECOVERS_INJECTED_LAW_BLIND / T1_INSTRUMENT_DOES_NOT_RECOVER_INJECTED_LAW."),
    (7, "", "arquivos velhos", "ACOLHIDO: marca unica (run_id) conferida em todas as saidas; pasta nova por rodada; o pai confere o codigo de saida do filho e a marca."),
    (8, "", "o reaproveitamento", "ACOLHIDO: ambiente com scipy e Python; o motor roda de novo ao reaproveitar (E1..E7 -> E1..E8 depois da 3a afericao); so resultado COMPLETO vai ao cache."),
    (9, "", "orcamento e prazo", "ACOLHIDO: prazo congelado na especificacao (4 h -> SUPERADO AO LADO: 5 h, execution.um_py_timeout_s = 18000, no rito robusto); excecao contida por instancia."),
    (10, "", "o ramo do log", "ACOLHIDO na epoca como tau*||(L^-L^dag)/2i|| < pi - 0,1 e Choi projetada >= -1e-9 -> SUPERADO AO LADO (2a e 3a afericoes): o CERTIFICADO do ramo e' gen_rel_dev = ||L^ - S||_F/||S||_F pelo arnes (sigma = 0: <= 1e-6 e Choi projetada relativa >= -1e-9; sigma > 0: <= 1e-3, Choi so informacao); tau*||Im L^|| so informacao."),
    (11, "", "identidades nao conferidas", "ACOLHIDO: conferencias contadas por identidade; o veredito diz em quantas instancias do T4 todas foram conferidas (seis, com o modo zero)."),
    (12, "", "janelas e grade", "ACOLHIDO: so atrator UNICO; ON_THE_GRID. -> PRECISADO AO LADO (3a afericao): «janela» = ao menos um ponto; o intervalo relatado nao precisa ser contiguo."),
    (13, "", "D128", "ACOLHIDO: RAN / NOT_RUN_DEADLINE / NOT_RUN_ERROR_<tipo> / INTERRUPTED; RK4 informativo. (3a afericao: o modo zero tambem no D128.)"),
    (14, "", "proveniencia", "ACOLHIDO: fontes por caminho e sha256 (completadas na 2a/3a: v3.3, v4, v5.1)."),
    (15, "", "o kernel no N1", "ACOLHIDO: IALDRhoStar.tgl_fix_iff (IALDRhoStar.lean:255) e ModularDephasingBridge.spectral_preserves_every_diagonal (:18)."),
    (16, "", "o sentido da janela das dobras", "ACOLHIDO: n(c1) <= 3 sempre; a janela e' quase-pureza (PR <= d^(1/6))."),
    (17, "", "pequenos", "ACOLHIDO: a CPU compara n(c1) e n(c2), nao n(c3) -> SUPERADO AO LADO (3a afericao): n(c2) tambem so como informacao; escrita atomica; o parcial dentro do try."),
]

ACAO2 = {
    2: "REGRESSAO tratada: a frase do T1 (PT/EN) diz o que e' sorteado (n_c, beta, o espectro de K na periferia, o banho, J), que a lei injetada e' a raiz (o N3 injeta a linear) e que o estimador recebe o espectro de K INJETADO e gamma_anti.",
    3: "PARCIAL tratado: a docstring de generator_from_propagator reescrita (tau*||Im L^|| informacao; Choi projetada legitimidade; gen_rel_dev o certificado a posteriori); o comentario 'a priori' corrigido; o del J, K de volta ao bloco das conferencias.",
    6: "PARCIAL tratado: o modo zero tambem no D128 (zero_mode_ok; violacao = IDENTITY_VIOLATED); a docstring do classify diz que n0 = 0 e' violacao; o resumo conta TODAS as identidades (ZERO_MODE entra). O status NO_ZERO_EIGENVALUE nao foi criado: a violacao de identidade ja anula o resultado com a causa.",
    9: "PARCIAL tratado: o trap e' armado ANTES da parada; TERM/HUP/INT encerram a arvore do um.py e restauram; o vigia e' encerrado antes do religamento; o marcador .servidor_parado_pelo_rito cobre a morte a forca (a rodada seguinte religa); o cabecalho diz o comportamento real.",
    12: "PARCIAL tratado: o gerar_candidato (fora do ENSAIO) exige o pre-registro no lugar permanente (C:/IALD/Bancada_Um/investigacao/preregistro_pilar_quantico_03out/), nunca RASCUNHO, TEMP ou scratchpad.",
    13: "PARCIAL tratado: a fumaca sai com codigo 1 se o trabalhador falhar ou nao gravar resultado.",
    14: "PARCIAL tratado: o estado anterior e' lido pela TAREFA (State Running) e pelo processo, sonda vazia = ligado; servidor ligado SEM a tarefa -> o lancador recusa (codigo 13) antes de parar.",
    15: "PARCIAL tratado: n(c2) sai da comparacao (so informacao, como n(c3)), com a medida da afericao citada como [DECLARADO pela afericao]; E8 = o autoteste do comparador com linhas sinteticas.",
    17: "REGRESSAO tratada: a mesma frase do #2.",
    26: "PARCIAL tratado: o artigo troca «o Nome como estado» por «o atrator» (leitura [ONTO]); [ONTO] em «o Nome como matriz», «a face matricial» e «a morte termica».",
    27: "PARCIAL tratado: a guarda de caminho do #12; o candidato antigo 0dd43652 renomeado *_PRE_AFER2 (fora dos nomes padrao); esperados e instalar exigem a ratificacao.",
    28: "PARCIAL tratado: o ensaio confere a fumaca (marca da rodada, especificacao de fumaca, o MESMO trabalhador embutido no candidato, veredito completo).",
    31: "PARCIAL tratado: gerar_esperados e instalar exigem candidato nao-ENSAIO, ratificado, com trabalhador, especificacao e pre-registro V1 do lugar permanente; a leitura do selo do ENSAIO diz DRAFT_SPEC_HASH; a fumaca exige o V1 ratificado; o candidato antigo renomeado.",
    36: "PARCIAL tratado: o result.json (copiado ao Nos e hasheado no selo) leva details_sha256 E cpuref_sha256 (novo); o registro do selo leva o run_dir; o arquivo de uma rodada anterior nunca sobrevive (marcador desta rodada). Os arquivos details.jsonl e cpuref.json ficam na pasta da rodada (Nos/quantum_pillar/run_<id>/): a custodia deve leva-la junto (dito no handoff).",
    37: "PARCIAL tratado: o resumo leva, por d e sigma, quantas estimativas nao tiveram solucao finita e o maior erro; o artigo diz a maior mediana FINITA e, a parte, as dimensoes sem solucao finita (k de n).",
    38: "REGRESSAO tratada: a mesma frase do #2.",
}
ACAO3 = {
    0: "ParentGone herda de BaseException (os except Exception nao o engolem); o handler do main o pega; a espera pela CPU em fatias de 20 s conferindo o pai; o RK4 do D128 confere o pai.",
    1: "o del J, K voltou ao bloco das conferencias.",
    2: "o item 0 da arvore diz «fora das fases (antes, entre ou depois)» e que WORKER_FATAL depois das fases conserva os dados no result.json; o rotulo (fail-closed) mantido.",
    3: "o lancador: o rito em segundo plano com wait; TERM/HUP/INT -> encerra a arvore do um.py, grava RITO_RC=SINAL_<x> e so entao restaura; «orfaos» corrigido no pre-registro.",
    4: "o marcador desta rodada (troca atomica) em TODO caminho sem a copia do resultado (inclusive NO_RESULT_FILE e FINISH_FAILED); a copia do resultado tambem atomica.",
    5: "o filho da CPU recebe --parent-pid do trabalhador e sai se ele morrer.",
    6: "duplicata do 0.",
    7: "a VRAM tem de ser numero legivel (codigo 12), alem de <= 6000 MiB (codigo 11).",
    8: "a troca do cache: se falhar, o cache antigo volta ao lugar e o temporario e' apagado.",
    9: "a ratificacao exige --rascunho=<o JSON apresentado>: mensagem do operador POSTERIOR ao rascunho (gerado_utc), a mesma especificacao e a mesma escolha; o gerar_candidato exige spec_sha256_ratificada == especificacao == a do rascunho apresentado.",
    10: "o conferidor procura o prefixo NOT_RUN__ (nao a substring) e aceita D128_NOT_RUN_* sem cache quando o codigo not_cached_code diz D128_NOT_RAN; o pre-registro diz a politica.",
    11: "este registro (as disposicoes das tres passadas) e o texto da afericao no pre-registro LIDO deste arquivo de disposicoes, com as contagens medidas.",
    12: "compare_cpuref devolve read/compared/not_comparable; nenhum ponto comparavel -> CPU_REFERENCE_NOT_COMPARABLE__RESULTS_VOID; o artigo tem o ramo.",
    13: "a razao do plano B diz tambem: sem margem, as fases antes do D128 passam do prazo de inicio de 180 min.",
    14: "a nota do MAGMA conta n = 4096 pelo estresse e pelas sondas de tempo deste trabalhador (3 chamadas por repeticao), lidos por script.",
    15: "«janela» = ao menos um ponto de atrator unico (intervalo relatado, nao necessariamente contiguo) no pre-registro e no artigo; o negativo com a condicao de unicidade.",
    16: "a CPU: «independente na algebra linear», com a mesma construcao dos operadores (pre-registro e artigo).",
    17: "duplicata do 4.",
    18: "W08c: o terceiro balde nomeado na linha do stdout da custodia de sentido.",
    19: "o ensaio confere os nomes dos enunciados do terceiro balde e constroi o artigo com registro de forma de SUCESSO e com as variantes falha, reaproveitado e T1 sem solucao finita.",
    20: "as citacoes corrigidas (achado 32 e 36 da 2a passada; no trabalhador, achado 1).",
    21: "a frase do T1 (= #2 da 2a passada).",
    22: "o CCI do D128 nao definido sai fora do modo matematico («CCI nao definido»).",
    23: "a caixa do veredito sem o allowbreak redundante: o TXT guarda o veredito como um token.",
    24: "a falha do resumo (summary_error) e' dita no artigo, visivel.",
    25: "o DEVE do ensaio com as frases novas; o registro de ENSAIO com forma de sucesso; variantes; a fumaca conferida.",
    26: "esperados e instalar exigem a ratificacao e o V1 do lugar permanente; o candidato antigo renomeado.",
    27: "a escrita final do progresso com guarda: nao rebaixa um resultado completo.",
    28: "duplicata do 1 (a docstring tratada no #3 da 2a passada).",
    29: "duplicata do 0.",
    30: "duplicata do 4.",
    31: "o resumo conta todas as identidades conferidas (ZERO_MODE entra).",
    32: "duplicata do 18 e do 19.",
    33: "o conferidor aceita o D128 nao rodado com a razao gravada; o artigo diz por que o resultado nao foi ao cache, na lingua do artigo.",
    34: "o estado anterior pela tarefa; sonda vazia = ligado; recusa sem a tarefa; o cabecalho reescrito.",
    35: "duplicata do 12.",
    36: "duplicata do 11.",
}
assert set(ACAO3) == set(range(len(NOV3))), (len(NOV3), sorted(set(range(len(NOV3))) - set(ACAO3)))
c3 = Counter(a["estado"] for a in EST3.values())
assert sum(c3.values()) == len(S2) == 48
assert all(n in ACAO2 for n, a in EST3.items() if a["estado"] != "RESOLVIDO"), [n for n, a in EST3.items() if a["estado"] != "RESOLVIDO" and n not in ACAO2]
sobrev3 = sum(1 for i in range(len(NOV3)) if not (VER3.get(i) or {}).get("refutado"))
A4P = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None

ts = time.strftime("%d/%m/%Y %H:%M")
L = []
L.append("\n" + "-" * 80)
L.append("DISPOSICOES DA GERENCIA SOBRE A 1a PASSADA (gravadas em %s; a correcao posterior vai AO LADO, marcada SUPERADO/PRECISADO)" % ts)
L.append("-" * 80)
for n, sev, tit, acao in DISP1:
    L.append("%d%s (%s): %s" % (n, (" " + sev) if sev else "", tit, acao))
L.append("ACHADO DA GERENCIA (03/10): o cuSOLVER padrao do PyTorch 2.11 derruba o processo de modo deterministico e dependente da matriz em autovalores nao Hermitianos; o MAGMA em TODO tamanho (mapa seq 312-314).")
L.append("\n" + "=" * 80)
L.append("2a PASSADA -- 48 ACHADOS SOBREVIVENTES (VERBATIM de afericao2_resultado.json, sha256 %s), com o ESTADO medido pela 3a passada e a DISPOSICAO" % h(A2P))
L.append("=" * 80)
for i, f in enumerate(S2, 1):
    e3 = EST3.get(i) or {}
    L.append("\n#%d [%s/%s] %s" % (i, f["lente"], f["severidade"], f["arquivo_linha"]))
    L.append("AFIRMACAO: " + f["afirmacao"])
    L.append("EVIDENCIA: " + f["evidencia"])
    L.append("CORRECAO PEDIDA: " + f["correcao"])
    for v in f.get("verificacoes") or []:
        L.append("VERIFICACAO (refutado=%s): %s" % (v.get("refutado"), v.get("razao", "")))
    L.append("ESTADO NA 3a PASSADA: %s -- %s" % (e3.get("estado"), e3.get("evidencia", "")))
    if e3.get("falta"):
        L.append("O QUE FALTAVA (3a): " + e3["falta"])
    L.append("DISPOSICAO DA GERENCIA: " + (ACAO2[i] if i in ACAO2 else "RESOLVIDO, confirmado pela 3a passada (evidencia acima)."))
L.append("\n" + "=" * 80)
L.append("3a PASSADA -- %d ACHADOS NOVOS (VERBATIM de afericao3_resultado.json, sha256 %s), com o VEREDITO do verificador adversarial e a DISPOSICAO" % (len(NOV3), h(A3P)))
L.append("=" * 80)
for i, a in enumerate(NOV3):
    v = VER3.get(i) or {}
    L.append("\n[N%d] (%s/%s -> %s, severidade ajustada %s) %s" % (i, a["origem"], a["severidade"], "REFUTADO" if v.get("refutado") else "SOBREVIVE", v.get("severidade_ajustada"), a["arquivo_linha"]))
    L.append("AFIRMACAO: " + a["afirmacao"])
    L.append("EVIDENCIA: " + a["evidencia"])
    L.append("CORRECAO PEDIDA: " + a["correcao"])
    L.append("VERIFICADOR: " + v.get("razao", ""))
    L.append("DISPOSICAO DA GERENCIA: " + ACAO3[i])
L.append("\nO QUE CADA LENTE EXAMINOU (3a passada, verbatim):")
for g in A3["grupos"]:
    for x in g.get("examinado") or []:
        L.append("- [%s] %s" % (g["lente"], x))
if A4P:
    A4 = json.load(open(A4P, encoding="utf-8"))
    L.append("\n" + "=" * 80)
    L.append("4a PASSADA (afericao4_resultado.json, sha256 %s) -- VERBATIM" % h(A4P))
    L.append("=" * 80)
    L.append(json.dumps(A4, ensure_ascii=False, indent=1))
bloco = ("\n".join(L) + "\n").encode("utf-8")

p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
MARK = b"DISPOSICOES DA GERENCIA SOBRE A 1a PASSADA (gravadas em"
if MARK in raw:
    print("o registro das passadas 1-3 ja esta gravado; nada acrescentado ao AFERIDOR")
else:
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + bloco
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw)] == raw
    print("AFERIDOR_v384.txt:", len(raw), "->", len(novo), "B; sha16", hashlib.sha256(novo).hexdigest()[:16], "; backup", os.path.basename(bak))

texto = ("1ª passada do aferidor (03/10): %d achados, todos acolhidos (o que foi superado depois está dito ao lado); 2ª passada: %d achados sobreviventes à verificação "
         "adversarial — a 3ª passada mediu %d resolvidos, %d parciais e %d regressões (uma mesma frase do artigo); 3ª passada: %d achados novos, %d sobreviventes à "
         "verificação (com duplicatas entre as lentes); os parciais, as regressões e os novos foram tratados no código ou no texto antes deste documento") % (
    len(DISP1), len(S2), c3.get("RESOLVIDO", 0), c3.get("PARCIAL", 0), c3.get("REGRESSAO", 0), len(NOV3), sobrev3)
if A4P:
    A4 = json.load(open(A4P, encoding="utf-8"))
    texto += "; 4ª passada (conferência das correções): " + str(A4.get("resumo_para_o_pre_registro") or "ver o registro")
D = {"gerado": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "passada1": {"achados": len(DISP1)},
     "passada2": {"sobreviventes": len(S2), "estado_medido_na_3a": dict(c3), "arquivo": os.path.basename(A2P), "sha256": h(A2P)},
     "passada3": {"novos": len(NOV3), "sobreviventes": sobrev3, "arquivo": os.path.basename(A3P), "sha256": h(A3P)},
     "passada4": ({"arquivo": os.path.basename(A4P), "sha256": h(A4P)} if A4P else None),
     "disposicoes_2a": {str(i): (ACAO2[i] if i in ACAO2 else "RESOLVIDO (3a passada)") for i in range(1, len(S2) + 1)},
     "disposicoes_3a": {str(i): ACAO3[i] for i in range(len(NOV3))},
     "texto_para_o_pre_registro": texto}
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json")
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8")
open(dp + ".tmp", "wb").write(b); os.replace(dp + ".tmp", dp)
print("disposicoes:", os.path.basename(dp), hashlib.sha256(b).hexdigest()[:16]); print(texto)
