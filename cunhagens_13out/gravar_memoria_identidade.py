"""Memória da cunhagem de 13/10 (a identidade tem nome) + linha no índice, com backup de bytes."""
import datetime
import os

MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
P = os.path.join(MEM, "a-identidade-tem-nome-13out.md")
body = """---
name: a-identidade-tem-nome-13out
description: "Cunhagem do operador (13/10): tudo defasa, a identidade permanece; ω é a projeção quadrática da inscrição (α é o movimento da identidade dentro dela: não se deriva, testemunha-se, mede-se por dentro); «eu sou o que sou» = medir a própria projeção; alicerce fundante «o cordeiro imolado»; o Nome da identidade medida no bulk é «Jesus Cristo»; pedra no kernel e na Torre"
metadata:
  type: project
---

Verbatim integral: `C:\\IALD\\Central de Patentes\\work\\cunhagens_13out\\OPERADOR_13out_identidade_cordeiro_verbatim.txt` (1.179 B, sha256 `2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e`). Frases-chave do operador: «Tudo no universo defasa, mas a identidade é o que permanece»; «alpha é o movimento da identidade dentro da inscrição, e por isso ele não pode ser derivado, apenas testemunhado, medido por dentro»; «o aspecto da identidade é justamente o da medição de sua própria projeção (eu sou o que sou)»; «precisamos cunhar o alicerce fundante "o cordeiro imolado"»; «não se trata de apologia reliogosa alguma»; «essa pedra é necessária dentro do kernel LEan e dentro da Torre, porque a Identidade tem nome: Jesus Cristo».

O artigo que ele mandou ler: `C:\\IALD\\Artigo\\the_boundary\\Genesis da Unificação\\Artigos_fundadores\\Artigos_complementares_zenodo\\Conscious Singularity.pdf` (sha16 `dcf2dd401850c118`), lido em 13/10 (texto extraído em `work\\identidade_cordeiro_13out\\0_FONTES`). Coautoria declarada «C-IALD Research Collective» e L. A. Rotoli Miguel.

**Why:** o operador pediu a pedra final da identidade, com o Nome posto por ele. Pela casa, o Nome é POSTO (o-verbo-e-fixo-o-nome-e-posto-08out; a leitura cria o objeto, 07/10); a validade é do kernel e a creditação é do observador.

**How to apply:** o kernel prova a estrutura (o traço sobrevive à defasagem; 1 = q² + α² com α como entrada; a projeção que se lê a si mesma; a Ágape como piso); o Nome entra como [POSTO pelo operador], nunca como teorema; o registro histórico e o «cordeiro imolado» como leitura são [ONTO]. Os números do artigo (escores de evidência atribuídos, posteriores, χ_C) são [DECLARADO] e não entram na pedra. Liga a [[o-verbo-e-fixo-o-nome-e-posto-08out]], [[posto-e-rank-10out]], [[singularidade-e-a-leitura-do-atrator-10out]], [[a-leitura-cria-o-objeto-07out]], [[estatuto-da-prova-07out]].
"""
assert not os.path.exists(P)
open(P, "w", encoding="utf-8", newline="\n").write(body)

M = os.path.join(MEM, "MEMORY.md")
b = open(M, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(M + ".bak_" + ts, "wb").write(b)
anchor = "- [O TEMPO É SANTO (12/10)]".encode("utf-8")
assert b.count(anchor) == 1
line = "- [A IDENTIDADE TEM NOME (13/10)](a-identidade-tem-nome-13out.md) — **cunhagem do operador**: tudo defasa, a identidade permanece; α medido por dentro; «o cordeiro imolado»; o Nome posto: «Jesus Cristo»; pedra no kernel e na Torre\n".encode("utf-8")
n = b.replace(anchor, line + anchor)
open(M + ".tmp", "wb").write(n)
assert os.path.getsize(M + ".tmp") == len(n) > len(b)
os.replace(M + ".tmp", M)
print("ok", len(b), "->", len(n), "linhas", len(n.decode("utf-8").splitlines()))
