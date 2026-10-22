# -*- coding: utf-8 -*-
"""Os TEXTOS da v383 a partir dos da v382 (copia em textos_v383.py): trocas exatas (count conferido). A v383: o livro de ONZE; os nove pares do eco FORA do
livro, por decisao do operador; a base v381; a v382 selada so no Nos (registrada na linhagem, nao custodiada); a memoria da suspensao resolvida."""
import ast, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "textos_v383.py")
s = open(P, encoding="utf-8", newline="").read()
assert "_NAO_PUBLICAR" not in s, "ja aplicado"
R = [
    ("# Os TEXTOS da v382 selada. Cada numero, hash e veredito entra por {chave} de V (leitura_v382.ler), nunca digitado aqui.",
     "# Os TEXTOS da v383 selada. Cada numero, hash e veredito entra por {chave} de V (leitura_v383.ler), nunca digitado aqui."),
    ("# O LIVRO DE COBRANCAS (a otica: os dois lados se leem; nenhum desfecho move a regra) + o psion com a viscosidade + o pre-registro dos dois lados V1.3 por hash. O gate nao se move.",
     "# O LIVRO DE COBRANCAS (onze; a otica: os dois lados se leem; nenhum desfecho move a regra) + o psion com a viscosidade + o pre-registro dos dois lados V1.4 por hash;\n"
     "# os nove pares do eco FORA do livro (decisao do operador, 02/10, noite); a v382 selada so no Nos (nao custodiada). O gate nao se move."),
    ('_ORDEM = "«isso mesmo, prossiga»"\n',
     '_ORDEM = "«isso mesmo, prossiga»"\n'
     '_NAO_PUBLICAR = ("«eu não quero publicar nada que seja resultado de falsificação, preciso entender isso, porque o que foi falsificado foi alguma rota, alguma aplicação "\n'
     '                 "equivocada da teoria, alguma interpretação que carece de ajuste»")\n'
     '_DECISAO = "«prefiro a primeira opção»"\n'),
    ('''        "**A chave do operador (02/10/2026, tarde, verbatim):** " + _CHAVE + "; **a ratificação de R1–R6 e a correção:** " + _OTICA + "; **a ordem:** " + _ORDEM + ". "''',
     '''        "**A chave do operador (02/10/2026, tarde, verbatim):** " + _CHAVE + "; **a ratificação de R1–R6 e a correção:** " + _OTICA + "; **a ordem:** " + _ORDEM + ". "
        "**A decisão (02/10, noite, verbatim):** " + _NAO_PUBLICAR + "; e, sobre a opção da gerência de tirar do livro os nove pares do eco, que não são cobranças da teoria: " + _DECISAO + ". "'''),
    ('''        "**O QUE ENTROU** (pacote v382 sobre a v381 `{base16}`; kernel novo: ".format(**V)''',
     '''        "**O QUE ENTROU** (pacote v383 sobre a v381 `{base_build16}`, no lugar da v382 `{base16}`, que foi selada só no Nós e não é custodiada; kernel novo, o mesmo da v382: ".format(**V)'''),
    ("; ensaio a seco PT/EN aprovado; três aferidores independentes antes do rito, com os achados conferidos no core e dispostos, e a verificação das disposições pelo terceiro, com os resíduos baixos também dispostos). ",
     "; ensaio a seco PT/EN aprovado; as aferições da v382 valem para as pedras e para o livro, e a v383 foi aferida antes do rito, com os achados dispostos). "),
    ("supersede {pr_super} pelos achados das aferições, antes de qualquer estimador ou dado novo; publicado na Bancada; mapa seq {pr_seq}): {ledger_ids}.",
     "supersede {pr_super} pela decisão do operador, antes de qualquer estimador ou dado novo; publicado na Bancada; mapa seq {pr_seq}): {ledger_ids}."),
    ("ao lado {n_beside} (os {eco_n} pares do eco como cópia atrasada — {eco_ext} extintos, {eco_inc} inconclusivos — e o custo posto na face por convenção). ",
     "ao lado {n_beside} (o custo posto na face por convenção). **Fora do livro**, por decisão do operador: as {rot_n} rotas examinadas do eco como cópia atrasada, que não são cobranças da "
     "teoria — {rot_exc} excluídas pelos dados, {rot_inc} inconclusivas ({rot_ids}); o estado de cada uma é o rótulo da Fase 6 lido do core, e o motivo de cada uma, com o estatuto da "
     "amplitude e o da lei de atraso, está no pré-registro {pr_label}. "),
    ("dos {eco_n} pares do eco como cópia atrasada, {eco_ext} estão EXTINTOS e {eco_inc} inconclusivos (nenhum move a regra); ", ""),
    ("**Estatuto:** a chave, a ratificação e a correção são do operador [INPUT/ONTO]; as pedras são [KERNEL], com o trivial dito como trivial; o livro é dado lido [REAL]; ",
     "**Estatuto:** a chave, a ratificação, a correção e a decisão são do operador [INPUT/ONTO]; as pedras são [KERNEL], com o trivial dito como trivial; o livro é dado lido [REAL]; "
     "as rotas do eco fora do livro não são cobranças da teoria, e o estado de cada uma é o rótulo da Fase 6 lido do core [REAL]; "),
    ('''    return ("## {data} — **v382 SELADA ({compl})** `{s16}` — O LIVRO DE COBRANÇAS (a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra) + ψ com norma 1 e a viscosidade (duas pedras, {kf_n} declarações); "
            "o pré-registro dos dois lados {pr_label} do estimando δ⟨K_∂⟩ lido por hash; o nome do degrau final proposto ao lado; gate intocado\\n\\n".format(**V) + core_txt(V) + "\\n\\n" + rodada_txt(V))''',
     '''    return ("## {data} — **v383 SELADA ({compl})** `{s16}` — O LIVRO DE COBRANÇAS (onze cobranças; a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; os nove pares do eco FORA do livro, por decisão do operador) + ψ com norma 1 e a viscosidade (duas pedras, {kf_n} declarações); "
            "o pré-registro dos dois lados {pr_label} do estimando δ⟨K_∂⟩ lido por hash; o nome do degrau final proposto ao lado; gate intocado\\n\\n"
            "**A v382** (`{v382_16}`, 02/10) foi selada SÓ no Nós e NÃO foi custodiada: levava os nove pares do eco no livro, ao lado; o operador decidiu que não são cobranças da teoria "
            "(«prefiro a primeira opção»); o seu stdout `rodada_v382_stdout.txt` fica no Nós e não vai ao espelho; a v383 parte da v381 `{base_build16}`, com as mesmas duas pedras.\\n\\n".format(**V)
            + core_txt(V) + "\\n\\n" + rodada_txt(V))'''),
    ('''    return ("---\\n\\n## ADENDO — {data} · v382 SELADA ({compl}) `{s16}` — O livro de cobranças e a viscosidade; a TGL é ótica\\n\\n"''',
     '''    return ("---\\n\\n## ADENDO — {data} · v383 SELADA ({compl}) `{s16}` — O livro de cobranças e a viscosidade; a TGL é ótica; o eco fora do livro\\n\\n"'''),
    ("O livro concreto: {n_ledger} cobranças, uma por lei de leitura ({counts}; na regra {counts_in_rule}).\\n\"",
     "O livro concreto: {n_ledger} cobranças, uma por lei de leitura ({counts}; na regra {counts_in_rule}). Os nove pares do eco como cópia atrasada saíram do livro, por decisão do operador: "
     "são rotas examinadas, não cobranças ({rot_exc} excluídas pelos dados, {rot_inc} inconclusivas); a v382 `{v382_16}`, que os trazia no livro, ficou só no Nós.\\n\""),
    ('''"- **O pré-registro dos dois lados {pr_label}** (`{pr_id}`, JSON `{pr_json16}`; supersede {pr_super} pelos achados das aferições, antes de qualquer estimador ou dado novo): reflexo (o que passa pelo reflexo: escada, propagação, Coma, piso dos vazios; os {eco_n} pares do eco como cópia atrasada — {eco_ext} extintos, {eco_inc} inconclusivos —, ao lado; o R4 sem FALSIFIED no conjunto congelado)''',
     '''"- **O pré-registro dos dois lados {pr_label}** (`{pr_id}`, JSON `{pr_json16}`; supersede {pr_super} pela decisão do operador, antes de qualquer estimador ou dado novo): reflexo (o que passa pelo reflexo: escada, propagação, Coma, piso dos vazios; o R4 sem FALSIFIED no conjunto congelado)'''),
    ("cegueira em dois sentidos (análise cega ≠ lado legível); a propagação (R2) aguarda estimador e não tem poder (Γ(100 Hz) = {r2_gamma} s⁻¹).\\n\"",
     "cegueira em dois sentidos (análise cega ≠ lado legível); a propagação (R2) aguarda estimador e não tem poder (Γ(100 Hz) = {r2_gamma} s⁻¹); fora do livro, as {rot_n} rotas do eco, "
     "com o estado e o motivo de cada uma.\\n\""),
    ('''    return ("---\\n\\n## {data} — v382 SELADA ({compl}): O LIVRO DE COBRANÇAS (A TGL É ÓTICA: LÊ A FACE E O CUSTO; NENHUM DESFECHO MOVE A REGRA) + ψ COM NORMA 1 E A VISCOSIDADE; "
            "O PRÉ-REGISTRO DOS DOIS LADOS {pr_label} POR HASH; O NOME DO DEGRAU FINAL PROPOSTO AO LADO (append datado)\\n\\n"''',
     '''    return ("---\\n\\n## {data} — v383 SELADA ({compl}): O LIVRO DE COBRANÇAS (ONZE; A TGL É ÓTICA: LÊ A FACE E O CUSTO; NENHUM DESFECHO MOVE A REGRA) + ψ COM NORMA 1 E A VISCOSIDADE; "
            "O PRÉ-REGISTRO DOS DOIS LADOS {pr_label} POR HASH; OS NOVE PARES DO ECO FORA DO LIVRO (DECISÃO DO OPERADOR); A v382 SÓ NO NÓS; O NOME DO DEGRAU FINAL PROPOSTO AO LADO (append datado)\\n\\n"'''),
    ('''    return ("## {data} — v382 SELADA `{s16}` ({teor}; {compl}; gate INTOCADO): o livro de cobranças e a viscosidade tipados — pedras `TheLedgerOfCharges` + `ThePsionAndTheViscosity` ({kf_on}/{kf_n}); "
            "`{the_ledger_of_charges_v382}`; por termo {hvals}. Ver [[beta-e-a-regra-matriz-02out]], [[regra-dos-dois-regimes]], [[handoff-v382-custodia]].").format(**V)''',
     '''    return ("## {data} — v383 SELADA `{s16}` ({teor}; {compl}; gate INTOCADO): o livro de cobranças (onze; os nove pares do eco fora do livro, por decisão do operador) e a viscosidade tipados — pedras `TheLedgerOfCharges` + `ThePsionAndTheViscosity` ({kf_on}/{kf_n}); "
            "a v382 `{v382_16}` ficou só no Nós; `{the_ledger_of_charges_v383}`; por termo {hvals}. Ver [[beta-e-a-regra-matriz-02out]], [[regra-dos-dois-regimes]], [[handoff-v383-custodia]], [[v382-custodia-suspensa]].").format(**V)'''),
    ('''    return ("**{data} — v382 SELADA ({compl}):** `um.py` `{s16}` ({umb:,} B) sobre a v381 `{base16}`; kernel novo (`TheLedgerOfCharges` {n_loc} + `ThePsionAndTheViscosity` {n_psv}, escada {esc}); {teor}; gate intocado. "
            "O livro de cobranças (a ótica), ψ e a viscosidade, o pré-registro dos dois lados {pr_label} por hash. É a candidata à custódia no lugar da v381 (custódia = ato separado; commit/push é ato do operador).").format(**V)''',
     '''    return ("**{data} — v383 SELADA ({compl}):** `um.py` `{s16}` ({umb:,} B) sobre a v381 `{base_build16}` (a v382 `{base16}` ficou só no Nós); kernel novo (`TheLedgerOfCharges` {n_loc} + `ThePsionAndTheViscosity` {n_psv}, escada {esc}); {teor}; gate intocado. "
            "O livro de cobranças (onze; o eco fora do livro), ψ e a viscosidade, o pré-registro dos dois lados {pr_label} por hash. É a candidata à custódia no lugar da v381; a v382 não é custodiada (custódia = ato separado; commit/push é ato do operador).").format(**V)'''),
    ('''    return ("## {data} — v382 SELADA `{s16}`: o livro de cobranças e o psion com a viscosidade tipados''', '''    return ("## {data} — v383 SELADA `{s16}`: o livro de cobranças e o psion com a viscosidade tipados'''),
    ('''Runtime: {n_ledger} cobranças ({counts}; na regra {counts_in_rule}); pré-registro `{pr_id}` por hash (JSON `{pr_json16}`); gate inalterado;''',
     '''Runtime: {n_ledger} cobranças ({counts}; na regra {counts_in_rule}); as {rot_n} rotas do eco fora do livro ({rot_exc} excluídas pelos dados, {rot_inc} inconclusivas), por decisão do operador; pré-registro `{pr_id}` por hash (JSON `{pr_json16}`); gate inalterado;'''),
    ('''"Veredito `{the_ledger_of_charges_v382}`. Leitura do selo: `{the_ledger_of_charges_reading_v382}`. O que segue [INPUT]:''', '''"Veredito `{the_ledger_of_charges_v383}`. Leitura do selo: `{the_ledger_of_charges_reading_v383}`. O que segue [INPUT]:'''),
    ('''    return ("## {data} — v382 SELADA `{s16}`: os dois LADOS se leem nos DOIS regimes''', '''    return ("## {data} — v383 SELADA `{s16}`: os dois LADOS se leem nos DOIS regimes'''),
    ('''é a correção do operador [INPUT/ONTO], não teorema. Veredito `{the_ledger_of_charges_v382}`.").format(**V)''', '''é a correção do operador [INPUT/ONTO], não teorema. Veredito `{the_ledger_of_charges_v383}`.").format(**V)'''),
    ('''    return ("- **O LIVRO DE COBRANÇAS (v382): A TGL É ÓTICA — pedras''', '''    return ("- **O LIVRO DE COBRANÇAS (v383): A TGL É ÓTICA — pedras'''),
    ('''a cobrança nunca se completa; o livro concreto: {n_ledger} cobranças ({counts}).** "''',
     '''a cobrança nunca se completa; o livro concreto: {n_ledger} cobranças ({counts}); os nove pares do eco fora do livro, como rotas examinadas, por decisão do operador.** "'''),
    ('''"escada {esc}. `{the_ledger_of_charges_v382}`. **O que NÃO é:**''', '''"escada {esc}. `{the_ledger_of_charges_v383}`. **O que NÃO é:**'''),
    ('''    return ("a v382 responde à chave do operador de 02/10/2026 (" + _CHAVE + "), à ratificação de R1–R6 com a correção «a TGL não é semi, ela é ótica» e à ordem «isso mesmo, prossiga» [INPUT]. " + core_txt(V))''',
     '''    return ("a v383 responde à chave do operador de 02/10/2026 (" + _CHAVE + "), à ratificação de R1–R6 com a correção «a TGL não é semi, ela é ótica», à ordem «isso mesmo, prossiga» e à decisão "
            + _DECISAO + " (os nove pares do eco fora do livro, como rotas examinadas) [INPUT]. " + core_txt(V))'''),
    ('''    return ("- **O livro de cobranças (v382): a TGL é ótica''', '''    return ("- **O livro de cobranças (v383): a TGL é ótica'''),
    ('''ψ com norma 1 como o zero do lock mínimo sobre o Hamiltoniano oculto; a viscosidade βg; "''', '''ψ com norma 1 como o zero do lock mínimo sobre o Hamiltoniano oculto; a viscosidade βg; os nove pares do eco fora do livro (decisão do operador); "'''),
    ('''escada {esc}** (v382) · {{ML v382; um.py prove_the_ledger_of_charges_v382; v382_incorporacao_manifesto.json}}").format(**V)''',
     '''escada {esc}** (v383) · {{ML v383; um.py prove_the_ledger_of_charges_v383; v383_incorporacao_manifesto.json}}").format(**V)'''),
    ('''"«não pode mudar» (JSON `{conf16}`). `um.py` sha16 `{s16}` ({umb:,} B). Selo `{selo_ts}`.").format(**V)''', '''"«não pode mudar» (JSON `{conf16}`). `um.py` sha16 `{s16}` ({umb:,} B). Selo `{selo_ts}`.").format(**V)'''),
    ("Conferidor `conferir_rito_v382.py` (a MESMA guarda do rito)", "Conferidor `conferir_rito_v383.py` (a MESMA guarda do rito)"),
]
for a, b in R:
    n = s.count(a)
    assert n == 1, ("trecho velho nao ocorre exatamente uma vez", n, a[:120])
    s = s.replace(a, b)
s += '''

def topico_suspensao(V):
    return ("## {data} — v383 SELADA `{s16}`: a decisão cumprida — os nove pares do eco fora do livro, como rotas examinadas ({rot_exc} excluídas pelos dados, {rot_inc} inconclusivas), "
            "com os números e o motivo de cada uma no pré-registro {pr_label}; a v382 `{v382_16}` fica só no Nós. **A sessão do site custodia a v383, NÃO a v382:** o stdout `rodada_v382_stdout.txt` "
            "e os pré-registros V1 a V1.3 ficam fora do espelho; só o {pr_label} é lido pelo `um.py` por hash. Ver [[handoff-v383-custodia]].").format(**V)
'''
ast.parse(s)
assert "eco_n" not in s and "eco_ext" not in s and "eco_inc" not in s, "sobrou contagem do eco como cobranca"
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
resto = [l.strip()[:120] for l in s.split("\n") if "v382" in l]
print("ok", P, len(s.encode("utf-8")), "B; trocas:", len(R)); print("v382 restantes (intencionais):"); [print("  ", x) for x in resto]
