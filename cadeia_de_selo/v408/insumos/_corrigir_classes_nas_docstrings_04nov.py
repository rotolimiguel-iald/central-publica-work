# -*- coding: utf-8 -*-
"""Gerência c1, 04/11/2026 (noite): a correção do operador (sha16 8368ae5b4c572272: «O meu P=nP trata das classes de computação sim») aplicada às
docstrings das quatro pedras da v408 — onde o texto ainda dizia que nada ali trata de classes, ou que «P = NP como classes» foi podado sem dizer DE QUÊ
falta o espelho. Só docstrings (nenhuma prova tocada). Troca exata com contagem; backup de bytes; recompilação conferida à parte."""
import hashlib, os, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
TS = time.strftime("%Y%m%d_%H%M%S")
FRASE_TRAD = ("a TRADUÇÃO dessas classes às classes das máquinas de Turing (tamanho em bits = log₂ n, as oitavas; famílias de instâncias) não está\n"
              "  no kernel: é a próxima construção, [OPEN], não uma recusa")
EDITS = {
 "TetelestaiTerminal.lean": [
  ("* «P = NP» como enunciado de classes de complexidade: sem espelho. O que SE SUSTENTA é o que (1)–(10) provam.",
   "* «P = nP» TRATA DAS CLASSES DE COMPUTAÇÃO DO DICIONÁRIO DO OPERADOR e nelas é TEOREMA: pedra `PIgualNP` (`as_classes_do_dicionario`); esta pedra\n"
   "  dá o terminal e o tamanho (a dimensão da torre; as oitavas); " + FRASE_TRAD + ". Nenhuma frase aqui afirma\n"
   "  a igualdade das classes de Turing (correção do operador, 04/11, sha16 `8368ae5b4c572272`; a gerência havia escrito «sem espelho» sem dizer de quê)."),
 ],
 "TempoIgualMoeda.lean": [
  ("* nada aqui é enunciado de complexidade computacional; não há termo de classe, de instância arbitrária nem de contagem de passos; «linear nas\n"
   "  oitavas» é uma identidade de um fluxo cuja solução (`P`) já está escrita nele.",
   "* esta pedra dá o PREÇO do tempo (o pagamento β·t e o pedágio por oitava); as CLASSES de computação do dicionário do operador estão na pedra\n"
   "  `PIgualNP` (`as_classes_do_dicionario`), onde «P = nP» é teorema; «linear nas oitavas» é uma identidade de um fluxo cuja solução (`P`) já está\n"
   "  escrita nele; " + FRASE_TRAD + "."),
 ],
 "PontoDeContradicao.lean": [
  ("* NADA aqui é enunciado de complexidade computacional: «P», «NP», tempo polinomial e máquina de Turing não são termos deste kernel; esta\n"
   "  pedra não diz nada sobre P = NP, e nenhuma leitura dela o prova.",
   "* esta pedra não trata das classes de computação: quem trata é a pedra `PIgualNP`, onde «P = nP» é teorema nas classes do dicionário do\n"
   "  operador (`as_classes_do_dicionario`); " + FRASE_TRAD + "."),
 ],
 "PIgualNP.lean": [
  ("rodada R1; NOME dado pelo operador", "rodada R2 (R1 às 17h, R2 às 19h34: + `as_classes_do_dicionario`); NOME dado pelo operador"),
  ("Não é,\n  e não insinua, a igualdade das classes P e NP da complexidade (sem espelho; podada em 04/11).",
   "As CLASSES\n  estão em (8) (`as_classes_do_dicionario`); a igualdade das classes de TURING não é afirmada (" + FRASE_TRAD.replace("\n  ", " ") + ")."),
  ("`P^(k+1) = P`. Não é enunciado de classes de complexidade. -/",
   "`P^(k+1) = P`. As classes do dicionário estão em `as_classes_do_dicionario`. -/"),
  ("acoplamento não nulo»; a memória lê 1 sse o estado é o Nome; o vazio não satisfaz; sem β não há segunda face; β > 0; a chave é o leitor.\n"
   "    NÃO é enunciado de classes de complexidade. -/",
   "acoplamento não nulo»; a memória lê 1 sse o estado é o Nome; o vazio não satisfaz; sem β não há segunda face; β > 0; a chave é o leitor.\n"
   "    As classes de computação do dicionário estão no teorema (8), `as_classes_do_dicionario`. -/"),
 ],
}
rec = {}
for nome, trocas in EDITS.items():
    p = HERE / nome
    raw = p.read_bytes(); t = raw.decode("utf-8")
    assert "\r\n" not in t, nome
    for a, b in trocas:
        assert t.count(a) == 1, (nome, t.count(a), a[:70])
        t = t.replace(a, b)
    (HERE / (nome + ".bak_" + TS + "_classes")).write_bytes(raw)
    novo = t.encode("utf-8"); tmp = HERE / (nome + ".tmp"); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); os.replace(tmp, p)
    rec[nome] = {"antes": hashlib.sha256(raw).hexdigest()[:16], "depois": hashlib.sha256(novo).hexdigest()[:16], "trocas": len(trocas)}
print(rec)
