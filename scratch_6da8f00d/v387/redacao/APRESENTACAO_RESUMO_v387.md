# v387 — as frases curtas: APRESENTAÇÃO (subtítulo), RESUMO («O método») e PALAVRAS-CHAVE — PT e EN

Lente `redacao` (aferidor-redator), 05/10/2026. Pares `old → new` contra o `um.py` do Nós **tal como está na v386 selada** (as linhas `old` foram
lidas do arquivo: PT 165851 / 165913 / 165939–165941 / 165845; EN 169590 / 169651 / 169677–169679 / 169586). Cada `old` ocorre **uma vez** no
`um.py` (conferido por `grep -n`); o patch segue o padrão do `patch_W10_gpu_apresentacao_v386.py` (`assert src.count(old) == 1`; CRLF do arquivo).
Números **por variável do core**, nunca literais; o prelúdio abaixo define as variáveis e vai **depois** do bloco `_qp_sub` da v386 (que já lê o pilar).

Régua: NOT_FALSIFIED nunca é confirmação; PROVADA ≠ CONFIRMADA; a RG é o limite clássico, não rival; «simulação» da GPU = experimento numérico
(cálculo determinístico), nunca «simulação de LLM»; os três pilares contam JUNTOS em P1; P2 (β na natureza) não determinada.

---

## 0. Prelúdio (PT) — logo após o `else:` do `_qp_sub` (linha ~165869 na v386), antes do `s.append` do subtítulo

```python
    # v387 (ordem do operador 05/10/2026, 23:00:29 UTC): os TRÊS testes de estresse — ritos, kernel, GPU — contam JUNTOS; entram na apresentação,
    # no resumo e nas palavras-chave; números lidos do core (livro de cobranças v383 + registro three_stress_tests_v387 se houver); nunca literais
    _lg7 = core.get("the_ledger_of_charges_v383") or {}
    _lc7 = _lg7.get("counts") or {}
    _tt7s = core.get("three_stress_tests_v387") or {}
    _nq7 = len(_lg7.get("ledger") or [])
    if _nq7 and _lc7.get("FALSIFIED") is not None:
        _tres_sub = (r", e lê os três como um só teste de estresse conjunto --- os ritos com dados públicos (" + str(_lc7.get("FALSIFIED")) + r" falsificada(s) em "
                     + str(_nq7) + r" cobranças do livro; a correspondência com a RG recuperada canal a canal, sem discriminação à sensibilidade disponível), o kernel formal e o "
                     r"experimento numérico na GPU --- que contam juntos na probabilidade de a teoria ser consistente e recuperar a física conhecida; a probabilidade de os "
                     r"efeitos $\beta$ existirem na natureza segue indeterminada")
    else:
        _tres_sub = r", e lê os três --- ritos, kernel, GPU --- como um só teste de estresse conjunto (nesta rodada o livro de cobranças não trouxe contagens: dito, não suposto)"
```

## 1. APRESENTAÇÃO (subtítulo) — PT

**old** (linha 165851, uma ocorrência):
```python
             r"com falsificadores pré-registrados" + _qp_sub + r" --- tudo enquanto audita um kernel Lean de "
```
**new**:
```python
             r"com falsificadores pré-registrados" + _qp_sub + _tres_sub + r" --- tudo enquanto audita um kernel Lean de "
```

Leitura resultante (com os valores da v386): «…cálculo do sistema da teoria [COMPUTED], não medição da natureza, e lê os três como um só teste de
estresse conjunto --- os ritos com dados públicos (0 falsificada(s) em 11 cobranças do livro; a correspondência com a RG recuperada canal a canal,
sem discriminação à sensibilidade disponível), o kernel formal e o experimento numérico na GPU --- que contam juntos na probabilidade de a teoria
ser consistente e recuperar a física conhecida; a probabilidade de os efeitos $\beta$ existirem na natureza segue indeterminada --- tudo enquanto
audita um kernel Lean de 6137 teoremas limpos…»

## 1b. A errata da gerência de 05/10 (pós-dição), no MESMO subtítulo — PT

Decisão já registrada (`registrar_pos_dicao_05out.py`; memória `pos-dicao-nao-e-prova-diabolica-05out.md`): «pós-dição» nunca mais como demérito.

**old** (linha 165845, uma ocorrência):
```python
de mecanismo; pós-dição declarada; zero parâmetro ajustado), publicado
```
**new**:
```python
de mecanismo; retrodição sem ajuste --- novidade de uso, precedente: o periélio de Mercúrio \textsf{[KNOWN]}; zero parâmetro ajustado), publicado
```
(Substituição de substring dentro da linha `r"..."`; o resto da linha fica intacto.)

## 2. RESUMO («O método») — PT

**old** (linha 165913, uma ocorrência):
```python
             r"é calculado em tempo real na GPU, em paralelo com o kernel e os ritos (cálculo do sistema, não medição da natureza). A cadeia é "
```
**new**:
```python
             r"é calculado em tempo real na GPU, em paralelo com o kernel e os ritos (cálculo do sistema, não medição da natureza). Os três --- ritos, kernel, GPU --- "
             r"são um só teste de estresse conjunto e contam juntos na probabilidade de a teoria ser consistente e recuperar a física conhecida; a de os efeitos "
             r"$\beta_{\rm TGL}$ existirem na natureza não está determinada, porque nenhum canal discrimina a RG à sensibilidade disponível; nenhuma soma de "
             r"consistências vira confirmação (seção ``Os três testes de estresse, conjuntos''). A cadeia é "
```

