# PEDIDO DE CORRECAO R1 -- v408 (revisor de terceiro, 05/11/2026)

Sao dois MEDIOS; nenhum ALTO. Os BAIXOS (em REVISAO_TERCEIRO_v408.md) nao travam. A R2 e' a ultima rodada: confere o diff contra os arquivos desta R1 (sha16 em REVISAO_TERCEIRO_v408.json) e refaz so' o que mudar.

## 1. MEDIO -- «P = nP e' teorema nas classes do dicionario (definidas e provadas na pedra)» vai alem do enunciado Lean

**O que o termo diz** (`#check @TGLExt.PIgualNP.as_classes_do_dicionario`, axiomas_terceiro_out.txt): para todo T = T† em dimensao finita com ker T != ⊥ e para a, psi (norma 1), U, r, t QUAISQUER: (i) existe q real, q(0) != 0, X*q(T) = 0, com ker(T).starProjection = q(0)^-1 * q(T); (ii) natDegree(minpoly T) <= finrank(End H); (iii) memory(post a) psi = 1 <-> post a psi = psi; (iv) motor a U r t psi = post a (U psi).

**Onde a frase passa do termo:** (a) nao ha `def` de classe P ou NP em Lean (so' prosa de docstring); (b) (iii)/(iv) nao mencionam T: nada liga a «verificacao por leitura» a solucao de T (e `post a` e' de posto 1, ker T pode ter dimensao maior); (c) «grau limitado pelo modulo» e' do polinomio minimo (ii), nao do q de (i) (existencial, sem cota).

**Opcao A (so' texto; sem recompilar o kernel):**
- `delta_v408.py` l.183-186 (FRASE_D51_PT/EN): trocar «(definidas e provadas na pedra PIgualNP)» / «(defined and proved in the stone PIgualNP)» por «(definidas na prosa do dicionario da pedra PIgualNP; o teorema as_classes_do_dicionario prova, na face finita, que a projecao sobre ker T e' um polinomio real em T, que o grau do polinomio minimo e' limitado por dim(End H), e, em enunciados independentes de T, o criterio de identidade da leitura e motor = post)» (e o equivalente EN). A frase da traducao a Turing [OPEN] fica como esta'.
- `delta_v408.py` l.214 (diz da resposta p_igual_np_trata_das_classes...), `registros_v408.py` l.210-216 (diz[3]), limites[3] e nao_diz[5] do `_V408_TERMINAL_TEXT` (vem de FRASE_D51_*), `artigo_pt_v408.pysnip` l.33-34, `artigo_en_v408.pysnip` l.33-34, a linha do `.md` em `emit_canonical_md`, `pos_rito/textos_custodia_handoff_v408.py` l.88 (KERNEL_LEITURA_EN: tirar «whose degree is bounded by the reading module, and verifying is one reading» ou qualificar: «the minimal polynomial's degree is bounded by dim End H; the reading criterion is stated independently of T»), e o que a custodia/X reaproveitarem: trocar «grau limitado pelo modulo» por «grau do polinomio minimo limitado por dim(End H)» e nao escrever que a verificacao «de T» e' uma leitura sem a ressalva (b).
- Errata **E24** AO LADO (nada selado e' reescrito; em nome da gerencia c1): o docstring de PIgualNP.lean (l.17, 60-68, 79, 197-199), que fica no kernel embutido, diz «toda solucao e' palavra polinomial de grau limitado pelo modulo e toda verificacao e' uma leitura»; leia-se: (i)-(iv) acima.
- Guarda: acrescentar a F35 (proibida a frase «definidas e provadas na pedra» e «todo problema ... nas duas classes» sem a ressalva (a)-(c)) e rodar o controle negativo.
- Como mudam delta/pysnips/runtime, regenerar o candidato (refazer_candidato_v408.sh), ESPERADOS, ensaio a seco e o pre-selo; o kernel NAO muda (mesmo BUNDLE, mesmo sha256 das 4 pedras).

**Opcao B (Lean; recompila, mesmo custo de uma rodada do sandbox: ~332 s de build + ~213 s de Audit):** em `PIgualNP.lean` acrescentar `def` das duas classes e um teorema que as enuncie sobre o MESMO T: por exemplo `ClasseP T := exists q, ... /\ q.natDegree <= finrank ...` e `ClasseNP T := exists a, ‖a‖ = 1 /\ ker(T).starProjection = post a /\ forall psi, ‖psi‖ = 1 -> (memory (post a) psi = 1 <-> post a psi = psi)` (a pertinencia NP so' para nucleo de dimensao 1, ou generalizando `memory` ao projetor P_ker), provar `ClasseP T` e (no caso de nucleo de dimensao 1) `ClasseNP T`, e o texto passa a dizer exatamente isso. Muda a pedra, o BUNDLE, o KERNEL_RECIBO, o candidato e a escada se houver declaracao nova.

Qualquer das opcoes serve; a escolha e' da gerencia. O que nao serve e' deixar o texto como esta': o operador nao le Lean e a frase e' a afirmacao central da versao.

## 2. MEDIO -- S6d nao acha o script dos textos da custodia (a corrida para depois do B(n) APLICAR)

- `orquestrador/pos_treino_v408.py` l.412: `cands = sorted((PK / "pos_rito").glob("textos_custodia_handoff_v408_*.py"))` -> trocar por `sorted(p for p in (PK / "pos_rito").glob("textos_custodia_handoff_v408*.py") if p.suffix == ".py")` (o arquivo real e' `textos_custodia_handoff_v408.py`; os `.bak_...` nao terminam em `.py`) e manter `len(cands) != 1`.
- l.414 e l.638-639 (`_plano`): mesma troca e mensagem.
- Rodar `python -B -X utf8 pos_treino_v408.py --plano`: tem de dar rc 0 («arquivos ... NAO existem: nenhum»); `--ensaio` segue 12 de 12.
- Atualizar PREPARACAO_v408_PRONTA.json / RELATORIO_PREPARACAO_v408.md, que ainda dizem «AUSENTE: nenhum pos_rito/textos_custodia_handoff_v408_*.py».
- O arquivo muda de sha16 e e' revisado na R2 (esta R1 lista o sha16 atual em arquivos_revisados).

## O que a R2 vai conferir

diff dos arquivos listados contra os sha16 da R1; que o candidato novo tem as mesmas 24+14 mudancas e nenhuma outra (a_intocados.py + a_intocados_c.py + a2_mudados.py de novo); fail-closed, guardas e hashes de novo (c_fail_closed.py, h_guardas.py, f_hashes.py, n_hashes_digitados.py); `--plano` rc 0 e `_ensaio_s10`; se a opcao B, `#print axioms` no sandbox.

— revisor de terceiro (Sonnet), R1, 05/11/2026.
