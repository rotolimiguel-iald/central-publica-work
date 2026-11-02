# -*- coding: utf-8 -*-
"""R3. Gera REVISAO_TERCEIRO_v405.json e .md a partir de achados_fonte.json; o sha16 do candidato e lido do arquivo agora."""
import json, hashlib, time, sys
sys.stdout.reconfigure(encoding="utf-8")
D = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v405/"
F = json.load(open(D + "revisao_terceiro/achados_fonte.json", encoding="utf-8"))
bx = [{"sev": "BAIXO", **b} for b in F["baixos"]]
ach = F["achados"] + bx
n = {k: sum(1 for a in ach if a["sev"] == k) for k in ("ALTO", "MÉDIO", "BAIXO")}
sha = hashlib.sha256(open(D + "um_v405_candidato.py", "rb").read()).hexdigest()[:16]
quando = time.strftime("%Y-%m-%dT%H:%M:%S")
J = {"aprovada": n["ALTO"] == 0 and n["MÉDIO"] == 0, "candidato_sha16": sha, "revisor": "revisor terceiro independente, R3 (agente Claude Opus 5.5, pedido da gerência c1; não construiu a v405)", "quando": quando,
     "n_alto": n["ALTO"], "n_medio": n["MÉDIO"], "n_baixo": n["BAIXO"], "achados": ach,
     "ressalvas": ["BAIXO: %s: %s" % (b["onde"], b["o_que"]) for b in bx] + F["nao_examinado"] + ["R1 e R2: os 18 achados ALTO e MÉDIO seguem fechados; nenhum reabriu."], "rotas_examinadas": F["rotas_examinadas"]}
json.dump(J, open(D + "revisao_terceiro/REVISAO_TERCEIRO_v405.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
T = []
w = T.append
w("# Revisão de terceiro da v405, terceira rodada")
w("")
w("Revisor independente; não construí nada disto. Candidato `%s`, lido por script ao fechar, %s. **Veredito: %s: %d ALTO, %d MÉDIO, %d BAIXO.** Os 5 achados da R2 estão fechados nos lugares onde existiam, e os 13 da R1 não reabriram. O escopo foi só o que mudou; R1 e R2 estão em `_R1` e `_R2`." % (sha, quando, "APROVADA" if J["aprovada"] else "NÃO APROVADA", n["ALTO"], n["MÉDIO"], n["BAIXO"]))
w("")
w("## 1. Os 5 achados da R2")
w("")
w("| # | sev | achado | estado | conferência |")
w("|---|---|---|---|---|")
for r in F["fechamento_r2"]:
    w("| %s | %s | %s | %s | %s |" % tuple(r))
w("")
w("**BAIXOS da R2:** " + F["fechamento_baixos_r2"])
w("")
w("## 2. O código novo de `PontoZeroDoPsion` [REAL, compilado por mim]")
w("")
w("- **`lockDe` em Hilbert qualquer:** correto. `lockDe Ω = 1 − P`, sem certificado.")
w("- **`HminMic_e_o_lock`:** é `rfl` de verdade. Conferi com `example` próprio em `r3_axiomas.lean`, sem depender do teorema da pedra, e instanciei `lock_no_angulo` em `C.Ω` para `HminMic C`: compila. `HminMic = 1 − PFmic`, `PFmic = (ℂ∙C.Ω).starProjection`.")
w("- **`o_gap_com_unidade`:** multiplica `o_lock_tem_gap_um` por u. Prova o que diz.")
w("- **`o_retido_e_o_valor_esperado_do_lock`:** é o elo que faltava: `u·⟨ψ_M, lockDe Ω ψ_M⟩ = retidoNoAngulo c u`.")
w("- **`the_gap_closes` reescrito:** sete conjuntos, entre eles o gap em u, E₀ = u, tônica = √e·u e o elo. Os conjuntos compartilham `u`, e o elo liga o produto interno à energia retida.")
w("- **Nome chamando Δ de gap:** nenhum. Os nomes com «gap» são do gap espectral (`o_lock_tem_gap_um`, `o_gap_com_unidade`, `the_gap_closes`), mais o nome do registro e da seção, que vêm da fala. `gap_sobre_Delta` é a razão entre os dois. Busca por 7 nomes antigos: zero, salvo no regex da guarda.")
w("- **Vacuidade:** com o certificado, χ existe (`revisor_chi_existe`, no trio); sem ele, qualquer Hilbert de dimensão ≥ 2 serve.")
w("")
w("## 3. O que o preparador acrescentou")
w("")
w("| item | juízo | conferência |")
w("|---|---|---|")
for r in F["preparador"]:
    w("| %s | %s | %s |" % tuple(r))
w("")
w("## 4. Regressão, por script")
w("")
w("- **Intocados:** as 7 funções e `GA_WINDOW_STATUS` têm AST e fonte idênticas às da base `3820476c83267f61`; 21 nós mudados, 0 removidos, 46 novos.")
w("- **Trio:** 26 teoremas por `#print axioms`, zero `sorryAx`, rc 0 (`r3_axiomas_out.txt`).")
w("- **Pedras:** embutido = sandbox = `pedra/` nas oito, batendo com o recibo R7.")
w("- **Citações:** 295 varridas; toda fala atribuída ao operador é substring exata. **Hashes:** 28 de 28.")
w("- **Números:** Δ, τ, Γ_B, Q, E_fluxo, gap/Δ = 83,117, m₂ e K iguais ao ensaio a seco.")
w("- **Achados da R1 e da R2:** nenhum reabriu, inclusive `the_terminal_reads_one` e as frases residuais. Guarda sobre pedras, snippets, textos e tradução: só as falas dele, que são a exceção declarada.")
w("- **Preparação:** `pronta` true, `falta` vazio, os três hashes iguais ao candidato; purga com zero ocorrência.")
w("")
w("## 5. Achados abertos")
w("")
w("Nenhum ALTO, nenhum MÉDIO.")
w("")
w("## 6. BAIXOS, que não travam")
w("")
for i, b in enumerate(F["baixos"], 1):
    w("%d. **%s:** %s %s" % (i, b["onde"], b["o_que"], b["proposta"]))
w("")
w("## 7. O que ficou de fora")
w("")
for s in F["nao_examinado"]:
    w("- " + s)
w("")
w("Rotas lidas no Mapa: " + ", ".join("`%s`" % r for r in F["rotas_examinadas"]) + ".")
open(D + "revisao_terceiro/REVISAO_TERCEIRO_v405.md", "w", encoding="utf-8").write("\n".join(T) + "\n")
print(sha, n, J["aprovada"], len(ach))