## 3. PALAVRAS-CHAVE — PT

**old** (linha 165941, uma ocorrência):
```python
             r"piso dos vazios cósmicos; sistema quântico aberto (GKLS) calculado em tempo real na GPU\par\vspace{4pt}")
```
**new**:
```python
             r"piso dos vazios cósmicos; sistema quântico aberto (GKLS) calculado em tempo real na GPU; três testes de estresse conjuntos (ritos com dados públicos, kernel formal, experimento numérico na GPU)\par\vspace{4pt}")
```

## 4. SUMÁRIO — PT (a miudeza da v386 + a seção nova)

A seção nova já traz o seu `\addcontentsline` dentro do pysnip. A seção «Ao lado (v386)» ficou sem entrada no sumário (medido na v386: 0 ocorrências
de `addcontentsline{toc}{section}{Ao lado (v386)`); acrescentar logo após a linha 165968:
```python
    s.append(r"\addcontentsline{toc}{section}{Ao lado (v386): o Verbo seleciona; o ramo B reaberto por pré-registro}")   # v387: no sumário
```

---

## 0-EN. Prelude (EN) — right after the `else:` of `_qp_sub` (EN block, ~line 169608 in v386), before the subtitle `s.append`

```python
    # v387 (operator order 2026-10-05, 23:00:29 UTC): the THREE stress tests -- rites, kernel, GPU -- count TOGETHER; they enter the presentation,
    # the abstract and the keywords; numbers read from the core (ledger of charges v383 + the three_stress_tests_v387 record if present); never literal
    _lg7 = core.get("the_ledger_of_charges_v383") or {}
    _lc7 = _lg7.get("counts") or {}
    _tt7s = core.get("three_stress_tests_v387") or {}
    _nq7 = len(_lg7.get("ledger") or [])
    if _nq7 and _lc7.get("FALSIFIED") is not None:
        _tres_sub = (r", and reads the three as one joint stress test --- the rites on public data (" + str(_lc7.get("FALSIFIED")) + r" falsified in "
                     + str(_nq7) + r" charges of the ledger; the correspondence with GR recovered channel by channel, with no discrimination at the available sensitivity), the formal "
                     r"kernel and the numerical experiment on the GPU --- which count together in the probability that the theory is consistent and recovers the known physics; "
                     r"the probability that the $\beta$ effects exist in nature remains undetermined")
    else:
        _tres_sub = r", and reads the three --- rites, kernel, GPU --- as one joint stress test (in this run the ledger of charges brought no counts: stated, not assumed)"
```

## 1-EN. PRESENTATION (subtitle)

**old** (line 169590, one occurrence):
```python
             r"confronts the neutrino mass with pre-registered falsifiers" + _qp_sub + r" --- all while auditing a Lean "
```
**new**:
```python
             r"confronts the neutrino mass with pre-registered falsifiers" + _qp_sub + _tres_sub + r" --- all while auditing a Lean "
```

## 1b-EN. The management's erratum of 05/10 (postdiction), same subtitle

**old** (line 169586, one occurrence):
```python
mechanism; declared postdiction; zero fitted parameters), published
```
**new**:
```python
mechanism; retrodiction without adjustment --- use-novelty, precedent: Mercury's perihelion \textsf{[KNOWN]}; zero fitted parameters), published
```

## 2-EN. ABSTRACT («The method»)

**old** (line 169651, one occurrence):
```python
             r"pillar --- is computed in real time on the GPU, in parallel with the kernel and the rites (a computation of the system, not a measurement of nature). The chain is "
```
**new**:
```python
             r"pillar --- is computed in real time on the GPU, in parallel with the kernel and the rites (a computation of the system, not a measurement of nature). The three --- rites, kernel, GPU --- "
             r"are one joint stress test and count together in the probability that the theory is consistent and recovers the known physics; the probability that the "
             r"$\beta_{\rm TGL}$ effects exist in nature is not determined, because no channel discriminates GR at the available sensitivity; no sum of consistencies "
             r"becomes confirmation (section ``The three stress tests, taken together''). The chain is "
```

## 3-EN. KEYWORDS

**old** (line 169679, one occurrence):
```python
             r"cosmic void floor; open quantum system (GKLS) computed in real time on the GPU\par\vspace{4pt}")
```
**new**:
```python
             r"cosmic void floor; open quantum system (GKLS) computed in real time on the GPU; three joint stress tests (public-data rites, formal kernel, numerical experiment on the GPU)\par\vspace{4pt}")
```

## 4-EN. CONTENTS

After the EN line `s.append(r"\section*{Beside (v386): the Verb selects; branch B reopened by preregistration}")`:
```python
    s.append(r"\addcontentsline{toc}{section}{Beside (v386): the Verb selects; branch B reopened by preregistration}")   # v387: in the contents
```

---

## Conferência (o que a gerência deve medir depois do patch, como no W10)

- `grep -c "teste de estresse conjunto"` no `um_absoluto_pt.txt` ≥ 2 (apresentação + método) e `grep -c "joint stress test"` no `_en.txt` ≥ 2;
  `.toc` com a entrada «Os três testes de estresse, conjuntos (v387)» e «Ao lado (v386)…».
- A regex proibida `(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED` sobre os `.txt`: 0 novos acertos (as frases acima usam «confirmação»/
  «confirmation» em minúsculas, nunca o token).
- `grep -c "pós-dição declarada"` → 0 no PT e `grep -c "declared postdiction"` → 0 no EN após 1b.
